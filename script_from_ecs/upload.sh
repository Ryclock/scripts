#!/usr/bin/env bash

local_dir=""
cleanup_script="./cleanup_directories.sh"

server_ip=""
server_user=""
server_dir=""

bash "${cleanup_script}" "${local_dir}"
scp -r "${local_dir}" "${server_user}@${server_ip}:${server_dir}"

ssh "${server_user}@${server_ip}" "cd ${server_dir} && sh ./modify_and_clean_app.sh"