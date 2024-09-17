#!/bin/bash

# get enviroment variables
source .env

# if pgvector1 container does not exist, create it
CONTAINER_NAME="pgvector1"

if docker ps -a | grep -i $CONTAINER_NAME; then
    echo "Container $CONTAINER_NAME already exists."
    docker start pgvector1
else
    echo "Container $CONTAINER_NAME does not exist."
    docker run -dt -p 5432:5432 --name pgvector1 ankane/pgvector
fi

# if pgadmin1 container does not exist, create it
CONTAINER_NAME="pgadmin1"

if docker ps -a | grep -i $CONTAINER_NAME; then
    echo "Container $CONTAINER_NAME already exists."
    docker start pgadmin1
else
    echo "Container $CONTAINER_NAME does not exist."
    docker run -dt -p 20080:80 --name pgadmin1 dpage/pgadmin4
fi
