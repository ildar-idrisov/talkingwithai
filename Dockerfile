FROM python:3.10

ARG DATABASE_NAME

RUN apt-get update && apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Python
RUN apt-get update --fix-missing && \
    apt-get install -y tar git curl wget nano && \
    pip3 install virtualenv && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir -p /talkingwithai /ve /etc

# TelegramBot
COPY ./requirements.txt /talkingwithai/requirements.txt

RUN virtualenv -p python /ve
RUN chmod +x /ve/bin/*
ENV PATH="/ve/bin/:$PATH"

RUN pip install -U pip
RUN pip install --default-timeout=1000 -r /talkingwithai/requirements.txt

COPY . /talkingwithai

ENV DATABASE_NAME=${DATABASE_NAME}
RUN python /talkingwithai/scripts/generate_config.py
