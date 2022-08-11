"""Pubnub Subscribe Callback"""
from logger.logging_config import get_logger
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory

LOG = get_logger()

class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        print("Message channel: %s" % message.channel)
        print("Message subscription: %s" % message.subscription)
        print("Message timetoken: %s" % message.timetoken)
        print("Message payload: %s" % message.message)
        print("Message publisher: %s" % message.publisher)
        LOG.info(message)

    def presence(self, pubnub, presence):
        # Can be join, leave, state-change, timeout, or interval
        print("Presence event: %s" % presence.event)

        # The channel to which the message was published
        print("Presence channel: %s" % presence.channel)

        # Number of users subscribed to the channel
        print("Presence occupancy: %s" % presence.occupancy)

        # User state
        print("Presence state: %s" % presence.state)

        # Channel group or wildcard subscription match, if any
        print("Presence subscription: %s" % presence.subscription)

        # UUID to which this event is related
        print("Presence UUID: %s" % presence.uuid)

        # Publish timetoken
        print("Presence timestamp: %s" % presence.timestamp)

        # Current timetoken
        print("Presence timetoken: %s" % presence.timetoken)

        LOG.info(presence)

        # List of users that have joined the channel (if event is 'interval')
        joined = presence.join
        LOG.info("List of users that have joined the channel (if event is 'interval')")

        # List of users that have left the channel (if event is 'interval')
        left = presence.leave
        LOG.info("List of users that have left the channel (if event is 'interval')")

        # List of users that have timed-out off the channel (if event is 'interval')
        timed_out = presence.timeout
        LOG.info("List of users that have timed-out off the channel (if event is 'interval')")

    def status(self, pubnub, status):

        # The status object returned is always related to subscribe but could contain
        # information about subscribe, heartbeat, or errors
        # use the operationType to switch on different options
        if status.operation == PNOperationType.PNSubscribeOperation \
                or status.operation == PNOperationType.PNUnsubscribeOperation:
            if status.category == PNStatusCategory.PNConnectedCategory:
                pass
                # This is expected for a subscribe, this means there is no error or issue whatsoever
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                pass
                # This usually occurs if subscribe temporarily fails but reconnects. This means
                # there was an error but there is no longer any issue
            elif status.category == PNStatusCategory.PNDisconnectedCategory:
                pass
                # This is the expected category for an unsubscribe. This means there
                # was no error in unsubscribing from everything
            elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                pass
                # This is usually an issue with the internet connection, this is an error, handle
                # appropriately retry will be called automatically
            elif status.category == PNStatusCategory.PNAccessDeniedCategory:
                pass
                # This means that Access Manager does not allow this client to subscribe to this
                # channel and channel group configuration. This is another explicit error
            else:
                pass
                # This is usually an issue with the internet connection, this is an error, handle appropriately
                # retry will be called automatically
        elif status.operation == PNOperationType.PNSubscribeOperation:
            # Heartbeat operations can in fact have errors, so it is important to check first for an error.
            # For more information on how to configure heartbeat notifications through the status
            # PNObjectEventListener callback, consult http://www.pubnub.com/docs/sdks/python/api-reference/configuration#configuration
            if status.is_error():
                pass
                # There was an error with the heartbeat operation, handle here
            else:
                pass
                # Heartbeat operation was successful
        else:
            pass
            # Encountered unknown status type

    def signal(self, pubnub, signal):
        print("Signal channel: %s" % signal.channel)
        print("Signal subscription: %s" % signal.subscription)
        print("Signal timetoken: %s" % signal.timetoken)
        print("Signal payload: %s" % signal.message)
        print("Signal publisher: %s" % signal.publisher)

    def message_action(self, pubnub, message_action):
        print("Message action type: %s" % message_action.type)
        print("Message action value: %s" % message_action.value)
        print("Message action uuid: %s" % message_action.uuid)
        print("Message action action_timetoken: %s" % message_action.action_timetoken)
        print("Message action message_timetoken: %s" % message_action.message_timetoken)