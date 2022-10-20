"""Test file for request_function.py."""
from unittest import TestCase
from logging import DEBUG

from src.pubnub_python_tools.logger.logging_config import set_logger
from src.pubnub_python_tools.app.pubnub_on_request import get

LOG = set_logger("test_request_function", DEBUG)  # Create a logger if needed. 


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
        # self.assertEqual(str(resp.content.decode()), str({'Content': 'Awesome bro!'}))

        # Expect status code to be 200 OK
        self.assertEqual(resp.status_code, 200)
