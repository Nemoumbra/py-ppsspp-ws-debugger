import asyncio
import json
from collections import deque

import pytest

from ppsspp import AsyncSession, PPSSPPRequest
from ppsspp.exceptions.connection_terminated import ConnectionTerminated
from ppsspp.exceptions.request_failed_error import RequestFailedError

from ppsspp.model.events.base_event import BaseEvent
from ppsspp.model.events.cpu.common import CpuResumeEvent
from ppsspp.model.events.game.common import GameQuitEvent
from ppsspp.model.events.input.analog import InputAnalogEvent
from ppsspp.model.events.other.log import LogEvent
from ppsspp.model.ppsspp_objects.input.analog_stick import AnalogStick
from ppsspp.model.ppsspp_objects.logs.log_level import LogLevel
from ppsspp.model.requests.other.version import VersionRequest


# TODO: actually test all events and requests...

class MockConnection:
    def __init__(self, exhausted: asyncio.Event, events: list[dict]):
        self.gen = (event for event in events)
        self.exhausted = exhausted

    def _next(self):
        item = next(self.gen)
        return item

    async def recv(self) -> dict:
        try:
            return self._next()
        except StopIteration:
            self.exhausted.set()
            raise ConnectionTerminated from None

    async def send(self, _):
        # Do nothing
        pass


class MockStepByStepConnection:
    def __init__(self, events: list[dict], manual: bool):
        self.gen = (event for event in events)
        self.proceed_requested = asyncio.Event()
        self.manual = manual

    def _next(self):
        item = next(self.gen)
        return item

    async def recv(self) -> dict:
        try:
            await self.proceed_requested.wait()
            self.proceed_requested.clear()
            return self._next()
        except StopIteration:
            raise ConnectionTerminated from None

    async def send(self, _):
        if self.manual:
            # Do nothing
            return
        self.proceed()

    def proceed(self):
        self.proceed_requested.set()


class MockTicketMonitorConnection:
    def __init__(self, events: list[dict]):
        self.gen = (event for event in events)
        self.proceed_requested = asyncio.Event()
        self.tickets: deque[str] = deque()

    def _next(self):
        item = next(self.gen)
        return item

    async def recv(self) -> dict:
        try:
            await self.proceed_requested.wait()
            self.proceed_requested.clear()
            event = self._next()
            assert "ticket" not in event, "What are you doing with your tests?"
            # Inject the correct
            event["ticket"] = self.tickets.popleft()
            return event
        except StopIteration:
            raise ConnectionTerminated from None

    async def send(self, data: str):
        request = json.loads(data)
        assert isinstance(request, dict), "What are you doing with your tests?"
        assert "ticket" in request, "What are you doing with your tests?"
        ticket = request.get("ticket")
        assert ticket is not None, "What are you doing with your tests?"

        self.tickets.append(ticket)
        self.proceed()

    def proceed(self):
        self.proceed_requested.set()


@pytest.fixture()
def log_ev():
    return LogEvent(
        event="log", timestamp="", header="",
        message="message",
        level=LogLevel.INFO, channel=""
    )


@pytest.fixture()
def cpu_ev():
    return CpuResumeEvent(
        event="cpu.resume"
    )


@pytest.fixture()
def game_ev():
    return GameQuitEvent(
        event="game.quit", game=None
    )


@pytest.fixture()
def input_ev():
    return InputAnalogEvent(
        event="input.analog", stick=AnalogStick.left, x=1.0, y=-1.0
    )


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


async def test_serialization():
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
    session = AsyncSession()
    events = get_events()
    exhausted = asyncio.Event()
    connection = MockConnection(exhausted, events)

    await session.run(connection)
    await exhausted.wait()
    pass


async def test_responses_low_level():
    # Testing 'send_request{_raw}' here

    session = AsyncSession()
    kTicket = "TICKET"
    events = [
        {"event": "error", "message": "oh man", "level": LogLevel.ERROR.value, "ticket": kTicket},
        {"event": "error", "message": "oh man", "level": LogLevel.ERROR.value, "ticket": kTicket}
    ]

    notifier = asyncio.Event()
    async def handler(ev: BaseEvent):
        notifier.set()

    connection = MockStepByStepConnection(events, manual=True)
    await session.run(connection)

    request = PPSSPPRequest("version")
    request.set_ticket(kTicket)
    await session.send_request_raw(request, handler)
    # Simulate a response
    connection.proceed()
    await notifier.wait()
    notifier.clear()

    await session.send_request(VersionRequest(ticket=kTicket), handler)
    # Simulate a response
    connection.proceed()
    await notifier.wait()


async def test_responses_mid_level():
    # Testing 'execute_unchecked{_raw}' here

    session = AsyncSession()
    kTicket = "TICKET"
    events = [
        {"event": "error", "message": "oh man", "level": LogLevel.ERROR.value, "ticket": kTicket},
        {"event": "error", "message": "oh man", "level": LogLevel.ERROR.value, "ticket": kTicket}
    ]

    connection = MockStepByStepConnection(events, manual=False)
    await session.run(connection)

    request = PPSSPPRequest("version")
    request.set_ticket(kTicket)
    await session.execute_unchecked_raw(request)

    await session.execute_unchecked(VersionRequest(ticket=kTicket))


async def test_responses_high_level():
    # Testing 'execute{_raw}' here

    session = AsyncSession()
    kTicket = "TICKET"
    events = [
        {"event": "version", "name": "mock", "version": "0", "ticket": kTicket},
        {"event": "version", "name": "mock", "version": "0", "ticket": kTicket},

        {"event": "error", "message": "oh man", "level": LogLevel.ERROR.value, "ticket": kTicket},
        {"event": "error", "message": "oh man", "level": LogLevel.ERROR.value, "ticket": kTicket},
    ]

    connection = MockStepByStepConnection(events, manual=False)
    await session.run(connection)

    request = PPSSPPRequest("version")
    request.set_ticket(kTicket)

    await session.execute_raw(request)
    await session.execute(VersionRequest(ticket=kTicket))

    with pytest.raises(RequestFailedError):
        await session.execute_raw(request)
    with pytest.raises(RequestFailedError):
        await session.execute(VersionRequest(ticket=kTicket))


async def test_auto_tickets():
    session = AsyncSession()
    events = [
        {"event": "error", "message": "oh man", "level": LogLevel.ERROR.value},
        {"event": "error", "message": "oh man", "level": LogLevel.ERROR.value}
    ]

    connection = MockTicketMonitorConnection(events)
    await session.run(connection)

    request = PPSSPPRequest("version")
    await session.execute_unchecked_raw(request)
    await session.execute_unchecked(VersionRequest())

#
# async def test_subscriptions(log_ev, cpu_ev, game_ev, input_ev):
#     session = AsyncSession()
#     log_count = 0
#     cpu_count = 0
#     game_count = 0
#     input_count = 0
#
#     @session.log_handler()
#     async def handle_log(ev: BaseEvent):
#         nonlocal log_count
#         log_count += 1
#
#     @session.stepping_handler()
#     async def handle_cpu(ev: BaseEvent):
#         nonlocal cpu_count
#         cpu_count += 1
#
#     @session.game_handler()
#     async def handle_game(ev: BaseEvent):
#         nonlocal game_count
#         game_count += 1
#
#     @session.input_handler()
#     async def handle_input(ev: BaseEvent):
#         nonlocal input_count
#         input_count += 1
#
#     pass