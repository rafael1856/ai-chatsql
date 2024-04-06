#!/bin/bash

# This script is used to start the SQLChat application.

# Load the environment variables, this file is not in the repo for security reasons
source .env

enviro='sqlchat'
if !(conda info --envs | grep -q $enviro); then
  # Create a new conda environment named "$enviro" using the configuration file "conda_config.yaml"
  conda create -n $enviro -f conda_config.yaml
fi

# Activate the "$enviro" conda environment
conda activate sqlchat

# Start the SQLChat application using Streamlit
streamlit run app.py