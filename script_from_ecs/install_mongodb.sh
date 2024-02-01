#!/usr/bin/env bash

# Install MongoDB
echo "Install MongoDB ... "
#!outside
wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2204-6.0.7.tgz
wget https://downloads.mongodb.com/compass/mongosh-1.10.1-linux-x64.tgz
tar -xvzf mongodb-linux-x86_64-ubuntu2204-6.0.7.tgz
tar -xvzf mongosh-1.10.1-linux-x64.tgz
mv mongodb-linux-x86_64-ubuntu2204-6.0.7 /var/lib/mongodb
cp mongosh-1.10.1-linux-x64/bin/mongosh /var/lib/mongodb/bin

cd /var/lib/mongodb
mkdir -p ./data/db ./log ./conf
touch ./log/mongodb.log
cat <<EOF >>./conf/mongodb.conf
dbpath=/var/lib/mongodb/data/db
logpath=/var/lib/mongodb/log/mongodb.log
port=27017
fork=True
bind_ip=0.0.0.0
maxConns=5000
auth=true
EOF

./bin/mongod -f ./conf/mongodb.conf