# vpburchenya/nginx-onbuild
FROM debian:buster-slim
LABEL maintainer="Burchenya Valentin <vp.burchenya@oz.net.ru>"


ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qq
RUN apt-get install --no-install-recommends -qy \
                    nginx \
    && rm -rf /var/lib/apt/lists/*


ONBUILD COPY ./conf/nginx.conf /etc/nginx/nginx.conf

ONBUILD EXPOSE 80


ONBUILD CMD '/usr/sbin/nginx'
