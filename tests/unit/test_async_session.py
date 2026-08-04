import asyncio
import json
from collections import deque
from json import JSONDecodeError

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


class MockStepByStepConnection:
    def __init__(self, events: list, recv_requested: asyncio.Event | None = None, *, manual: bool):
        self.gen = (event for event in events)
        self.proceed_requested = asyncio.Event()
        self.recv_requested = recv_requested
        self.manual = manual

    def _next(self):
        item = next(self.gen)
        if isinstance(item, Exception):
            raise item
        return item

    async def recv(self):
        try:
            if self.recv_requested is not None:
                self.recv_requested.set()
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

    async def close(self):
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

    async def close(self):
        self.proceed_requested.set()


@pytest.fixture()
def log_ev():
    return {
        "event": "log", "timestamp": "", "header": "",
        "message": "message",
        "level": LogLevel.INFO.value, "channel": ""
    }


@pytest.fixture()
def cpu_ev():
    return {
        "event": "cpu.resume"
    }


@pytest.fixture()
def game_ev():
    return {
        "event": "game.quit", "game": None
    }


@pytest.fixture()
def input_ev():
    return {
        "event": "input.analog", "stick": AnalogStick.left.value, "x": 1.0, "y": -1.0
    }


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


async def test_subscriptions(log_ev, cpu_ev, game_ev, input_ev):
    session = AsyncSession()
    log_count = 0
    cpu_count = 0
    game_count = 0
    input_count = 0
    count = 0
    count_all = 0

    events = [
        log_ev, cpu_ev, game_ev, input_ev, log_ev, cpu_ev, game_ev, input_ev
    ]

    connection = MockStepByStepConnection(events, manual=True)
    notifier = asyncio.Event()

    await session.run(connection)

    @session.log_handler()
    async def handle_log(ev: BaseEvent):
        nonlocal log_count
        log_count += 1
        notifier.set()
        notifier.clear()

    @session.stepping_handler()
    async def handle_cpu(ev: BaseEvent):
        nonlocal cpu_count
        cpu_count += 1
        notifier.set()
        notifier.clear()

    @session.game_handler()
    async def handle_game(ev: BaseEvent):
        nonlocal game_count
        game_count += 1
        notifier.set()
        notifier.clear()

    @session.input_handler()
    async def handle_input(ev: BaseEvent):
        nonlocal input_count
        input_count += 1
        notifier.set()
        notifier.clear()

    listen_notifier = asyncio.Event()

    @session.listen_for(CpuResumeEvent)
    async def listen(ev: BaseEvent):
        nonlocal count
        count += 1
        listen_notifier.set()
        listen_notifier.clear()

    prom_notifier = asyncio.Event()

    @session.listen_for(None)
    async def listen_all(ev: BaseEvent):
        nonlocal count_all
        count_all += 1
        prom_notifier.set()
        prom_notifier.clear()

    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (0, 0, 0, 0, 0, 0)

    connection.proceed()
    await asyncio.gather(notifier.wait(), prom_notifier.wait())
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 0, 0, 0, 0, 1)
    connection.proceed()
    await asyncio.gather(notifier.wait(), listen_notifier.wait(), prom_notifier.wait())
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 0, 0, 1, 2)
    connection.proceed()
    await asyncio.gather(notifier.wait(), prom_notifier.wait())
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 0, 1, 3)
    connection.proceed()
    await asyncio.gather(notifier.wait(), prom_notifier.wait())
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 1, 1, 4)
    connection.proceed()
    await asyncio.gather(notifier.wait(), prom_notifier.wait())
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (2, 1, 1, 1, 1, 5)
    connection.proceed()
    await asyncio.gather(notifier.wait(), listen_notifier.wait(), prom_notifier.wait())
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (2, 2, 1, 1, 2, 6)
    connection.proceed()
    await asyncio.gather(notifier.wait(), prom_notifier.wait())
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (2, 2, 2, 1, 2, 7)
    connection.proceed()
    await asyncio.gather(notifier.wait(), prom_notifier.wait())
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (2, 2, 2, 2, 2, 8)


async def test_stopping(log_ev):
    session = AsyncSession()
    await session.stop()

    exhausted = asyncio.Event()

    events = [

    ]
    connection = MockConnection(exhausted, events)

    await session.run(connection)
    await session.stop()

    events = [
        log_ev
    ]
    recv_requested = asyncio.Event()
    connection = MockStepByStepConnection(events, recv_requested, manual=True)
    await session.run(connection)
    await recv_requested.wait()
    recv_requested.clear()
    connection.proceed()
    await session.stop()

async def test_errors():
    session = AsyncSession()

    broken_events = [
        ["sup, I'm not a dict"],
    ]

    try:
        json.loads("wtf")
    except JSONDecodeError as e:
        broken_events.append(e)

    recv_requested = asyncio.Event()
    connection = MockStepByStepConnection(broken_events, recv_requested, manual=True)
    await session.run(connection)

    await recv_requested.wait()
    recv_requested.clear()
    connection.proceed()
    await recv_requested.wait()
    recv_requested.clear()
    connection.proceed()
    await recv_requested.wait()
    recv_requested.clear()
    await session.stop()


