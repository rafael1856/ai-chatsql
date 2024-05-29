#!/bin/bash
#

# Extract the environment name from the YAML file
env_name=$(grep 'name:' conf/conda_config.yaml | cut -d ' ' -f 2)

# Get the name of the current conda environment
current_env=$(conda env list | grep '*' | awk '{print $1}')

# Check if the environments match
if [ "$env_name" != "$current_env" ]; then
    echo " *** ERROR ***"
    echo "The current conda environment is not the same as the one specified in the YAML file."
    echo ""
    echo "run: conda activate "$env_name
  exit 1
fi


# clean old logs
rm logs/*.log > /dev/null 2>&1

# # Start the main app
streamlit run src/app.py



