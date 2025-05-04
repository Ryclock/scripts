#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Error: Please provide a directory path as an argument."
    echo "Usage: $0 [directory_path]"
    exit 1
fi

src_dir="$1"

if [ ! -d "$src_dir" ]; then
    echo "Error: Directory does not exist or is not accessible: $src_dir"
    exit 1
fi

echo "Scanning .lua files in $src_dir and their modification times..."

for file in "$src_dir"/*.lua; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        mtime=$(stat -c "%y" "$file" | cut -d. -f1)  # extract date and time, remove milliseconds
        echo "$filename: 作用，更新时间$mtime"
    fi
done
