#!/bin/bash




# if mamba1 container does not exist, create it. Else start it
CONTAINER_NAME="mamba1"

if docker ps -a | grep -i $CONTAINER_NAME; then
    echo "Container $CONTAINER_NAME already exists....starting ...."
    docker start  $CONTAINER_NAME
else
    echo "Container $CONTAINER_NAME does not exist.... creating...and starting."
    docker run -dt -p 8501:8501 --name  $CONTAINER_NAME condaforge/miniforge3:latest
fi

# Copy non-hidden files to docker app folder (/code)
for file in $(find . -maxdepth 1 -type f ! -path '*/\.*'); do
  docker cp "$file" mamba1:/code/
done

# copy .env to docker app folder (/code)
docker cp .env $CONTAINER_NAME:/code/

# get enviroment variables
source .env

# Execute script inside container
docker exec $CONTAINER_NAME bash /code/app-setup-docker-program.sh

# start the python app inside the container
docker exec $CONTAINER_NAME bash /code/app-start-docker-program.sh &

# docker exec mamba1 bash /code/app-start-docker-program.sh &