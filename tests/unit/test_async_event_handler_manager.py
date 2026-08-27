from ppsspp.async_event_handler_manager import AsyncEventHandlerManager, Router
from ppsspp.model.events.base_event import BaseEvent
from ppsspp.model.events.cpu.common import CpuResumeEvent
from ppsspp.model.events.game.common import GameQuitEvent
from ppsspp.model.events.input.analog import InputAnalogEvent
from ppsspp.model.events.other.log import LogEvent
from ppsspp.model.ppsspp_objects.input.analog_stick import AnalogStick
from ppsspp.model.ppsspp_objects.logs.log_level import LogLevel
from ppsspp.ticket_manager import TicketManager

import pytest


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


# TODO: more fixtures? This gotta be reworked in some way or another, too much copy-paste...

# TODO: add tests that check that there can be >= 2 handlers of each kind

async def test_broadcasts(log_ev, cpu_ev, game_ev, input_ev):
    event_handler_man = AsyncEventHandlerManager(TicketManager(ticket_length=4))
    router = Router()
    event_handler_man.include_router(router)

    log_count = 0
    cpu_count = 0
    game_count = 0
    input_count = 0

    async def handle_log(ev: BaseEvent):
        nonlocal log_count
        log_count += 1
    router.subscribe_log(handle_log)

    async def handle_cpu(ev: BaseEvent):
        nonlocal cpu_count
        cpu_count += 1
    router.subscribe_stepping(handle_cpu)

    async def handle_game(ev: BaseEvent):
        nonlocal game_count
        game_count += 1
    router.subscribe_game(handle_game)

    async def handle_input(ev: BaseEvent):
        nonlocal input_count
        input_count += 1
    router.subscribe_input(handle_input)

    await event_handler_man.handle_event(log_ev)
    assert (log_count, cpu_count, game_count, input_count) == (1, 0, 0, 0)
    await event_handler_man.handle_event(cpu_ev)
    assert (log_count, cpu_count, game_count, input_count) == (1, 1, 0, 0)
    await event_handler_man.handle_event(game_ev)
    assert (log_count, cpu_count, game_count, input_count) == (1, 1, 1, 0)
    await event_handler_man.handle_event(input_ev)
    assert (log_count, cpu_count, game_count, input_count) == (1, 1, 1, 1)


async def test_subscribers():
    ticket_man = TicketManager(ticket_length=4)
    event_handler_man = AsyncEventHandlerManager(ticket_man)
    ticket = ticket_man.get_ticket()

    called = False

    async def subscriber(ev: BaseEvent):
        nonlocal called
        called = True

        assert ev.ticket == ticket
    event_handler_man.subscribe(ticket, subscriber)

    event = BaseEvent(event="test_event", ticket=ticket)
    await event_handler_man.handle_event(event)
    assert called

    with pytest.RaisesGroup(RuntimeError):
        # That's unknown ticket
        await event_handler_man.handle_event(event)


async def test_listeners(cpu_ev, game_ev):
    event_handler_man = AsyncEventHandlerManager(TicketManager(ticket_length=4))
    router = Router()
    event_handler_man.include_router(router)

    count = 0
    count_all = 0

    async def listen(ev: BaseEvent):
        nonlocal count
        count += 1
    router.install_listener(CpuResumeEvent, listen)

    async def listen_all(ev: BaseEvent):
        nonlocal count_all
        count_all += 1
    router.install_promiscuous_listener(listen_all)

    await event_handler_man.handle_event(cpu_ev)
    assert (count, count_all) == (1, 1)
    await event_handler_man.handle_event(game_ev)
    assert (count, count_all) == (1, 2)


async def test_combined(log_ev, cpu_ev, game_ev, input_ev):
    ticket_man = TicketManager(ticket_length=4)
    event_handler_man = AsyncEventHandlerManager(ticket_man)
    router = Router()
    event_handler_man.include_router(router)

    log_count = 0
    cpu_count = 0
    game_count = 0
    input_count = 0

    async def handle_log(ev: BaseEvent):
        nonlocal log_count
        log_count += 1
    router.subscribe_log(handle_log)

    async def handle_cpu(ev: BaseEvent):
        nonlocal cpu_count
        cpu_count += 1
    router.subscribe_stepping(handle_cpu)

    async def handle_game(ev: BaseEvent):
        nonlocal game_count
        game_count += 1
    router.subscribe_game(handle_game)

    async def handle_input(ev: BaseEvent):
        nonlocal input_count
        input_count += 1
    router.subscribe_input(handle_input)

    count = 0
    count_all = 0

    async def listen(ev: BaseEvent):
        nonlocal count
        count += 1
    router.install_listener(type(cpu_ev), listen)

    async def listen_all(ev: BaseEvent):
        nonlocal count_all
        count_all += 1
    router.install_promiscuous_listener(listen_all)

    ticket = ticket_man.get_ticket()
    called = False

    async def subscriber(ev: BaseEvent):
        nonlocal called
        called = True

        assert ev.ticket == ticket
    event_handler_man.subscribe(ticket, subscriber)

    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (0, 0, 0, 0, 0, 0)
    await event_handler_man.handle_event(log_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 0, 0, 0, 0, 1)
    await event_handler_man.handle_event(cpu_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 0, 0, 1, 2)
    await event_handler_man.handle_event(game_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 0, 1, 3)
    await event_handler_man.handle_event(input_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 1, 1, 4)

    event = BaseEvent(event="test_event", ticket=ticket)
    assert not called
    await event_handler_man.handle_event(event)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 1, 1, 5)
    assert called


