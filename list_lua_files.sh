#!/bin/bash

# 格式
# 文件名: 作用，更新时间YYYY-MM-DD HH:MM:SS

echo "scan lua files..."

for file in *.lua; do
    if [ -f "$file" ]; then
        mtime=$(stat -c "%y" "$file" | cut -d. -f1)  # extract date and time, excluding milliseconds
        echo "$file: 作用，更新时间$mtime"
    fi
done
