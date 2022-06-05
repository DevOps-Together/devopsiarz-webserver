from dataclasses import dataclass
from json import load
from logging import error


@dataclass
class ConfigServer:
    __config_name: str = "./config/config.json"
    try:
        with open(__config_name, 'r') as config_file:
            config_data = load(config_file)
        port: int = config_data['port']
        hostname: str = config_data['hostname']
        address_server: str = config_data['address_server']
        web_directory: str = config_data['web-directory']
        start_html = config_data['start-html']
    except FileNotFoundError as err:
        error(f"{err}")
