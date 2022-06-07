from encodings import utf_8
import logging

from model.config import Configuration

def setup_logging(config: Configuration):
    logging.basicConfig(format=config.log_format, level=logging.INFO, encoding='utf-8', filename=config.log_file)
