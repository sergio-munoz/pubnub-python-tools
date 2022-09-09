"""config.py with minimal configuration for the module."""
import os

from logging import INFO  # change it to DEBUG for more information

try:
    import dotenv
except ImportError:
    print("Warning: dotenv package not installed.")
    dotenv = None

# Current Root Path
ROOT_DIR = str(os.path.dirname(os.path.abspath(__file__)).rsplit("/config")[0])

# OVERRIDE GLOBAL VARIABLES
SUBSCRIBE_KEY = None   # NOTE might be insecure to override
PUBLISH_KEY = None     # NOTE might be insecure to override
USER_ID = None         # NOTE might be insecure to override

# OVERRIDE LOGGER VARIABLES
DEFAULT_LOGGER_NAME = "main_log"   # main logger name
LOGGER_LEVEL = INFO                # logger level
LOGGER_DIR = ROOT_DIR + "/logger"  # logger directory
LOGGER_FORMAT = "simple"           # logger format

# PubNub Environment Variables
if dotenv is not None:
    dotenv.load_dotenv()
    SUBSCRIBE_KEY = str(os.getenv('PN_SUBSCRIBE_KEY'))
    PUBLISH_KEY = str(os.getenv('PN_PUBLISH_KEY'))
    USER_ID = str(os.getenv('PN_USER_ID'))
