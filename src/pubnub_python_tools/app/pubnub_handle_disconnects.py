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
        pass

    def message(self, pubnub, message):
        pass

    def signal(self, pubnub, signal):
        pass

