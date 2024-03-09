import kivy
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.properties import BooleanProperty, DictProperty, ListProperty, NumericProperty, ObjectProperty, OptionProperty, StringProperty
from kivy.core.text import LabelBase
from kivy.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.list import OneLineAvatarIconListItem, TwoLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.filemanager import MDFileManager

import datetime
import sqlite3
import os
import requests
import json


Builder.load_file("kvs/pages/welcome_screen.kv")
Builder.load_file("kvs/pages/login_screen.kv")
Builder.load_file("kvs/pages/signup_screen.kv")
Builder.load_file("kvs/pages/menu_screen.kv")
Builder.load_file("kvs/pages/quiz_screen.kv")
Builder.load_file('kvs/pages/new_chat_screen.kv')
Builder.load_file('kvs/pages/config_screen.kv')
Builder.load_file("kvs/pages/chat_screen.kv")

Builder.load_file('kvs/widgets/chats_layout.kv')
Builder.load_file("kvs/widgets/chat_list_item.kv")
Builder.load_file("kvs/widgets/quiz_list_item.kv")
Builder.load_file("kvs/widgets/score_list_item.kv")
Builder.load_file("kvs/widgets/chat_bubble.kv")


Window.size = (320, 600)


class thelab(Screen):
    pass


class LoginPage(Screen):
    pass

class signupPage(Screen):
    pass

class ConfigScreen(Screen):
    
    username = StringProperty()
    email = StringProperty()
    imagen = StringProperty()

class WindowManager(ScreenManager):
    pass

class MessageScreen(Screen):
    '''A screen that display the story fleets and all message histories.'''

class ChatScreen(Screen):
    '''A screen that display messages with a user.'''
    text = StringProperty()
    image = StringProperty()
    modelo = StringProperty()

class QuizPage(Screen):
    """pass"""

class ChatsQuizzes(MDCard):
    id_widget = NumericProperty()
    name = StringProperty()
    image = StringProperty()

class QuizListItem(MDBoxLayout):
    id = NumericProperty()
    chatName = StringProperty()
    chatImage = StringProperty()
    question = StringProperty()
    ans1 = StringProperty()
    ans2 = StringProperty()
    ans3 = StringProperty()
    ans4 = StringProperty()
    rightAns = StringProperty()
    explanation = StringProperty()
    estado = StringProperty()
    resp_usu = StringProperty()

class ScoreListItem(MDCard):
    id = NumericProperty()
    chatName = StringProperty()
    total = StringProperty()
    score = StringProperty()

class ChatListItem(MDCard):
    id = NumericProperty()
    mssg = StringProperty()
    chat_image = StringProperty()
    timestamp = StringProperty()
    chat_name = StringProperty()
    profile = DictProperty()

class ChatBubble(MDBoxLayout):
    msg = StringProperty()
    time = StringProperty()
    sender = StringProperty()


class CreateNewChat(Screen):
    
    img = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        

    def callback_image(self, new_image_address):

        self.img = new_image_address
        self.ids.imagen.source = self.img
        self.ids.imagen.reload()


class Message(MDLabel):
    """sdsdsad"""


