FROM debian:stretch-slim
LABEL maintainer="Burchenya Valentin <vp.burchenya@oz.net.ru>"


ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qq
RUN apt-get install --no-install-recommends -qy \
                    python3.5-minimal \
                    python3.5 \
                    python3-pip \
                    python3-setuptools \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir aiohttp
