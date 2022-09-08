"""Main Wrapper --- Runs Python APP"""
import os
import sys

from pubnub_python_tools.app import main_app
from pubnub_python_tools.logger.logging_config import get_logger

ROOT_DIR = str(os.path.dirname(os.path.abspath(__file__)).rsplit("/scripts")[0])
sys.path.append(f"{ROOT_DIR}")

LOG = get_logger()  # Get logger if needed. Default: INFO

if __name__ == '__main__':
    LOG.info("Starting pubnub python tools main app.")

    # Runs main function on pubnub_python_tools/app/main_app.py
    main_app.main()

    LOG.info("Finished pubnub python tools main app.")
