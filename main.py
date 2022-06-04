import sys
import config_loader
from model.config import Configuration
from server.server import Server

def main(argv):
    config_path = argv[1]
    config: Configuration = config_loader.load_config(config_path)
    

if __name__ == "__main__":
    main(sys.argv)