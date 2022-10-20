from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from ..logger.logging_config import get_logger

LOG = get_logger()


class HandleDisconnectsCallback(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            # internet got lost, do some magic and call reconnect when ready
            pubnub.reconnect()
        elif status.category == PNStatusCategory.PNTimeoutCategory:
            # do some magic and call reconnect when ready
            pubnub.reconnect()
        else:
            LOG.debug(status)

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
        LOG.debug("List of users that have joined the channel (if event is 'interval'): %s", presence.join)
        LOG.debug("List of users that have left the channel (if event is 'interval'): %s", presence.leave)
        LOG.debug("List of users that have timed-out off the channel (if event is 'interval'): %s", presence.timeout)
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
            "timed_out": presence.timeout
        }
        print("Got disconnect presence: ", self._presence)

    def message(self, pubnub, message):
        pass

    def signal(self, pubnub, signal):
        pass

