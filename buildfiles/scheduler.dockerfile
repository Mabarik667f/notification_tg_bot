FROM python:3.11-alpine
LABEL authors="mamba"


WORKDIR /home/src/scheduler/

RUN apk update \
    && apk add --no-cache build-base mariadb-dev

RUN pip install --upgrade pip
COPY .requirements.txt .
RUN pip install -r requirements.txt

#COPY ..src/scheduler $SCHEDULER_HOME
COPY ../src/config.py .