class TheLabApp(MDApp):

    connection = None
    cursor = None
    filemanager = None
    selected_file = ''
    def build(self):

        # Crear la conexión a la base de datos
        connection = sqlite3.connect("chatbot.db")
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS Usuarios (Id	INTEGER, Nombre_Usuario	TEXT NOT NULL, Email TEXT NOT NULL, Contraseña TEXT NOT NULL, Imagen TEXT, PRIMARY KEY(Id AUTOINCREMENT))")

        cursor.execute("CREATE TABLE IF NOT EXISTS Chats (Id INTEGER, Usuarios_Id INTEGER, Nombre_Chat TEXT, Imagen TEXT, Modelo_Lenguaje TEXT, Rol_Agente TEXT, FOREIGN KEY(Usuarios_Id) REFERENCES Usuarios(Id), PRIMARY KEY(Id AUTOINCREMENT))")

        cursor.execute("CREATE TABLE IF NOT EXISTS Mensajes (Id INTEGER, Chats_Id INTEGER, Mensaje TEXT, Tiempo TEXT, Emisor TEXT, FOREIGN KEY(Chats_Id) REFERENCES Chats(Id), PRIMARY KEY(Id AUTOINCREMENT))")

        cursor.execute("CREATE TABLE IF NOT EXISTS Archivos (Id INTEGER, Nombre_Archivo TEXT, PRIMARY KEY(Id AUTOINCREMENT))")

        cursor.execute("CREATE TABLE IF NOT EXISTS ArchivosUsuarios (Chats_Id INTEGER, Archivos_Id INTEGER, PRIMARY KEY(Chats_Id, Archivos_Id), FOREIGN KEY(Chats_Id) REFERENCES Chats(Id), FOREIGN KEY(Archivos_Id) REFERENCES Archivos(Id))")

        cursor.execute("CREATE TABLE IF NOT EXISTS Quiz (Id INTEGER, Chats_Id INTEGER, Pregunta TEXT, Respuesta1 TEXT, Respuesta2 TEXT, Respuesta3 TEXT, Respuesta4 TEXT, RespuestaCorrecta TEXT, Explicacion TEXT, Estado TEXT, RespuestaUsu TEXT, FOREIGN KEY(Chats_Id) REFERENCES Chats(Id), PRIMARY KEY(Id AUTOINCREMENT))")


        connection.commit()

        connection.close()


        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.accent_hue = '400'
        self.theme_cls.material_style = "M3"


        self.wm = WindowManager(transition=FadeTransition())

        screens = [MessageScreen(name='message'), ConfigScreen(name='config-screen'), CreateNewChat(name='new-chat'), 
                   ChatScreen(name='chat-screen'), thelab(name='lab'), LoginPage(name='loginPage'), 
                   signupPage(name='signupPage'), QuizPage(name='quiz-screen')]
        
        for screen in screens:
            self.wm.add_widget(screen)


        self.path = os.path.expanduser('~') or os.path.expanduser('/')
        self.filemanager = MDFileManager(
            select_path=self.select_path,
            exit_manager=self.close_filemanager,
        )

        self.wm.current = 'lab'

        return self.wm


    def change_screen(self, screen):
        '''cambiar de pantalla usando el administrador de pantalla.'''
        self.wm.current = screen 
    
    def filter_builder(self):
        '''filtro de los quizzes por chat'''

        self.wm.screens[7].ids['story_layout'].clear_widgets()
        self.quiz_screen = QuizPage()
        connection = sqlite3.connect("chatbot.db")
        cursor = connection.cursor()
        id = self.id
        query = "SELECT Id, Nombre_Chat, Imagen FROM Chats WHERE Usuarios_Id = ? AND Id IN (SELECT Chats_Id FROM Quiz)"
        cursor.execute(query, (id,))
        results = cursor.fetchall()

        for id_chat, nombre_chat, imagen in results:
            
            self.story = ChatsQuizzes()
            self.story.id_widget = id_chat
            self.story.name = nombre_chat
            self.story.image = imagen

            self.wm.screens[7].ids['story_layout'].add_widget(self.story)
        
        connection.close()

    def create_chat(self, profile, id):

        connection = sqlite3.connect("chatbot.db")
        cursor = connection.cursor()
        self.chat_screen = ChatScreen()
        self.msg_builder(id, self.chat_screen)
        chatId = id

        query = ("SELECT Nombre_Chat, Imagen, Modelo_Lenguaje FROM Chats WHERE Id = ?")
        cursor.execute(query, (chatId,))
        datoschat = cursor.fetchall()
        for nombre_chat, imagen, modelo in datoschat:
            self.chat_screen.text = nombre_chat
            self.chat_screen.image = imagen
            self.chat_screen.modelo = modelo
        
        connection.close()
        self.wm.switch_to(self.chat_screen)

    def msg_builder(self, id, screen):
        
        connection = sqlite3.connect("chatbot.db")
        cursor = connection.cursor()

        # Seleccionar todos los mensajes del chat específico
        query = "SELECT Mensaje, Tiempo, Emisor FROM Mensajes WHERE Chats_Id = ? ORDER BY Id ASC"
        cursor.execute(query, (id,))
        messages = cursor.fetchall()

        for message, time, chatname in messages:
            self.chatmsg = ChatBubble()
            self.chatmsg.msg = message
            self.chatmsg.time = time
            self.chatmsg.sender = chatname
            screen.ids['msgHistory'].add_widget(self.chatmsg)
        
        connection.close()


    def create_profile(self):

        connection = sqlite3.connect("chatbot.db")
        cursor = connection.cursor()

        self.config_screen = ConfigScreen()
        self.score_builder(self.config_screen)

        query = "SELECT Nombre_Usuario, Email, Imagen FROM Usuarios WHERE id = ?"
        cursor.execute(query, (self.id,))
        results = cursor.fetchone()

        if results is None or len(results) == 0:
            print("No se encontró el usuario.")
        else:
            self.config_screen.username = results[0]
            self.config_screen.email = results[1]
            self.config_screen.imagen = results[2]

        connection.close()
        self.wm.switch_to(self.config_screen)


    def score_builder(self, screen):

        screen.ids['scoreList'].clear_widgets()
        id = self.id
        connection = sqlite3.connect("chatbot.db")
        cursor = connection.cursor()

        query = """
        SELECT Quiz.Chats_Id, COUNT(Quiz.Id) AS TotalQuizzes, 
               SUM(CASE WHEN Quiz.Estado = 'Acierto' THEN 1 ELSE 0 END) AS TotalAcertados,
               SUM(CASE WHEN Quiz.Estado = 'Equivocación' THEN 1 ELSE 0 END) AS TotalEquivocaciones,
               Chats.Nombre_Chat
        FROM Quiz
        INNER JOIN Chats ON Quiz.Chats_Id = Chats.Id
        WHERE Chats.Usuarios_Id = ?
        GROUP BY Quiz.Chats_Id
        """

        cursor.execute(query, (id,))
        results = cursor.fetchall()

        for result in results:
            chats_id, total_quizzes, total_acertados, total_equivocaciones, nombre_chat = result
            scoreitem = ScoreListItem()
            scoreitem.id = chats_id
            scoreitem.chatName = nombre_chat
            scoreitem.total = "Total: " + str(total_quizzes)
            scoreitem.score = str(total_acertados) + "/" + str(total_acertados + total_equivocaciones)

            screen.ids['scoreList'].add_widget(scoreitem)
        
        connection.close()

    def quizlist_builder(self, chat):

        self.wm.screens[7].ids['quizlist'].clear_widgets()
        connection = sqlite3.connect("chatbot.db")
        cursor = connection.cursor()

        if chat == 'Todos':
            userId = self.id
            query = """
            SELECT Quiz.Id, Quiz.Pregunta, Quiz.Respuesta1, Quiz.Respuesta2, Quiz.Respuesta3, Quiz.Respuesta4, Quiz.RespuestaCorrecta, Quiz.Explicacion, Quiz.Estado, Quiz.RespuestaUsu, Chats.Nombre_Chat, Chats.Imagen
            FROM Quiz
            INNER JOIN Chats ON Quiz.Chats_Id = Chats.Id
            WHERE Chats.Usuarios_Id = ?
            ORDER BY Quiz.Id DESC
            """
            cursor.execute(query,(userId,))
            results = cursor.fetchall()
        
        else:
            query = """
            SELECT Quiz.Id, Quiz.Pregunta, Quiz.Respuesta1, Quiz.Respuesta2, Quiz.Respuesta3, Quiz.Respuesta4, Quiz.RespuestaCorrecta, Quiz.Explicacion, Quiz.Estado, Quiz.RespuestaUsu, Chats.Nombre_Chat, Chats.Imagen
            FROM Quiz
            INNER JOIN Chats ON Quiz.Chats_Id = Chats.Id
            WHERE Chats.Id = ?
            ORDER BY Quiz.Id DESC
            """
            cursor.execute(query, (chat,))
            results = cursor.fetchall()

        for result in results:
            id, pregunta, respuesta1, respuesta2, respuesta3, respuesta4, respuesta_correcta, explicacion, estado, resp_usu, nombre_chat, imagen = result
            quizitem = QuizListItem()
            quizitem.id = id
            quizitem.question = pregunta
            quizitem.ans1 = respuesta1
            quizitem.ans2 = respuesta2
            quizitem.ans3 = respuesta3
            quizitem.ans4 = respuesta4
            quizitem.rightAns = respuesta_correcta
            quizitem.explanation = explicacion
            quizitem.estado = estado
            quizitem.resp_usu = resp_usu
            quizitem.chatName = nombre_chat
            quizitem.chatImage = imagen

            self.wm.screens[7].ids['quizlist'].add_widget(quizitem)
            #if estado == realizado:
                
        connection.close()

    def show_explanation(self, pressed, id, resp_usu, resp_correcta):

        connection = sqlite3.connect("chatbot.db")
        cursor = connection.cursor()

        print(pressed)

        if resp_usu == resp_correcta:
            query = "UPDATE Quiz SET Estado = 'Acierto', RespuestaUsu = ? WHERE Id = ?"
            cursor.execute(query, (resp_usu, id))

            pressed.icon = "check-circle"
            pressed.icon_color = (0, 1, 0, 1)
            pressed.line_color = (0, 1, 0, 1)
        else:
            query = "UPDATE Quiz SET Estado = 'Equivocación', RespuestaUsu = ? WHERE Id = ?"
            cursor.execute(query, (resp_usu, id))

            pressed.icon = "close-circle-outline"
            pressed.icon_color = (1, 0, 0, 1)
            pressed.line_color = (1, 0, 0, 1)

        # Obtener el nombre de la columna que contiene el valor resp_correcta
        
        cursor.execute("PRAGMA table_info(Quiz)")
        columns = [column[1] for column in cursor.fetchall()]
        column_name = None
        for column in columns:
            query = f"SELECT COUNT(*) FROM Quiz WHERE {column} = ?"
            cursor.execute(query, (resp_correcta,))
            count = cursor.fetchone()[0]
            if count > 0:
                column_name = column
                break

        if column_name:
            quizlist = self.wm.screens[7].ids['quizlist']
            for child in quizlist.children:
                if isinstance(child, QuizListItem) and child.id == id:
                    quiz_list_item = child
                    break

        connection.commit()


        #quiz_list_item.clear_widgets()
        self.quizlist_builder()


        connection.close()
        

    def chatlist_builder(self):

        self.wm.screens[0].ids['chatlist'].clear_widgets()
        connection = sqlite3.connect("chatbot.db")
        cursor = connection.cursor()
        
        """
        username = self.username

        query = "SELECT Id FROM Usuarios WHERE Nombre_Usuario = ?"
        cursor.execute(query, (username,))
        user_id = cursor.fetchone()
        
        self.user_id = user_id[0]"""
      

        query =  """
        SELECT 
            C.Id,
            C.Nombre_Chat,
            C.Imagen,
            M.Mensaje AS Ultimo_Mensaje,
            M.Tiempo AS Tiempo_Ultimo_Mensaje
        FROM Chats AS C
        LEFT JOIN Mensajes AS M ON C.Id = M.Chats_Id
        WHERE C.Usuarios_Id = ?
          AND M.Id = (
              SELECT MAX(Id)
              FROM Mensajes
              WHERE Chats_Id = C.Id
          );
        """
        cursor.execute(query, (self.id,))
        results = cursor.fetchall()

        for result in results:
            id, nombre_chat, imagen, ultimo_mensaje, tiempo = result
            chatitem = ChatListItem()
            chatitem.id = id
            chatitem.chat_image = imagen
            chatitem.chat_name = nombre_chat
            chatitem.mssg = ultimo_mensaje
            chatitem.timestamp = tiempo

            self.wm.screens[0].ids['chatlist'].add_widget(chatitem)

        connection.close()


    def send(self, message):
        
        if message != '':
            
            time = datetime.datetime.now()
            self.value = ChatBubble()

            self.value.msg = message
            self.value.time = time.strftime("%I:%M %p")
            self.value.sender = 'you'

            connection = sqlite3.connect("chatbot.db")
            cursor = connection.cursor()

            query = "INSERT INTO Mensajes (Emisor, Mensaje, Tiempo, Chats_Id) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (self.value.sender, self.value.msg, self.value.time, self.id))

            connection.commit()

            screen = self.chat_screen
            screen.ids['msgHistory'].add_widget(self.value)
            connection.close()
            Modelo = self.chat_screen.modelo 
            idchat = self.id

            from threading import Thread
            query_thread = Thread(target=self.process_message, args=(message, Modelo, idchat))
            query_thread.start()

    def process_message(self, message, Modelo, idchat):
    
        from kivy.clock import Clock
        import json
        connection = sqlite3.connect("chatbot.db")
        cursor = connection.cursor()
        query = """
        SELECT Archivos.Nombre_Archivo FROM Archivos JOIN ArchivosUsuarios ON Archivos.Id = ArchivosUsuarios.Archivos_Id
        WHERE ArchivosUsuarios.Chats_Id = ?
        """
        cursor.execute(query, (idchat,))
        fetch_result = cursor.fetchone()


        if fetch_result != None:
            archivo = fetch_result[0]

            headers = {"accept": "application/json"}
            params = {"message": message, "archivo": archivo, "modelo": Modelo}

            url = "http://localhost:80/info"
            response = requests.post(url, headers=headers, data=json.dumps(params))
    
        else: 
            Prompt = message
            headers = {"accept": "application/json"}
            params = {"Prompt": Prompt, "Modelo": Modelo}

            url = "http://localhost:80/chatbot"
            response = requests.post(url, headers=headers, data=json.dumps(params))
        
        response = response.json()

        connection.close()
    
        def update_result(dt):

            connection = sqlite3.connect("chatbot.db")
            cursor = connection.cursor()

            time = datetime.datetime.now()
            respuesta = ChatBubble()
            respuesta.msg = response
            respuesta.time = time.strftime("%I:%M %p")
            respuesta.sender = 'ia'

            query = "INSERT INTO Mensajes (Emisor, Mensaje, Tiempo, Chats_Id) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (respuesta.sender, respuesta.msg, respuesta.time, idchat))

            connection.commit()
            screen = self.chat_screen
            connection.close()

            screen.ids['msgHistory'].add_widget(respuesta)

        Clock.schedule_once(update_result)


    def archivos_bottom_sheet(self, pressed):
        bottom_sheet = MDListBottomSheet()
        

    def modelos_bottom_sheet(self, pressed):
        bottom_sheet = MDListBottomSheet()
        data = {
            "ChatGPT 3.5": "assets/icons8-chatbot-96.png",
            "Bard": "assets/icons8-chatbot-96.png",
            "Llama2": "assets/icons8-chatbot-96.png",
        }

        for option_text, option_icon in data.items():
            bottom_sheet.add_item(
                option_text,
                lambda x, option=option_text: self.handle_modelo(pressed, option),
                icon = option_icon 
            )
        bottom_sheet.open()
    
    def profesion_bottom_sheet(self, pressed):
        
        bottom_sheet = MDListBottomSheet()
        data = {
            "Experto en Ciberseguridad", 
            "Experto en DSA",
            "Experto en Machine Learning",
            "Experto en Economia",
            "Experto en PMBOK",
            "Experto en Matematicas",
            "Experto en Fisica",
        }
        for option_text in data:
            bottom_sheet.add_item(
                option_text,
                lambda x, option=option_text: self.handle_agente(pressed, option)
            )
        bottom_sheet.open()


    def handle_modelo(self, pressed, modelo):

        self.modelo = modelo
        pressed.secondary_text = self.modelo

    def handle_agente(self, pressed, agente):
        
        self.agente = agente
        pressed.secondary_text = self.agente

    def create_new_chat(self):

        connection = sqlite3.connect("chatbot.db")
        cursor = connection.cursor()

        id_usuario = self.id

        query = "INSERT INTO Chats (Usuarios_Id, Nombre_Chat, Imagen, Modelo_Lenguaje, Rol_Agente) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (id_usuario, self.wm.screens[2].ids['Nombre_Chat'].text, self.wm.screens[2].ids['imagen'].source, self.modelo, self.agente))

        # Obtén el ID del chat recién creado
        chat_id = cursor.lastrowid

        archivo = self.wm.screens[2].ids['archivo'].secondary_text

        if archivo != 'pdf, docx, txt, etc':

            query = "INSERT INTO Archivos (Nombre_Archivo) VALUES (?)"
            cursor.execute(query, (archivo,))
            self.archivo_id = cursor.lastrowid
            connection.commit()


            query = "INSERT INTO ArchivosUsuarios (Chats_Id, Archivos_Id) VALUES (?, ?)"
            cursor.execute(query, (chat_id, self.archivo_id))


        time = datetime.datetime.now()
        self.time = time.strftime("%I:%M %p")

        # Inserta un mensaje de bienvenida en el chat
        mensaje_bienvenida = "¡Bienvenido al chat, soy un "+self.agente+"!, preguntame lo que quieras, si quieres cargar un archivo para que lo analice, presiona el boton con icono de clip" 
        
        query = "INSERT INTO Mensajes (Chats_Id, Emisor, Mensaje, Tiempo) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (chat_id, "Sistema", mensaje_bienvenida, self.time))

        connection.commit()
        connection.close()

        self.chatlist_builder()
        self.wm.screens[2].ids['imagen'].source = ''
        self.wm.screens[2].ids['Nombre_Chat'].text = ''

        self.change_screen('message')


    def open_filemanager(self, pressed):
        self.pressed = pressed
        self.filemanager.show(self.path)

    def select_path(self, path: str):

        self.close_filemanager()
        
        if self.pressed == 'imagen':
            new_image_address = path
            new_image = self.wm.current_screen
            new_image.callback_image(new_image_address)
        
        elif self.pressed == 'archivos':

            file_name = os.path.basename(path)

            connection = sqlite3.connect("chatbot.db")
            cursor = connection.cursor()


            self.filemanager.close()
            self.wm.current_screen.ids['archivo'].secondary_text = file_name
            query = "SELECT Id FROM Archivos WHERE Nombre_Archivo = ?"
            cursor.execute(query, (file_name,))
            results = cursor.fetchone()

            
            if results is None or len(results) == 0: 
            
                url = "http://localhost:80/uploadfile"
                files = {"file": open(path, "rb")}
                headers = {"accept": "application/json"}
                response = requests.post(url, files=files, headers=headers)


                if response.status_code == 200:
                    print("Archivo enviado y almacenado correctamente.")
                else:
                    print("Error al enviar el archivo.")

            connection.close()


    def close_filemanager(self, *args):
        self.filemanager.close()



    def dropdown(self, instance):

        self.menu_items = [{"viewclass": "OneLineListItem", 
                            "text": "Nuevo chat",
                            "font_style": "Caption",
                            "on_release": lambda x = "Nuevo chat": self.drop_change_screen('new-chat')},

                            {"viewclass": "OneLineListItem",
                            "text": "Mensajes destacados",
                            "font_style": "Caption",
                            "on_release": lambda x = "Mensajes destacados": self.drop_change_screen('new-chat')},

                            {"viewclass": "OneLineListItem",
                            "text": "Ajustes",
                            "font_style": "Caption",
                            "on_release": lambda x = "Ajustes": self.drop_change_screen('new-chat')},
        
                            {"viewclass": "OneLineListItem",
                            "text": "Ayuda",
                            "font_style": "Caption",
                            "on_release": lambda x = "Ajustes": self.drop_change_screen('new-chat')}]

        self.menu = MDDropdownMenu(
            items = self.menu_items,
            width_mult = 2.5,
            max_height = 250,
            background_color=self.theme_cls.primary_color,
            hor_growth="left",
            ver_growth="down"
            )
        self.menu.caller = instance
        self.menu.open()

    def drop_change_screen(self, screen):
        '''Change screen using the window manager.'''
        self.menu.dismiss()   
        self.wm.current = screen 

