
def read_config_byconfigparser(key_section: str, key_name: str) -> str:
    import configparser
    import os
    conf_path = os.path.dirname(__file__) + "/config"
    conf_inner = configparser.ConfigParser()
    if not conf_inner.read(conf_path):
        raise FileNotFoundError(conf_path)

    try:
        value = conf_inner.get(key_section, key_name)
        return value
    except (configparser.NoSectionError, configparser.NoOptionError):
        return None

if __name__ == '__main__':
    import os
    filename = os.path.basename(__file__)
    value = read_config_byconfigparser(filename, "test_key")
    print(value)
