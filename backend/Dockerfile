# pip-dependencies
FROM vpburchenya/py3-ws as pip-dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt


# vpburchenya/bodylog-api
FROM pip-dependencies
LABEL maintainer="Burchenya Valentin <vp.burchenya@oz.net.ru>"


WORKDIR /usr/local/app

VOLUME sdata
COPY ./src/ .
COPY ./ep.sh .
RUN chmod +x ep.sh

EXPOSE 8080

ENTRYPOINT ["/usr/local/app/ep.sh"]
CMD ["python3", "/usr/local/app/run.py"]
