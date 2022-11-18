"""Unit test file for main_app.py."""
from src.pubnub_python_tools.app import main_app
from src.pubnub_python_tools.logger.logging_config import set_logger
from src.pubnub_python_tools.__about__ import __version__
from logging import DEBUG
from unittest import TestCase

# Create a logger if needed for testing cases
LOG_TEST = set_logger("test_main_app", DEBUG)  # Defaults as INFO


class TestMainApp(TestCase):

    # Health-check function test - get current version
    def test_function_get_version(self):
        LOG_TEST.info("Test function get_version()")
        # This should never fail :)
        self.assertEqual(main_app.get_version(), __version__)

    def test_version(self):
        arg = "--version"
        expected = f"PubNub Python Tools v{__version__}"
        self.assertEqual(main_app.main([arg]), expected)

    def test_publish(self):
        args = ["--publish", "test.ch", "--message", "test123"]
        response = main_app.main(args)
        expected = f"Publish success with timetoken {response.split()[-1]}"
        self.assertEqual(response, expected)

    def test_args_invalid(self):
        arg = "--invalid"
        expected = f"unrecognized arguments: {arg}"
        self.assertEqual(main_app.main([arg]), expected)
