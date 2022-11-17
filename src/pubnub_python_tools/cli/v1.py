"""CLI v1 Argument Parser."""
import argparse

DESCRIPTION = "Quickly interact with PubNub's Python SDK."


# sub class ArgumentParser to catch an error message and prevent application closing
class MyArgumentParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(MyArgumentParser, self).__init__(*args, **kwargs)

        self.error_message = ''

    def error(self, message):
        print("error: ", message)
        self.error_message = message

    def parse_args(self, *args, **kwargs):
        # catch SystemExit exception to prevent closing the application
        result = None
        if args[0] is None or args[0] == "":
            self.error("invalid empty arguments")
            return result
        try:
            result = super().parse_args(*args, **kwargs)
        except SystemExit:
            pass
        return result


def create_parser():
    # Create argument parser
    parser = MyArgumentParser(add_help=True, description=DESCRIPTION)

    # Add arguments to parser
    parser.add_argument("--version", action='store_true', help="Current pubnub-python-tools Version")
    parser.add_argument("-a", "--async-cmd", type=str, help="Run command asynchronously using Asyncio")
    parser.add_argument("-dm", "--dev-man", type=str, help="Attach a Device Manager to file")
    parser.add_argument("-here", "--here-now", type=str, help="Here now on a Channel")
    parser.add_argument("-m", "--message", type=str, help="Message to publish")
    parser.add_argument("-p", "--publish", type=str, help="Publish a message to a Channel")
    parser.add_argument("-pk", "--publish-key", type=str, help="PubNub PublishKey")
    parser.add_argument("-pres", "--presence", action='store_true', help="Subscribe with Presence")
    parser.add_argument("-s", "--subscribe", type=str, help="Subscribe to a Channel")
    parser.add_argument("-sk", "--subscribe-key", type=str, help="PubNub SubscribeKey")
    parser.add_argument("-u", "--uuid", type=str, help="PubNub UUID")
    parser.add_argument("-us", "--unsubscribe", type=str, help="Unsubscribe from a Channel")

    # Return parser
    return parser
