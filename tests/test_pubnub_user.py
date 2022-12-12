"""Test file for pubnub_user.py."""
from unittest import TestCase
from logging import DEBUG

from src.pubnub_python_tools.logger.logging_config import set_logger
from src.pubnub_python_tools.app.pubnub_user import PubNubUser

LOG = set_logger("test_pubnub_user", DEBUG)  # Create a logger if needed. 


class TestPubNubUser(TestCase):

    def setUp(self):
        """SetUp PubNub user."""
        self.user = PubNubUser()

    def test_login(self):
        """Tests login function."""
        LOG.info("Testing login()")
        EMAIL = "6unrdlsk2@mozmail.com"
        PASSWORD = "=T[(_VD9<?Fv=k>d"
        is_login = self.user.login(EMAIL, PASSWORD)
        LOG.debug(is_login)
        self.assertTrue(is_login)

    def test_login_invalid(self):
        """Tests login invalid function."""
        LOG.info("Testing invalid login()")
        EMAIL = "garbage"
        PASSWORD = "not_a_password"
        is_login = self.user.login(EMAIL, PASSWORD)
        LOG.debug(is_login)
        self.assertFalse(is_login)

    def test_load(self):
        """Tests load function."""
        LOG.info("Testing load()")
        EMAIL = "6unrdlsk2@mozmail.com"
        PASSWORD = "=T[(_VD9<?Fv=k>d"
        self.user.login(EMAIL, PASSWORD)

        loaded = self.user.load()
        LOG.debug(loaded)
        self.assertTrue(loaded)

    def test_all_metrics(self):
        """Tests all_metrics function."""
        LOG.info("Testing all_metrics()")
        EMAIL = "6unrdlsk2@mozmail.com"
        PASSWORD = "=T[(_VD9<?Fv=k>d"
        self.user.login(EMAIL, PASSWORD)
        self.user.load()

        metrics = self.user.all_metrics()
        self.assertIsNotNone(metrics)
