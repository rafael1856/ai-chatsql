#!/bin/bash -x
# This script is used to start the SQLChat application.

# Check if .env file exists
if [ ! -f .env ]; then
  echo "Error: .env file not found."
  exit 1
fi

# Load the environment variables
source .env
enviro='sqlchat'

# Function to check if a Conda environment is activated
is_conda_env_activated() {
  local env_name="$1"
  if [[ "$CONDA_DEFAULT_ENV" == "$enviro" ]]; then
    return 0
  else
    return 1
  fi
}

if !(conda info --envs | grep -q $enviro); then
  # Create a new conda environment named "$enviro" using the configuration file "conda_config.yaml"
  conda create -n $enviro -f conda_config.yaml
fi

# Check if RUN_ENV is activated
if is_conda_env_activated "RUN_ENV"; then
  echo "RUN_ENV is already activated."
else
  echo "RUN_ENV is not activated. Activating now..."
  conda activate $enviro
fi
# Start the SQLChat application using Streamlit
streamlit run src/app.py