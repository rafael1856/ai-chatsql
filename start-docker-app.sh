#!/bin/bash

# get enviroment variables
source .env

# if mamba1 container does not exist, create it. Else start it
CONTAINER_NAME="mamba1"

if docker ps -a | grep -i $CONTAINER_NAME; then
    echo "Container $CONTAINER_NAME already exists....starting ...."
    docker start  $CONTAINER_NAME
else
    echo "Container $CONTAINER_NAME does not exist.... creating...and starting."
    docker run -dt -p 8501:8501 --name  $CONTAINER_NAME condaforge/miniforge3:latest
fi

# Execute script inside container
docker exec $CONTAINER_NAME bash /code/app-start-docker-program.sh &

