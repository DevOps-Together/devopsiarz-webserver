from encodings import utf_8
import logging

from model.config import Configuration

def setup_logging(config: Configuration):
    logging.basicConfig(format=config.log_format, level=logging.INFO, encoding=utf_8, filename=config.log_file)
