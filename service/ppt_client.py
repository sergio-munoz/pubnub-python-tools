import sys
import os
import getpass

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from dbus_next import Message, MessageType
from dbus_next.aio import MessageBus

import asyncio
import json

loop = asyncio.get_event_loop()


async def main():
    username = getpass.getuser()
    bus_address = f"unix:path=/tmp/dbus/{username}.session.usock"
    bus = await MessageBus(bus_address).connect()

    reply = await bus.call(
        Message(destination='com.example.name',
                path='/com/example/sample0',
                interface='com.example.SampleInterface0',
                member='Frobate',
                signature='is',
                body=[1, "yes"]))

    if reply.message_type == MessageType.ERROR:
        raise Exception(reply.body[0])

    print(json.dumps(reply.body[0], indent=2))

    reply = await bus.call(
        Message(destination='com.example.name',
                path='/com/example/sample0',
                interface='com.example.SampleInterface0',
                member='subscribe',
                signature='s',
                body=["test.dbus.subscribe-2"]))

    reply = await bus.call(
        Message(destination='com.example.name',
                path='/com/example/sample0',
                interface='com.example.SampleInterface0',
                member='publish',
                signature='ss',
                body=["test.ch", "dbus test"]))

    if reply.message_type == MessageType.ERROR:
        raise Exception(reply.body[0])

    print(json.dumps(reply.body[0], indent=2))
loop.run_until_complete(main())