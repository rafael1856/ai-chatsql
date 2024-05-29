#!/bin/bash
# This script sets up the Conda environment for the project.
# 
#

APP_PATH=$(dirname "$0")

# get enviroment name from the conda_config.yaml file
yaml_file_path="conf/conda_config.yaml"
enviro=$(grep 'name:' "$yaml_file_path" | awk '{print $2}')

if [ -z "$enviro" ] ; then
  echo "Error: Environment name not found in conda_config.yaml"
  # Set enviro to the name of the current directory
  enviro=$(basename "$PWD")
fi

# Check if the environment exists
if ! conda env list | grep -q "$enviro"; then
  echo "Creating a new conda environment named $enviro..."
  # Create a new conda environment named "$enviro" using the configuration file "conda_config.yaml"
  conda env create -f $yaml_file_path -n $enviro -y
fi

echo " ------------------------------ "
echo "conda activate "$enviro
echo "pip install -r requirements.txt"
echo " ------------------------------ "
echo "To remove a conda environment, use the following command:"
echo "conda env remove --name myenv"
echo "or rm -rf /path/to/anaconda3/envs/myenv"