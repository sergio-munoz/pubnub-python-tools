"""Test file for request_function.py."""
from pubnub_python_tools.app.pubnub_on_request import get
from pubnub_python_tools.logger.logging_config import set_logger
from unittest import TestCase

# Create a logger if needed for testing cases
from logging import DEBUG
LOG = set_logger("test_request_function", DEBUG)  # Defaults as INFO

class RunMainAppTests(TestCase):

    def test_request_function(self):
        """Tests request_function function from device_manager.py."""
        LOG.info("Testing request_function()")

        URL = "https://ps.pndsn.com/v1/blocks/sub-key/sub-c-0b961af6-42b7-463d-ac2f-99a6714b57af/conn"
        PARAMS = {'channelid': 'us.e001.UUID'}
        BODY = {"Content": "Awesome bro!"} 

        resp = get(URL, PARAMS, BODY)
        LOG.debug(resp)

        # Expect Content matches what we sent
        self.assertEqual(str(resp.content.decode()), "{\"Content\":\"Awesome bro!\"}")

        # Expect status code to be 200 OK
        self.assertEqual(resp.status_code, 200)
