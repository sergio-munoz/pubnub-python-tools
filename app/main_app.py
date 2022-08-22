from logger.logging_config import get_logger
from app import pubnub_manager
from cli.v1 import create_cli_v1

LOG = get_logger()

def main():
    # Create PubNub Manager
    pnmg = pubnub_manager.PubNubManager()

    # Get CLI arguments
    args = create_cli_v1()
    if args.device_manager:
        pnmg.add_device_manager(args.device_manager)
    if args.subscribe:
        pnmg.subscribe(args.subscribe, presence=args.presence)
    if args.publish:
        if not args.message:
            LOG.error("Can't publish empty message")
            return
        pnmg.publish_message(args.publish, args.message)
    if args.here_now:
        pnmg.here_now(args.here_now)
    if args.unsubscribe:
        pnmg.unsubscribe(args.unsubscribe)


# Simple function to be tested with pytest
def simple_function(real_number):
    """:returns: real_number + 1"""
    LOG.debug("Adding 1 to %d", real_number)
    return real_number + 1