async def test_clearing(log_ev, cpu_ev, game_ev, input_ev):
    ticket_man = TicketManager(ticket_length=4)
    event_handler_man = AsyncEventHandlerManager(ticket_man)
    router = Router()
    event_handler_man.include_router(router)

    log_count = 0
    cpu_count = 0
    game_count = 0
    input_count = 0

    async def handle_log(ev: BaseEvent):
        nonlocal log_count
        log_count += 1

    async def handle_cpu(ev: BaseEvent):
        nonlocal cpu_count
        cpu_count += 1

    async def handle_game(ev: BaseEvent):
        nonlocal game_count
        game_count += 1

    async def handle_input(ev: BaseEvent):
        nonlocal input_count
        input_count += 1

    count = 0
    count_all = 0

    async def listen(ev: BaseEvent):
        nonlocal count
        count += 1

    async def listen_all(ev: BaseEvent):
        nonlocal count_all
        count_all += 1

    router.subscribe_log(handle_log)
    router.subscribe_stepping(handle_cpu)
    router.subscribe_game(handle_game)
    router.subscribe_input(handle_input)
    router.install_listener(type(cpu_ev), listen)
    router.install_promiscuous_listener(listen_all)

    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (0, 0, 0, 0, 0, 0)
    await event_handler_man.handle_event(log_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 0, 0, 0, 0, 1)
    await event_handler_man.handle_event(cpu_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 0, 0, 1, 2)
    await event_handler_man.handle_event(game_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 0, 1, 3)
    await event_handler_man.handle_event(input_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 1, 1, 4)

    event_handler_man.clear()
    router.clear()

    # The values don't change
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 1, 1, 4)
    await event_handler_man.handle_event(log_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 1, 1, 4)
    await event_handler_man.handle_event(cpu_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 1, 1, 4)
    await event_handler_man.handle_event(game_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 1, 1, 4)
    await event_handler_man.handle_event(input_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 1, 1, 4)


async def test_unsubscribe(log_ev, cpu_ev, game_ev, input_ev):
    ticket_man = TicketManager(ticket_length=4)
    event_handler_man = AsyncEventHandlerManager(ticket_man)
    router = Router()
    event_handler_man.include_router(router)

    log_count = 0
    cpu_count = 0
    game_count = 0
    input_count = 0

    async def handle_log(ev: BaseEvent):
        nonlocal log_count
        log_count += 1
        return True

    async def handle_cpu(ev: BaseEvent):
        nonlocal cpu_count
        cpu_count += 1
        return True

    async def handle_game(ev: BaseEvent):
        nonlocal game_count
        game_count += 1
        return True

    async def handle_input(ev: BaseEvent):
        nonlocal input_count
        input_count += 1
        return True

    count = 0
    count_all = 0

    async def listen(ev: BaseEvent):
        nonlocal count
        count += 1
        return True

    async def listen_all(ev: BaseEvent):
        nonlocal count_all
        count_all += 1
        if count_all == 9:
            return True

    router.subscribe_log(handle_log)
    router.subscribe_stepping(handle_cpu)
    router.subscribe_game(handle_game)
    router.subscribe_input(handle_input)
    router.install_listener(type(cpu_ev), listen)
    router.install_promiscuous_listener(listen_all)

    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (0, 0, 0, 0, 0, 0)

    await event_handler_man.handle_event(log_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 0, 0, 0, 0, 1)
    await event_handler_man.handle_event(log_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 0, 0, 0, 0, 2)

    await event_handler_man.handle_event(cpu_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 0, 0, 1, 3)
    await event_handler_man.handle_event(cpu_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 0, 0, 1, 4)

    await event_handler_man.handle_event(game_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 0, 1, 5)
    await event_handler_man.handle_event(game_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 0, 1, 6)

    await event_handler_man.handle_event(input_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 1, 1, 7)
    await event_handler_man.handle_event(input_ev)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 1, 1, 8)

    event = BaseEvent(event="test_event")
    await event_handler_man.handle_event(event)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 1, 1, 9)
    await event_handler_man.handle_event(event)
    assert (log_count, cpu_count, game_count, input_count, count, count_all) == (1, 1, 1, 1, 1, 9)
