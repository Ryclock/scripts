import os
import requests
import json
import logging
from datetime import datetime
from config_loader import read_config_byconfigparser

backup_directory = read_config_byconfigparser('PATH','backup_directory')
log_directory = read_config_byconfigparser('PATH','log_directory')

filename =  os.path.basename(__file__)
sub_id = read_config_byconfigparser(filename,'sub_id')
backup_directory = os.path.join(backup_directory, sub_id)

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file = os.path.join(log_directory, sub_id)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file
)

if not os.path.exists(backup_directory):
    os.makedirs(backup_directory)
    logging.info(f"create directory '{backup_directory}' for backup")

GITHUB_TOKEN = read_config_byconfigparser(filename,'github_token')
GITHUB_USER = read_config_byconfigparser(filename,'github_username')

response = requests.get("https://api.github.com")
RESPONSE_TIME = response.elapsed.total_seconds()
logging.info(f"GitHub API response time: {RESPONSE_TIME} seconds")

THRESHOLD = read_config_byconfigparser(filename,'test_threshold')
if RESPONSE_TIME > THRESHOLD:
    logging.error(f"Response time is too high ({RESPONSE_TIME} > {THRESHOLD}), skipping backup.")
    exit(1)

logging.info(f"Starting backup for user {GITHUB_USER} at {datetime.now()}")
headers = {"Authorization": f"token {GITHUB_TOKEN}"}
response = requests.get(f"https://api.github.com/users/{GITHUB_USER}/repos", headers=headers)

if response.status_code != 200:
    logging.error(f"Failed to fetch repository list. HTTP response code: {response.status_code}")
    exit(1)

repos = response.json()
exclude_repos = read_config_byconfigparser(filename,'exclude_repos')
for repo in repos:
    repo_name = repo['name']
    if repo_name in exclude_repos:
        logging.info(f"Skipping repository {repo_name} as it is in exclude list.")
        continue
    clone_dir = os.path.join(backup_directory, repo_name)

    if os.path.isdir(clone_dir):
        logging.info(f"Repository {repo_name} already exists, updating all branches.")
        os.chdir(clone_dir)
        if os.system("git fetch --all >> " + log_file) != 0:
            logging.error(f"Failed to fetch all branches for {repo_name}.")
        if os.system("git pull --all >> " + log_file) != 0:
            logging.error(f"Failed to update all branches for {repo_name}.")
        os.chdir(backup_directory)
        continue
    logging.info(f"Cloning all branches of {repo['clone_url']}")
    sub_log_file = os.path.join(log_directory, f"{sub_id}_{repo_name}.log")
    if os.system(f"git clone --mirror {repo['clone_url']} {clone_dir} >> " + sub_log_file) != 0:
        logging.error(f"Failed to clone all branches of {repo['clone_url']}.")

logging.info(f"Backup completed for user {GITHUB_USER} at {datetime.now()}")
logging.shutdown()