#!/bin/bash

# 参数检查
if [ $# -lt 2 ]; then
    echo "Usage: $0 source_dir start_time [file_pattern] [recursive]"
    echo "Example: $0 /path/to/src '2023-01-01 00:00:00' '*.lua' true"
    exit 1
fi

source_dir=$1
start_time=$2
file_pattern=${3:-"*.lua"}
recursive=${4:-false}

start_timestamp=$(date -d "$start_time" +%s)
if [ ! $? ]; then
    echo "Error: Invalid start time format. Please use 'YYYY-MM-DD HH:MM:SS'"
    exit 1
fi

maxdepth_option=""
if [ "$recursive" = "false" ]; then
    maxdepth_option="-maxdepth 1"
fi

find "$source_dir" "$maxdepth_option" -type f -name "$file_pattern" -printf "%p:%TY-%Tm-%Td %TH:%TM:%TS\n" | while IFS= read -r line; do
    file_path=$(echo "$line" | cut -d':' -f1)
    file_time=$(echo "$line" | cut -d':' -f2- | cut -d'.' -f1)

    file_timestamp=$(date -d "$file_time" +%s 2>/dev/null)

    if [ -n "$file_timestamp" ] && [ "$file_timestamp" -gt "$start_timestamp" ]; then
        echo "${file_path}:${file_time}"
    fi
done