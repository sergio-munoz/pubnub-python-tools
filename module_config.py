"""config.py with minimal configuration for the module."""
import os
from logging import INFO,DEBUG  # change it to DEBUG for more information
from dotenv import load_dotenv

# Current Root Path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# PubNub Environment Variables
load_dotenv()
SUBSCRIBE_KEY = str(os.getenv('pubnub_subscribe_key'))
PUBLISH_KEY = str(os.getenv('pubnub_publish_key'))
USER_ID = str(os.getenv('pubnub_user_id'))

# Log Level default
DEFAULT_LOGGER_NAME = "main_log"
LOGGER_LEVEL = DEBUG   # change it to DEBUG for more information
LOGGER_FORMAT = "simple"