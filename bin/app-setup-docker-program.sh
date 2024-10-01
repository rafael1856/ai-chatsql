#!/bin/bash +x

# get enviroment variables
source conf/config

# install conda environment
mamba env update --name base --file conf/conda_config.yaml 

# streamlit is installed at:



