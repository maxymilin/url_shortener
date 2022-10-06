FROM python:3.9

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./backend/requirements.txt

COPY shortener_app ./backend/shortener_app

COPY . ./backend

