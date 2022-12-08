from dbus_next.aio import MessageBus
from dbus_next.service import (ServiceInterface,
                               method, dbus_property, signal)
from dbus_next import Variant, DBusError
from pubnub_python_tools.app import main_app
from pubnub_python_tools.logger.logging_config import get_logger

import getpass
import asyncio
import os
import sys

ROOT_DIR = str(os.path.dirname(os.path.abspath(__file__)).rsplit("/service")[0])
sys.path.append(f"{ROOT_DIR}")

LOG = get_logger()  # Get logger if needed. Default: INFO



class ExampleInterface(ServiceInterface):
    def __init__(self):
        super().__init__('com.example.SampleInterface0')
        self._bar = 105
        # Start the pubnub main class
        self.pn = None

    @method()
    def Frobate(self, foo: 'i', bar: 's') -> 'a{us}':
        print(f'called Frobate with foo={foo} and bar={bar}')

        return {
            1: 'one',
            2: 'two'
        }

    @method()
    def publish(self, channel: 's', message: 's') -> 's':
        self.pn = main_app.main(["-p", channel, "-m", message])
        print(f'called publish with channel={channel} and message={message}')
        return self.pn

    @method()
    def subscribe(self, channel: 's') -> 's':
        self.pn = main_app.main(["-s", channel])
        print(f'called subscribe with channel={channel}')
        return self.pn

    @method()
    async def Bazify(self, bar: '(iiu)') -> 'vv':
        print(f'called Bazify with bar={bar}')

        return [Variant('s', 'example'), Variant('s', 'bazify')]

    @method()
    def Mogrify(self, bar: '(iiav)'):
        raise DBusError('com.example.error.CannotMogrify',
                        'it is not possible to mogrify')

    @signal()
    def Changed(self) -> 'b':
        return True

    @dbus_property()
    def Bar(self) -> 'y':
        return self._bar

    @Bar.setter
    def Bar(self, val: 'y'):
        if self._bar == val:
            return

        self._bar = val

        self.emit_properties_changed({'Bar': self._bar})


async def main():
    username = getpass.getuser()
    bus_address = f"unix:path=/tmp/dbus/{username}.session.usock"
    print(bus_address)
    bus = await MessageBus(bus_address).connect()
    interface = ExampleInterface()
    bus.export('/com/example/sample0', interface)
    await bus.request_name('com.example.name')

    LOG.info("Starting PubNub Python Tools unix socket.")

    # emit the changed signal after two seconds.
    await asyncio.sleep(2)

    interface.Changed()

    await bus.wait_for_disconnect()


asyncio.get_event_loop().run_until_complete(main())

LOG.info("Closing PubNub Python Tools unix socket.")
