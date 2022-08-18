"""Pubnub HereNow Callback"""
from logger.logging_config import get_logger

LOG = get_logger()

def here_now_callback(result, status):
    LOG.debug("Calling here_now")
    if status.is_error():
        # handle error
        LOG.error(status)
        return

    LOG.debug("here_now response: %s", result)
    for channel_data in result.channels:
        print("---")
        print("channel: %s" % channel_data.channel_name)
        print("occupancy: %s" % channel_data.occupancy)

        print("occupants: %s" % channel_data.channel_name)
    for occupant in channel_data.occupants:
        print("uuid: %s, state: %s" % (occupant.uuid, occupant.state))