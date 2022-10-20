# pubnub-python-tools
[![Python application](https://github.com/sergio-munoz/pubnub-python-tools/actions/workflows/python-app.yml/badge.svg)](https://github.com/sergio-munoz/pubnub-python-tools/actions/workflows/python-app.yml) [![Upload Python Package](https://github.com/sergio-munoz/pubnub-python-tools/actions/workflows/python-publish-testing.yml/badge.svg)](https://github.com/sergio-munoz/pubnub-python-tools/actions/workflows/python-publish-testing.yml) [![ghlastcommit](https://img.shields.io/github/last-commit/sergio-munoz/pubnub-python-tools?style=flat-square)](https://img.shields.io/github/last-commit/sergio-munoz/pubnub-python-tools?style=flat-square)

Quickly interact with PubNub using the Python SDK.

## Pre-requisites
-----------------

For MacOS use `homebrew` to install packages or the following [PubNub Ansible Role Python SDK](https://github.com/sergio-munoz/pubnub-ansible-role-python-sd) that sets *everything* for you. 

- python3
- python-tk

## Install
----------

To install `pubnub-python-tools`:

### Install using pip

> This is only uploaded in the testing repository version of `pypi` as this is not yet officially released. Check it out: [https://test.pypi.org/project/pubnub-python-tools/](https://test.pypi.org/project/pubnub-python-tools/)

To install the latest managed packaged version:

```shell
$ python -m pip install -i https://test.pypi.org/simple/ pubnub-python-tools
```

### Automatic build and install

> It is recommended to setup a [virtual environment]().

To install locally the latest git version:

```shell
$ git clone https://github.com/sergio-munoz/pubnub-python-tools
$ ./scripts/build_install.sh
```

> Set script permissions with `chmod +x`

### Manually build and install

Setup a new python virtual environment and install packages in `requirements_build.txt`:

```shell
$ python3 -m venv build_venv
$ source build_venv/bin/activate
(build_venv) $ pip install -r build_requirements.txt
(build_venv) $ hatch build
(build_venv) $ pip install dist/pubnub_python_tools-${VERSION}.tar.gz
```

### Install into a Jupyter Notebook

To install the latest testing repository version into the Jupyter Notebook kernel:

```shell
import sys
!{sys.executable} -m pip install -U pubnub
!{sys.executable} -m pip install -U --index-url https://test.pypi.org/simple/ --no-deps pubnub-python-tools
```

## PubNub Auth Settings
-----------------------

> Always set the UUID (USER_ID) to uniquely identify the user or device that connects to PubNub. This UUID should be persisted, and should remain unchanged for the lifetime of the user or the device. Not setting the UUID can significantly impact your billing.

To run `pubnub` commands you need to setup your PubNub credentials using any of the following ways:

### Automatically

Run the `setup.sh` script with your PubNub subscribe key, publish key and user_id:

```shell
$ ./scripts/install.sh $PN_SUBSCRIBE_KEY $PN_PUBLISH_KEY $PN_USER_ID
```

### Using an .env file

> Requires [python-dotenv](https://pypi.org/project/python-dotenv/). Install using: `pip install python-dotenv`

> If you can't see your `.env` file try using: `ls -la`

Create an `.env` file to avoid typing your credentials each time.

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

### Manually via CLI

> This has the highest precedence

Manually set cli variables before each command:

```shell
-sk $PN_SUBSCRIBE_KEY -pk $PN_PUBLISH_KEY -u $PN_USER_ID
```

__CLI Args:__

* `-sk`, `--subscribe-key` - PubNub subscribe key.
* `-pk`, `--publish-key` - PubNub publish key.
* `-u`, `--user-id` - User ID (UUID).

### Overriding Global variables

> This has the lowest precedence

__NOTE: It is not recommended to hard-code your credentials due to security purposes.__

Override the global variables manually in file `pubnub_python_tools/config/module_config.py`:

```python
# OVERRIDE GLOBAL VARIABLES
SUBSCRIBE_KEY = "pub-xxx-xxx"
PUBLISH_KEY = "sub-xxx-xxx"
USER_ID = "UUID"
```

## Sample Use
-------------

Run PubNub using the script: `run_pn.py`. 

```shell
$ python ./scripts/run_pn.py -s "Space01" -p "Space01" -m "Hello from MySpace01"
```

Or if installed, run PubNub using the command: `pubnub-python-tools`.

```shell
$ pubnub-python-tools -s "Space01" -p "Space01" -m "Hello from MySpace01"
```

Get help using the `--help` flag.

```shell
$ python ./scripts/run_pn.py --help
$ pubnub-python-tools --help
```

## CLI Usage Reference
----------------------

> Remember to always set up your UUID `USER_ID` with `-u`.

### Subscribe

Subscribe to a channel forever.

```shell
python run_pn.py -s "Space"
```
__CLI Args:__

* `-sk`, `--subscribe-key` - PubNub subscribe key (or set in `.env`)
* `-s`, `--subscribe` - PubNub subscribe channel name

### Publish

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
___

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
---

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
(venv) $ python -m coverage run -m unittest discover
(venv) $ python -m coverage report -i
```

```
Name                                                       Stmts   Miss  Cover
------------------------------------------------------------------------------
src/pubnub_python_tools/app/device_manager.py                 74     16    78%
src/pubnub_python_tools/app/main_app.py                       46     35    24%
src/pubnub_python_tools/app/pubnub_config.py                  16      0   100%
src/pubnub_python_tools/app/pubnub_handle_disconnects.py      29     20    31%
src/pubnub_python_tools/app/pubnub_here_now_callback.py       45      9    80%
src/pubnub_python_tools/app/pubnub_listener.py               133     73    45%
src/pubnub_python_tools/app/pubnub_manager.py                 89     33    63%
src/pubnub_python_tools/app/pubnub_manager_asyncio.py         48     11    77%
src/pubnub_python_tools/app/pubnub_on_request.py               3      0   100%
src/pubnub_python_tools/app/pubnub_publish.py                 15     11    27%
src/pubnub_python_tools/cli/v1.py                             18      0   100%
src/pubnub_python_tools/config/module_config.py               20      3    85%
src/pubnub_python_tools/logger/logging_config.py              32      9    72%
tests/__init__.py                                              4      0   100%
tests/test_device_manager.py                                  67      0   100%
tests/test_main_app.py                                         9      0   100%
tests/test_pubnub_manager.py                                  79      0   100%
tests/test_pubnub_manager_asyncio.py                         102     10    90%
tests/test_request_function.py                                15      0   100%
tests/test_v1.py                                              32      0   100%
------------------------------------------------------------------------------
TOTAL                                                        876    230    74%

6 empty files skipped.
```