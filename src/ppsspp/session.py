
import json
from threading import Thread
from logging import getLogger

from ppsspp.connection import PpssppConnection
from ppsspp.exceptions.connection_terminated import ConnectionTerminated
from ppsspp.model.events.base_event import BaseEvent
from ppsspp.model.requests.base_request import BaseRequest

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
from ppsspp.dispatchers.event_dispatcher import EventDispatcher
from ppsspp.exceptions.event_parse_error import EventParseError
from ppsspp.dispatchers.request_dispatcher import RequestDispatcher

from ppsspp.util.closeable_queue import CloseableQueue, QueueReader
from ppsspp.exceptions.queue_closed_error import QueueClosedError


logger = getLogger("ppsspp.sync_session")


def populate_event_queue(queue: CloseableQueue[BaseEvent], connection: PpssppConnection, dispatcher: EventDispatcher):
    # TODO: error handling
    logger.debug("'populate_event_queue' started!")
    while True:
        try:
            data = connection.recv()
            if not isinstance(data, dict):
                logger.error(f"Something weird has happened: got '{data}' from async connection!")
                continue

            event = dispatcher.parse_event(data)
            queue.put(event)
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

        event_lookup_table = self.init_parsers()
        self._event_dispatcher = EventDispatcher(event_lookup_table)

        self._request_dispatcher = RequestDispatcher()

        self.producer_thread = Thread()

        self._connection: PpssppConnection | None = None
        self._running: bool = False

    def run(self, connection: PpssppConnection):
        """
        Initiates the PPSSPP debugging session.

        Pre-condition: the call to 'connection.connect' has completed.
        :param connection: the connection to be used by the session
        :return: None
        """
        self.producer_thread = Thread(
            target=populate_event_queue, name="PpssppEventReader",
            args=(self._event_queue, connection, self._event_dispatcher)
        )
        self._connection = connection
        self.producer_thread.start()

        self._running = True

    def stop(self):
        """
        Terminates the PPSSPP debugging session. Automatically closes the connection.
        Keep in mind that this will most likely trigger the 'on_disconnected' handler. Reconnecting is meaningless:
        the internal queue will be closed by then, so the session will shut down nonetheless.
        :return: None
        """
        if not self._running:
            return False

        self._event_queue.close()
        self._connection.close()
        logger.debug("Waiting for producer to join...")
        self.producer_thread.join()
        logger.debug("Producer joined!")

        self._connection = None
        return True

    def get_queue(self) -> QueueReader[BaseEvent]:
        """
        Returns a queue reader object which makes it possible to access the events coming from PPSSPP directly
        :return: the queue reader
        """
        return QueueReader(self._event_queue)

    def send_request_raw(self, request: PPSSPPRequest):
        """
        The low-level API for sending requests to PPSSPP.

        May raise ``ConnectionTerminated``.
        :param request: the request
        :return: None
        """
        self._connection.send(str(request))

    def send_request(self, request: BaseRequest):
        """
        The mid-level API for sending requests to PPSSPP.

        May raise ``ConnectionTerminated``.
        :param request: the request
        :return: None
        """
        raw = self._request_dispatcher.make_request(request)
        self._connection.send(raw)
