#!/usr/bin/env bash

if [ -n "$1" ]; then
    while read -r server_ip; do
        echo "Installing on ${server_ip}..."
        scp install_tomcat.sh root@"${server_ip}":/root/
        ssh -n root@"${server_ip}" ". ./install_tomacat.sh"
    done < "$1"
fi