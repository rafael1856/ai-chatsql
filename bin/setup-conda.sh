#!/bin/bash
# This script setup conda environment for the project.
# conda,miniconda, mamba and micromamba are all similar tools
# any of them are fine to use.
# Use source to run this script:
#
# source bin/setup-conda.sh
#

APP_PATH=$(dirname "$0")

yaml_file_path="conf/conda_config.yaml"

# get enviroment name from the conda_config.yaml file
enviro=$(grep 'name:' "$yaml_file_path" | awk '{print $2}')

micromamba create -f $yaml_file_path -n $enviro -y

micromamba activate $enviro

pip install --upgrade pip setuptools
pip install  python-dotenv

