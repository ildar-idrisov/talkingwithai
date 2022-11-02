#FROM nvidia/cuda:11.4.1-cudnn8-devel-ubuntu18.04
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

RUN apt-get update && apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Python
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install -y --no-install-recommends python3-pip python3-dev git nano
#RUN apt install -y ffmpeg libsm6 libxext6 libxrender-dev libgl1-mesa-glx wget mc
#RUN apt install -y libopencv-dev python3-opencv
RUN rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --no-cache-dir setuptools
RUN python3 -m pip install --upgrade pip

# TelegramBot
WORKDIR /talkingwithai
RUN git clone https://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@github.com/ildar-idrisov/talkingwithai.git /talkingwithai
RUN python3 -m pip install -r requirements.txt

# OpenChat
WORKDIR /talkingwithai
RUN git clone https://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@github.com/ildar-idrisov/openchat.git
RUN python3 -m pip install -r openchat/requirements.txt
#RUN wget --show-progress -T 1000 http://parl.ai/downloads/_models/blender/BST400Mdistill_v1.1.tgz
#RUN cp BST400Mdistill_v1.1.tgz ...

WORKDIR /talkingwithai