"""Test file for cli/v1.py."""
from logging import DEBUG
from unittest import TestCase

from src.pubnub_python_tools.cli.v1 import create_parser
from src.pubnub_python_tools.logger.logging_config import set_logger

LOG = set_logger("test_v1", DEBUG)  # Create a logger if needed. Default: INFO


class TestCliV1(TestCase):

    # setup
    def setUp(self):
        self.parser = create_parser()

    def test_parse_arguments_short_flags(self):
        """Test parsed arguments."""
        # you can also test long flags but it's redundant.
        parsed = self.parser.parse_args(['--version'])
        self.assertEqual(parsed.version, True)
        parsed = self.parser.parse_args(['-a', 'a.test'])
        self.assertEqual(parsed.async_cmd, 'a.test')
        parsed = self.parser.parse_args(['-dm', 'dm.test'])
        self.assertEqual(parsed.dev_man, 'dm.test')
        parsed = self.parser.parse_args(['-here', 'here.test'])
        self.assertEqual(parsed.here_now, 'here.test')
        parsed = self.parser.parse_args(['-m', 'm.test'])
        self.assertEqual(parsed.message, 'm.test')
        parsed = self.parser.parse_args(['-p', 'p.test'])
        self.assertEqual(parsed.publish, 'p.test')
        parsed = self.parser.parse_args(['-pk', 'pk.test'])
        self.assertEqual(parsed.publish_key, 'pk.test')
        parsed = self.parser.parse_args(['-pres'])
        self.assertEqual(parsed.presence, True)
        parsed = self.parser.parse_args(['-s', 's.test'])
        self.assertEqual(parsed.subscribe, 's.test')
        parsed = self.parser.parse_args(['-sk', 'sk.test'])
        self.assertEqual(parsed.subscribe_key, 'sk.test')
        parsed = self.parser.parse_args(['-u', 'u.test'])
        self.assertEqual(parsed.uuid, 'u.test')
        parsed = self.parser.parse_args(['-us', 'us.test'])
        self.assertEqual(parsed.unsubscribe, 'us.test')

    def test_parse_arguments_invalid(self):
        test_arguments = '--unknown invalid'
        self.parser.parse_args(test_arguments.split())
        expected = f"unrecognized arguments: {test_arguments}"
        self.assertEqual(self.parser.error_message, expected)

    def test_parse_arguments_empty(self):
        test_arguments = None
        self.parser.parse_args(test_arguments)
        print(self.parser.error_message)
        expected = "invalid empty arguments"
        self.assertEqual(self.parser.error_message, expected)