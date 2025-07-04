
import json
from threading import Thread

from src.ppsspp.events.base_event import BaseEvent
from src.ppsspp.connection import PpssppConnection
from src.ppsspp.parsers.detailed_parsers.cpu.cpu_event_parser import CPUEventParser
from src.ppsspp.parsers.detailed_parsers.game.game_event_parser import GameEventParser
from src.ppsspp.parsers.detailed_parsers.input.input_event_parser import InputEventParser
from src.ppsspp.parsers.detailed_parsers.log.log_event_parser import LogEventParser
from src.ppsspp.parsers.detailed_parsers.version.version_event_parser import VersionEventParser
from src.ppsspp.requests.request_builders.input.input_request_builder import InputRequestBuilder
from src.ppsspp.requests.request_builders.version.version_request_builder import VersionRequestBuilder

from src.ppsspp.ticket_manager import TicketManager
from src.ppsspp.event_handler_manager import EventHandlerManager, EventHandler
from src.ppsspp.parsers.event_dispatcher import EventDispatcher
from src.ppsspp.exceptions.event_parse_error import EventParseError
from src.ppsspp.requests.request_dispatcher import RequestDispatcher

from src.ppsspp.event_queue import EventQueue
from src.ppsspp.exceptions.queue_closed_error import QueueClosedError


def populate_event_queue(queue: EventQueue, connection: PpssppConnection, dispatcher: EventDispatcher):
    # TODO: error handling
    while True:
        try:
            data = connection.recv()
            if not isinstance(data, dict):
                continue

            event = dispatcher.parse_event(data)
            queue.put(event)
        except json.JSONDecodeError as e:
            continue
        except EventParseError as e:
            continue
        except QueueClosedError:
            return
    pass

def process_events(queue: EventQueue, event_handler_man: EventHandlerManager):
    while True:
        try:
            event = queue.get()
            event_handler_man.handle_event(event)
        except QueueClosedError:
            return
    pass

class Session:
    @staticmethod
    def init_parsers():
        return {
            "log": LogEventParser(),
            "input": InputEventParser(),
            "version": VersionEventParser(),
            "cpu": CPUEventParser(),
            "game": GameEventParser(),
        }

    @staticmethod
    def init_builders():
        return {
            "version": VersionRequestBuilder(),
            "input": InputRequestBuilder(),
        }

    def __init__(self):
        self._event_queue: EventQueue = EventQueue()
        self._ticket_man: TicketManager = TicketManager(0x8)
        self._event_handler_man: EventHandlerManager = EventHandlerManager(self)

        event_lookup_table = self.init_parsers()
        self._event_dispatcher: EventDispatcher = EventDispatcher(event_lookup_table)

        request_lookup_table = self.init_builders()
        self._request_dispatcher: RequestDispatcher = RequestDispatcher(request_lookup_table)

        self.producer_thread: Thread = Thread()
        self.consumer_thread: Thread = Thread()


    def Run(self, connection: PpssppConnection):
        self.producer_thread = Thread(
            target=populate_event_queue, name="PpssppEventReader",
            args=(self._event_queue, connection, self._event_dispatcher)
        )
        self.consumer_thread = Thread(
            target=process_events, name="PpssppEventHandler",
            args=(self._event_queue, self._event_handler_man)
        )

        self.producer_thread.start()
        self.consumer_thread.start()

    def Stop(self):
        self._event_queue.close()
        self.producer_thread.join()
        self.consumer_thread.join()
        self._event_handler_man.clear()


    def log_handler(self):
        def decorator(handler_func: EventHandler):
            self._event_handler_man.subscribe_log(handler_func)
            return handler_func
        return decorator

    def stepping_handler(self):
        def decorator(handler_func: EventHandler):
            self._event_handler_man.subscribe_stepping(handler_func)
            return handler_func
        return decorator

    def game_handler(self):
        def decorator(handler_func: EventHandler):
            self._event_handler_man.subscribe_game(handler_func)
            return handler_func
        return decorator

    def input_handler(self):
        def decorator(handler_func: EventHandler):
            self._event_handler_man.subscribe_input(handler_func)
            return handler_func
        return decorator