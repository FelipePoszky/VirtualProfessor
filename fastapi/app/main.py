from fastapi import FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
import shutil
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import ChatOllama
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import DirectoryLoader
import pickle
import os
from langchain.vectorstores import FAISS
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings

import urllib.request

load_dotenv()

app = FastAPI()


class info(BaseModel):
    message: str
    archivo: str
    modelo: str

class chatbot(BaseModel):
    Prompt: str
    Modelo: str


@app.get("/")
async def saludo():
    return RedirectResponse(url="/docs/")

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    # verifica si el archivo es pdf
    if file.filename.endswith(".pdf"):
        # Crear el directorio "data" si no existe
        if not os.path.exists("data"):
            os.makedirs("data")
        # guarda el archivo en el servidor
        file_path = os.path.join("data", file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        response = embedder(file_path, file.filename)
        return response
    else:
        return {"message": "Formato de archivo no permitido"}

def embedder(archivo, nombre):

    print(archivo, nombre)
    store_name = nombre[:-4]
    pdf_reader = PdfReader(archivo)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=0
    )
    chunks = text_splitter.split_text(text)
    embeddings = HuggingFaceInstructEmbeddings(model_name='hkunlp/instructor-large', model_kwargs={"device": "cpu"})
    VectorStore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    
    # Crea el archivo 'embeddings' si no existe
    if not os.path.exists('embeddings'):
        os.makedirs('embeddings')
    
    with open(os.path.join('embeddings', f"{store_name}.pkl"), "wb") as f:
        pickle.dump(VectorStore, f)
    
    return {"message": "archivo descargado, y embedding realizado correctamente"}



@app.post("/chatbot")
async def conectar_a_chatbot(date: chatbot):

    response = chatbot(date.Prompt, date.Modelo)
    return response


def chatbot(Prompt, Modelo):
  
    # LLM
    if Modelo == "Llama2":
        
        from langchain.llms import LlamaCpp
        
        ggml_model_path = "https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-GGUF/resolve/main/dolphin-2.6-mistral-7b.Q4_K_M.gguf"
        filename = "/code/app/model/dolphin-2.6-mistral-7b.Q4_K_M.gguf"
        
        
        if not os.path.isfile(filename):
            urllib.request.urlretrieve(ggml_model_path, filename)
            print("Descarga realizada correctamente")
        else:
            print("Modelo ya existente")

        
        llm = LlamaCpp(
            streaming = True,
            model_path="/code/app/model/dolphin-2.6-mistral-7b.Q4_K_M.gguf",
            temperature=0.75,
            top_p=1,
            verbose=True,
            n_ctx=4096,
            n_threads=1,
            n_gpu_layers=0
        )

        response = llm(Prompt)

    elif Modelo == "ChatGPT":

        llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.5)

        response = llm(Prompt)
    

    return response

@app.post("/info")
async def conectar_con_contexto(datos: info):

    response = connect(datos.message, datos.archivo, datos.modelo)
    return response

def connect(Question, archivo, modelo):
    
    store_name = archivo[:-4]

    with open(os.path.join('embeddings', f"{store_name}.pkl"), "rb") as f:        
        VectorStore = pickle.load(f)
            
    retriever = VectorStore.similarity_search(query=Question, k=3)

    # LLM
    if modelo == "Llama2":
        
        llm = ChatOllama(model='llama2:7b-chat', temperature=0.5)

    elif modelo == "ChatGPT":

        llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.5)

    chain = load_qa_chain(llm=llm, chain_type="stuff")
    response = chain.run(input_documents=retriever, question=Question)


    return response
