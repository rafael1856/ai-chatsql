#!/bin/bash

# get enviroment variables
source .env_dockers
 
# docker compose create --build --force-recreate --remove-orphans 
docker compose create --build --remove-orphans --force-recreate

# list images and containers
docker ps -a
docker images

# Start PostgreSQL container
# docker-compose up -d db

# # Start pgAdmin container
# docker-compose up -d pgadmin

# # Verify services are running
# docker-compose ps