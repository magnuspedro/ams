FROM python:3.7-alpine
MAINTAINER Pedro Magnus and Matheus Roberto


ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /ams
WORKDIR /ams
COPY ./ams /ams

RUN adduser -D zuul
USER zuul

