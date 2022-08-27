# pubnub-python-tools
[![ghlastcommit](https://img.shields.io/github/last-commit/sergio-munoz/pubnub-python-tools?style=flat-square)](https://img.shields.io/github/last-commit/sergio-munoz/pubnub-python-tools?style=flat-square)

Useful Tools for interacting with PubNub using Python. 

## Pre-requisites

For MacOS use `homebrew` to install packages or the following [PubNub Ansible Role Python SDK](https://github.com/sergio-munoz/pubnub-ansible-role-python-sdk).

- python3
- python-tk

## TLDR;

Run the install script:

```shell
chomod +x ./scripts/install.sh
./scripts/install.sh SubscribeKey PublishKey UUID
```

You can run python cli commands to PubNub:

```shell
python3 run_pn.py -s "Space01" -p "Space01" -m "Hello world!"
```

## Manual Setup

Setup a new python environment and install packages in `requirements.txt`:

```shell
$ python3 -m venv Venv
$ source /Venv/bin/activate
$ (python) pip install -r requirements.txt
$ (python) run_pn.py --help
```

## Configure PubNub

Copy the environment sample `env` file into your own environment `.env` (watch the dot `'.'`) file and replace your keys from the Admin Portal.

```shell
$ cp env .env
$ vim .env
```

> If you can't see your `.env` file try using `ls -a`

A minimal `.env` file to work properly needs at least your `SubscribeKey`, `PublishKey` and `UUID`.

```shell
$ cat .env
SUBSCRIBE_KEY=sub-xxx-xxx
PUBLISH_KEY=pub-xxx-xxx
USER_ID=UUID
```

There are more [settings](#more_settings) that you can configure.

## CLI

File location: `./scripts/run_pn.py`

To run with via CLI you are going to need your credentials according to whatever operation you want to do. 

Always set the UUID to uniquely identify the user or device that connects to PubNub. This UUID should be persisted, and should remain unchanged for the lifetime of the user or the device. Not setting the UUID can significantly impact your billing.

> Remember to always set up your `UUID` with `-u`.

For help use:

```shell
$ cd scripts/
$ python3 run_pn.py --help
```

### Subscribe

Subscribe to a channel forever. 

* `-sk`, `--subscribe-key` - PubNub subscribe key
* `-s`, `--subscribe` - PubNub subscribe channel name

```shell
$ python3 run_pn.py -sk SubscribeKey -s ChannelName
```

### Publish

Publish a message to a channel.

* `-pk`, `--subscribe-key` - PubNub subscribe key
* `-pk`, `--publish-key` - PubNub publish key
* `-p`, `--publish` - PubNub publish channel name
* `-m`, `--message` - Message to publish

> For some reason the pubnub python sdk fails to publish when instantiated withoud a subscribe key, so pass it to avoid issues.

```shell
python3 run_pn.py -sk SubscribeKey -pk PublishKey -p ChannelName -m "Hello world!"
```

### Subscribe and Publish

Because subscribe and publish happen so fast the subscribe might not be listening when the publish was made and thus it will not be shown, but it will be published, if other devices are listening, they will reflect the changes. This is classic pub/sub behavior.

```shell
python3 run_pn.py -u UUID -sk SubscribeKey -pk PublishKey -s ChannelName -p ChannelName -m "Hello world!"
```

Open another terminal and run that command again to show that the user is still subscribed the channel.

Dig into the `logger/main_log.log` to see more information.

### Presence

Subscribe to a channel with Presence forever. 

* `-sk`, `--subscribe-key` - PubNub subscribe key
* `-s`, `--subscribe` - PubNub subscribe channel name
* `-pres`, `--presence` - Presence flag

```shell
python3 run_pn.py -sk SubscribeKey -s ChannelName -pres
```

### Unsubscribe

Send a leave event to a channel subscribed with Presence. 

* `-sk`, `--subscribe-key` - PubNub subscribe key
* `-us`, `--unsubscribe` - PubNub channel name to unsubscribe from

```shell
python3 run_pn.py -sk SubscribeKey -us ChannelName
```

### HereNow

Call `Here Now` on a channel. 

* `-here`, `--here-how` - Here now on a channel name

```shell
python3 run_pn.py -here ChannelName
```

For advanced topics see: [cache busting information](#cache_busting). __NOTE: TBD SOON__

## Settings

You can set up `SubscribeKey`, `PublishKey`, and `UserId` from the environmental variables file `.env`. If you use the CLI you're technically overriding them using arguments, which should have preference. You can see how things work in the `pubnub_python_tools/config` module.

## Testing

To all run tests use `unittest`:

```shell
python3 -m unittest tests/test_*
```
```
----------------------------------------------------------------------
Ran 10 tests in 0.163s

OK
```

## Packaging

Currently this is only uploaded in the testing repository version of `pypi` as this is not yet officially released. Check it out: [https://test.pypi.org/project/pubnub-python-tools/](https://test.pypi.org/project/pubnub-python-tools/)

### Install using pip

```shell
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pubnub-python-tools
```

### Install to a Jupyter Notebook

```shell
import sys
!{sys.executable} -m pip install -U pubnub
!{sys.executable} -m pip install -U --index-url https://test.pypi.org/simple/ --no-deps pubnub-python-tools
```