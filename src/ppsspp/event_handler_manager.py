
from src.ppsspp.model.events.base_event import BaseEvent
from typing import Callable

from src.ppsspp.model.events.event_groups import (
    kCpuEvents, kInputEvents, kGameEvents, kLoggingEvents
)
from src.ppsspp.ticket_manager import TicketManager


EventHandler = Callable[[BaseEvent], None]

class EventHandlerManager:
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
