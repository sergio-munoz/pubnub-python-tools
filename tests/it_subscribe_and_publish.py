"""Simple test file for main_app.py."""
from pubnub_python_tools.app import main_app
from logging import DEBUG
from pubnub_python_tools.logger.logging_config import set_logger
from unittest import TestCase

# Create a logger if needed for testing cases
LOG_TEST = set_logger("it_subscribe_and_publish", DEBUG)  # Defaults as INFO

class RunMainAppTests(TestCase):

    def test_subscribe_ok():
        pass
    def test_subscribe_fail():
        pass
    def test_publish_ok():
        pass
    def test_publish_fail():
        pass

    def test_simple_function(self):
        """Tests simple function from main_app.py."""
        LOG_TEST.info("Testing simple_function")
        self.assertEqual(main_app.simple_function(1),2)
