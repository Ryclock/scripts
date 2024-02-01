#!/bin/bash

filename="${HOME}/.gitconfig"

if grep -qE '^[[:space:]]*[#].*proxy' "${filename}"; then
    sed -i '/proxy/s/^[#]//' "${filename}"
else
    sed -i '/proxy/s/^/#/' "${filename}"
fi
