#!/bin/bash

for zip_file in *.zip; do
    if [ -f "$zip_file" ]; then
        folder_name="${zip_file%.*}"

        if [ -d "$folder_name" ]; then
            echo "文件夹 $folder_name 已存在，跳过解压。"
        else
            unzip "$zip_file" -d "$folder_name"
        fi
    fi
done