"""Configuration file for pubnub."""
from pubnub.pnconfiguration import PNConfiguration

from ..config.module_config import SUBSCRIBE_KEY, PUBLISH_KEY, USER_ID
from ..logger.logging_config import get_logger

LOG = get_logger()  # Get logger if needed. Default: INFO


class PubnubConfig():
    """Custom pubnub configuration class."""

    def __init__(self, subscribe_key=SUBSCRIBE_KEY, publish_key=PUBLISH_KEY, user_id=USER_ID):
        """Start a custom PNConfiguration object.

        Args:
            subscribe_key (str): Subscribe key for PubNub. Defaults to SUBSCRIBE_KEY.
            publish_key (str): Publish key for PubNub. Defaults to PUBLISH_KEY.
            user_id (str): User ID or UUID for this PubNub instance. Defaults to USER_ID.
        """
        self.subscribe_key = subscribe_key
        self.publish_key = publish_key
        self.user_id = user_id
        self.pnconfig = PNConfiguration()
        self.pnconfig.subscribe_key = subscribe_key
        self.pnconfig.publish_key = publish_key
        self.pnconfig.user_id = user_id
        LOG.debug("Pubnub Config: subscribe_key=%s,publish_key=%s,user_id=%s",
                  self.pnconfig.subscribe_key, self.pnconfig.publish_key, self.pnconfig.user_id)

    def get_config(self):
        """Get parsed pnconfig

        Returns:
            pnconfig: parsed pnconfig.
        """
        return self.pnconfig
