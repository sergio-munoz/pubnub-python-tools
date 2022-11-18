"""Simple test file for device_manager.py."""
import os
import time

from logging import DEBUG
from unittest import TestCase

from src.pubnub_python_tools.logger.logging_config import set_logger
from src.pubnub_python_tools.config.module_config import SUBSCRIBE_KEY, PUBLISH_KEY
from src.pubnub_python_tools.app.pubnub_listener import MySubscribeCallback
from src.pubnub_python_tools.app.pubnub_here_now_callback import HereNowCallback
from src.pubnub_python_tools.app import pubnub_manager as pm

LOG = set_logger(
    "test_pubnub_manager", DEBUG
)  # Create a logger if needed. Default: INFO

# Global test folder
TEST_FOLDER = str(os.path.dirname(os.path.abspath(__file__)))


class TestPubNubManager(TestCase):
    """Test PubNubManager."""

    # NOTE: For more detailed comments see test_pubnub_manager_asyncio.py

    def setUp(self):
        """setUp PubNub instance."""
        self.server = pm.PubNubManager(
            SUBSCRIBE_KEY, PUBLISH_KEY, "UUID", default_listeners=False
        )
        self.channel = "test.channel"
        self.message = "test_message"

    def tearDown(self):
        """tearDown PubNub running instances."""
        self.server.unsubscribe(self.channel)
        self.server.pn.stop()

    def test_publish(self):
        """Test publish a message."""
        self.channel = "test.publish"

        # This is encapsulated on publish_wrap
        envelope = self.server.publish(self.channel, self.message)
        response = str(envelope.result)  # get e.result as str
        LOG.info(str(envelope.result))

        # Extract timetoken from result
        expected = f"Publish success with timetoken {response.split()[-1]}"
        self.assertEqual(expected, response)

    def test_publish_wrap(self):
        """Test publish wrap"""
        self.channel = "test.publish_wrap"
        response = self.server.publish_wrap(self.channel, self.message)
        expected = f"Publish success with timetoken {response.split()[-1]}"
        self.assertEqual(expected, response)

    def test_publish_wrap_error(self):
        """Test publish wrap error"""
        self.channel = "test.error.publish_wrap."
        response = self.server.publish_wrap(self.channel, self.message)
        err = "HTTP Client Error (400): [0,\"Wildcard maximum depth "
        expected = f"{err}{response.split()[-1]}"
        self.assertEqual(expected, response)

    def test_subscribe_message(self):
        """Test subscribe to a channel message."""
        self.channel = "test.channel.2"
        callback = MySubscribeCallback()  # create callback
        self.server._add_listener(callback)  # add callback
        self.server.subscribe(self.channel)  # subscribe
        time.sleep(4)
        self.server.publish(self.channel, self.message)  # publish
        time.sleep(2)
        result = callback.get_message()  # get result
        self.assertIsNotNone(result)  # assert not empty
        LOG.debug("Callback result: %s", str(result))
        expected = {  # Craft expected dict object
            "channel": self.channel,
            "subscription": None,
            "timetoken": result["timetoken"],  # extract timetoken from result
            "payload": self.message,
            "publisher": self.server.device_uuid,  # extract publisher from server UUID
        }

        # assert result callback
        self.assertEqual(expected, result)

    def test_subscribe_presence(self):
        """Test subscribe to a channel presence."""
        self.channel = "test.channel.3"
        callback = MySubscribeCallback()  # create callback
        self.server._add_listener(callback)  # add callback
        self.server.unsubscribe(self.channel)  # unsubscribe
        time.sleep(1)
        self.server.subscribe(self.channel, presence=True)  # subscribe with presence
        time.sleep(4)
        self.server.publish(self.channel, self.message)  # publish
        time.sleep(2)
        result = callback.get_presence()  # get result
        self.assertIsNotNone(result)  # assert not empty
        LOG.info("Callback result: %s", str(result))
        expected = {
            "event": "join",
            "channel": f"{self.channel}",
            "occupancy": 1,
            "state": None,
            "subscription": None,
            "UUID": self.server.device_uuid,  # extract publisher from server UUID
            "timestamp": result["timestamp"],  # extract timestamp from result
            "timetoken": result["timetoken"],  # extract timetoken from result
            "joined": None,
            "left": None,
            "timed_out": None,
        }

        # assert result callback
        self.assertEqual(expected, result)

    def test_unsubscribe(self):
        """Test unsubscribe to a channel."""
        self.channel = "test.channel.4"
        callback = MySubscribeCallback()  # Try with a subscribe callback
        self.server._add_listener(callback)
        self.server.subscribe(self.channel, presence=True)
        time.sleep(4)
        self.server.unsubscribe(self.channel)
        time.sleep(3)
        result = callback.get_presence()  # get result
        self.assertIsNotNone(result)  # assert not empty
        LOG.info("Callback result: %s", str(result))
        expected = {
            "event": "leave",
            "channel": f"{self.channel}",
            "occupancy": 0,
            "state": None,
            "subscription": None,
            "UUID": self.server.device_uuid,  # extract publisher from server UUID
            "timestamp": result["timestamp"],  # extract timestamp from result
            "timetoken": result["timetoken"],  # extract timetoken from result
            "joined": None,
            "left": None,
            "timed_out": None,
        }

        # assert result callback
        self.assertEqual(expected, result)

    def test_here_now(self):
        """Test hereNow in a channel."""
        # Test with no subscribes
        self.server.unsubscribe(self.channel)
        time.sleep(3)

        # Create HereNowCallback
        hnc = HereNowCallback()

        # Call here_now with override_listener
        self.server.here_now(self.channel, override_listener=hnc.here_now_callback)
        time.sleep(5)

        LOG.info(hnc)
        self.assertEqual(
            hnc.__repr__(),
            str(
                {
                    "here_now_channels": ["test.channel"],
                    "here_now_occupancy": [0],
                    "here_now_uuids": [],
                    "here_now_states": [],
                }
            ),
        )

        # Test with one subscribe
        self.server.unsubscribe(self.channel)
        time.sleep(1)
        self.server.subscribe(self.channel, presence=True)
        time.sleep(4)

        # Call here_now
        self.server.here_now(self.channel, override_listener=hnc.here_now_callback)
        time.sleep(3)

        LOG.info(hnc)
        self.assertEqual(
            hnc.__repr__(),
            str(
                {
                    "here_now_channels": ["test.channel"],
                    "here_now_occupancy": [1],
                    "here_now_uuids": ['UUID'],
                    "here_now_states": [None],
                }
            ),
        )
