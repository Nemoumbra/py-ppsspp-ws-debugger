import json

import asyncio
from asyncio.tasks import Task
from logging import getLogger

from ppsspp.async_connection import AsyncPpssppConnection
from ppsspp.exceptions.connection_terminated import ConnectionTerminated
from ppsspp.exceptions.request_failed_error import RequestFailedError
from ppsspp.model.events.base_event import BaseEvent
from ppsspp.model.events.error_event import ErrorEvent

from ppsspp.model.requests.base_request import BaseRequest
from ppsspp.ppsspp_request import PPSSPPRequest

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

from ppsspp.ticket_manager import TicketManager
from ppsspp.async_event_handler_manager import AsyncEventHandlerManager, AsyncEventHandler
from ppsspp.dispatchers.event_dispatcher import EventDispatcher
from ppsspp.exceptions.event_parse_error import EventParseError
from ppsspp.dispatchers.request_dispatcher import RequestDispatcher

from ppsspp.util.async_closeable_queue import AsyncCloseableQueue
from ppsspp.exceptions.queue_closed_error import QueueClosedError


logger = getLogger("ppsspp.async_session")


async def populate_event_queue(queue: AsyncCloseableQueue[BaseEvent], connection: AsyncPpssppConnection, dispatcher: EventDispatcher):
    logger.debug("'populate_event_queue' started!")
    while True:
        try:
            data = await connection.recv()
            if not isinstance(data, dict):
                logger.error(f"Something weird has happened: got '{data}' from async connection!")
                continue

            event = dispatcher.parse_event(data)
            await queue.put(event)
        except json.JSONDecodeError as e:
            logger.error(e)
        except EventParseError as e:
            logger.error(e)
        except ConnectionTerminated:
            logger.debug("ConnectionTerminated, 'populate_event_queue' returning...")
            return
        except QueueClosedError:
            logger.debug("Queue closed, 'populate_event_queue' returning...")
            return


async def process_events(queue: AsyncCloseableQueue[BaseEvent], event_handler_man: AsyncEventHandlerManager):
    logger.debug("'process_events' started!")
    async with asyncio.TaskGroup() as tg:
        while True:
            try:
                event = await queue.get()
                tg.create_task(event_handler_man.handle_event(event))
            except QueueClosedError:
                logger.debug("Queue closed, 'process_events' returning...")
                return
            except Exception:
                # TODO: this is probably unreachable due to TaskGroup's exception semantics
                logger.exception(f"Process events error")
                continue


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

    def __init__(self):
        self._event_queue = AsyncCloseableQueue[BaseEvent]()
        self._ticket_man = TicketManager(0x8)
        self._event_handler_man = AsyncEventHandlerManager(self._ticket_man)

        event_lookup_table = self._init_parsers()
        self._event_dispatcher = EventDispatcher(event_lookup_table)

        self._request_dispatcher = RequestDispatcher()

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
        # TODO: think about monitoring the state of these tasks
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

        # TODO: maybe cancel them?
        logger.debug("Waiting for producer to join...")
        await self.producer_task
        logger.debug("Producer joined!")
        logger.debug("Waiting for consumer to join...")
        await self.consumer_task
        logger.debug("Consumer joined!")
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

    async def send_request_raw(self, request: PPSSPPRequest, handler: AsyncEventHandler | None = None):
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

    async def execute_unchecked_raw(self, request: PPSSPPRequest) -> BaseEvent:
        """
        The mid-level API for executing the remote PPSSPP requests and acquiring the result.

        Warning! PPSSPP may not respond to certain events at all! This may cause ``execute_unchecked_raw`` to never return!

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

        await self.send_request_raw(request, handler)
        await ppsspp_responded.wait()
        return result

    async def execute_raw(self, request: PPSSPPRequest) -> BaseEvent:
        """
        The mid-level API for executing the remote PPSSPP requests and acquiring the result.
        If PPSSPP responds with the ``ErrorEvent``, ``RequestFailedError`` is raised.

        Warning! PPSSPP may not respond to certain events at all! This may cause ``execute_raw`` to never return!

        May raise ``ConnectionTerminated``.
        :param request: the request
        :return: the event returned by PPSSPP
        """
        result = await self.execute_unchecked_raw(request)
        if isinstance(result, ErrorEvent):
            raise RequestFailedError(result, request)
        return result

    async def send_request(self, request: BaseRequest, handler: AsyncEventHandler | None = None):
        """
        The mid-level API for sending requests to PPSSPP.
        If handler is provided and request contains a ticket, schedules the handler once PPSSPP echoes
        the same ticket in its response. If handler is provided with no ticket, generates a ticket automatically.

        Never provide a ticket without the handler!

        May raise ``ConnectionTerminated``.
        :param request: the request
        :param handler: optional handler to be called once PPSSPP responds to this request
        :return: None
        """
        if handler is None:
            assert request.ticket is None
        else:
            ticket = request.ticket
            if ticket is None:
                ticket = self._ticket_man.get_ticket()
                request.ticket = ticket
            else:
                self._ticket_man.add_custom_ticket(ticket)

            self._event_handler_man.subscribe(ticket, handler)

        raw = self._request_dispatcher.make_request(request)
        await self._connection.send(raw)

    async def execute_unchecked(self, request: BaseRequest) -> BaseEvent:
        """
        The high-level API for executing the remote PPSSPP requests and acquiring the result.

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

    async def execute(self, request: BaseRequest) -> BaseEvent:
        """
        The high-level API for executing the remote PPSSPP requests and acquiring the result.
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
