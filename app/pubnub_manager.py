"""Manage PubNub"""
from logger.logging_config import get_logger
from app.pubnub_config import PubnubConfig
from app.pubnub_listener import MySubscribeCallback
from app.pubnub_handle_disconnects import HandleDisconnectsCallback
from app.pubnub_publish import my_publish_callback
from app.pubnub_here_now_callback import here_now_callback
from app.device_manager import DeviceManager
from pubnub.pubnub import PubNub

# Set Main Logger
LOG = get_logger()

class PubNubManager():
    # Start PubNub 
    def __init__(self, subscribe_key=None, publish_key=None, user_id=None):
        self.pn = PubNub(PubnubConfig(subscribe_key, publish_key, user_id))
        self.device_manager = None
        self.__add_listeners()
        LOG.info("Started PubNub")

    def __add_listeners(self):
        self.pn.add_listener(MySubscribeCallback()) # Add Listener Callback
        disconnect_listener = HandleDisconnectsCallback() # Create Disconnect Callback
        self.pn.add_listener(disconnect_listener) # Add Disconnect Callback
    
    def add_device_manager(self, device_manager_file_location=None):
        self.device_manager = DeviceManager(db_location=device_manager_file_location)
    
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
