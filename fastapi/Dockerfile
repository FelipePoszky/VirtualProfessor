FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --default-timeout=900 --no-cache-dir --upgrade -r /code/requirements.txt

RUN apt-get update && apt-get install -y build-essential cmake

RUN pip install llama-cpp-python

RUN apt-get update && apt-get install -y git

RUN pip install torch

COPY ./app /code/app

COPY ./.env /code/.env

CMD exec gunicorn --config /code/app/gunicorn.py app.main:app