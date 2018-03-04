Ingress network is the swarm routing-mesh network
Swarm internal dns server is 127.0.0.11

docker network create -d overlay --attachable temp
docker run --rm -ti --network temp vpburchenya/bodylog-api:latest cat /etc/resolv.conf
docker network rm temp
