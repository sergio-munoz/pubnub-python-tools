"""Simple test file for device_manager.py."""
from pubnub_python_tools.app import pubnub_manager
from pubnub_python_tools.logger.logging_config import set_logger
from pubnub_python_tools.config.module_config import SUBSCRIBE_KEY, PUBLISH_KEY
from logging import DEBUG
from unittest import TestCase
from time import sleep
import os
import sys

# Create a logger if needed for testing cases
LOG = set_logger("test_pubnub_manager", DEBUG)  # Defaults as INFO

# Global test folder
TEST_FOLDER = str(os.path.dirname(os.path.abspath(__file__)))

class RunMainAppTests(TestCase):
    # SubscribeKey and PublishKey are read from .env

    def test_init(self):
        LOG.info("Testing __init__")
        pm = pubnub_manager.PubNubManager(SUBSCRIBE_KEY, PUBLISH_KEY, user_id="UUID")
        self.assertIsNotNone(pm.pn)

    def test_subscribe(self):
        LOG.info("Testing subscribe")
        pm = pubnub_manager.PubNubManager(SUBSCRIBE_KEY, PUBLISH_KEY, user_id="UUID")

        LOG.debug("Testing subscribe to channel")
        channel = "testing.subscribe"

        # Testing real-time systems is not straight forward.
        # NOTE: I need to address this with more seasoned SA's and maybe even the engineering team.
        # A simple 'solution' is using different processes (or threads) and use one right away
        # and use the other one with a delay to assert the 'results' of the first one.
        # The only issue is if PN fails to deliver the pauload under (1000ms) which should be impossible.
        # due to PN ~200 ms delivery time.
        # NOTE 2: Cache busting, presence, objects, history, and C, C++ SDKs are probaly immune to these tests.
        # But again, in onder to really test this, you'll have to have access to underlying
        # AWS implementation with direct connection to a NLB's and due to the 7 Points of presence with PN:
        # Unless you specify a single Point of Presence (PoP) (r=<REGION>), then:
        # There might be message loss between subscribe API calls.
        # NOTE 3: It would really help an unknowing customer to have presence ACL enabled by default

        # Create a new process
        pid = os.fork()
        if pid == 0:
            pm.subscribe(channels=channel)
            sleep(5)
            print("Exit subscribe")
            sys.exit()
        else:
            sleep(1)
            pm.publish_message(channel=channel, message="TEST!")
            
        # Fail on purpose
        self.assertFalse(True)

    # def test_publish_message(self):
    #     LOG.info("Testing publish_message")
    #     pm = pubnub_manager.PubNubManager(user_id="UUID")
    #     self.assertIsNotNone(pm.pn)

    # def test_unsubscribe(self):
    #     LOG.info("Testing unsubscribe")
    #     pm = pubnub_manager.PubNubManager(user_id="UUID")
    #     self.assertIsNotNone(pm.pn)

    # def test_here_now(self):
    #     """Tests here_now cache busting using the PubNub SDK."""
    #     LOG.info("Testing here_now")

    #     # Subscribe with presence
    #     channel = "testing.here_now.default"
    #     uuid = "UUID"
    #     devices = ppt.main(["-u", uuid, "-s", channel, "-pres", "-here", channel])
    #     print(devices)
    #     self.assertTrue(False)
    #     LOG.info("Here_now hits cache 3s")
