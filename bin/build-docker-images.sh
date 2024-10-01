#!/bin/bash

# get enviroment variables
source conf/config
 
# create images  and containers
# docker compose create --build --force-recreate 

# create only images 
# docker compose build --no-cache

# create images, containers and start them
docker compose up & # --no-cache

# list images and containers
docker ps -a
docker images

