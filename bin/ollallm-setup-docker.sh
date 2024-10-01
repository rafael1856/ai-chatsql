#!/bin/bash 

source conf/config
printenv > environment-setup.txt

echo "------------ downloading and installing OLLAMA ----------"
curl -fsSL https://ollama.com/install.sh | sh

# ollama installed at:
# /usr/local/bin/
echo "starting OLLAMA SERVER"
/usr/local/bin/ollama serve &

# installed here because is nonroot user
echo "########################"
echo " starting olllama RUN "
echo "########################"
/usr/local/bin/ollama run $MODEL

echo " --------------- END -----------------"




