"""Runs Python App. Supports sync and async."""
# import os
# import sys

from ..app import main_app
from ..logger.logging_config import get_logger
from ..config.time_config import TimeConfig

LOG = get_logger()  # Get logger if needed. Default: INFO


def main():
    LOG.info("Starting pubnub-python-tools app")

    # TODO: Extract arguments from here and decide if
    # the process should be run on the foreground
    # the process should be run on the background
    # the process should be run on the foreground async
    # the process should be run on the background async

    # TODO: Validate arguments.
    # security wise always validate user input

    # TODO: Logging.
    # come up with standards to use for logging.
    # check what are they using in the official pn sdk

    # Track time
    LOG.debug("Started tracking execution time of main function.")
    time_config = TimeConfig()

    # Runs main function on pubnub_python_tools/app/main_app.py
    main_app.main()

    # End tracking time
    td = time_config.total_seconds()
    LOG.debug(f'Finished tracking execution time of main function: {td:.03f}ms')

    LOG.info("Finished pubnub-python-tools-app")


if __name__ == '__main__':
    main()
