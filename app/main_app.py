from logger.logging_config import get_logger
from app import pubnub_manager
from cli.v1 import create_cli_v1

LOG = get_logger()

def main():
    LOG.info("Running Main App")
    # Create PubNub Manager
    pnmg = pubnub_manager.PubNubManager()

    # Get CLI arguments
    override_args = create_cli_v1()

    if override_args.message:
        MESSAGE = override_args.message
    if override_args.subscribe:
        pnmg.subscribe(override_args.subscribe, presence=override_args.presence)  # subscribe channel name comes from cli
        LOG.info("Subscribed")
    if override_args.publish:
        if not MESSAGE:
            LOG.error("Can't publish empty message")
            return
        pnmg.publish_message(override_args.publish, MESSAGE) # message commes appart 
        LOG.info("Published")
    if override_args.unsubscribe:
        pnmg.unsubscribe(override_args.unsubscribe)  # unsubscribe channel name comes from cli
        LOG.info("Unsubscribed")
    if override_args.here_now:
        pnmg.here_now(override_args.here_now)  # here_now channel name comes from cli
        LOG.info("Called here_now")


# Simple function to be tested with pytest
def simple_function(real_number):
    """:returns: real_number + 1"""
    LOG.debug("Adding 1 to %d", real_number)
    return real_number + 1