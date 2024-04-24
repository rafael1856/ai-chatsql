#!/bin/bash
# This script is used to start the SQLChat application.
export PATH="/home/rafael/anaconda3/bin:$PATH"

# get enviroment name from the conda_config.yaml file
yaml_file_path="./conda_config.yaml"
enviro=$(grep 'name:' "$yaml_file_path" | awk '{print $2}')

conda activate $enviro

# Start the SQLChat application using Streamlit
streamlit run src/app.py