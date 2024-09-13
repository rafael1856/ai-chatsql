#!/bin/bash

# TODO setup postgres vars
# start postgres server
# start pgadmin


##############################################
docker start pgvector1



# checking postres is running

sudo pg_createcluster 15 main -- --initdb

# postgres@7479520bec4c:~/data$ pg_createcluster 12 main -- --initdb
# Error: no initdb program for version 12 found

# postgres@7479520bec4c:~/data$ pg_createcluster 12 main -- --initdb
# Error: no initdb program for version 12 found
# postgres@7479520bec4c:~/data$ postgres --version
# postgres (PostgreSQL) 15.4 (Debian 15.4-2.pgdg120+1)
# postgres@7479520bec4c:~/data$ 

# as postgres user 'sudo' is not nedeed
sudo /usr/lib/postgresql/15/bin/pg_ctl init -D /var/lib/postgresql/15/main



# sleep 10
# ps -ax

# check ports:
# lsof -nP -iTCP -sTCP:LISTEN

# see dockers
# docker ps --format json | jq


