import asyncio
from asyncio import TaskGroup
from collections import defaultdict

from ppsspp.model.events.base_event import BaseEvent
from typing import Callable, Awaitable

from ppsspp.model.events.event_groups import (
    kCpuEvents, kInputEvents, kGameEvents, kLoggingEvents, kBroadcastEvents
)
from ppsspp.ticket_manager import TicketManager


EventHandler = Callable[[BaseEvent], None]
AsyncEventHandler = Callable[[BaseEvent], Awaitable]


class SyncEventHandlerManager:
    def __init__(self, ticket_manager: TicketManager):
        self.ticket_manager = ticket_manager

        self._log_handlers: list[EventHandler] = []
        self._stepping_handlers: list[EventHandler] = []
        self._game_handlers: list[EventHandler] = []
        self._input_handlers: list[EventHandler] = []

        self._subscribers: dict[str, EventHandler] = {}

    def subscribe(self, ticket: str, handler: EventHandler):
        self._subscribers[ticket] = handler

    def handle_event(self, event: BaseEvent):
        self._notify_listeners(event)
        self._report_to_subscriber(event)

    def _notify_listeners(self, event: BaseEvent):
        event_type = type(event)
        if event_type in kLoggingEvents:
            self._handle_log(event)
        elif event_type in kCpuEvents:
            self._handle_stepping(event)
        elif event_type in kGameEvents:
            self._handle_game(event)
        elif event_type in kInputEvents:
            self._handle_input(event)

    def _report_to_subscriber(self, event: BaseEvent):
        # Of course, there may not be a subscriber (for instance, if that's a Log event)
        ticket = event.ticket
        if ticket is None:
            return

        # That shouldn't happen, but let's make a check anyway
        if ticket not in self._subscribers:
            raise RuntimeError(f"Unknown ticket {ticket}")

        # Run the callback
        self._subscribers[ticket](event)

        # The ticket has been dealt with!
        self._subscribers.pop(ticket)
        self.ticket_manager.finalize_ticket(ticket)
        pass

    def subscribe_log(self, event_handler: EventHandler):
        self._log_handlers.append(event_handler)

    def subscribe_stepping(self, event_handler: EventHandler):
        self._stepping_handlers.append(event_handler)

    def subscribe_game(self, event_handler: EventHandler):
        self._game_handlers.append(event_handler)

    def subscribe_input(self, event_handler: EventHandler):
        self._input_handlers.append(event_handler)

    def _handle_log(self, event: BaseEvent):
        for handler in self._log_handlers:
            handler(event)

    def _handle_stepping(self, event: BaseEvent):
        for handler in self._stepping_handlers:
            handler(event)

    def _handle_game(self, event: BaseEvent):
        for handler in self._game_handlers:
            handler(event)

    def _handle_input(self, event: BaseEvent):
        for handler in self._input_handlers:
            handler(event)

    def clear(self):
        self._log_handlers.clear()
        self._stepping_handlers.clear()
        self._input_handlers.clear()
        self._game_handlers.clear()
        self._subscribers.clear()


async def run_handler(event: BaseEvent, handler: AsyncEventHandler, all_handlers: list[AsyncEventHandler]):
    result = await handler(event)
    if result:
        all_handlers.remove(handler)


async def run_handlers(event: BaseEvent, handlers: list[AsyncEventHandler]):
    async with TaskGroup() as tg:
        for handler in handlers:
            tg.create_task(run_handler(event, handler, handlers))


class AsyncEventHandlerManager:
    def __init__(self, ticket_manager: TicketManager):
        self.ticket_manager = ticket_manager

        self._log_handlers: list[AsyncEventHandler] = []
        self._stepping_handlers: list[AsyncEventHandler] = []
        self._game_handlers: list[AsyncEventHandler] = []
        self._input_handlers: list[AsyncEventHandler] = []

        self._subscribers: dict[str, AsyncEventHandler] = {}

        self._listeners: dict[type[BaseEvent], list[AsyncEventHandler]] = defaultdict(list)
        self._promiscuous_listeners: list[AsyncEventHandler] = []

    def subscribe(self, ticket: str, handler: AsyncEventHandler):
        self._subscribers[ticket] = handler

    async def handle_event(self, event: BaseEvent):
        # TODO: should we use the caller's TaskGroup?
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self._report_to_listeners(event))
            if type(event) in kBroadcastEvents:
                tg.create_task(self._on_broadcast(event))
            tg.create_task(self._report_to_subscriber(event))

    async def _on_broadcast(self, event: BaseEvent):
        event_type = type(event)
        if event_type in kLoggingEvents:
            await run_handlers(event, self._log_handlers)
        elif event_type in kCpuEvents:
            await run_handlers(event, self._stepping_handlers)
        elif event_type in kGameEvents:
            await run_handlers(event, self._game_handlers)
        elif event_type in kInputEvents:
            await run_handlers(event, self._input_handlers)

    async def _report_to_subscriber(self, event: BaseEvent):
        # Of course, there may not be a subscriber (for instance, if that's a Log event)
        ticket = event.ticket
        if ticket is None:
            return

        # That shouldn't happen, but let's make a check anyway
        if ticket not in self._subscribers:
            raise RuntimeError(f"Unknown ticket {ticket}")

        # Run the callback
        await self._subscribers[ticket](event)

        # The ticket has been dealt with!
        self._subscribers.pop(ticket)
        self.ticket_manager.finalize_ticket(ticket)
        pass

    async def _report_to_listeners(self, event: BaseEvent):
        exact_listeners = self._listeners[type(event)]
        async with asyncio.TaskGroup() as tg:
            for listener in exact_listeners:
                tg.create_task(run_handler(event, listener, exact_listeners))
            for listener in self._promiscuous_listeners:
                tg.create_task(run_handler(event, listener, self._promiscuous_listeners))

    def subscribe_log(self, event_handler: AsyncEventHandler):
        self._log_handlers.append(event_handler)

    def subscribe_stepping(self, event_handler: AsyncEventHandler):
        self._stepping_handlers.append(event_handler)

    def subscribe_game(self, event_handler: AsyncEventHandler):
        self._game_handlers.append(event_handler)

    def subscribe_input(self, event_handler: AsyncEventHandler):
        self._input_handlers.append(event_handler)

    def install_listener(self, target: type[BaseEvent], handler: AsyncEventHandler):
        self._listeners[target].append(handler)

    def install_promiscuous_listener(self, handler: AsyncEventHandler):
        self._promiscuous_listeners.append(handler)

    def clear(self):
        self._log_handlers.clear()
        self._stepping_handlers.clear()
        self._input_handlers.clear()
        self._game_handlers.clear()
        self._subscribers.clear()
        self._listeners.clear()
        self._promiscuous_listeners.clear()
