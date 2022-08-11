"""Configuration file for pubnub."""
from logger.logging_config import get_logger
from pubnub.pnconfiguration import PNConfiguration
from module_config import SUBSCRIBE_KEY,PUBLISH_KEY,USER_ID

LOG = get_logger()

pnconfig = PNConfiguration()

pnconfig.subscribe_key = SUBSCRIBE_KEY
pnconfig.publish_key  = PUBLISH_KEY
pnconfig.user_id = USER_ID

LOG.info("Configured PubNub")
LOG.debug("Pubnub Config: subscribe_key={},publish_key={},user_id={}".format(
    pnconfig.subscribe_key, pnconfig.publish_key, pnconfig.user_id
))
