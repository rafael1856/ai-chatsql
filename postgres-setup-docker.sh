#!/bin/bash

# start postgres container
docker start pgvector1

# start pgadmin container
docker start pgadmin1


#apt-get update && apt-get update && apt-get install -y curl nano git iputils-ping procps lsof supervisor

# copy database file
data/employees.tar.gz

# generate DB structure
# load backup - recovery backup
# setup credentials and access

# check connectivity to other containers

su postgres

############### installed ############
# postgres@7479520bec4c:/code$ ls -ltr /etc/init.d/
# total 16
# -rwxr-xr-x 1 root root  959 Dec 19  2022 procps
# -rwxr-xr-x 1 root root 3729 Dec 27  2022 supervisor
# -rwxr-xr-x 1 root root 1748 Feb 13  2023 hwclock.sh
# -rwxr-xr-x 1 root root 1490 Sep 14  2023 postgresql

# postgres@7479520bec4c:/code$ pg_isready
# /var/run/postgresql:5432 - accepting connections


#####################################
# check ports:
# lsof -nP -iTCP -sTCP:LISTEN

# see dockers
# docker ps --format json | jq


