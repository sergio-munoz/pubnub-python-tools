"""Main Wrapper --- Runs Python APP"""
from app import main_app
from logger.logging_config import set_logger

# Start logger configuration
set_logger()

# Runs main function on app/main_app.py
if __name__ == '__main__':
    main_app.main()