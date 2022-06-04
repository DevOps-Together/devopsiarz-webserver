from dataclasses import dataclass


@dataclass
class Configuration:
    port: int = 80
    web_directory: str = './resources/www'
    index_files = []
    security:str = 'none'
    username:str = ''
    password:str = ''
    list_files:bool = False