#-----------------------------------------------------------------------------------------------------

    def login(self, username, password):
            
        connection = sqlite3.connect("chatbot.db")
        cursor = connection.cursor()

        query = ("SELECT Id, Email FROM Usuarios WHERE Nombre_Usuario = ? AND Contraseña = ?")
        cursor.execute(query, (username, password))
        results = cursor.fetchone()

        if results:
            self.id = results[0]
            self.email = results[1]
            self.username = username  # Almacenar el nombre de usuario
            self.chatlist_builder()
            self.wm.current = 'message'
            self.change_screen('message')

        else:
            print('Usuario o contraseña incorrectos')
        
        connection.close()

    def signup(self, username, email, password):
            
            connection = sqlite3.connect("chatbot.db")
            cursor = connection.cursor()

            imagen_pred = "assets/icons8-chatbot-96.png"

            query = ("INSERT INTO Usuarios (Nombre_Usuario, Email, Contraseña, Imagen) VALUES(?, ?, ?, ?)")
            cursor.execute(query, (username, email, password, imagen_pred))  
    
            connection.commit()

            query = ("SELECT Id FROM Usuarios WHERE Nombre_Usuario = ? AND Contraseña = ?")
            cursor.execute(query, (username, password))
            results = cursor.fetchone()
            
            self.id = results[0]        # almacenar el id del usuario ingresado
    
            connection.close()
            self.username = username  # Almacenar el nombre de usuario
            self.wm.current = 'message'

if __name__ == "__main__":
    
    LabelBase.register(name='MPoppins', fn_regular="fuentes/Poppins-Medium.ttf")
    LabelBase.register(name='BPoppins', fn_regular="fuentes/Poppins-Bold.ttf")

    TheLabApp().run()    


        