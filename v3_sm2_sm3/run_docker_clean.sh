#!/bin/sh

sudo sh -c '
docker stop $(docker ps -q) || true &&
docker rm $(docker ps -aq) || true &&
docker rmi $(docker images -q) || true &&
docker volume rm $(docker volume ls -q) || true &&
docker network rm $(docker network ls --filter "type=custom" -q) || true &&
docker builder prune -af &&
docker system prune -af --volumes
'