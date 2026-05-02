
import json

import asyncio
from asyncio.tasks import Task

from src.ppsspp.async_connection import AsyncPpssppConnection
from src.ppsspp.exceptions.connection_terminated import ConnectionTerminated

from src.ppsspp.parsers.detailed_parsers.broadcast_config import BroadcastConfigEventParser
from src.ppsspp.parsers.detailed_parsers.cpu import CPUEventParser
from src.ppsspp.parsers.detailed_parsers.game import GameEventParser
from src.ppsspp.parsers.detailed_parsers.gpu import GPUEventParser
from src.ppsspp.parsers.detailed_parsers.hle import HLEEventParser
from src.ppsspp.parsers.detailed_parsers.input import InputEventParser
from src.ppsspp.parsers.detailed_parsers.log import LogEventParser
from src.ppsspp.parsers.detailed_parsers.memory import MemoryEventParser
from src.ppsspp.parsers.detailed_parsers.replay import ReplayEventParser
from src.ppsspp.parsers.detailed_parsers.version import VersionEventParser

from src.ppsspp.ppsspp_request import PPSSPPRequest
from src.ppsspp.requests.request_builders.input.input_request_builder import InputRequestBuilder
from src.ppsspp.requests.request_builders.version.version_request_builder import VersionRequestBuilder

from src.ppsspp.ticket_manager import TicketManager
from src.ppsspp.event_handler_manager import AsyncEventHandlerManager, AsyncEventHandler
from src.ppsspp.parsers.event_dispatcher import EventDispatcher
from src.ppsspp.exceptions.event_parse_error import EventParseError
from src.ppsspp.requests.request_dispatcher import RequestDispatcher

from src.ppsspp.async_event_queue import AsyncEventQueue
from src.ppsspp.exceptions.queue_closed_error import QueueClosedError


async def populate_event_queue(queue: AsyncEventQueue, connection: AsyncPpssppConnection, dispatcher: EventDispatcher):
    # TODO: error handling
    while True:
        try:
            data = await connection.recv()
            if not isinstance(data, dict):
                continue

            event = dispatcher.parse_event(data)
            await queue.put(event)
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

async def process_events(queue: AsyncEventQueue, event_handler_man: AsyncEventHandlerManager):
    while True:
        try:
            event = await queue.get()
            await event_handler_man.handle_event(event)
        except QueueClosedError:
            # print("'process_events' returning...")
            return
        except Exception as e:
            print("Process events error:", e)
            continue
    pass

class AsyncSession:
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

    @staticmethod
    def init_builders():
        return {
            "version": VersionRequestBuilder(),
            "input": InputRequestBuilder(),
        }

    def __init__(self):
        self._event_queue: AsyncEventQueue = AsyncEventQueue()
        self._ticket_man: TicketManager = TicketManager(0x8)
        self._event_handler_man: AsyncEventHandlerManager = AsyncEventHandlerManager(self._ticket_man)

        event_lookup_table = self.init_parsers()
        self._event_dispatcher: EventDispatcher = EventDispatcher(event_lookup_table)

        request_lookup_table = self.init_builders()
        self._request_dispatcher: RequestDispatcher = RequestDispatcher(request_lookup_table)

        self.producer_task: Task | None = None
        self.consumer_task: Task | None = None

        self._connection: AsyncPpssppConnection | None = None
        self._running: bool = False

    async def Run(self, connection: AsyncPpssppConnection):
        self.producer_task = asyncio.create_task(
            populate_event_queue(self._event_queue, connection, self._event_dispatcher), name="PpssppEventReader"
        )
        self.consumer_task = asyncio.create_task(
            process_events(self._event_queue, self._event_handler_man), name="PpssppEventHandler"
        )
        self._connection = connection
        self._running = True

    async def Stop(self):
        if not self._running:
            return False

        await self._event_queue.close()
        await self._connection.close()

        # TODO
        await self.producer_task
        # print("Producer joined!")
        await self.consumer_task
        # print("Consumer joined!")
        self._event_handler_man.clear()

        self._connection = None
        return True

    def log_handler(self):
        def decorator(handler_func: AsyncEventHandler):
            self._event_handler_man.subscribe_log(handler_func)
            return handler_func
        return decorator

    def stepping_handler(self):
        def decorator(handler_func: AsyncEventHandler):
            self._event_handler_man.subscribe_stepping(handler_func)
            return handler_func
        return decorator

    def game_handler(self):
        def decorator(handler_func: AsyncEventHandler):
            self._event_handler_man.subscribe_game(handler_func)
            return handler_func
        return decorator

    def input_handler(self):
        def decorator(handler_func: AsyncEventHandler):
            self._event_handler_man.subscribe_input(handler_func)
            return handler_func
        return decorator

    async def send_request(self, request: PPSSPPRequest, handler: AsyncEventHandler | None = None):
        if handler is not None:
            ticket = self._ticket_man.get_ticket()
            request.set_ticket(ticket)
            await self._event_handler_man.subscribe(ticket, handler)

        await self._connection.send(str(request))
