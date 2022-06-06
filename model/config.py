from dataclasses import dataclass


@dataclass
class Configuration:
    port: int = 80
    address: str = '0.0.0.0'
    log_file: str = 'log/httpy.log'
    log_format: str = '%(asctime)s - %(module)s.%(funcName)s:%(lineno)d - %(levelname)s - %(message)s'
    web_directory: str = './resources/www'
    index_files = []
    security:str = 'none'
    username:str = ''
    password:str = ''
    list_files:bool = False
