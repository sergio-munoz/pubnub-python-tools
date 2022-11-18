"""Manage PubNub instance."""
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException

from .pubnub_config import PubnubConfig
from .pubnub_listener import MySubscribeCallback
from .pubnub_handle_disconnects import HandleDisconnectsCallback
from .pubnub_here_now_callback import HereNowCallback
from .pubnub_publish import my_publish_callback as pub_callback
from .device_manager import DeviceManager
from .pubnub_on_request import get
from ..logger.logging_config import get_logger

LOG = get_logger()  # Get logger if needed. Default: INFO


class PubNubAnalytics:
    def __init__(self):
        self.tx_count = 0
        self.metrics = {"publish": 0, "subscribe": 0, "here_now": 0, "unsubscribe": 0}

    def incr(self, metric):
        if metric not in self.metrics:
            LOG.error("unknown metric: ", metric)
            return
        # Increment metric by 1
        self.metrics[metric] += 1

    def decr(self, metric):
        if metric not in self.metrics:
            LOG.error("unknown metric: ", metric)
            return
        # Decrement metric by 1
        self.metrics[metric] -= 1


class PubNubManager:
    """Create a new PubNub instance."""

    def __init__(
        self, subscribe_key=None, publish_key=None, user_id=None, default_listeners=True
    ):
        """Start PubNub Manager

        Args:
            subscribe_key (str): Subscribe key for PubNub.
            publish_key (str): Publish key for PubNub.
            user_id (str): User ID or UUID for this PubNub instance.
            default_listeners (bool, opt): Set to false to add custom listeners. Defaults to True.
        """
        # Check for None values
        if not subscribe_key or not publish_key or not user_id:
            LOG.critical("Missing credentials/uuid for PubNub Configuration.")
            exit()

        # Start PubNub Manager
        LOG.info("Starting PubNub instance.")
        self.pn = PubNub(PubnubConfig(subscribe_key, publish_key, user_id).get_config())
        if not self.pn:
            LOG.critical("Invalid PubNub Configuration. Check your keys/user_id.")
            exit()

        # Duplicate user_id as device_uuid for [future](link) PubNub support
        self.device_uuid = user_id  # Register device as current user_id by default

        # Setup default listeners
        if default_listeners:
            self.__add_default_listeners()

        # Add device manager for 'local' presence management (optional)
        self.device_manager = None

        # Add PubNub http on request function callback (optional)
        self.on_request_callback = None

        LOG.info("Started PubNub instance.")

    def __add_default_listeners(self):
        """Add default callback listeners to instance."""
        self.pn.add_listener(MySubscribeCallback())        # Add MySubscribe Callback
        disconnect_listener = HandleDisconnectsCallback()  # Create Disconnect Callback
        self.pn.add_listener(disconnect_listener)          # Add Disconnect Callback

    def _add_listener(self, listener):
        """Manually add a callback listener to instance.

        Args:
            listener (function): Function callback.
        """
        self.pn.add_listener(listener)

    def add_device_manager(self, device_manager_file_location):
        """Add Device Manager local presence capabilities.

        Args:
            device_manager_file_location (str): Uri to database file.
        """
        self.device_manager = DeviceManager(device_manager_file_location)

    def add_on_request_get_callback(self, url, params, body):
        """Add HTTP GET on_request callback.

        Args:
            url (str): URL for API call.
            params (json): parameters for GET API call.
            body (str): body for GET API call.
        """
        if self.device_manager:
            self.device_manager._add_on_request_callback(get(url, params, body))
            LOG.info("Custom on_request_get_callback added.")
        else:
            LOG.warning("Add device manager first: add_device_uuid(self, device_uuid).")
        # self.device_uuid = device_uuid

    def subscribe(self, channels, channel_groups=None, timetoken=None, presence=False):
        """Subscribe to a channel indefinitely (blocking).

        Args:
            channels (str|list|tuple): Channel(s) to subscribe to.
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

    def publish(self, channel, message):
        """Publish a message to a channel.

        Args:
            channel (str): Channel to publish.
            message (str): Message to publish.

        Returns:
            future: Asyncio future envelope.
        """
        func = self.pn.publish().channel(channel).message(message)
        return func.sync()

    def publish_wrap(self, channel, message):
        try:
            envelope = self.publish(channel, message)
            response = str(envelope.result)
            return response
        except PubNubException as e:
            print("Publish error: ", e)
            return str(e)

    def here_now(self, channels, include_uuids=True, include_state=False, override_listener=None):
        """HereNow call on a channel. This is an async call.

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
        if override_listener:
            # Expecting a here_now_callback
            return function_builder.pn_async(override_listener)
        hnc = HereNowCallback()
        return function_builder.pn_async(hnc.here_now_callback)

    def unsubscribe(self, channels, channel_groups=None):
        """Unsubscribe from a channel. Sends leave event to presence.

        Args:
            channels (str|list|tuple): Channel(s) to unsubscribe from.
            channel_groups (str|list, optional): Channel Group(s) to unsubscribe from. Defaults to None.
        """
        function_builder = self.pn.unsubscribe()
        if channels:
            function_builder = function_builder.channels(channels)
        if channel_groups:
            function_builder = function_builder.channel_groups(channel_groups)
        function_builder.execute()

    # TODO: Test
    async def publish_async(self, channel, message):
        """Publish a message to a channel async.

        Args:
            channel (str): Channel to publish.
            message (str): Message to publish.

        Returns:
            future: Asyncio future envelope.
        """
        return (
            await self.pn.publish()
            .channel(channel)
            .message(message)
            .pn_async(pub_callback)
        )
