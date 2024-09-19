#!/bin/bash

# get enviroment variables
source .env

# run fisrt time to create container
docker run -dt -p 24000:4000 -p 21434:11434 --name ollallm1 ai-chatsql-ollallm:latest
# Execute script inside container
docker exec ollallm1 bash /code/ollallm-start-docker-programs.sh &

############### doc ##################
# Run Docker container if it exists
# docker start --name myollallm ollallm

# run interactive shell inside container
# docker run -ti --name myollallm ollallm

# export ports from container ports
#  docker run -d -p HOST_PORT:CONTAINER_PORT app

# build and run
# docker run -it $(docker build -q .)

# docker stop myollallm