#!/bin/bash
# This script is used to start the SQLChat application.

# get enviroment name from the conda_config.yaml file
yaml_file_path="./conda_config.yaml"
enviro=$(grep 'name:' "$yaml_file_path" | awk '{print $2}')

# Check if the environment exists
if ! $(conda env list | grep -q "$enviro"); then
  echo "The environment $enviro does not exist. Please create it first."
  echo "run: source ./setup_conda"
fi

conda activate $enviro

# Start the SQLChat application using Streamlit
streamlit run src/app.py