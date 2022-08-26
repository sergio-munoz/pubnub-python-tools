"""Configuaration for HTTP function callbacks."""
import os
from logging import INFO,DEBUG  # change it to DEBUG for more information
try: 
    import dotenv
except ImportError: 
    print("Warning: dotenv package not installed.")
    dotenv = None

# Current Root Path
ROOT_DIR = str(os.path.dirname(os.path.abspath(__file__)).rsplit("/config")[0])


# Set default variables #DANGER!
ON_REQUEST_URL = "https://ps.pndsn.com/v1/blocks/sub-key/sub-c-0b961af6-42b7-463d-ac2f-99a6714b57af/conn"
ON_REQUEST_PARAMS = {'channelid': 'us.e001.UUID'}
print(type(ON_REQUEST_PARAMS))
ON_REQUEST_BODY = {"Content": "Awesome bro!"} 
print(type(ON_REQUEST_BODY))

# PubNub On Request Environment Variables
if dotenv is not None:
    dotenv.load_dotenv()
    ON_REQUEST_URL = str(os.getenv('on_request_url'))
    # NOTE: there might be some json.load() needed for this to work:
    ON_REQUEST_PARAMS = str(os.getenv('on_request_params'))
    # NOTE: there might be some json.load() needed for this to work:
    ON_REQUEST_BODY = str(os.getenv('on_request_body'))
