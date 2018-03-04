# vpburchenya/bodylog-www
FROM debian:buster-slim
LABEL maintainer="Burchenya Valentin <vp.burchenya@oz.net.ru>"


ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qq
RUN apt-get install --no-install-recommends -qy \
                    nginx \
    && rm -rf /var/lib/apt/lists/*


VOLUME sdata
COPY ./conf/nginx.conf /etc/nginx/nginx.conf
COPY ./html/ /var/www/html/

EXPOSE 80


CMD '/usr/sbin/nginx'
