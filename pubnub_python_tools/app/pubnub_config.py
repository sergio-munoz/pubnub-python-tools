"""Configuration file for pubnub."""
from pubnub.pnconfiguration import PNConfiguration
from ..logger.logging_config import get_logger
from ..config.module_config import SUBSCRIBE_KEY,PUBLISH_KEY,USER_ID

LOG = get_logger()

class PubnubConfig():

    def __init__(self, subscribe_key=SUBSCRIBE_KEY, publish_key=PUBLISH_KEY, user_id=USER_ID) -> None:
        self.subscribe_key = subscribe_key
        self.publish_key = publish_key
        self.user_id = user_id
        self.pnconfig = PNConfiguration()
        self.pnconfig.subscribe_key = subscribe_key
        self.pnconfig.publish_key  = publish_key
        self.pnconfig.user_id = user_id
        LOG.debug("Pubnub Config: subscribe_key={},publish_key={},user_id={}".format(
            self.pnconfig.subscribe_key, self.pnconfig.publish_key, self.pnconfig.user_id)
            )
    def get_config(self):
        return self.pnconfig
