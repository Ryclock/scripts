import subprocess
import sys

try:
    import ruamel.yaml
except ImportError:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "ruamel.yaml"])
    import ruamel.yaml


yaml_file = 'environment.yml'

yaml = ruamel.yaml.YAML()
yaml.indent(offset=2)

with open(yaml_file, 'r') as file:
    data = yaml.load(file)

updated_dependencies = []
for package in data['dependencies']:
    if isinstance(package, str):
        package_name = package.split('=')[0].strip()
        updated_dependencies.append(package_name)

data['dependencies'] = updated_dependencies

with open(yaml_file, 'w') as file:
    yaml.dump(data, file)
