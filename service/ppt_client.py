import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from dbus_next import Message, MessageType
from dbus_next.aio import MessageBus

import asyncio
import json

loop = asyncio.get_event_loop()


async def main():
    username = os.environ.get('USERNAME')
    bus = await MessageBus(f"unix:path=/tmp/dbus/{username}.session.usock").connect()

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


loop.run_until_complete(main())