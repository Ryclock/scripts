#!/usr/bin/env bash

docker build -t fastapi_docker -f ./fastapi.dockerfile .
docker run -d -p 8000:8000 --name fastapi_container1 -v /etc/localtime:/etc/localtime:ro fastapi_docker
