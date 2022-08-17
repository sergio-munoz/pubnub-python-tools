"""config.py with minimal configuration for the module."""
import os
from logging import INFO,DEBUG  # change it to DEBUG for more information
from dotenv import load_dotenv
from cli.v1 import create_cli_v1

# Current Root Path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# PubNub Environment Variables
load_dotenv()

SUBSCRIBE_KEY = str(os.getenv('pubnub_subscribe_key'))
PUBLISH_KEY = str(os.getenv('pubnub_publish_key'))
USER_ID = str(os.getenv('pubnub_user_id'))

# Override with CLI arguments if set
override_args = create_cli_v1()

if override_args.subscribe_key:
    SUBSCRIBE_KEY = override_args.subscribe_key
if override_args.publish_key:
    PUBLISH_KEY = override_args.publish_key
if override_args.uuid:
    USER_ID = override_args.uuid

# Log Level default
DEFAULT_LOGGER_NAME = "main_log"
LOGGER_LEVEL = DEBUG   # change it to DEBUG for more information
LOGGER_FORMAT = "simple"