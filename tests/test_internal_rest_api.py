"""Test file for pubnub_internal_rest_api.py."""
from unittest import TestCase
from logging import DEBUG

from src.pubnub_python_tools.logger.logging_config import set_logger
from src.pubnub_python_tools.app.pubnub_internal_rest_api import authenticate, get_accounts, get_accounts_ids, get_apps, get_apps_ids, get_app_based_usage

LOG = set_logger("pubnub_internal_rest_api", DEBUG)  # Create a logger if needed. 


class TestPubNubInternalRestAPI(TestCase):

    def test_authenticate(self):
        """Tests authenticate function."""
        LOG.info("Testing authenticate()")
        EMAIL = "6unrdlsk2@mozmail.com"
        PASSWORD = "=T[(_VD9<?Fv=k>d"

        resp = authenticate(EMAIL, PASSWORD)
        LOG.debug(resp)

        # Expect the id to be 594221
        self.assertEqual(resp[0], 594221)
        # Expect token not to be empty
        self.assertIsNotNone(resp[1])

    def test_authenticate_incorrect_credentials(self):
        """Tests authenticate incorrect credentials function."""
        LOG.info("Testing invalid credentials authenticate()")
        EMAIL = "garbage"
        PASSWORD = "not_a_password"

        with self.assertRaises(Exception):  # TODO - Add specific exception
            authenticate(EMAIL, PASSWORD)

    def test_get_accounts(self):
        """Tests get_accounts function."""
        LOG.info("Testing get_accounts()")
        EMAIL = "6unrdlsk2@mozmail.com"
        PASSWORD = "=T[(_VD9<?Fv=k>d"
        auth = authenticate(EMAIL, PASSWORD)

        resp = get_accounts(auth[0], auth[1])
        LOG.debug(resp)
        self.assertIsNotNone(resp)

    def test_get_accounts_ids(self):
        """Tests get_accounts_ids function."""
        LOG.info("Testing get_accounts_ids()")
        EMAIL = "6unrdlsk2@mozmail.com"
        PASSWORD = "=T[(_VD9<?Fv=k>d"
        auth = authenticate(EMAIL, PASSWORD)
        accounts = get_accounts(auth[0], auth[1])

        resp = get_accounts_ids(accounts)
        LOG.debug(resp)
        self.assertEquals(resp, [594172])

    def test_get_accounts_invalid(self):
        """Tests get_accounts invalid function."""
        LOG.info("Testing authenticagte()")
        EMAIL = "6unrdlsk2@mozmail.com"
        PASSWORD = "=T[(_VD9<?Fv=k>d"
        auth = authenticate(EMAIL, PASSWORD)

        # Add 1 to the user_id
        with self.assertRaises(Exception):  # TODO - Add specific exception
            get_accounts(auth[0]+1, auth[1])

    def test_get_apps(self):
        """Tests get_apps function."""
        LOG.info("Testing get_apps()")
        EMAIL = "6unrdlsk2@mozmail.com"
        PASSWORD = "=T[(_VD9<?Fv=k>d"
        auth = authenticate(EMAIL, PASSWORD)
        accounts = get_accounts(auth[0], auth[1])
        accounts_ids = get_accounts_ids(accounts)

        resp = get_apps(accounts_ids[0], auth[1])
        LOG.debug(resp)
        self.assertIsNotNone(resp)

    def test_get_apps_ids(self):
        """Tests get_apps_ids function."""
        LOG.info("Testing get_apps_ids()")
        EMAIL = "6unrdlsk2@mozmail.com"
        PASSWORD = "=T[(_VD9<?Fv=k>d"
        auth = authenticate(EMAIL, PASSWORD)
        accounts = get_accounts(auth[0], auth[1])
        accounts_ids = get_accounts_ids(accounts)
        apps = get_apps(accounts_ids[0], auth[1])

        resp = get_apps_ids(apps)
        LOG.debug(resp)
        self.assertEquals(resp, [35415338])

    def test_get_app_based_usage(self):
        """Tests get_app_based_usage function."""
        LOG.info("Testing get_app_based_usage()")
        EMAIL = "6unrdlsk2@mozmail.com"
        PASSWORD = "=T[(_VD9<?Fv=k>d"
        auth = authenticate(EMAIL, PASSWORD)
        accounts = get_accounts(auth[0], auth[1])
        accounts_ids = get_accounts_ids(accounts)
        apps = get_apps(accounts_ids[0], auth[1])
        apps_ids = get_apps_ids(apps)

        resp = get_app_based_usage(apps_ids[0], auth[1], "transaction", "2022-12-01", "2021-12-02")
        LOG.debug(resp)
        self.assertIsNotNone(resp)

    def test_get_app_based_usage_invalid(self):
        """Tests get_app_based_usage invalid function."""
        LOG.info("Testing invalid get_app_based_usage()")

        with self.assertRaises(Exception):  # TODO - Add specific exception
            resp = get_app_based_usage("no_user", "no_token", "transaction", "2022-12-01", "2021-12-02")
            print(resp)
            LOG.debug(resp)