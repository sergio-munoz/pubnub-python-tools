import argparse

def create_cli_v1():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-sk", "--subscribe-key", type=str, help="PubNub SubscribeKey")
    parser.add_argument("-pk", "--publish-key", type=str, help="PubNub PublishKey")
    parser.add_argument("-u", "--uuid", type=str, help="PubNub UUID")
    parser.add_argument("-s", "--subscribe", type=str, help="Subscribe to a Channel")
    parser.add_argument("-pres", "--presence", action='store_true', help="Subscribe with Presence")
    parser.add_argument("-p", "--publish", type=str, help="Publish a message to a Channel")
    parser.add_argument("-m", "--message", type=str, help="Message to publish")
    parser.add_argument("-us", "--unsubscribe", type=str, help="Unsubscribe from a Channel")
    args = parser.parse_args()
    return args