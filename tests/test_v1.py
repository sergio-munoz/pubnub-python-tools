"""Test file for cli/v1.py."""
from pubnub_python_tools.cli.v1 import get_parser, create_parser
from pubnub_python_tools.logger.logging_config import set_logger
from unittest import TestCase
import sys

# Create a logger if needed for testing cases
from logging import DEBUG
LOG = set_logger("test_v1", DEBUG)  # Defaults as INFO

class RunMainAppTests(TestCase):

    def setUp(self):
        self.parser = create_parser()

    def test_something(self):
        parsed = self.parser.parse_args(['--subscribe-key', 'test'])
        self.assertEqual(parsed.subscribe_key, 'test')
