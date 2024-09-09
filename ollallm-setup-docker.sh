#!/bin/bash

apt-get update && apt-get update && apt-get install -y curl python3.12-full pip nano git lsof supervisor

# TODO move enviroemnt varaibles to .env ?
export OLLAMA_KEEP_ALIVE=24h
export MODEL="llama3.1"
export OLLAMA_HOST="0.0.0.0:11434"

echo "########################"
echo "installing OLLAMA "
echo "########################"
curl -fsSL https://ollama.com/install.sh | sh

# ollama installed at:
# /usr/local/bin/

echo "########################"
echo "starting OLLAMA SERVER"
echo "########################"
/usr/local/bin/ollama serve &
sleep 10
ps -ax

echo "########################"
echo "starting ollama pull"
echo "########################"
ollama pull $MODEL

echo "ended OLLAMA SETUP"

echo "########################"
echo " starting LITELLM SETUP "
echo "########################"

# Create a virtual environment
python3 -m venv litellm_env

# Activate the virtual environment
source litellm_env/bin/activate

# Install litellm and its dependencies
pip install --no-cache-dir litellm litellm[proxy]

# litellm installed at:
# /code/litellm_env/bin/litellm 

#####################################
# check ports:
# lsof -nP -iTCP -sTCP:LISTEN

# see dockers
# docker ps --format json | jq


