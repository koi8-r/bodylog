# vpburchenya/bodylog-lb
FROM vpburchenya/nginx-onbuild
LABEL maintainer="Burchenya Valentin <vp.burchenya@oz.net.ru>"


VOLUME sdata

COPY ./ep.sh .
RUN chmod +x /ep.sh


ENTRYPOINT ["/ep.sh"]
CMD "/usr/sbin/nginx"
