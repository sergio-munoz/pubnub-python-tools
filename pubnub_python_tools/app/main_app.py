from app import pubnub_manager
from cli.v1 import get_parser
from logger.logging_config import get_logger
from config.module_config import SUBSCRIBE_KEY, PUBLISH_KEY, USER_ID
from config.http_on_request_on_connect import ON_REQUEST_URL, ON_REQUEST_PARAMS, ON_REQUEST_BODY
import sys

LOG = get_logger()

def main():
# PubNub Environment Variables

    args = get_parser(sys.argv[1:])
    print(args)
    print("HERE!")
    
    if args.subscribe_key is not None:
        SUBSCRIBE_KEY = args.subscribe_key 
    if args.publish_key is not None:
        PUBLISH_KEY = args.publish_key 
    if args.uuid is not None:
        USER_ID = args.uuid

    # Create PubNub Manager
    pnmg = pubnub_manager.PubNubManager(SUBSCRIBE_KEY, PUBLISH_KEY, USER_ID)

    # Do commands from CLI
    if args.device_manager:
        pnmg.add_device_manager(args.device_manager)

        # Get function callback
        if ON_REQUEST_URL and ON_REQUEST_PARAMS and ON_REQUEST_BODY:
            pnmg.add_on_request_get_callback(ON_REQUEST_URL, ON_REQUEST_PARAMS, ON_REQUEST_BODY)
        if USER_ID is not None:
            pnmg.add_device_uuid(USER_ID)

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
