#!/bin/bash

# get environment variables
source conf/config

# Initialize mamba for the current shell
eval "$(mamba shell hook --shell bash)"

# pip install --upgrade pip 
pip install python-dotenv setuptools
export PATH=$PATH:/home/nonroot/code/.local/bin

# Activate the mamba environment
mamba activate base

# clean old logs
rm logs/*.log > /dev/null 2>&1

# Start the main app
streamlit run src/app.py --logger.level=debug

