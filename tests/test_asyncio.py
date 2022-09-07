from pubnub_python_tools.app import pubnub_manager_asyncio
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

class TestPubnubAsyncio(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.get_event_loop()
        # cls.future = cls.loop.run_until_complete(setup_web_server(app, host=LOCALHOST, port=ASYNC_SERVER_PORT))

    def setUp(self):
        # Start empty Manager to be overriden in async run()
        self.server = pubnub_manager_asyncio.PubNubAsyncioManager()

        async def run():
            self.server = pubnub_manager_asyncio.PubNubAsyncioManager(SUBSCRIBE_KEY, PUBLISH_KEY, user_id="UUID")
            # await self.async_server.async_init()
        self.loop.run_until_complete(run())

    def tearDown(self):
        # mock_resp.clear()  You do need to clear the mock_resp after each test case
        async def run():
            await self.server.pn.stop()
        self.loop.run_until_complete(run())

    @async_test
    async def test_callaction_param_async(self):
        """
        Call an action with parameters and get the results.
        """
        #mock_resp.text = TEST_CALLACTION_PARAM
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
