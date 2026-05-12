import json

import asyncio
from asyncio.tasks import Task

from ppsspp.async_connection import AsyncPpssppConnection
from ppsspp.exceptions.connection_terminated import ConnectionTerminated
from ppsspp.exceptions.request_failed_error import RequestFailedError
from ppsspp.model.events.base_event import BaseEvent
from ppsspp.model.events.error_event import ErrorEvent

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
from ppsspp.event_handler_manager import AsyncEventHandlerManager, AsyncEventHandler
from ppsspp.parsers.event_dispatcher import EventDispatcher
from ppsspp.exceptions.event_parse_error import EventParseError
from ppsspp.requests.request_dispatcher import RequestDispatcher

from ppsspp.async_event_queue import AsyncEventQueue
from ppsspp.exceptions.queue_closed_error import QueueClosedError


async def populate_event_queue(queue: AsyncEventQueue, connection: AsyncPpssppConnection, dispatcher: EventDispatcher):
    # TODO: error handling
    while True:
        try:
            data = await connection.recv()
            if not isinstance(data, dict):
                print(f"Something weird has happened: got '{data}' from async connection!")
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
    async with asyncio.TaskGroup() as tg:
        while True:
            try:
                event = await queue.get()
                tg.create_task(event_handler_man.handle_event(event))
            except QueueClosedError:
                # print("'process_events' returning...")
                return
            except Exception as e:
                print("Process events error:", e)
                continue
    pass


class AsyncSession:
    @staticmethod
    def _init_parsers():
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
    def _init_builders():
        return {
            "version": VersionRequestBuilder(),
            "input": InputRequestBuilder(),
        }

    def __init__(self):
        self._event_queue: AsyncEventQueue = AsyncEventQueue()
        self._ticket_man: TicketManager = TicketManager(0x8)
        self._event_handler_man: AsyncEventHandlerManager = AsyncEventHandlerManager(self._ticket_man)

        event_lookup_table = self._init_parsers()
        self._event_dispatcher: EventDispatcher = EventDispatcher(event_lookup_table)

        request_lookup_table = self._init_builders()
        self._request_dispatcher: RequestDispatcher = RequestDispatcher(request_lookup_table)

        self.producer_task: Task | None = None
        self.consumer_task: Task | None = None

        self._connection: AsyncPpssppConnection | None = None
        self._running: bool = False

    async def run(self, connection: AsyncPpssppConnection):
        """
        Initiates the PPSSPP debugging session.

        Pre-condition: the call to 'connection.connect' has completed.
        :param connection: the connection to be used by the session
        :return: None
        """
        self.producer_task = asyncio.create_task(
            populate_event_queue(self._event_queue, connection, self._event_dispatcher), name="PpssppEventReader"
        )
        self.consumer_task = asyncio.create_task(
            process_events(self._event_queue, self._event_handler_man), name="PpssppEventHandler"
        )
        self._connection = connection
        self._running = True

    async def stop(self):
        """
        Terminates the PPSSPP debugging session. Automatically closes the connection.
        Keep in mind that this will most likely trigger the 'on_disconnected' handler. Reconnecting is meaningless:
        the internal queue will be closed by then, so the session will shut down nonetheless.
        :return: None
        """
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

    def listen_for(self, target: type[BaseEvent] | None):
        """
        Installs a listener for all incoming events or a particular event
        :param target: pass the type of the event or ``None`` to listen for all events
        :return: the original function
        """
        def decorator(handler_func: AsyncEventHandler):
            if target is None:
                self._event_handler_man.install_promiscuous_listener(handler_func)
            else:
                self._event_handler_man.install_listener(target, handler_func)
            return handler_func

        return decorator

    async def send_request(self, request: PPSSPPRequest, handler: AsyncEventHandler | None = None):
        """
        The low-level API for sending requests to PPSSPP.
        If handler is provided and request contains a ticket, schedules the handler once PPSSPP echoes
        the same ticket in its response. If handler is provided with no ticket, generates a ticket automatically.

        Never provide a ticket without the handler!

        May raise ``ConnectionTerminated``.
        :param request: the request
        :param handler: optional handler to be called once PPSSPP responds to this request
        :return: None
        """
        if handler is None:
            assert request.get_ticket() is None
        else:
            ticket = request.get_ticket()
            if ticket is None:
                ticket = self._ticket_man.get_ticket()
                request.set_ticket(ticket)
            else:
                self._ticket_man.add_custom_ticket(ticket)

            self._event_handler_man.subscribe(ticket, handler)

        await self._connection.send(str(request))

    async def execute_unchecked(self, request: PPSSPPRequest) -> BaseEvent:
        """
        The mid-level API for executing the remote PPSSPP requests and acquiring the result.

        Warning! PPSSPP may not respond to certain events at all! This may cause ``execute_unchecked`` to never return!

        May raise ``ConnectionTerminated``.
        :param request: the request
        :return: the event returned by PPSSPP
        """
        ppsspp_responded = asyncio.Event()
        result: BaseEvent

        async def handler(event: BaseEvent):
            nonlocal result, ppsspp_responded
            result = event
            ppsspp_responded.set()

        await self.send_request(request, handler)
        await ppsspp_responded.wait()
        return result

    async def execute(self, request: PPSSPPRequest) -> BaseEvent:
        """
        The mid-level API for executing the remote PPSSPP requests and acquiring the result.
        If PPSSPP responds with the ``ErrorEvent``, ``RequestFailedError`` is raised.

        Warning! PPSSPP may not respond to certain events at all! This may cause ``execute`` to never return!

        May raise ``ConnectionTerminated``.
        :param request: the request
        :return: the event returned by PPSSPP
        """
        result = await self.execute_unchecked(request)
        if isinstance(result, ErrorEvent):
            raise RequestFailedError(result, request)
        return result
