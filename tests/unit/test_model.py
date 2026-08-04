import asyncio

from ppsspp import AsyncSession, PPSSPPRequest
from ppsspp.exceptions.connection_terminated import ConnectionTerminated
from ppsspp.model.ppsspp_objects.logs.log_level import LogLevel
from ppsspp.model.requests.other.version import VersionRequest


# TODO: find a better place for this class (it's duplicated)
class MockConnection:
    def __init__(self, exhausted: asyncio.Event, events: list):
        self.gen = (event for event in events)
        self.exhausted = exhausted

    def _next(self):
        item = next(self.gen)
        return item

    async def recv(self):
        try:
            return self._next()
        except StopIteration:
            self.exhausted.set()
            raise ConnectionTerminated from None

    async def send(self, _):
        # Do nothing
        pass

    async def close(self):
        pass


# TODO: fixture?

def get_events():
    return [
        # Garbage data
        {},
        {"event": 123},
        {"event": "unknown_event"},
        {"event": "memory.unknown_event"},

        # The error event
        {"event": "error", "message": "oh man", "level": LogLevel.ERROR.value},

        # Breakpoints
        {"event": "cpu.breakpoint.add"},
        {"event": "cpu.breakpoint.update"},
        {"event": "cpu.breakpoint.remove"},
        {"event": "cpu.breakpoint.list", "breakpoints": [
            {'address': 0, 'enabled': False, 'log': True, 'code': "ooops", 'condition': None, 'logFormat': None,
             'symbol': None}
        ]},
        {"event": "cpu.breakpoint.list", "breakpoints": [
            {'address': 0, 'enabled': False, 'log': True, 'code': "ooops", 'condition': "true",
             'logFormat': "format text", 'symbol': "zz_func"}
        ]},
        {"event": "memory.breakpoint.add"},
        {"event": "memory.breakpoint.update"},
        {"event": "memory.breakpoint.remove"},
        {"event": "memory.breakpoint.list", "breakpoints": [
            {'address': 0, 'size': 1, 'enabled': False, 'log': True, 'read': True, 'write': True, 'change': True,
             'hits': -1, 'condition': None, 'logFormat': None, 'symbol': None}
        ]},
        {"event": "memory.breakpoint.list", "breakpoints": [
            {'address': 0, 'size': 1, 'enabled': False, 'log': True, 'read': True, 'write': True, 'change': True,
             'hits': -1, 'condition': "true", 'logFormat': "format text", 'symbol': "zz_func"}
        ]},
        # CPU

        # Disassembly

        # Game

        # GPU

        # HLE

        # Input

        # Memory

        # Replay

        # Other
        {"event": "version", "name": "mock", "version": "0"}
    ]


def get_requests():
    return {

    }

# TODO: actually test all events and requests...


async def test_serialization():
    # Sending requests

    session = AsyncSession()
    events = get_events()
    requests = get_requests()
    exhausted = asyncio.Event()
    connection = MockConnection(exhausted, events)

    await session.run(connection)

    # Low-level stuff, no ticket
    await session.send_request_raw(PPSSPPRequest("version"))
    await session.send_request(VersionRequest())

    pass


async def test_parsing():
    # Parsing events
    session = AsyncSession()
    events = get_events()
    exhausted = asyncio.Event()
    connection = MockConnection(exhausted, events)

    await session.run(connection)
    await exhausted.wait()
    pass
