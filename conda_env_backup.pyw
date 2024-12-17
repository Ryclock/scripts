import os
import subprocess
import logging
from config_loader import read_config_byconfigparser

backup_directory = eval(read_config_byconfigparser('PATH','backup_directory'))
log_directory = eval(read_config_byconfigparser('PATH','log_directory'))
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file = os.path.join(log_directory, "conda_env_backup.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file
)

if not os.path.exists(backup_directory):
    os.makedirs(backup_directory)
    logging.info(f"create directory '{backup_directory}' for backup")

env_list = subprocess.check_output(
    ["conda", "env", "list"], universal_newlines=True)
env_paths = [line.split()[1] for line in env_list.splitlines()[4:]
             if line.strip() and line.startswith("#") is False]

if not env_paths:
    logging.info("No conda environments found. Skipping backup.")
else:
    for env_path in env_paths:
        if not env_path:
            logging.warning(
                "Empty environment path encountered. Skipping backup for this environment.")
            continue
        env_name = os.path.basename(env_path)
        backup_file = os.path.join(
            backup_directory, f"{env_name}_environment.yml")

        activate_env_command = f"conda activate {env_name}"
        export_env_command = f"conda env export -n {env_name} > {backup_file}"

        logging.info(f"conda env '{env_name}' has backup to '{backup_file}'")
        try:
            subprocess.run(activate_env_command, shell=True, check=True)
            subprocess.run(export_env_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error: {e}")

logging.shutdown()
