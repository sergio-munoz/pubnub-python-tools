"""Manage PubNub"""
import sys
from ..logger.logging_config import get_logger
from .pubnub_config import PubnubConfig
from .pubnub_listener import MySubscribeCallback
from .pubnub_handle_disconnects import HandleDisconnectsCallback
from .pubnub_publish import my_publish_callback
from .pubnub_here_now_callback import here_now_callback
from .device_manager import DeviceManager
from .pubnub_on_request import get
from pubnub.pubnub import PubNub

# Set Main Logger
LOG = get_logger()

class PubNubManager():
    # Start PubNub 
    def __init__(self, subscribe_key="", publish_key="", user_id=""):
        pnconfig = PubnubConfig(subscribe_key, publish_key, user_id).get_config()
        self.pn = PubNub(pnconfig)
        if not self.pn:
            LOG.critical("Invalid PubNub Configuration. Check your keys/user_id.")
            exit()
        self.device_manager = None
        self.on_request_callback = None
        self.__add_listeners()
        self.device_uuid = user_id  # Register device as current user_id by default
        LOG.info("Started PubNub")

    def __add_listeners(self):
        self.pn.add_listener(MySubscribeCallback()) # Add Listener Callback
        disconnect_listener = HandleDisconnectsCallback() # Create Disconnect Callback
        self.pn.add_listener(disconnect_listener) # Add Disconnect Callback
    
    def add_device_manager(self, device_manager_file_location):
        self.device_manager = DeviceManager(device_manager_file_location)

    def add_on_request_get_callback(self, url, params, body):
        if self.device_manager:
            self.device_manager._add_on_request_callback(get(url, params, body))
            LOG.debug("custom on_request_get_callback added")
        else:
            LOG.warn("add device manager first: add_device_manager()")

    def add_device_uuid(self, device_uuid):
        self.device_uuid = device_uuid
    
    def subscribe(self, channels, channel_groups=None, time_token=None, presence=False):
        """channels: String|List|Tuple
           channel_groups: String|List|Tuple
           time_token: Int
           presence: Bool
        """
        function_builder = self.pn.subscribe()
        if channels:
            function_builder = function_builder.channels(channels)
        if channel_groups:
            function_builder = function_builder.channel_groups(channel_groups)
        if time_token:
            function_builder = function_builder.with_timetoken(int(time_token))
        if presence:
            function_builder = function_builder.with_presence()
        function_builder.execute()
    
    def publish_message(self, channel, message):
        self.pn.publish().channel(channel).message(message).pn_async(my_publish_callback)
        # LOG messages are called in the `my_publish_callback`
    
    def unsubscribe(self, channels, channel_groups=None):
        """channels: String|List|Tuple
           channel_groups: String|List|Tuple
        """
        function_builder = self.pn.unsubscribe()
        if channels:
            function_builder = function_builder.channels(channels)
        if channel_groups:
            function_builder = function_builder.channel_groups(channel_groups)
        function_builder.execute()

    def here_now(self, channels, include_uuids=True, include_state=False):
        """channels: String|List|Tuple
           include_uuids: Boolean
        """
        function_builder = self.pn.here_now()
        if channels:
            function_builder = function_builder.channels(channels)
        if include_uuids:
            function_builder = function_builder.include_uuids(include_uuids)
        if include_state:
            function_builder = function_builder.include_state(include_state)
        function_builder.pn_async(here_now_callback)
