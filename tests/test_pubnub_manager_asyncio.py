"""Unittest file for pubnub_manager_asyncio.py."""
import asyncio
import random
import string

from unittest import TestCase
from logging import DEBUG
from functools import wraps

from src.pubnub_python_tools.logger.logging_config import set_logger
from src.pubnub_python_tools.config.module_config import SUBSCRIBE_KEY, PUBLISH_KEY
from src.pubnub_python_tools.app.pubnub_listener import MySubscribeCallback
from src.pubnub_python_tools.app import pubnub_manager_asyncio as pma

LOG = set_logger("test_pubnub_manager_asyncio", DEBUG)  # Create a logger if needed. Default: INFO


def async_test(f):
    """Decorator to create asyncio context for asyncio methods or functions."""
    @wraps(f)
    def g(*args, **kwargs):
        args[0].loop.run_until_complete(f(*args, **kwargs))
    return g


class TestPubNubAsyncioManager(TestCase):
    """Test PubNubAsyncioManager."""

    @classmethod
    def setUpClass(cls):
        """setUp Class event loop."""
        cls.loop = asyncio.get_event_loop()
        # cls.future = cls.loop.run_until_complete(setup_server())

    def setUp(self):
        """setUp PubNub instance."""
        # Start empty Manager and override below at async run()
        self.server = None
        self.channel = "test.channel"
        self.message = "test_message"

        async def run():
            """setUp async resources."""
            # Start PubNub instance without default_listeners to test our own
            self.server = pma.PubNubAsyncioManager(SUBSCRIBE_KEY, PUBLISH_KEY, "UUID", default_listeners=False)
            # await self.async_server.async_init()
        self.loop.run_until_complete(run())

    def tearDown(self):
        """tearDown PubNub running instances."""
        self.server.unsubscribe(self.channel)

        async def run():
            """tearDown async resources."""
            await self.server.pn.stop()
        self.loop.run_until_complete(run())

    @async_test
    async def test_publish_async(self):
        """Test publish a message async."""
        envelope = await self.server.publish(self.channel, self.message)

        # The following should be encapsulated but this is how we can test it
        if envelope.is_error():
            # There is an error
            LOG.error("Error %s", str(envelope))
            LOG.error("Error category #%d", envelope.status.category)
            self.fail()
        else:
            # There is no error
            response = str(envelope.result)  # get e.result as str
            expected = f'Publish success with timetoken {response.split()[-1]}'  # Extract timetoken
            LOG.info(str(envelope.result))
            self.assertEqual(response, expected)

    @async_test
    async def test_subscribe_async_message(self):
        """Test subscribe to a channel async message."""
        # Create callback
        callback = MySubscribeCallback()

        # Add callback listener to PubNub instance
        self.server.add_listener(callback)

        # Subscribe to channel
        self.server.subscribe(self.channel)

        # give time for subscribe to complete
        await asyncio.sleep(1)

        # await publish to be done
        await self.server.publish(self.channel, self.message)

        # give time for callback to return
        await asyncio.sleep(3)

        # get result
        result = callback.get_message()
        self.assertIsNotNone(result)
        LOG.debug("Callback result: %s", str(result))

        print(result)

        # Craft expected dict object
        expected = {
            "channel": self.channel,
            "subscription": None,
            "timetoken": result['timetoken'],  # extract timetoken from result
            "payload": self.message,
            "publisher": self.server.device_uuid  # extract publisher from server UUID
        }

        # assert result callback
        self.assertEqual(expected, result)

    @async_test
    async def test_subscribe_async_presence(self):
        """Test subscribe to a channel async presence.

        This test can fail:
            if the user_id is already in the channel.
            or
            if the join event happens too fast.
        Run it multiple times until figuring out how to avoid this issue.
        """
        # Create callback
        callback = MySubscribeCallback()

        # Add callback listener to PubNub instance
        self.server.add_listener(callback)

        # Check you're unsubscribed
        self.server.unsubscribe(self.channel)
        await asyncio.sleep(1)

        # Subscribe to channel with presence
        self.server.subscribe(self.channel, presence=True)
        await asyncio.sleep(5)  # give time for subscribe to complete

        # get result
        result = callback.get_presence()
        LOG.info("Callback result: %s", str(result))
        await asyncio.sleep(3)  # give time for subscribe to complete
        self.assertIsNotNone(result)

        # Craft expected dict object
        expected = {
            "event": 'join',
            "channel": f'{self.channel}',
            "occupancy": 1,
            "state": None,
            "subscription": None,
            "UUID": self.server.device_uuid,  # extract publisher from server UUID
            "timestamp": result['timestamp'],  # extract timestamp from result
            "timetoken": result['timetoken'],  # extract timetoken from result
            "joined": None,
            "left": None,
            "timed_out": None
        }

        # assert result callback
        self.assertEqual(expected, result)

    @async_test
    async def test_here_now_async(self):
        """Test hereNow async to a channel."""
        envelope = await self.server.here_now(self.channel)

        # The following should be encapsulated but this is how we can test it
        if envelope.is_error():
            # There is an error
            LOG.error("Error %s", str(envelope))
            LOG.error("Error category #%d", envelope.status.category)
            self.fail()
        else:
            # There is no error
            response = str(envelope.result)  # get e.result as str
            num_channels = len(envelope.result.channels)
            occupancy = None
            for channel_data in envelope.result.channels:
                LOG.debug("channel: %s", channel_data.channel_name)
                LOG.debug("occupancy: %s", channel_data.occupancy)
                occupancy = channel_data.occupancy

                LOG.debug("occupants: %s", channel_data.channel_name)
            for occupant in channel_data.occupants:
                LOG.debug("uuid %s, state: %s", occupant.uuid, occupant.state)
            exp = f'HereNow Result total occupancy: {occupancy}, total channels: {num_channels}'
            LOG.info(str(envelope.result))
            self.assertEqual(response, exp)
        self.server.unsubscribe(self.channel)

    #@async_test
    #async def test_here_now_async_multiple_channels(self):
        #"""Test hereNow async to a channel list."""
        #self.server.unsubscribe(self.channel)
        #await asyncio.sleep(1)
        #rnd_ch = ''.join(random.choices(string.ascii_uppercase + string.digits, k=11))
        #envelope = await self.server.here_now((self.channel, rnd_ch))  # this is cache busted

        ## The following should be encapsulated but this is how we can test it
        #if envelope.is_error():
            ## There is an error
            #LOG.error("Error %s", str(envelope))
            #LOG.error("Error category #%d", envelope.status.category)
            #self.fail()
        #else:
            ## There is no error
            #response = str(envelope.result)  # get e.result as str
            #print("Response: ", response)
            #expected = "HereNow Result total occupancy: 0, total channels: 0"
            #self.assertEqual(expected, response)
