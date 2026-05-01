
from queue import SimpleQueue, Empty
from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.exceptions.queue_closed_error import QueueClosedError


class EventQueue:
    """
    Multi-producer, single-consumer unbounded queue for PPSSPP events
    """

    def __init__(self):
        self._queue: SimpleQueue[BaseEvent | None] = SimpleQueue()
        self._closed = False
        self._pill_inserted = False

    def put(self, event: BaseEvent):
        if self._closed:
            raise QueueClosedError

        self._queue.put(event)

    def _extract(self) -> BaseEvent | None:
        # If the poison pill wasn't inserted, then block
        if not self._pill_inserted:
            return self._queue.get()
        # Otherwise we know there won't be any more items
        try:
            return self._queue.get_nowait()
        except Empty:
            # Someone called 'get' after getting a poison pill, let's feed them with another pill
            return None

    def get(self):
        item = self._extract()
        if item is None:
            # Poison pill
            raise QueueClosedError

        return item

    def close(self):
        self._closed = True
        if self._pill_inserted:
            return

        # Poison pill
        self._queue.put(None)
        self._pill_inserted = True


class EventQueueReader:
    def __init__(self, queue: EventQueue):
        self._queue = queue

    def get(self):
        return self._queue.get()
