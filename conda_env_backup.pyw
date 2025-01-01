import os
import subprocess
import logging
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

env_list = subprocess.check_output(
    ["conda", "env", "list"], universal_newlines=True)
env_list_effective = [line.split()
             for line in env_list.splitlines()
             if line.strip() and not line.startswith("#")]

if not env_list_effective:
    logging.info("No conda environments found. Skipping backup.")
else:
    for env_li in env_list_effective:
        env_path = env_li[1]
        if env_path == "*":
            env_path = env_li[2]
        if not env_li:
            logging.warning(
                "Empty environment path encountered. Skipping backup for this environment.")
            continue
        env_name = env_li[0]
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
