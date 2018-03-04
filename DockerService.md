docker build -t vpburchenya/bodylog-api:latest backend/
docker push vpburchenya/bodylog-api:latest
docker service create --name test -p 8080:8080 vpburchenya/bodylog-api:latest
docker service ls
docker service scale test=5
docker service scale test=0

docker inspect <CONTAINER_ID> -f "{{json .State}}" | python -m json.tool | pygmentize -l json
