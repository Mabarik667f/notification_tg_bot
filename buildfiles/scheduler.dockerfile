FROM python:3.11-alpine
LABEL authors="mamba"


WORKDIR /home/src/scheduler/

RUN apk update \
    && apk add --no-cache build-base mariadb-dev

RUN pip install --upgrade pip
COPY ../requirements.txt .
RUN pip install -r requirements.txt

COPY ../src/__init__.py /home/src/
COPY ../src/config.py /home/src/
COPY ../src/scheduler/ .

ENV TZ Europe/Moscow
ENV PYTHONPATH /home

RUN chmod +x scheduler-entrypoint.sh

ENTRYPOINT ["/home/src/scheduler/scheduler-entrypoint.sh"]
