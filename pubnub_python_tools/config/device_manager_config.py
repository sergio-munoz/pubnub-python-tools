"""Configuaration for Device Manager."""
import os

try:
    import dotenv
except ImportError:
    print("Warning: dotenv package not installed.")
    dotenv = None

# Current Root Path
ROOT_DIR = str(os.path.dirname(os.path.abspath(__file__)).rsplit("/config")[0])

# PubNub On Request Environment Variables
if dotenv is not None:
    dotenv.load_dotenv()
    DEVICE_MANAGER_LOCATION = str(os.getenv('device_manager_location'))
else:
    # Set default variables #DANGER!
    DEVICE_MANAGER_LOCATION = ROOT_DIR + "/device_manager.db"
