import configparser
import logging
import os

CONFIG = configparser.RawConfigParser()

# preserve case on keys
CONFIG.optionxform = str

logger = logging.getLogger(__name__)

try:
    CONFIG.read(os.environ["TALKING_CONF"])
except KeyError as e:
    logger.fatal("Must set env var TALKING_CONF")
    raise e


def get_postgres_url():
    postgres_config = dict(CONFIG.items("postgres"))
    return "postgresql://{username}:{password}@{host}:{port}/{dbname}".format(**postgres_config)
