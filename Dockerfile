FROM python:3.7

RUN apt-get update && apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Python
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt-get update --fix-missing && \
    apt-get install -y tar git curl wget nano && \
    pip3 install virtualenv && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir -p /talkingwithai

# TelegramBot
COPY ./requirements.txt /talkingwithai/requirements.txt

RUN virtualenv -p python /ve
RUN chmod +x /ve/bin/*
ENV PATH="/ve/bin/:/opt/bin:$PATH"

RUN pip install -U pip
RUN pip install -r /talkingwithai/requirements.txt

COPY . /talkingwithai
