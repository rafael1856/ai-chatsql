#!/bin/bash

source .env

# mamba install -f conf/conda_config.yaml -y
mamba env update --name base --file conf/conda_config.yaml 

# pip install --upgrade pip setuptools
pip install  python-dotenv

# clean old logs
rm logs/*.log > /dev/null 2>&1

# Start the main app
streamlit run src/app.py



