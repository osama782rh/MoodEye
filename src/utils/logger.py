import logging
import logging.config
import yaml


def setup_logging(config_path="src/config/logging_config.yaml"):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)


def get_logger(name):
    setup_logging()
    return logging.getLogger(name)
