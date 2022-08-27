"""Main Wrapper --- Runs Python APP"""

import os
import sys

ROOT_DIR = str(os.path.dirname(os.path.abspath(__file__)).rsplit("/scripts")[0])
#sys.path.append(f"{ROOT_DIR}/pubnub_python_tools")
sys.path.append(f"{ROOT_DIR}")
print(sys.path)

from pubnub_python_tools.app import main_app

from pubnub_python_tools.logger.logging_config import set_logger

# Start logger configuration
set_logger()

# Runs main function on pubnub_python_tools/app/main_app.py
if __name__ == '__main__':
    main_app.main()
