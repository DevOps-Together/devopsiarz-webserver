import json
from model.config import Configuration
from types import SimpleNamespace as Namespace

def load_config(path):
    config_file = open(path,"r")
    json_config = config_file.read()
    return json.loads(json_config, object_hook=lambda d: Namespace(**d))
