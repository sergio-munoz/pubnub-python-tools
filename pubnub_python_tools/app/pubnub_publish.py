"""Callback function for publishing"""
from ..logger.logging_config import get_logger
LOG = get_logger()

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        LOG.info("Message successfully published to specified channel.")
    else:
        LOG.error("Error %s" % str(status.error_data.exception))
        LOG.error("Error category #%d" % status.category)
        print("Error %s" % str(status.error_data.exception))
        print("Error category #%d" % status.category)
        # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

def my_publish_callback_asyncio(task):
    # Check whether request successfully completed or not
    if not task.exception():
        envelope = task.result()
        # Message successfully published to specified channel.
        LOG.info("Message successfully published to specified channel.")
        LOG.debug("publish timetoken: %d" % envelope.result.timetoken)
        print("publish timetoken: %d" % envelope.result.timetoken)
        print("Message successfully published to specified channel.")
    else:
        LOG.error("Message publish error exception unhabdled.")
        print("Error publishing message.")
        # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];
