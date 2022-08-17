from logger.logging_config import get_logger
from app import pubnub_manager

LOG = get_logger()

def main():
    LOG.info("Running Main App")
    # Create PubNub Manager
    pnmg = pubnub_manager.PubNubManager()

    # Subscribe to a Channel
    pnmg.subscribe("Space01")

    # Publish Message to a Channel
    pnmg.publish_message("Space01", "Hello World!")

    LOG.info("Done running Main App")
    LOG.info("Still subscribed")

# Simple function to be tested with pytest
def simple_function(real_number):
    """:returns: real_number + 1"""
    LOG.debug("Adding 1 to %d", real_number)
    return real_number + 1