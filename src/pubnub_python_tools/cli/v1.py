"""CLI v1 Argument Parser."""
import argparse

DESCRIPTION = "Quickly interact with PubNub's Python SDK."

# Create argument parser
parser = argparse.ArgumentParser(add_help=True, description=DESCRIPTION)

# Add arguments to parser
parser.add_argument("-sk", "--subscribe-key", type=str, help="PubNub SubscribeKey")
parser.add_argument("-pk", "--publish-key", type=str, help="PubNub PublishKey")
parser.add_argument("-u", "--uuid", type=str, help="PubNub UUID")
parser.add_argument("-s", "--subscribe", type=str, help="Subscribe to a Channel")
parser.add_argument("-pres", "--presence", action='store_true', help="Subscribe with Presence")
parser.add_argument("-p", "--publish", type=str, help="Publish a message to a Channel")
parser.add_argument("-m", "--message", type=str, help="Message to publish")
parser.add_argument("-us", "--unsubscribe", type=str, help="Unsubscribe from a Channel")
parser.add_argument("-here", "--here-now", type=str, help="Here now on a Channel")
parser.add_argument("-dm", "--dev-man", type=str, help="Attach a Device Manager to file")
parser.add_argument("-a", "--async-cmd", type=str, help="Run command asynchronously using Asyncio")


def get_parser(args):
    """Get argument parser

    Args:
        args: user arguments

    Returns:
        parser: parser with arguments parsed
    """
    return parser.parse_args(args)


def create_parser():
    """Create argument parser

    Returns:
        parser: parser without arguments
    """
    return parser
