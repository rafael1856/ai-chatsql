#!/bin/bash

# get enviroment variables
source .env

# run fisrt time to create container
docker run -dt -p 24000:4000 -p 21434:11434 --name ollallm1 ai-chatsql-ollallm:latest

# Execute script inside container
docker exec ollallm1 bash /code/ollallm-start-docker-programs.sh &

