- Build image: docker build -t vpburchenya/py3-ws:latest .
- Run container from image: docker run --rm --name bodylog-api -P vpburchenya/py3-ws:latest
- Show ports: docker port bodylog-api
- Container shell: docker run -it --rm --name bodylog-api -P vpburchenya/py2-ws:latest bash
- Compose, build and run single container: docker-compose up --build bodylog-api
- Compose, run cli shell: docker-compose run --rm bodylog-api bash

