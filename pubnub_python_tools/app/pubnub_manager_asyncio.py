"""Manage PubNub Asyncio"""
import asyncio
from ..logger.logging_config import get_logger
from .pubnub_config import PubnubConfig
from .pubnub_listener import MySubscribeCallback
from .pubnub_handle_disconnects import HandleDisconnectsCallback
from .pubnub_publish import my_publish_callback_asyncio
from pubnub.pubnub_asyncio import PubNubAsyncio
from pubnub.exceptions import PubNubException

# Set logger
LOG = get_logger()

class PubNubAsyncioManager():

    def __init__(self, subscribe_key="", publish_key="", user_id="", default_listeners=True):
        """Start PubNub Asyncio Manager
        :subscribe_key: Subscribe Key for PubNub
        :publish_key: Publish Key for PubNub
        :user_id: UUID for PubNub
        :default_listeners: set to false to add your own listeners (for testing)
        """
        LOG.info("Starting PubNub")
        # Start PubNubAsyncio
        self.pn = PubNubAsyncio(PubnubConfig(subscribe_key, publish_key, user_id).get_config())
        if not self.pn:
            # Something went wrong!
            LOG.critical("Invalid PubNub Configuration. Check your keys/user_id.")
            exit()
        # Setup default listeners
        if default_listeners:
            self.__add_listeners()
        # Add device manager for 'local' presence management
        self.device_manager = None
        # Add PubNub http on request function callback
        self.on_request_callback = None
        # Duplicate user_id as device_uuid for [future](link) PubNub support
        self.device_uuid = user_id  # Register device as current user_id by default
        LOG.info("Started PubNub")

    def __add_listeners(self):
        self.pn.add_listener(MySubscribeCallback())  # Add Subscribe Callback
        disconnect_listener = HandleDisconnectsCallback() # Create Disconnect Callback
        self.pn.add_listener(disconnect_listener) # Add Disconnect Callback
    
    def add_listener(self, listener):
        self.pn.add_listener(listener)

    def subscribe(self, channels):
        self.pn.subscribe().channels(channels).execute()

    # WARNING: NOT TESTED
    # TODO: TEST
    async def publish_future(self, channel, message):
        """Publish using future."""
        res = await self.pn.publish().message(message).channel(channel).future()

        if res.is_error():
            print("Error: %s" % res)
            print("category id: #%d" % res.status.category)
            print("operation id: #%d" % res.status.operation)
            #_handle_error(e)
            LOG.error("Error publishing message!")
            self.publish_timetoken = 0
            return None
        else:
            print(res.result)
            LOG.info("Published message correctly.")
            # Publish success with timetoken 16621787928333380
            LOG.debug(res.result) 
            # You could instead return only the timetoken instead of having to extract it.
            self.publish_timetoken = res.publish_timetoken
            return res.result
    # WARNING: NOT TESTED
    # TODO: TEST

    async def publish_response(self, channel, message):
        try:
            result = await self.pn.publish().message(message).channel(channel).result()
            print("RESULT: ", result)
            return result
        except PubNubException as e:
            print("PubNubException: %s" % e) 
            print("category id: #%d" % e.status.category)
            print("operation id: #%d" % e.status.operation)
            #_handle_error(e) Add to log and cry
            return None
        except Exception as e:
            print("Error: %s" % e)
            #_handle_error(e)
            return None

    async def publish_async(self, channel, message):
        """ Publish async
        :channel: channel to publish
        :message: message to publish
        :returns: future envelope
        """
        return await self.pn.publish().channel(channel).message(message).future()

    # WARNING: NOT TESTED
    # TODO: TEST
    async def publish(self, channel, message):
        """Publish Async """
        return await self.pn.publish().channel(channel).message(message).future().add_done_callback(my_publish_callback_asyncio)
        # return await asyncio.ensure_future(
        #     self.pn.publish().channel(channel).message(message).future()
        # ).add_done_callback(my_publish_callback_asyncio)

    # WARNING: NOT TESTED
    # TODO: TEST
    async def start_loop(self, *function_callback, run_forever=True):
        """
        function_callback: function(s) to be run until_complete.
        run_forever: keep the loop running forever.
        """
        loop = asyncio.get_event_loop()
        for function in function_callback:
            LOG.info("Loop will continue to run forever.")
            loop.run_until_complete(function)
        if run_forever:
            LOG.info("Loop will continue to run forever.")
            return loop.run_forever()

