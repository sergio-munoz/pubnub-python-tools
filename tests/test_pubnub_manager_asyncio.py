"""Unittest file for pubnub_manager_asyncio.py."""
import asyncio

from functools import wraps
from logging import DEBUG
from re import L
from unittest import TestCase

from pubnub_python_tools.app import pubnub_manager_asyncio
from pubnub_python_tools.app.pubnub_listener import MySubscribeCallback
from pubnub_python_tools.logger.logging_config import set_logger
from pubnub_python_tools.config.module_config import SUBSCRIBE_KEY, PUBLISH_KEY

LOG = set_logger("test_asyncio", DEBUG)  # Create a logger if needed. Default: INFO

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
        # cls.future = cls.loop.run_until_complete(setup_web_server(app, host=LOCALHOST, port=ASYNC_SERVER_PORT))

    def setUp(self):
        """setUp PubNub instance."""
        # Start empty Manager and override below at async run()
        self.server = None

        async def run():
            """setUp async resources."""
            # Start PubNub instance without default_listeners to test our own
            self.server = pubnub_manager_asyncio.PubNubAsyncioManager(SUBSCRIBE_KEY, PUBLISH_KEY, user_id="UUID", default_listeners=False)
            # await self.async_server.async_init()
        self.loop.run_until_complete(run())

    def tearDown(self):
        """tearDown PubNub running instances."""
        async def run():
            """tearDown async resources."""
            await self.server.pn.stop()
        self.loop.run_until_complete(run())

    @async_test
    async def test_publish_async(self):
        """Test publish a message async."""
        e = await self.server.publish("ch","msg")
        
        # The following should be encapsulated but this is how we can test it
        if e.is_error():
            # There is an error
            LOG.error("Error %s" % str(e))
            LOG.error("Error category #%d" % e.status.category)
            self.assertTrue(False)  # Fail on purpose
        else:
            # There is no error
            response = str(e.result)  # get e.result as str
            expected = f'Publish success with timetoken {response.split()[-1]}'  # Extract timetoken
            LOG.info(str(e.result))
            self.assertEqual(response, expected)

    @async_test
    async def test_subscribe_async_message(self):
        """Test subscribe to a channel async message."""
        # test variables
        channel = "test.channel"
        message = "test.message"

        # Create callback
        callback = MySubscribeCallback()

        # Add callback listener to PubNub instance
        self.server.add_listener(callback)

        # Subscribe to channel
        self.server.subscribe(channel)

        # give time for subscribe to complete
        await asyncio.sleep(1)

        # await publish to be done
        await self.server.publish(channel, message)

        # give time for callback to return
        await asyncio.sleep(3)

        # get result
        result = callback.get_message()
        self.assertIsNotNone(result)
        LOG.debug("Callback result: %s", str(result))

        print(result)

        # Craft expected dict object
        expected = {
            "channel": channel,
            "subscription": None,
            "timetoken": result['timetoken'],  # extract timetoken from result
            "payload": message,
            "publisher": self.server.device_uuid  # extract publisher from server UUID
        }

        # assert result callback
        self.assertEqual(expected, result)
    
    @async_test
    async def test_subscribe_async_presence(self):
        """Test subscribe to a channel async presence."""
        # test variables
        channel = "test.channel"
        message = "test.message"

        # Create callback
        callback = MySubscribeCallback()

        # Add callback listener to PubNub instance
        self.server.add_listener(callback)

        # Subscribe to channel
        self.server.subscribe(channel, presence=True)

        # give time for subscribe to complete
        await asyncio.sleep(1)

        # await publish to be done
        await self.server.publish(channel, message)

        # give time for callback to return
        await asyncio.sleep(10)

        # get result
        result = callback.get_presence()
        self.assertIsNotNone(result)
        LOG.debug("Callback result: %s", str(result))

        print(result)

        # Craft expected dict object
        expected = {
            "event": 'join',
            "channel": f'{channel}-pres',  # explicitly add -pres to verify presence channel
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
        # test variables
        channel = "test.channel"

        e = await self.server.here_now(channel)

        # The following should be encapsulated but this is how we can test it
        if e.is_error():
            # There is an error
            LOG.error("Error %s" % str(e))
            LOG.error("Error category #%d" % e.status.category)
            self.assertTrue(False)  # Fail on purpose
        else:
            # There is no error
            response = str(e.result)  # get e.result as str
            total_channels = len(e.result.channels)
            occupancy = None
            for channel_data in e.result.channels:
                print("---")
                print("channel: %s" % channel_data.channel_name)
                print("occupancy: %s" % channel_data.occupancy)
                LOG.debug("channel: %s", channel_data.channel_name)
                LOG.debug("occupancy: %s", channel_data.occupancy)
                occupancy = channel_data.occupancy

                print("occupants: %s" % channel_data.channel_name)
                LOG.debug("occupants: %s", channel_data.channel_name)
            for occupant in channel_data.occupants:
                print("uuid: %s, state: %s" % (occupant.uuid, occupant.state))
                LOG.debug("uuid %s, state: %s", occupant.uuid, occupant.state)
            expected = f'HereNow Result total occupancy: {occupancy}, total channels: {total_channels}'
            LOG.info(str(e.result))
            self.assertEqual(response, expected)