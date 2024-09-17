#!/bin/bash

# get enviroment variables
source .env

# move to the docer app folder
cd /code/

# mamba install -f conf/conda_config.yaml -y
mamba env update --name base --file /code/conf/conda_config.yaml 

# pip install --upgrade pip setuptools
pip install  python-dotenv




