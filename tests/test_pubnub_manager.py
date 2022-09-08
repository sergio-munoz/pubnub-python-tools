"""Simple test file for device_manager.py."""
import os
import time

from logging import DEBUG
from unittest import TestCase

from pubnub_python_tools.app import pubnub_manager as pm
from pubnub_python_tools.app.pubnub_listener import MySubscribeCallback
from pubnub_python_tools.app.pubnub_here_now_callback import here_now_callback
from pubnub_python_tools.logger.logging_config import set_logger
from pubnub_python_tools.config.module_config import SUBSCRIBE_KEY, PUBLISH_KEY

LOG = set_logger("test_pubnub_manager", DEBUG)  # Create a logger if needed. Default: INFO

# Global test folder
TEST_FOLDER = str(os.path.dirname(os.path.abspath(__file__)))

class TestPubNubManager(TestCase):
    """Test PubNubManager."""
    # NOTE: For more detauled comments see test_pubnub_manager_asyncio.py

    def setUp(self):
        """setUp PubNub instance."""
        self.server = pm.PubNubManager(SUBSCRIBE_KEY, PUBLISH_KEY, "UUID", default_listeners=False)
        self.channel = "test.channel"
        self.message = "test_message"

    def tearDown(self):
        """tearDown PubNub running instances."""
        self.server.unsubscribe(self.channel)
        self.server.pn.stop()

    def test_publish(self):
        """Test publish a message."""
        envelope = self.server.publish(self.channel, self.message)

        # The following should be encapsulated but this is how we can test it
        response = str(envelope.result)  # get e.result as str
        LOG.info(str(envelope.result))

        # Extract timetoken from result
        expected = f'Publish success with timetoken {response.split()[-1]}'
        self.assertEqual(expected, response)

    def test_subscribe_message(self):
        """Test subscribe to a channel message."""
        callback = MySubscribeCallback()                # create callback
        self.server._add_listener(callback)             # add callback
        self.server.subscribe(self.channel)             # subscribe
        time.sleep(4)
        self.server.publish(self.channel, self.message) # publish
        time.sleep(2)
        result = callback.get_message()                 # get result
        self.assertIsNotNone(result)                    # assert not empty
        LOG.debug("Callback result: %s", str(result))
        expected = {                                    # Craft expected dict object
            "channel": self.channel,
            "subscription": None,
            "timetoken": result['timetoken'],           # extract timetoken from result
            "payload": self.message,
            "publisher": self.server.device_uuid        # extract publisher from server UUID
        }

        # assert result callback
        self.assertEqual(expected, result)

    def test_subscribe_presence(self):
        """Test subscribe to a channel presence."""
        callback = MySubscribeCallback()                # create callback
        self.server._add_listener(callback)             # add callback
        self.server.unsubscribe(self.channel)           # unsubscribe
        time.sleep(1)
        self.server.subscribe(self.channel, presence=True) # subscribe with presence
        time.sleep(4)
        self.server.publish(self.channel, self.message) # publish
        time.sleep(2)
        result = callback.get_presence()                # get result
        self.assertIsNotNone(result)                    # assert not empty
        LOG.info("Callback result: %s", str(result))
        expected = {
            "event": 'join',
            "channel": f'{self.channel}',
            "occupancy": 1,
            "state": None,
            "subscription": None,
            "UUID": self.server.device_uuid,   # extract publisher from server UUID
            "timestamp": result['timestamp'],  # extract timestamp from result
            "timetoken": result['timetoken'],  # extract timetoken from result
            "joined": None,
            "left": None,
            "timed_out": None
        }

        # assert result callback
        self.assertEqual(expected, result)

    def test_here_now(self):
        """Test hereNow to a channel."""
        # Test with one subscribe
        occupancy = 1
        num_channels = 1
        self.server.unsubscribe(self.channel)
        time.sleep(1)
        self.server.subscribe(self.channel, presence=True)
        time.sleep(4)

        # Call here_now
        envelope = self.server.here_now(self.channel)
        time.sleep(3)
        response = str(envelope.result)
        LOG.info(response)

        exp = f'HereNow Result total occupancy: {occupancy}, total channels: {num_channels}'
        self.assertEqual(response, exp)
