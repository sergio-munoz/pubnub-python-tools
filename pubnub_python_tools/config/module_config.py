"""config.py with minimal configuration for the module."""
import os
from logging import INFO,DEBUG  # change it to DEBUG for more information
try: 
    import dotenv
except ImportError: 
    print("Warning: dotenv package not installed.")
    dotenv = None

# Current Root Path
ROOT_DIR = str(os.path.dirname(os.path.abspath(__file__)).rsplit("/config")[0])

# PubNub Environment Variables
if dotenv is not None:
    dotenv.load_dotenv()
    SUBSCRIBE_KEY = str(os.getenv('pubnub_subscribe_key'))
    PUBLISH_KEY = str(os.getenv('pubnub_publish_key'))
    USER_ID = str(os.getenv('pubnub_user_id'))
else:
    # Set empty variables
    SUBSCRIBE_KEY = None
    PUBLISH_KEY = None
    USER_ID = None


# Log Level default
DEFAULT_LOGGER_NAME = "main_log"
LOGGER_LEVEL = DEBUG   # change it to DEBUG for more information
LOGGER_FORMAT = "simple"
LOGGER_DIR = ROOT_DIR + "/logger"
