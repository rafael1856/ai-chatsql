#!/bin/bash +x

source conf/config
printenv > environment-start.txt

# ollama installed at:
# /usr/local/bin/

# # wait for ollama to start
# sleep 10 # just in case server is still starting


# installed here because is nonroot user
echo "########################"
echo " starting LITELLM SETUP "
echo "########################"

# Create a virtual environment
python3 -m venv litellm_env

# Activate the virtual environment
source litellm_env/bin/activate

# Install litellm and its dependencies
pip install --no-cache-dir litellm litellm[proxy]

echo "starting LITELLM SETUP"
# running on http://0.0.0.0:4000 
/code/litellm_env/bin/litellm --model ollama/$MODEL  > server_litellm.log 



