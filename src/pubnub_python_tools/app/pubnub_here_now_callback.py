"""Pubnub HereNow Callback."""
from ..logger.logging_config import get_logger

LOG = get_logger()


class HereNowCallback:
    def __init__(self, sort_uuids=False):
        """HereNowCallback __init__()"""
        self.here_now_channels = None
        self.here_now_occupancy = None
        self.here_now_uuids = None
        self.here_now_states = None
        self.sort_uuids = sort_uuids

    def __repr__(self):
        return str(
            {
                "here_now_channels": self.here_now_channels,
                "here_now_occupancy": self.here_now_occupancy,
                "here_now_uuids": self.here_now_uuids,
                "here_now_states": self.here_now_states,
            }
        )

    def get(self):
        return self

    def _parse_channel_data(self, result_channels):
        channels = []
        occupancy = []

        # parse channel_names and occupancy
        try:
            for ch_data in result_channels:
                channels.append(ch_data.channel_name)
                occupancy.append(ch_data.occupancy)

            # parse uuids and states from occupants
            self._parse_channel_data_occupants(ch_data.occupants)

            # update internal variables
            self.here_now_channels = channels
            self.here_now_occupancy = occupancy

            # sort uuids
            if self.sort_uuids:
                if len(self.here_now_uuids) == 0:
                    self.here_now_uuids = []
                else:
                    self.here_now_uuids.sort()
        except Exception as e:
            print(e)  # Variable not found
            return e

    def _parse_channel_data_occupants(self, channel_data_occupants):
        uuids = []
        states = []
        for occupant in channel_data_occupants:
            uuids.append(occupant.uuid)
            states.append(occupant.state)

        # update internal variables
        self.here_now_uuids = uuids
        self.here_now_states = states

    def here_now_callback(self, result, status):
        print("result: ", result)
        if status.is_error():
            print("Status is error: ", str(status))
            return  # TODO: handle error
        else:
            self._parse_channel_data(result.channels)
            print(self.__repr__())
