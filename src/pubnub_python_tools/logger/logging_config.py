"""Configuration file for logging."""
import logging

from ..config.module_config import LOGGER_DIR,DEFAULT_LOGGER_NAME,LOGGER_LEVEL,LOGGER_FORMAT

# Catchall
if not LOGGER_LEVEL:
    LOGGER_LEVEL = logging.INFO
if not DEFAULT_LOGGER_NAME:
    DEFAULT_LOGGER_NAME = "main_log"
if not LOGGER_FORMAT:
    LOGGER_FORMAT = "simple"


def get_logger(log_name=DEFAULT_LOGGER_NAME):
    logger = logging.getLogger(log_name)
    return logger
    """Get a configured logger.
    :param log_name: Name of the logger
    """

# Create a simple logger in default directory "/Logger"
def set_logger(log_name=DEFAULT_LOGGER_NAME, log_level=LOGGER_LEVEL, format=LOGGER_FORMAT):
    """Create a simple logger in the default directory.
    :param log_name: Name of the logger and logger_name.log.
    :param log_level: logging.Debug, logging.Warning, etc.
    :param format: Formatter to use. See `set_formatter_format(option)`.
    :return: logger.
    """
    # Create Logger with name and level
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)

    # Define a formatter for the Logger (Defaults to simple)
    formatter = set_formatter_format(format)

    # Set path of the logger using ROOT_DIR and log_name
    path = f"{LOGGER_DIR}/{log_name}.log"
    print(f"Using {path} as the log file")

    # Set the and formatter and fileHandler
    fileh = logging.FileHandler(path, 'a')
    fileh.setFormatter(formatter)
    logger.addHandler(fileh)

    return logger  # Return Logger


def set_formatter_format(option='simple'):
    """Choose a formatter from the following or create your own.
    `simple` - Time LoggerName Level - Message
    `process` - Time moduleName -> processId lineNo Level - Message
    `function` - Time moduleName funcName -> lineNo Level - Message
    :param options: simple, process, function, custom.
    :return: formatter to be set with `setFormatter`.
    """
    # Check for valid input
    options = ['simple', 'process', 'function']
    if option not in options:
        print("Input error!")
        raise ValueError
    # Define a simple formatter
    if option == 'simple':
        return logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Define a process formatter
    if option == 'process':
        return logging.Formatter(
            '%(asctime)s %(module)s -> %(process)d %(lineno)d %(levelname)s' +
            ' -  %(message)s')
    # Define a function formatter
    if option == 'function':
        return logging.Formatter(
            '%(asctime)s %(module)s %(funcName)s -> %(lineno)d %(levelname)s' +
            ' -  %(message)s')
