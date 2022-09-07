"""Main app logic file."""
import sys
from . import pubnub_manager
from ..cli.v1 import get_parser
from ..logger.logging_config import get_logger
from ..config import module_config
from ..config import http_on_request_on_connect as oc

LOG = get_logger() # Get logger if needed. Default: INFO

def main(args=None):
    """Main function to interact with pubnub_python_tools.

    Args:
        args (arguments): User arguments to parse.

    Returns:
        _type_: _description_
    """
    # Check if args were passed
    if not args:
        args = sys.argv[1:]  # Obtain from cli
    # Parse arguments
    args = get_parser(args)
    LOG.debug("Parsed arguments: %s", args)

    # Environment variables from module_config
    subscribe_key = module_config.SUBSCRIBE_KEY
    publish_key = module_config.PUBLISH_KEY
    user_id = module_config.USER_ID

    # Override from CLI
    if args.subscribe_key is not None:
        subscribe_key = args.subscribe_key
    if args.publish_key is not None:
        publish_key = args.publish_key
    if args.uuid is not None:
        user_id = args.uuid

    # Create PubNub Manager
    pnmg = pubnub_manager.PubNubManager(subscribe_key, publish_key, user_id)

    # Do commands from CLI
    # Local Device Manager
    if args.device_manager:
        pnmg.add_device_manager(args.device_manager)

        # Get function callback
        if oc.ON_REQUEST_URL and oc.ON_REQUEST_PARAMS and oc.ON_REQUEST_BODY:
            pnmg.add_on_request_get_callback(oc.ON_REQUEST_URL, oc.ON_REQUEST_PARAMS, oc.ON_REQUEST_BODY)
        if user_id is not None:
            pnmg.add_device_uuid(user_id)

    # Subscribe
    if args.subscribe:
        pnmg.subscribe(args.subscribe, presence=args.presence)

    # Publish
    if args.publish:
        if not args.message:
            err_msg = "Can't publish empty message. Use -m flag."
            print(err_msg)
            LOG.error(err_msg)
            return
        pnmg.publish_message(args.publish, args.message)

    # HereNow
    if args.here_now:
        pnmg.here_now(args.here_now)

    # Unsubscribe
    if args.unsubscribe:
        pnmg.unsubscribe(args.unsubscribe)


# Simple health function to be tested with unittest
def simple_function(real_number):
    """:returns: real_number + 1"""
    LOG.debug("Adding 1 to %d", real_number)
    return real_number + 1
