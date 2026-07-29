
import json
from threading import Thread

from ppsspp.connection import PpssppConnection
from ppsspp.exceptions.connection_terminated import ConnectionTerminated
from ppsspp.model.events.base_event import BaseEvent

from ppsspp.parsers.detailed_parsers.broadcast_config import BroadcastConfigEventParser
from ppsspp.parsers.detailed_parsers.cpu import CPUEventParser
from ppsspp.parsers.detailed_parsers.game import GameEventParser
from ppsspp.parsers.detailed_parsers.gpu import GPUEventParser
from ppsspp.parsers.detailed_parsers.hle import HLEEventParser
from ppsspp.parsers.detailed_parsers.input import InputEventParser
from ppsspp.parsers.detailed_parsers.log import LogEventParser
from ppsspp.parsers.detailed_parsers.memory import MemoryEventParser
from ppsspp.parsers.detailed_parsers.replay import ReplayEventParser
from ppsspp.parsers.detailed_parsers.version import VersionEventParser

from ppsspp.ppsspp_request import PPSSPPRequest

from ppsspp.ticket_manager import TicketManager
from ppsspp.event_handler_manager import SyncEventHandlerManager, EventHandler
from ppsspp.dispatchers.event_dispatcher import EventDispatcher
from ppsspp.exceptions.event_parse_error import EventParseError
from ppsspp.dispatchers.request_dispatcher import RequestDispatcher

from ppsspp.util.closeable_queue import CloseableQueue
from ppsspp.exceptions.queue_closed_error import QueueClosedError


def populate_event_queue(queue: CloseableQueue[BaseEvent], connection: PpssppConnection, dispatcher: EventDispatcher):
    # TODO: error handling
    while True:
        try:
            data = connection.recv()
            if not isinstance(data, dict):
                continue

            event = dispatcher.parse_event(data)
            queue.put(event)
        except json.JSONDecodeError as e:
            print(e)
        except EventParseError as e:
            print(e)
        except ConnectionTerminated:
            # print("'populate_event_queue' returning...")
            return
        except QueueClosedError:
            # print("'populate_event_queue' returning...")
            return
        # except Exception as e:
        #     print(data)
    pass


def process_events(queue: CloseableQueue[BaseEvent], event_handler_man: SyncEventHandlerManager):
    while True:
        try:
            event = queue.get()
            event_handler_man.handle_event(event)
        except QueueClosedError:
            # print("'process_events' returning...")
            return
        except Exception as e:
            print("Process events error:", e)
            continue
    pass


class Session:
    @staticmethod
    def init_parsers():
        return {
            "broadcast": BroadcastConfigEventParser(),
            "cpu": CPUEventParser(),
            "game": GameEventParser(),
            "gpu": GPUEventParser(),
            "hle": HLEEventParser(),
            "input": InputEventParser(),
            "log": LogEventParser(),
            "memory": MemoryEventParser(),
            "replay": ReplayEventParser(),
            "version": VersionEventParser(),
        }

    def __init__(self):
        self._event_queue = CloseableQueue[BaseEvent]()
        self._ticket_man = TicketManager(0x8)
        self._event_handler_man = SyncEventHandlerManager(self._ticket_man)

        event_lookup_table = self.init_parsers()
        self._event_dispatcher = EventDispatcher(event_lookup_table)

        self._request_dispatcher = RequestDispatcher()

        self.producer_thread = Thread()
        self.consumer_thread = Thread()

        self._connection: PpssppConnection | None = None
        self._running: bool = False

    def run(self, connection: PpssppConnection):
        self.producer_thread = Thread(
            target=populate_event_queue, name="PpssppEventReader",
            args=(self._event_queue, connection, self._event_dispatcher)
        )
        self.consumer_thread = Thread(
            target=process_events, name="PpssppEventHandler",
            args=(self._event_queue, self._event_handler_man)
        )
        self._connection = connection
        self.producer_thread.start()
        self.consumer_thread.start()
        self._running = True

    def stop(self):
        if not self._running:
            return False

        self._event_queue.close()
        self._connection.close()
        self.producer_thread.join()
        # print("Producer joined!")
        self.consumer_thread.join()
        # print("Consumer joined!")
        self._event_handler_man.clear()

        self._connection = None
        return True

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

    def send_request(self, request: PPSSPPRequest, handler: EventHandler | None = None):
        if handler is not None:
            ticket = self._ticket_man.get_ticket()
            request.set_ticket(ticket)
            self._event_handler_man.subscribe(ticket, handler)

        self._connection.send(str(request))
