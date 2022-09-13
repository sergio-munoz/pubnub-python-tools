"""Test file for cli/v1.py."""
from logging import DEBUG
from unittest import TestCase

from src.pubnub_python_tools.cli.v1 import get_parser, create_parser
from src.pubnub_python_tools.logger.logging_config import set_logger

LOG = set_logger("test_v1", DEBUG)  # Create a logger if needed. Default: INFO


class TestCliV1(TestCase):
    """Test cli/v1.py
    """
    def test_created_parser(self):
        """Test created parser.
        """
        parser = create_parser()
        self.assertIsNotNone(parser)

    def test_parsed_arguments_short_flags(self):
        """Test parsed arguments.
        """
        parser = create_parser()
        parsed = parser.parse_args(['-sk', 'sk.test'])
        self.assertEqual(parsed.subscribe_key, 'sk.test')
        parsed = parser.parse_args(['-pk', 'pk.test'])
        self.assertEqual(parsed.publish_key, 'pk.test')
        parsed = parser.parse_args(['-u', 'u.test'])
        self.assertEqual(parsed.uuid, 'u.test')
        parsed = parser.parse_args(['-pres'])
        self.assertEqual(parsed.presence, True)
        parsed = parser.parse_args(['-p', 'p.test'])
        self.assertEqual(parsed.publish, 'p.test')
        parsed = parser.parse_args(['-m', 'm.test'])
        self.assertEqual(parsed.message, 'm.test')
        parsed = parser.parse_args(['-us', 'us.test'])
        self.assertEqual(parsed.unsubscribe, 'us.test')
        parsed = parser.parse_args(['-here', 'here.test'])
        self.assertEqual(parsed.here_now, 'here.test')
        parsed = parser.parse_args(['-dm', 'dm.test'])
        self.assertEqual(parsed.dev_man, 'dm.test')

    # you can also test long flags but it's redundant.

    def test_get_parser(self):
        """Test get_parser() with arguments
        """
        parsed = get_parser(['--subscribe-key', 'test'])
        self.assertEqual(parsed.subscribe_key, 'test')
        # You can also test all arguments but it's redundant
        # As long as one works, all should work
        # Unless you want to test for types or count arguments, etc.