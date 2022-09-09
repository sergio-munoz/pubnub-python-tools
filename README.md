# pubnub-python-tools
[![ghlastcommit](https://img.shields.io/github/last-commit/sergio-munoz/pubnub-python-tools?style=flat-square)](https://img.shields.io/github/last-commit/sergio-munoz/pubnub-python-tools?style=flat-square)

Useful Tools for quickly interacting with PubNub using Python. 

____
## Pre-requisites

For MacOS use `homebrew` to install packages or the following [PubNub Ansible Role Python SDK](https://github.com/sergio-munoz/pubnub-ansible-role-python-sdk).

- python3
- python-tk

## Packaging

Currently this is only uploaded in the testing repository version of `pypi` as this is not yet officially released. Check it out: [https://test.pypi.org/project/pubnub-python-tools/](https://test.pypi.org/project/pubnub-python-tools/)

### Install using pip

```shell
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps pubnub-python-tools
```

## TLDR;

Run the install script with your PubNub api credentials:

```shell
$ chmod +x ./scripts/install.sh
$ ./scripts/install.sh $PN_SUBSCRIBE_KEY $PN_PUBLISH_KEY $PN_USER_ID
```

After, you can quickly run python cli commands to PubNub:

```shell
python3 ./scripts/run_pn.py -s "Space01" -p "Space01" -m "Hello world!"
```

## Manual Setup

Setup a new python virtual environment and install packages in `requirements.txt`:

```shell
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ python -m pip install -r requirements.txt
```
Run commands:

```shell
(venv) $ python ./scripts/run_pn.py --help
```

### Set PubNub Credentials

To run commands you need to setup your PubNub api keys.

#### Manually via CLI

Manually set cli variables before each command:

```shell
-sk $PN_SUBSCRIBE_KEY -pk $PN_PUBLISH_KEY -u $PN_USER_ID
```

__CLI Args:__

* `-sk`, `--subscribe-key` - PubNub subscribe key.
* `-pk`, `--publish-key` - PubNub publish key.
* `-u`, `--user-id` - User ID or UUID.

#### Using an .env file

Create an `.env` file to avoid typing your credentials each time.

> Requires [python-dotenv](https://pypi.org/project/python-dotenv/). Install with `pip install python-dotenv`

Copy the env file sample `env` file into your own `.env` (watch the dot `'.'`) file and replace with your PubNub keys.

```shell
$ cp env .env
```

A minimal `.env` file to work properly needs at least your PubNub's `subscribe key`, `publish key` and a chosen `user id`:

```shell
$ cat .env

PN_SUBSCRIBE_KEY=sub-xxx-xxx
PN_PUBLISH_KEY=pub-xxx-xxx
PN_USER_ID=UUID
```

> If you can't see your `.env` file try using `ls -la`

#### Overriding Global variables

__NOTE: It is not recommended to hard-code your credentials on this file due to security purposes.__

Override the global variables manually in file `pubnub_python_tools/config/module_config.py`:

```python
# OVERRIDE GLOBAL VARIABLES
SUBSCRIBE_KEY = "pub-xxx-xxx"
PUBLISH_KEY = "sub-xxx-xxx"
USER_ID = "UUID"
```

## Usage

### CLI

After setting your environment and credentials, run CLI commands using the file`scripts/run_pn.py`:

```shell
(venv) $ cd scripts/
(venv) $ python run_pn.py -h
```

Always set the UUID to uniquely identify the user or device that connects to PubNub. This UUID should be persisted, and should remain unchanged for the lifetime of the user or the device. Not setting the UUID can significantly impact your billing.

> Remember to always set up your UUID `USER_ID` with `-u`.

#### Subscribe

Subscribe to a channel forever.

```shell
python run_pn.py -s "Space"
```
__CLI Args:__

* `-sk`, `--subscribe-key` - PubNub subscribe key (or set in `.env`)
* `-s`, `--subscribe` - PubNub subscribe channel name

#### Publish

Publish a message to a channel.

```shell
python run_pn.py -p "Space" -m "payload"
```

__CLI Args:__

* `-sk`, `--subscribe-key` - PubNub subscribe key (or set in `.env`)
* `-pk`, `--publish-key` - PubNub publish key (or set in `.env`)
* `-p`, `--publish` - PubNub publish channel name
* `-m`, `--message` - Message to publish

> For some reason the pubnub python sdk fails to publish when instantiated without a subscribe key, so pass it to avoid issues.

### Presence

Subscribe to a channel with Presence forever. 

```shell
python run_pn.py -s "Space" -pres
```

__CLI Args:__
* `-sk`, `--subscribe-key` - PubNub subscribe key (or set in `.env`)
* `-s`, `--subscribe` - PubNub subscribe channel name
* `-pres`, `--presence` - Presence flag

### HereNow

Call `Here Now` on a channel. 

```shell
python run_pn.py -here "Space"
```

__CLI Args:__
* `-sk`, `--subscribe-key` - PubNub subscribe key (or set in `.env`)
* `-here`, `--here-how` - Here now on a channel name

For advanced `HereNow` topics see: [cache busting information](#cache_busting). __NOTE: TBD SOON__

### Unsubscribe

Send a leave event to a channel subscribed with Presence. 

```shell
python run_pn.py -us "Space"
```

__CLI Args:__
* `-sk`, `--subscribe-key` - PubNub subscribe key (or set in `.env`)
* `-us`, `--unsubscribe` - PubNub channel name to unsubscribe from

## Use Cases
### Subscribe and Publish

Because subscribe and publish happen so fast the subscribe might not be listening when the publish was made and thus it will not be shown, but it will be published, if other devices are listening, they will reflect the changes. This is classic pub/sub behavior.

Open one terminal and run:

```shell
(venv) $ python run_pn.py -s "Space" -p "Space" -m "payload 1"
```

Open another terminal and run that command modified to show that the user is still subscribed the channel:

```shell
(venv) $ python run_pn.py -s "Space" -p "Space" -m "payload 2"
```

Dig into the `logger/main_log.log` to see more information.

## Tests

### Unit Tests

To all run tests use `unittest`:

```shell
(venv) $ python -m unittest tests/test_*
```

```
----------------------------------------------------------------------
Ran 20 tests in 30.680s

OK
```

### Coverage

```shell
(venv) $ python -m coverage run -m unittest
(venv) $ python -m coverage report
```

```
Name                                                       Stmts   Miss  Cover
------------------------------------------------------------------------------
pubnub_python_tools/__init__.py                                0      0   100%
pubnub_python_tools/app/__init__.py                            0      0   100%
pubnub_python_tools/app/device_manager.py                     74     16    78%
pubnub_python_tools/app/main_app.py                           44     32    27%
pubnub_python_tools/app/pubnub_config.py                      16      0   100%
pubnub_python_tools/app/pubnub_handle_disconnects.py          17      8    53%
pubnub_python_tools/app/pubnub_here_now_callback.py           15     12    20%
pubnub_python_tools/app/pubnub_listener.py                   112     56    50%
pubnub_python_tools/app/pubnub_manager.py                     65     18    72%
pubnub_python_tools/app/pubnub_manager_asyncio.py             51     11    78%
pubnub_python_tools/app/pubnub_on_request.py                   3      0   100%
pubnub_python_tools/app/pubnub_publish.py                     15     11    27%
pubnub_python_tools/cli/__init__.py                            0      0   100%
pubnub_python_tools/cli/v1.py                                 18      0   100%
pubnub_python_tools/config/__init__.py                         0      0   100%
pubnub_python_tools/config/http_on_request_on_connect.py      15      3    80%
pubnub_python_tools/config/module_config.py                   20      3    85%
pubnub_python_tools/logger/__init__.py                         0      0   100%
pubnub_python_tools/logger/logging_config.py                  32      9    72%
scripts/__init__.py                                            0      0   100%
tests/__init__.py                                              4      0   100%
tests/test_device_manager.py                                  67      0   100%
tests/test_main_app.py                                         9      0   100%
tests/test_pubnub_manager.py                                  64      0   100%
tests/test_pubnub_manager_asyncio.py                          88      7    92%
tests/test_request_function.py                                15      0   100%
tests/test_v1.py                                              32      0   100%
------------------------------------------------------------------------------
TOTAL                                                        776    186    76%
```

## Misc
### Install to a Jupyter Notebook

```shell
import sys
!{sys.executable} -m pip install -U pubnub
!{sys.executable} -m pip install -U --index-url https://test.pypi.org/simple/ --no-deps pubnub-python-tools
```
