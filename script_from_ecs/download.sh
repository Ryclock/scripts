#!/usr/bin/env bash

server_ip=""
server_user=""
server_dir=""
local_dir=""

if [ -d "${local_dir}" ]; then
    backup_dir="${local_dir}_backup_$(date +%Y%m%d%H%M%S)"
    mv "${local_dir}" "${backup_dir}"
fi

scp -r "${server_user}@${server_ip}:${server_dir}" "${local_dir}"
