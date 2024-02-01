#!/bin/bash

local_dir=$1

find "${local_dir}" -type d -name "__pycache__" -exec rm -rf {} +
find "${local_dir}" -type d -name ".pytest_cache" -exec rm -rf {} +
