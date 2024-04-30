FROM python:3.9-slim

WORKDIR /app

COPY Makefile /app
COPY requirements.txt /app

RUN apt-get update && apt-get install make && mkdir transcribe_app/ && pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY transcribe_app/ /app/transcribe_app/