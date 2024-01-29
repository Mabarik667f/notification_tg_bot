FROM python:3.11-alpine
LABEL authors="mamba"

WORKDIR /home

RUN apk update \
    && apk add --no-cache build-base mariadb-dev

RUN pip install --upgrade pip
COPY ../requirements.txt .
RUN pip install -r requirements.txt

COPY .. .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /home
ENV TZ Europe/Moscow


ENTRYPOINT ["python", "src/bot/bot.py"]