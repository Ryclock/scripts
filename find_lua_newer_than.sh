#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Error: Please provide a directory path and a timestamp."
    echo "Usage: $0 [directory_path] [YYYY-MM-DD HH:MM:SS]"
    exit 1
fi

src_dir="$1"
input_time="$2"

if [ ! -d "$src_dir" ]; then
    echo "Error: Directory does not exist or is not accessible: $src_dir"
    exit 1
fi

# Convert input time to Unix timestamp (for comparison)
target_timestamp=$(date -d "$input_time" +%s 2>/dev/null)
if [ -z "$target_timestamp" ]; then
    echo "Error: Invalid timestamp format. Please use 'YYYY-MM-DD HH:MM:SS'."
    exit 1
fi

echo "Scanning .lua files in $src_dir newer than $input_time..."

found_files=0
for file in "$src_dir"/*.lua; do
    if [ -f "$file" ]; then
        file_mtime=$(stat -c "%Y" "$file")
        if [ "$file_mtime" -gt "$target_timestamp" ]; then
            filename=$(basename "$file")
            readable_mtime=$(stat -c "%y" "$file" | cut -d. -f1)
            echo "$filename: 作用，更新时间$readable_mtime"
            found_files=1
        fi
    fi
done

if [ "$found_files" -eq 0 ]; then
    echo "No .lua files found newer than $input_time."
fi