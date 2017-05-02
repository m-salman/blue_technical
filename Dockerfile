FROM python:3-alpine

RUN apk update && apk add \
    ca-certificates zip \
    bash

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

