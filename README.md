# pubnub-python-tools
Useful Tools for interacting with PubNub using Python. 

## Pre-requisites

For MacOS use `homebrew` to install packages or the following [PubNub Ansible Role Python SDK](https://github.com/sergio-munoz/pubnub-ansible-role-python-sdk).

- python3
- python-tk

## TLDR;

Run the install script:

```
chomod +x ./scripts/install.sh
./scripts/install.sh SubscribeKey PublishKey UUID
```

You can run python commands to PubNub:

```
python3 pn_run.py -s Space01 -p Space01 "Hello world!"
```

## Manual Setup

Setup a new python environment and install packages in `requirements.txt`:

```
$ python3 -m venv Venv
$ source /Venv/bin/activate
$ (python) pip install -r requirements.txt
$ (python) pn_run.py --help
```

## Configure PubNub

Copy the environment sample `env` file into your own environment `.env` (watch the `.`) file and replace your keys from the Admin Portal.

```
$ cp env .env
$ vim .env
```

## CLI

To run with via CLI you are going to need your credentials according to whatever operation you want to do. 

Always set the UUID to uniquely identify the user or device that connects to PubNub. This UUID should be persisted, and should remain unchanged for the lifetime of the user or the device. Not setting the UUID can significantly impact your billing.

> Remember to always set up your `UUID` with `-u`.

For help use:

```
python3 pn_run.py --help
```

### Subscribe

Subscribe to a channel forever. 

* `-sk`, `--subscribe-key` - PubNub subscribe key
* `-s`, `--subscribe` - PubNub subscribe channel name

```
python3 run_app.py -sk SubscribeKey -s ChannelName
```

### Publish

Publish a message to a channel.

* `-pk`, `--publish-key` - PubNub publish key
* `-p`, `--publish` - PubNub publish channel name
* `-m`, `--message` - Message to publish

```
python3 run_app.py -pk PublishKey -p ChannelName -m "Hello world!"
```

### Subscribe and Publish

Because subscribe and publish happen so fast the subscribe might not be listening when the publish was made and thus it will not be shown, but it will be published, if other devices are listening, they will reflect the changes. This is classic pub/sub behavior.

```
python3 run_app.py -sk SubscribeKey -s ChannelName -pk PublishKey -p ChannelName -m "Hello world!" -u UUID
```

Open another terminal and run that command again to show that the user is still subscribed the channel.

Dig into the `logger/main_log.log` to see more information.

### Presence

Subscribe to a channel with Presence forever. 

* `-sk`, `--subscribe-key` - PubNub subscribe key
* `-s`, `--subscribe` - PubNub subscribe channel name
* `-pres`, `--presence` - Presence flag

```
python3 run_app.py -sk SubscribeKey -s ChannelName -pres
```

### Unsubscribe

Send a leave event to a channel subscribed with Presence. 

* `-sk`, `--subscribe-key` - PubNub subscribe key
* `-us`, `--unsubscribe` - PubNub channel name to unsubscribe from

```
python3 run_app.py -sk SubscribeKey -us ChannelName
```

## Settings

You can set up `SubscribeKey`, `PublishKey`, and `UserId` from the environmental variables file `.env`. If you use the CLI you're technically overriding them using arguments, which should have preference. You can see how things work in the file `module_config.py`. 


## Testing

To all run tests:

```
python3 -m test/test*
```