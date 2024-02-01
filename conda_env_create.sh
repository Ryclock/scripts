#!/usr/bin/env bash

if ! command -v conda &> /dev/null; then
    echo "Please ensure conda is correctly installed and added to the system path."
    exit 1
fi

for arg in "$@"
do
    case ${arg} in
        name=*)
            env_name="${arg#*=}"
            ;;
        python=*)
            python_version="${arg#*=}"
            ;;
        *)
            echo "Invalid parameter: ${arg}"
            exit 1
            ;;
    esac
done

if [ -z "${env_name}" ]; then
    echo "Environment name cannot be empty!"
    exit 1
fi

if [ -z "${python_version}" ]; then
    conda create -y -n "${env_name}" python=3.10
else
    conda create -y -n "${env_name}" python="${python_version}"
fi

conda install -y -n "${env_name}" pip

conda_envs_dir=$(conda info --base)/envs
env_dir=${conda_envs_dir}/${env_name}

site_file=${env_dir}/Lib/site.py
user_base_dir=${env_dir}/Scripts
user_site_dir=${env_dir}/Lib/site-packages
site_file=${site_file//\\/\/}
user_base_dir=${user_base_dir//\\/\/}
user_site_dir=${user_site_dir//\\/\/}

awk -v new_user_base="${user_base_dir}" -v new_user_site="${user_site_dir}" '
    /^USER_BASE/ {
        gsub(/USER_BASE = .*/, "USER_BASE = \047" new_user_base "\047")
    }
    /^USER_SITE/ {
        gsub(/USER_SITE = .*/, "USER_SITE = \047" new_user_site "\047")
    }
    { print }
' "${site_file}" > "${site_file}.tmp" && mv "${site_file}.tmp" "${site_file}"
