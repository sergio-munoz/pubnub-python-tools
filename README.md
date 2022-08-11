# pubnub-python-tools
Useful Tools for interacting with PubNub using Python. 

## Pre-requisites

For MacOS use `homebrew` to install packages or the following [PubNub Ansible Role Python SDK](https://github.com/sergio-munoz/pubnub-ansible-role-python-sdk).

- python3
- python-tk

## TLDR;

Run the following script:

```
chomod +x scripts/run.sh && ./scripts/run.sh
```


## Manual Setup

Setup a new python environment and install packages in `requirements.txt`:

```
$ python3 -m venv Venv
$ source /Venv/bin/activate
$ (python) pip install -r requirements.txt
```

## Configure PubNub

Copy the environment sample `env` file into your own environment `.env` (watch the `.`) file and replace your keys from the Admin Portal.

```
$ cp env .env
$ vim .env
```

## Run App

Running this app will configure pubnub, create listeners and callbacks, subscribe to a channel and publish a message.

```
python3 run_app.py
```

Open another terminal and run that command again to show that the user is still subscribed the channel.

Dig into the `logger/main_log.log` to see more information.


## Settings

`SubscribeKey`, `PublishKey`, and `UserId` are read from `.env` variable but you can override them in `module_config.py`.

## Testing

To all run tests:

```
python3 -m test/test*
```