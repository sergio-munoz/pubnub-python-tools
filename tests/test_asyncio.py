from pubnub_python_tools.app import pubnub_listener
from pubnub_python_tools.app import pubnub_publish
from pubnub_python_tools.app import pubnub_manager
from pubnub_python_tools.app import pubnub_manager_asyncio
from pubnub_python_tools.logger.logging_config import set_logger
from pubnub_python_tools.config.module_config import SUBSCRIBE_KEY, PUBLISH_KEY
from logging import DEBUG
import asyncio
import itertools
import unittest
import aiohttp
#from pubnub.pubnub_asyncio import PNPublishResult

# async def bg_task():
#     for n in itertools.count():
#         print(n)
#         await asyncio.sleep(0.25)

# def publish_callback(task):
#     exception = task.exception()

#     if exception:
#         envelope = task.result()
#         # Handle PNPublishResult(envelope.result) and PNStatus (envelope.status)
#         pass
#     else:
#         # Handle exception
#         pass

# async def publish():
#     pm = pubnub_manager.PubNubManager(SUBSCRIBE_KEY, PUBLISH_KEY, user_id="UUID")
#     asyncio.ensure_future(pm.pn.publish().channel('such_channel').message(['hello', 'there']).future()).add_done_callback(publish_callback)



# class BgTaskMixin:
#     async def asyncSetUp(self):
#         await super().asyncSetUp()
#         asyncio.create_task(bg_task())

# class FooTest(
#     BgTaskMixin,
#     unittest.IsolatedAsyncioTestCase,
# ):
#     # async def test_bg(self):
#     #     print('TEST START')
#     #     await asyncio.sleep(2)
#     #     self.assertTrue(False)

#     async def test_publish(self):
#         print('TEST START')
#         pm = pubnub_manager_asyncio.PubNubAsyncioManager(SUBSCRIBE_KEY, PUBLISH_KEY, user_id="UUID")
#         #envelope = await asyncio.create_task(pm.publish_async("ch","msg"))
#         #pub = await asyncio.create_task(pm.publish_future("ch","msg"))
#         envelope = await asyncio.create_task(publish())
#         print(envelope)
#         # timetoken = envelope.add_done_callback(pubnub_publish.my_publish_callback_asyncio())
#         # print(timetoken)
#         self.assertTrue(False)

from functools import wraps

def async_test(f):
    """
    Decorator to create asyncio context for asyncio methods or functions.
    """
    @wraps(f)
    def g(*args, **kwargs):
        args[0].loop.run_until_complete(f(*args, **kwargs))
    return g

def add_async_test(f):
    """
    Test both the synchronous and async methods of the device (server).
    """
    @wraps(f)
    def g(*args, **kwargs):
        f(*args, **kwargs)  # run the original test
        async_args = [a for a in args]  # make mutable copy of args
        server = async_args[0].server  # save reference to self.server
        async_args[0].server = async_args[0].async_server  # set copy.server to async_server
        f(*async_args, **kwargs)  # run the test using the async instance
        async_args[0].server = server  # point self.server back to original
    return g

class TestSomeEndpointsAndParsers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # you probably have some existing code above here
        cls.loop = asyncio.get_event_loop()
        # cls.future = cls.loop.run_until_complete(
        #     setup_web_server(app, host=LOCALHOST, port=ASYNC_SERVER_PORT)
        # )

    def setUp(self):
        # self.server = pubnub_manager_asyncio.PubNubAsyncioManager(SUBSCRIBE_KEY, PUBLISH_KEY, user_id="UUID")
        self.server = None

        async def run():
            # self.session = aiohttp.ClientSession()
            # self.async_server = Device(use_async=True, session=self.session)
            # await self.async_server.async_init()
            self.server = pubnub_manager_asyncio.PubNubAsyncioManager(SUBSCRIBE_KEY, PUBLISH_KEY, user_id="UUID")
        self.loop.run_until_complete(run())

# You do need to clear the mock_resp after each test case

    def tearDown(self):
        # mock_resp.clear()  

        async def run():
            await self.server.pn.stop()
        self.loop.run_until_complete(run())

    @async_test
    async def test_callaction_param_async(self):
        """
        Call an action with parameters and get the results.
        """
        #mock_resp.text = TEST_CALLACTION_PARAM
        #response = await self.async_server.GetPortMapping(NewPortMappingIndex=0)
        e = await self.server.publish_async("ch","msg")

        if e.is_error():
            print("Error %s" % str(e))
            print("Error category #%d" % e.status.category)
            self.assertTrue(False)
        else:
            response = str(e.result)
            time_token = response.split()[-1]
            expected = f'Publish success with timetoken {time_token}'
            print(str(e.result))
            self.assertEqual(response, expected)

# Remember to save references of functions
# background_tasks = set()

# for i in range(10):
#     task = asyncio.create_task(bg_task())

#     # Add task to the set. This creates a strong reference.
#     background_tasks.add(task)

#     # To prevent keeping references to finished tasks forever,
#     # make each task remove its own reference from the set after
#     # completion:
#     task.add_done_callback(background_tasks.discard)

