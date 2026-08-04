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
        {},
        {"event": 123},
        {"event": "unknown_event"},
        {"event": "error", "message": "oh man", "level": LogLevel.ERROR.value},

        {"event": "memory.unknown_event"},
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
