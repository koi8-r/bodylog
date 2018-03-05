docker build -t vpburchenya/bodylog-api:latest backend/
docker push vpburchenya/bodylog-api:latest
docker service create --name test -p 8080:8080 vpburchenya/bodylog-api:latest
docker service ls
docker service scale test=5
docker service scale test=0

docker inspect <CONTAINER_ID> -f "{{json .State}}" | python -m json.tool | pygmentize -l json


docker run --rm -ti \
  --add-host api:172.17.0.2 \
  --add-host www:172.17.0.1 \
  -p 8181:80 vpburchenya/bodylog-lb


python3 -m httpie get http://0.0.0.0/guid Host:api.oz.net.ru
python3 -m httpie get http://0.0.0.0/api/guid
