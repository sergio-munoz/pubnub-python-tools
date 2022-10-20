"""Simple test file for device_manager.py."""
import os
import random
import string
import time

import pytest

from logging import DEBUG
from unittest import TestCase
from flaky import flaky

from src.pubnub_python_tools.logger.logging_config import set_logger
from src.pubnub_python_tools.config.module_config import SUBSCRIBE_KEY, PUBLISH_KEY
from src.pubnub_python_tools.app.pubnub_here_now_callback import HereNowCallback
from src.pubnub_python_tools.app import pubnub_manager as pm

LOG = set_logger(
    "test_pubnub_manager", DEBUG
)  # Create a logger if needed. Default: INFO

# Global test folder
TEST_FOLDER = str(os.path.dirname(os.path.abspath(__file__)))

SERVERS = []
TEST_CHANNEL = "test.channel"
CLEANUP_RUNNER = True


def setup_module():
    """setUp 3 pubnub instances and subscribe with presence."""
    for i in range(3):
        SERVERS.append(
            pm.PubNubManager(SUBSCRIBE_KEY, PUBLISH_KEY, f"UUID{i}", default_listeners=False),
        )
    print("Setup complete")


def teardown_module():
    """Stop pubnub instances."""
    [i.unsubscribe(TEST_CHANNEL) for i in SERVERS]
    [i.pn.stop() for i in SERVERS]
    print("Teardown done")


class TestHereNowCache(TestCase):
    """Test HereNow Cache."""

    def setUp(self):
        """setUp data to run before each test."""
        self.channel = TEST_CHANNEL
        self.message = "test_message"
        # Create HereNowCallback with sorted uuids for testing
        self.hnc = HereNowCallback(sort_uuids=True)

    def tearDown(self):
        """tearDown data to destroy after each test."""
        global CLEANUP_RUNNER
        if CLEANUP_RUNNER:
            [i.unsubscribe(self.channel) for i in SERVERS]
            CLEANUP_RUNNER = False
            print("CLEANUP DONE BOIZ!")
        print("NO CLEANUP")

    @flaky(max_runs=3)
    def test_hit_cache(self):
        """Test hereNow hit cache."""
        # Test with 3 subscribes, hit cache
        [i.subscribe(self.channel, presence=True) for i in SERVERS]

        # Call here_now with override_listener
        SERVERS[0].here_now(self.channel, override_listener=self.hnc.here_now_callback)
        time.sleep(3)

        LOG.info(self.hnc)
        self.assertEqual(
            self.hnc.__repr__(),
            str(
                {
                    "here_now_channels": ["test.channel"],
                    "here_now_occupancy": [0],
                    "here_now_uuids": [],
                    "here_now_states": [],
                }
            ),
        )

        # Call here_now again after waiting
        time.sleep(5)
        SERVERS[0].here_now(self.channel, override_listener=self.hnc.here_now_callback)
        time.sleep(3)

        LOG.info(self.hnc)
        self.assertEqual(
            self.hnc.__repr__(),
            str(
                {
                    "here_now_channels": ["test.channel"],
                    "here_now_occupancy": [3],
                    "here_now_uuids": ['UUID0', 'UUID1', 'UUID2'],
                    "here_now_states": [None, None, None],
                }
            ),
        )

    @flaky(max_runs=3)
    def test_cache_bust(self):
        """Test hereNow cache busting adding a randomly named channel."""
        # Test with 3 subscribes
        # This should be actually a fixture, but subscribing again
        # would only send a new join request but won't interfere with the current
        # maybe.
        [i.subscribe(self.channel, presence=True) for i in SERVERS]

        # Create random channel
        rnd_ch = 'test.'+''.join(random.choices(string.ascii_uppercase + string.digits, k=11))

        # Call herenow
        time.sleep(1)
        SERVERS[0].here_now((self.channel, rnd_ch), override_listener=self.hnc.here_now_callback)
        time.sleep(3)

        LOG.info(self.hnc)
        print(self.hnc)
        self.assertEqual(
            self.hnc.__repr__(),
            str(
                {
                    "here_now_channels": ["test.channel"],
                    "here_now_occupancy": [3],
                    "here_now_uuids": ['UUID0', 'UUID1', 'UUID2'],
                    "here_now_states": [None, None, None],
                }
            ),
        )

