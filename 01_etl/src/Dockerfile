FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/

RUN pip install -r requirements.txt --no-cache-dir

COPY . /app

COPY ./wait-for-it.sh /app/wait-for-it.sh

CMD uvicorn --port 8888 --host 0.0.0.0 main:app
