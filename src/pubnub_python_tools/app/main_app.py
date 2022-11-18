"""Main app logic file."""
import sys

from . import pubnub_manager
from . import pubnub_manager_asyncio
from ..cli.v2 import create_parser
from ..config import module_config
from ..logger.logging_config import get_logger

LOG = get_logger()  # Get logger if needed. Default: INFO


def main(args=None):
    """Main function to interact with pubnub_python_tools.

    Args:
        args: User arguments to parse. See cli/v1.py.
    """
    # Args obtain from CLI
    if not args:
        args = sys.argv[1:]
        # No parameter args sent. Try system argv
        if len(args) <= 0:
            print("No args detected. Run: pubnub-python-tools --help")
            return None

    # Validate args
    print(args)  # TODO change to log
    parser = create_parser()
    args = parser.parse_args(args)
    if parser.error_message:
        stdout = f"{parser.error_message}"
        print(stdout)
        return stdout
    if not args:
        exit()

    # Environment variables from module_config
    subscribe_key = module_config.SUBSCRIBE_KEY
    publish_key = module_config.PUBLISH_KEY
    user_id = module_config.USER_ID

    # Display version
    if args.version:
        stdout = f"PubNub Python Tools v{get_version()}"
        print(stdout)
        return stdout

    # Override Environment variables from CLI
    if args.subscribe_key is not None:
        subscribe_key = args.subscribe_key
    if args.publish_key is not None:
        publish_key = args.publish_key
    if args.uuid is not None:
        user_id = args.uuid

    # Create PubNub instance
    pnmg = None
    if args.async_cmd:
        # Create PubNub Async Manager
        pnmg = pubnub_manager_asyncio.PubNubAsyncioManager(
            subscribe_key, publish_key, user_id
        )
    else:
        # Create PubNub Manager
        pnmg = pubnub_manager.PubNubManager(subscribe_key, publish_key, user_id)

    # Local Device Manager
    if args.dev_man:
        pnmg.add_device_manager(args.device_manager)

    # Get function callback
    # if oc.ON_REQUEST_URL and oc.ON_REQUEST_PARAMS and oc.ON_REQUEST_BODY:
    # pnmg._add_on_request_get_callback(oc.ON_REQUEST_URL, oc.ON_REQUEST_PARAMS, oc.ON_REQUEST_BODY)
    # if user_id is not None:
    # pnmg.add_device_uuid(user_id)

    # Subscribe
    if args.subscribe:
        pnmg.subscribe(args.subscribe, presence=args.presence)

    # Publish
    if args.publish:  # -p
        # Publish multiple messages
        if args.multiple_messages:  # -mm
            responses = []
            for msg in args.multiple_messages:
                responses.append(pnmg.publish_wrap(args.publish, msg))
            return responses

        # Publish one message
        if not args.message:  # -m
            err_msg = "Can't publish empty message. Use -m flag."
            print(err_msg)
            LOG.error(err_msg)
            return err_msg
        return pnmg.publish_wrap(args.publish, args.message)

    # Publish Multiple Channels
    if args.publish_multiple_channels:
        # Publish multiple messages
        if args.multiple_messages:  # -mm
            responses = []
            for msg in args.multiple_messages:
                for channel in args.publish_multiple_channels:
                    responses.append(pnmg.publish_wrap(channel, msg))
            return responses

        # Publish one message
        if not args.message:
            err_msg = "Can't publish empty message. Use -m flag."
            print(err_msg)
            LOG.error(err_msg)
            return err_msg
        responses = []
        for channel in args.publish_multiple_channels:
            responses.append(pnmg.publish_wrap(channel, args.message))
        return responses

    # HereNow
    if args.here_now:
        pnmg.here_now(args.here_now)

    # Unsubscribe
    if args.unsubscribe:
        pnmg.unsubscribe(args.unsubscribe)


# Health-check function - get current version
def get_version() -> str:
    """Get pubnub-python-tools version.

    Returns:
        str: Current pubnub-python-tools package version.
    """
    from ..__about__ import __version__ as ppt_version
    return f"{ppt_version}"


def validate_args(args) -> dict:
    LOG.debug("Validating args")
    # Check if args were passed
    if not args:
        # Try obtain from CLI
        args = sys.argv[1:]
        # No parameter args sent. Try system argv
        if len(args) <= 0:
            print("No args detected. Run: pubnub-python-tools --help")
            return None
        return args
