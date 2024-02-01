#!/usr/bin/env bash

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 file1 file2 ..."
    exit 1
fi

for file_path in "$@"; do
    if [ ! -f "${file_path}" ]; then
        echo "File not found: ${file_path}"
        continue
    fi

    updated_content=$(sed -E 's/([a-z0-9])([A-Z])/\1_\L\2/g' "${file_path}" |
                        sed -E 's/([a-z0-9])([A-Z])/\1_\L\2/g')
    echo "${updated_content}" > "${file_path}"
done
