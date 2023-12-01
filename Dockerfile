FROM nvidia/cudagl:11.4.2-base

VOLUME ["/tmp/.X11-unix"]

ENV DISPLAY :0
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt -y install \
    python3-pip \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir paiagym