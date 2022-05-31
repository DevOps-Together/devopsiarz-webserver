#!/bin/bash

docker stop devopsiarz-webserver
docker rm devopsiarz-webserver

docker run -d -p 9000:80 --name devopsiarz-webserver devopsiarz-webserver:latest

