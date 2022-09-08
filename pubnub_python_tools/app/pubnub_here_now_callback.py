"""Pubnub HereNow Callback."""
from ..logger.logging_config import get_logger

LOG = get_logger()

def here_now_callback(result, status):
    """here_now function callback resolver.

    Args:
        result (PNResult): here_now result envelope.
        status (PNStatus): here_now status envelope.
    """
    if status.is_error():
        # handle error
        LOG.error("here_now_callback error status: %s", status)

    for channel_data in result.channels:
        print(f'channel: {channel_data.channel_name}')
        print(f'occupancy: {channel_data.occupancy}')
        print(f'occupants: {channel_data.channel_name}')
    for occupant in channel_data.occupants:
        print(f'uuid: {occupant.uuid}, state: {occupant.state}')

    LOG.info("here_now_callback response: %s", result)
