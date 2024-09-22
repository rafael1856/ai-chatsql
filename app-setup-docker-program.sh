#!/bin/bash

# get enviroment variables
source .env

echo "America/New_York" > /etc/timezone

# move to the app folder
cd /code/

# install conda environment
mamba env update --name base --file /code/conf/conda_config.yaml 

# pip install --upgrade pip setuptools
pip install python-dotenv





