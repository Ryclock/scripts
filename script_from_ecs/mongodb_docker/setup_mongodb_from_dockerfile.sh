#!/usr/bin/env bash

docker build -t mongodb_docker -f ./mongodb.dockerfile .
docker run -d -p 27017:27017 --name mongodb_container1 -v /etc/localtime:/etc/localtime:ro -v /data/db:/data/db mongodb_docker
