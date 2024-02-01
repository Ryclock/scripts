#!/usr/bin/env bash

dirty_dir=""
app_dir=""
backup_dir="${app_dir}_backup_$(date +%Y%m%d%H%M%S)"

if [ -d "${app_dir}" ]; then
    mv "${app_dir}" "${backup_dir}"
fi

if [ -d "${dirty_dir}" ]; then
    mv "${dirty_dir}" "${app_dir}"
else
    echo "Error: Directory 'backend' does not exist."
    exit 1
fi

cp "${backup_dir}/fastapi.dockerfile" "${app_dir}"
cp "${backup_dir}/requirements.txt" "${app_dir}"
cp "${backup_dir}/setup_fastapi_from_dockerfile.sh" "${app_dir}"
cp "${backup_dir}/.env" "${app_dir}"
cp "${backup_dir}/main.py" "${app_dir}"

find "${app_dir}" -type f -name "hereisbackend" -delete
find "${app_dir}" -type f -name "refer.md" -delete
find "${app_dir}" -type d -name "test" -exec rm -rf {} +
find "${app_dir}" -type d -name "__pycache__" -exec rm -rf {} +
find "${app_dir}" -type d -name ".pytest_cache" -exec rm -rf {} +

# if [ -f "${app_dir}/start.py" ]; then
#     mv "${app_dir}/start.py" "${app_dir}/main.py"
# else
#     echo "Error: File 'start.py' does not exist."
#     exit 1
# fi
