"""PubNub Listeners and Callbacks."""
import traceback
import requests

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory

from ..logger.logging_config import get_logger

LOG = get_logger()


class MySubscribeCallback(SubscribeCallback):
    """Create a Subscribe Callback."""

    def __init__(self, device_manager=None):
        """Hold callback results on local variables.

        Args:
            device_manager (file, optional): Add device manager. Defaults to None.
        """
        self._message = None
        self._presence = None
        # Add device_manager capabilities
        self.device_manager = device_manager
        self.on_request_callback = None
        self.device_uuid = None

    def get_message(self):
        """Return internal callback message result

        Returns:
            dict: message result
        """
        return self._message

    def get_presence(self):
        """Return internal callback presence result

        Returns:
            dict: presence result
        """
        return self._presence

    def _add_get_callback(self, get_callback):
        """Function get callback"""
        self.on_request_callback = get_callback

    def _add_device_uuid(self, device_uuid):
        """Target Device UUID"""
        self.device_uuid = device_uuid

    def message(self, pubnub, message):
        """Message callback. Sets private message variable."
        Sets:
            _message (dict): Message.
        """
        LOG.debug("Message channel: %s", message.channel)
        LOG.debug("Message subscription: %s", message.subscription)
        LOG.debug("Message timetoken: %s", message.timetoken)
        LOG.debug("Message payload: %s", message.message)
        LOG.debug("Message publisher: %s", message.publisher)
        self._message = {
            "channel": message.channel,
            "subscription": message.subscription,
            "timetoken": message.timetoken,
            "payload": message.message,
            "publisher": message.publisher,
        }
        print("Got message: ", self._message)

    def presence(self, pubnub, presence):
        """Presence callback. Sets private presence variable."
        Sets:
            _presence (dict): Presence.
        """
        # Can be join, leave, state-change, timeout, or interval
        LOG.debug("Presence event: %s", presence.event)
        # The channel to which the message was published
        LOG.debug("Presence channel: %s", presence.channel)
        # Number of users subscribed to the channel
        LOG.debug("Presence occupancy: %s", presence.occupancy)
        # User state
        LOG.debug("Presence state: %s", presence.state)
        # Channel group or wildcard subscription match, if any
        LOG.debug("Presence subscription: %s", presence.subscription)
        # UUID to which this event is related
        LOG.debug("Presence UUID: %s", presence.uuid)
        # Publish timetoken
        LOG.debug("Presence timestamp: %s", presence.timestamp)
        # Current timetoken
        LOG.debug("Presence timetoken: %s", presence.timetoken)
        # Interval Mode
        LOG.debug(
            "List of users that have joined the channel (if event is 'interval'): %s",
            presence.join,
        )
        LOG.debug(
            "List of users that have left the channel (if event is 'interval'): %s",
            presence.leave,
        )
        LOG.debug(
            "List of users that have timed-out off the channel (if event is 'interval'): %s",
            presence.timeout,
        )
        self._presence = {
            "event": presence.event,
            "channel": presence.channel,
            "occupancy": presence.occupancy,
            "state": presence.state,
            "subscription": presence.subscription,
            "UUID": presence.uuid,
            "timestamp": presence.timestamp,
            "timetoken": presence.timetoken,
            "joined": presence.join,
            "left": presence.leave,
            "timed_out": presence.timeout,
        }
        if self._presence["event"] == "leave":
            print("Presence Unsubscribed:", self._presence)
        elif self._presence["event"] == "join":
            print("Presence Subscribed:", self._presence)
        else:
            print("Got presence event: ", self._presence)

    def status_event(self, pubnub, event):
        print("Is there an error? ", event.is_error())
        print("Status value for category: %s" % event.category)
        print("Status value for error_data: %s" % event.error_data)
        print("Status value for error: %s" % event.error)
        print("Status value for status_code: %s" % event.status_code)
        print("Status value for operation: %s" % event.operation)
        print("Status value for tls_enabled: %s" % event.tls_enabled)
        print("Status value for uuid: %s" % event.uuid)
        print("Status value for auth_key: %s" % event.auth_key)
        print("Status value for origin: %s" % event.origin)
        print("Status value for client_request: %s" % event.client_request)
        print("Status value for client_response: %s" % event.client_response)
        print("Status value for original_response: %s" % event.original_response)
        print("Status value for affected_channels: %s" % event.affected_channels)
        print("Status value for affected_groups: %s" % event.affected_groups)

    def status(self, pubnub, status):
        # The status object returned is always related to subscribe but could contain
        # information about subscribe, heartbeat, or errors
        # use the operationType to switch on different options
        if (
            status.operation == PNOperationType.PNSubscribeOperation
            or status.operation == PNOperationType.PNUnsubscribeOperation
        ):
            if status.category == PNStatusCategory.PNConnectedCategory:
                LOG.debug(
                    "This is expected for a subscribe, this means there is no error or issue whatsoever"
                )
                self._status = "PNConnectedCategory"
                print("Status: ", self._status)
                # confirm channelId u.e555.u123 is in e.affectedChannels
                # if !connected then use the fetch API to GET request URL
                # set connected = true
                # https://ps.pndsn.com/v1/blocks/sub-key/{your_sub_key}/connect
                # with query params: channelid=u.e555.u123
                if self.on_request_callback:
                    if not self.device_manager:
                        LOG.warning(
                            "Local device manager not found. Function might not work as expected."
                        )
                        return  # Maybe return something else?
                    else:
                        if self.device_manager.is_connected(self.device_uuid):
                            LOG.info("Device already connected to pubnub!")
                            return  # Maybe return something else
                        else:
                            LOG.info("Device not connected. Making callback to PubNub.")
                            try:
                                res = (
                                    self.on_request_callback()
                                )  # Send PubNub on_request HTTP Rest call
                                if res.status_code == 200:
                                    for msg in res:
                                        print(msg)
                                        LOG.info("On Request Response Message: %s", msg)
                            except Exception:
                                print(traceback.format_exc())
                                LOG.error("Response get failed!")

                # How to get channelid from request?
                # params = self.on_request_callback().params
                # # '{"channelid": "u.001.UUID" }'
                # chid = params["channelid"]

            elif status.category == PNStatusCategory.PNReconnectedCategory:
                LOG.debug(
                    "This usually occurs if subscribe temporarily fails but reconnects. This means there was an error but there is no longer any issue"
                )
            elif status.category == PNStatusCategory.PNDisconnectedCategory:
                LOG.debug(
                    "This is the expected category for an unsubscribe. This means there was no error in unsubscribing from everything"
                )
                print("Disconnected Correctly")
                # if envelope.event == "leave":
                # LOG.debug("Unsubscribe user_id: %s", envelope.uuid)
                # LOG.debug("Unsubscribe timetoken: %s", envelope.timetoken)
                # LOG.debug("Unsubscribe occupancy: %s", envelope.occupancy)
                # my_envelope = {
                # "user_id": envelope.uuid,  # 175c2c67-b2a9-470d-8f4b-1db94f90e39e
                # "timetoken": envelope.timestamp,  # 1345546797
                # "occupancy": envelope.occupancy,  # 2
                # }
                # print("Got unsubscribe: ", my_envelope)
            elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                LOG.debug(
                    "This is usually an issue with the internet connection, this is an error, handle appropriately retry will be called automatically "
                )
            elif status.category == PNStatusCategory.PNAccessDeniedCategory:
                LOG.debug(
                    "This means that Access Manager does not allow this client to subscribe to this channel and channel group configuration. This is another explicit error"
                )
            else:
                LOG.debug(
                    "This is usually an issue with the internet connection, this is an error, handle appropriately retry will be called automatically"
                )
        elif status.operation == PNOperationType.PNSubscribeOperation:
            # Heartbeat operations can in fact have errors, so it is important to check first for an error.
            # For more information on how to configure heartbeat notifications through the status
            # PNObjectEventListener callback, consult http://www.pubnub.com/docs/sdks/python/api-reference/configuration#configuration

            if status.is_error():
                LOG.error(
                    "There was an error with the heartbeat operation, handle here"
                )

            else:
                LOG.debug("Heartbeat operation was successful")

        else:
            LOG.error("Encountered unknown status type")

    def signal(self, pubnub, signal):
        print("Signal channel: %s" % signal.channel)
        LOG.debug("Signal channel: %s", signal.channel)
        print("Signal subscription: %s", signal.subscription)
        LOG.debug("Signal subscription: %s", signal.subscription)
        print("Signal timetoken: %s", signal.timetoken)
        LOG.debug("Signal timetoken: %s", signal.timetoken)
        print("Signal payload: %s" % signal.message)
        LOG.debug("Signal payload: %s", signal.message)
        print("Signal publisher: %s", signal.publisher)
        LOG.debug("Signal publisher: %s", signal.publisher)

    def message_action(self, pubnub, message_action):
        print("Message action type: %s" % message_action.type)
        LOG.debug("Message action type: %s" % message_action.type)
        print("Message action value: %s" % message_action.value)
        LOG.debug("Message action value: %s" % message_action.value)
        print("Message action uuid: %s" % message_action.uuid)
        LOG.debug("Message action uuid: %s" % message_action.uuid)
        print("Message action action_timetoken: %s" % message_action.action_timetoken)
        LOG.debug(
            "Message action action_timetoken: %s" % message_action.action_timetoken
        )

    def pubnub_after_presence_function(self, query, channelid):
        endpoint = "https://ps.pndsn.com/v1/blocks/sub-key/sub-c-0b961af6-42b7-463d-ac2f-99a6714b57af/conn"
        query_params = {"channelid": channelid}
        try:
            response = requests.get(endpoint, params=query_params)
            if response.status_code == 200:
                for msg in response:
                    print(msg)
                    LOG.info("After Presence Response Message: %s", msg)
        except Exception:
            print(traceback.format_exc())
            LOG.error("Response get failed!")
