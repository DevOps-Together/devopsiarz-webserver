from logging import info
import sys
from config_loader import load_config
from logging_config import setup_logging
from model.config import Configuration
from server.server import Server

def main(argv):
    config_path = argv[1]
    config: Configuration = load_config(config_path)
    setup_logging(config)
    info('Configuration loaded')
    info('Logging configured correctly')
    server = Server(config)
    info('Starting server')
    server.start()
    

if __name__ == "__main__":
    main(sys.argv)