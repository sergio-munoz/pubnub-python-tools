from pubnub_python_tools.app import pubnub_manager_asyncio
from pubnub_python_tools.app.pubnub_listener import MySubscribeCallback
from pubnub_python_tools.logger.logging_config import set_logger
from pubnub_python_tools.config.module_config import SUBSCRIBE_KEY, PUBLISH_KEY
from logging import DEBUG
from functools import wraps
from unittest import TestCase
import asyncio

LOG = set_logger("test_asyncio", DEBUG)  # Defaults as INFO

def async_test(f):
    """
    Decorator to create asyncio context for asyncio methods or functions.
    """
    @wraps(f)
    def g(*args, **kwargs):
        args[0].loop.run_until_complete(f(*args, **kwargs))
    return g

class TestPubNubAsyncioManager(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.get_event_loop()
        # cls.future = cls.loop.run_until_complete(setup_web_server(app, host=LOCALHOST, port=ASYNC_SERVER_PORT))

    def setUp(self):
        # Start empty Manager and override below at async run()
        self.server = None

        async def run():
            # Start PubNub instance without default_listeners to test our own
            self.server = pubnub_manager_asyncio.PubNubAsyncioManager(SUBSCRIBE_KEY, PUBLISH_KEY, user_id="UUID", default_listeners=False)
            # await self.async_server.async_init()
        self.loop.run_until_complete(run())

    def tearDown(self):
        # mock_resp.clear()  You do need to clear the mock_resp after each test case
        async def run():
            await self.server.pn.stop()
        self.loop.run_until_complete(run())

    @async_test
    async def test_publish_async(self):
        """
        Publish a message async
        """
        e = await self.server.publish_async("ch","msg")
        
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
    async def test_subscribe_async(self):
        """
        Subscribe to a channel async
        """
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
        await self.server.publish_async(channel, message)

        # give time for callback to return
        await asyncio.sleep(3)

        # get result
        result = callback.get_result()
        self.assertIsNotNone(result)
        LOG.debug("Callback result: ", result)

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