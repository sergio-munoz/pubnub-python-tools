"""Manage PubNub Asyncio."""
from pubnub.pubnub_asyncio import PubNubAsyncio

from .pubnub_config import PubnubConfig
from .pubnub_listener import MySubscribeCallback
# from .pubnub_here_now_callback import here_now_callback 
from .pubnub_handle_disconnects import HandleDisconnectsCallback
from ..logger.logging_config import get_logger

LOG = get_logger()  # Get logger if needed. Default: INFO


class PubNubAsyncioManager():
    """Create a new PubNub Asyncio instance."""

    def __init__(self, subscribe_key=None, publish_key=None, user_id=None, default_listeners=True):
        """Start PubNub Asyncio Manager

        Args:
            subscribe_key (str): Subscribe key for PubNub.
            publish_key (str): Publish key for PubNub.
            user_id (str): User ID or UUID for this PubNub instance.
            default_listeners (bool, optional): Set to false to add your own listeners. Defaults to True.
        """
        # Check for None values
        if not subscribe_key or not publish_key or not user_id:
            LOG.critical("Missing credentials/uuid for PubNub Configuration.")
            exit()

        # Start PubNubAsyncio
        LOG.info("Starting PubNub Async instance.")
        self.pn = PubNubAsyncio(PubnubConfig(subscribe_key, publish_key, user_id).get_config())
        if not self.pn:
            # Something went wrong!
            LOG.critical("Invalid PubNub Configuration. Check your keys/user_id.")
            exit()

        # Duplicate user_id as device_uuid for [future](link) PubNub support
        self.device_uuid = user_id  # Register device as current user_id by default

        # Setup default listeners
        if default_listeners:
            self.__add_listeners()

        # Add device manager for 'local' presence management (optional)
        self.device_manager = None

        # Add PubNub http on request function callback (optional)
        self.on_request_callback = None

        LOG.info("Started PubNub Async instance successfully.")

    def __add_listeners(self):
        """Add default callback listeners to instance.
        """
        self.pn.add_listener(MySubscribeCallback())  # Add Subscribe Callback
        disconnect_listener = HandleDisconnectsCallback() # Create Disconnect Callback
        self.pn.add_listener(disconnect_listener) # Add Disconnect Callback

    def add_listener(self, listener):
        """Manually add a callback listener to instance.

        Args:
            listener (function): Function callback.
        """
        self.pn.add_listener(listener)

    def subscribe(self, channels, channel_groups=None, timetoken=None, presence=False):
        """Subscribe to a channel indefinitely (blocking).

        Args:
            channels (srt|list|tuple): Channel(s) to subscribe to.
            channel_groups (str|list|tuple, optional): Channel Group(s) to subscribe to.
            timetoken (int, optional): Subscribe with timetoken.
            presence (bool, optional): Subscribe with presence. Defaults to False.
        """
        function_builder = self.pn.subscribe().channels(channels)
        if channel_groups:
            function_builder = function_builder.channel_groups(channel_groups)
        if timetoken:
            function_builder = function_builder.with_timetoken(int(timetoken))
        if presence:
            function_builder = function_builder.with_presence()
        function_builder.execute()

    async def publish(self, channel, message):
        """Publish a message to a channel async.

        Args:
            channel (str): Channel to publish.
            message (str): Message to publish.

        Returns:
            future: Asyncio future envelope.
        """
        return await self.pn.publish().channel(channel).message(message).future()

    async def here_now(self, channels, include_uuids=True, include_state=False):
        """HereNow async call on a channel.

        Args:
            channels (str|list|tuple): Channel(s) to call here_now.
            include_uuids (bool, optional): Include UUIDs. Defaults to True.
            include_state (bool, optional): Include State. Defaults to False.
        """
        # print("Herenow Async channels: ", channels)
        # print("Isinstance: ", channels.__class__.__name__)
        function_builder = self.pn.here_now().channels(channels)
        if include_uuids:
            function_builder = function_builder.include_uuids(include_uuids)
        if include_state:
            function_builder = function_builder.include_state(include_state)
        return await function_builder.future()

    def unsubscribe(self, channels):
        """Unsubscribe from a channel. Sends leave event to presence.

        Args:
            channels (str|list|tuple): Channel(s) to unsubscribe from.
        """
        self.pn.unsubscribe().channels(channels).execute()
