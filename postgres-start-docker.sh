#!/bin/bash

# TODO setup postgres vars
# start postgres server
# start pgadmin


##############################################


export OLLAMA_KEEP_ALIVE=24h
export MODEL="llama3.1"
export OLLAMA_HOST="0.0.0.0:11434"



echo "########################"
echo " starting LITELLM SETUP "
echo "########################"

# # running on http://0.0.0.0:4000 
/code/litellm_env/bin/litellm --model ollama/$MODEL  > server_litellm.log 


# sleep 10
# ps -ax

# check ports:
# lsof -nP -iTCP -sTCP:LISTEN

# see dockers
# docker ps --format json | jq


