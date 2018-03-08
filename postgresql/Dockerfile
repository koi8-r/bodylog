# vpburchenya/postgresql
FROM debian:buster-slim
LABEL maintainer="Burchenya Valentin <vp.burchenya@oz.net.ru>"


ENV locale ru_RU.UTF-8
ENV PG_MAJOR 10


ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qq
RUN apt-get install --no-install-recommends -qy \
    procps \
    inetutils-tools \
    net-tools \
    iproute2 \
    iputils-ping \
    ca-certificates wget \
    gnupg dirmngr \
    locales \
    && true


# RUN localedef -i ru_RU -c -f UTF-8 -A /etc/locale.alias ru_RU.UTF-8
# locale-gen work
RUN localedef -i "${locale%.*}" -c -f "${locale#*.}" -A /etc/locale.alias "${locale}"
ENV LANG $locale

# deb postinst script during cluster init read locale from
# update-locale work
RUN echo "LANG=\"${locale}\"" >> /etc/default/locale


RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" >> /etc/apt/sources.list.d/postgresql.list
RUN apt-key adv --keyserver ipv4.pool.sks-keyservers.net --recv-keys 'B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8'

RUN apt-get update -qq && \
    apt-get install --no-install-recommends -qy postgresql-${PG_MAJOR}

RUN apt-get purge -y --auto-remove ca-certificates wget gnupg dirmngr
RUN rm -rf /var/lib/apt/lists/*


# todo: try ram disk
RUN mkdir -p /var/run/postgresql/${PG_MAJOR}-main.pg_stat_tmp/
RUN chown postgres:postgres /var/run/postgresql/${PG_MAJOR}-main.pg_stat_tmp/
RUN chmod 2750 /var/run/postgresql/${PG_MAJOR}-main.pg_stat_tmp/

RUN echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/${PG_MAJOR}/main/pg_hba.conf


# todo: resolve PGPASSWD inline and unset PGPASSWD env, change owner and perm of ep.sh to postgres and 400
RUN (echo '#!/bin/bash' ; \
     echo 'set -o pipefail' ; \
     echo -n "echo -e \"ALTER USER postgres PASSWORD '\${PGPASSWD:-postgres}' ;\\\n\"" ; \
     echo " | postgres --single -E -D \"\${PGDATA}\" -c config_file=\"\${PGCFG}\"" ; \
     echo ; \
     echo 'exec "$@"' \
    ) >> /ep.sh
RUN chmod +x /ep.sh


ENTRYPOINT ["/ep.sh"]
VOLUME ["/var/lib/postgresql/"]
EXPOSE 5432


USER postgres
ENV PATH "$PATH:/usr/lib/postgresql/${PG_MAJOR}/bin/"
ENV PGDATA "/var/lib/postgresql/${PG_MAJOR}/main"
ENV PGCFG="/etc/postgresql/${PG_MAJOR}/main/postgresql.conf"

CMD [ "bash", "-c", "postgres -D ${PGDATA} -c config_file=${PGCFG} -c listen_addresses=*" ]
