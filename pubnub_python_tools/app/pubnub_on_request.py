"""Use requests to call http on_request PubNub functions."""
import requests


def get(url, params, json):
    """Get wrapper."""
    return requests.get(url=url, params=params, json=json)
