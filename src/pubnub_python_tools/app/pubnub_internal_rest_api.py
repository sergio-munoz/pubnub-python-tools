"""Interact with PubNub's internal api."""
import requests
import json


def get(url, params, json):
    """Get wrapper."""
    return requests.get(url=url, params=params, json=json)


def authenticate(email, password):
    """Authenticate using PubNub internal rest api."""
    URL = 'https://admin.pubnub.com/api/me'
    HEADER = {'Content-Type': 'application/json'}
    DATA_RAW = '{"email": "' + email + '", "password": "' + password + '"}'

    response = requests.post(url=URL, headers=HEADER, data=DATA_RAW)
    decoded = str(response.content.decode())
    parsed = json.loads(decoded)

    try:
        token = parsed['result']['token']
        user = parsed['result']['user']['id']
    except KeyError:
        raise Exception("Invalid credentials")

    return (user, token)


def get_accounts(user, token):
    """Authenticate using PubNub internal rest api."""
    URL = f'https://admin.pubnub.com/api/accounts?user_id={user}'
    HEADER = {'X-Session-Token': token}

    response = requests.get(url=URL, headers=HEADER)
    decoded = str(response.content.decode())
    parsed = json.loads(decoded)

    try:
        accounts = parsed['result']['accounts']
    except KeyError:
        raise Exception("Invalid credentials")

    return accounts


def get_accounts_ids(accounts) -> list:
    ids = []
    for account in accounts:
        ids.append(account['id'])
    return ids


def get_apps(account_id, token):
    """Get apps using PubNub internal rest api."""
    URL = f'https://admin.pubnub.com/api/apps?owner_id={account_id}&no_keys=1'
    HEADER = {'X-Session-Token': token}

    response = requests.get(url=URL, headers=HEADER)
    decoded = str(response.content.decode())
    parsed = json.loads(decoded)

    try:
        apps = parsed['result']
    except KeyError:
        raise Exception("Invalid credentials")

    return apps


def get_apps_ids(apps) -> list:
    ids = []
    for app in apps:
        ids.append(app['id'])
    return ids


def get_app_based_usage(app_id, token, usage_type, start_date, end_date):
    """Get app based usage using PubNub internal rest api."""
    URL = f'https://admin.pubnub.com/api/v4/services/usage/legacy/usage?app_id={app_id}&usageType={usage_type}&file_format=json&start={start_date}&end={end_date}'
    HEADER = {'X-Session-Token': token}

    response = requests.get(url=URL, headers=HEADER)
    decoded = str(response.content.decode())
    parsed = json.loads(decoded)
    if 'error' in parsed:
        raise Exception("Invalid credentials")
    return parsed
