#FROM nvidia/cuda:11.4.1-cudnn8-devel-ubuntu18.04
#FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04
FROM python:3

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

RUN virtualenv -p python3 /ve
RUN chmod +x /ve/bin/*
ENV PATH="/ve/bin/:/opt/bin:$PATH"

RUN pip install -U pip
RUN python3 -m pip install --default-timeout=1000 -r /talkingwithai/requirements.txt

COPY . /talkingwithai

# OpenChat
WORKDIR /talkingwithai
RUN git clone https://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@github.com/ildar-idrisov/openchat.git
RUN python3 -m pip install --default-timeout=1000 -r openchat/requirements.txt
#RUN wget --show-progress -T 1000 http://parl.ai/downloads/_models/blender/BST400Mdistill_v1.1.tgz
#RUN cp BST400Mdistill_v1.1.tgz ...
