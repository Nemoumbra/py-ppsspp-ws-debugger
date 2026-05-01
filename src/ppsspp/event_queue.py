
from queue import SimpleQueue, Empty
from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.exceptions.queue_closed_error import QueueClosedError


class EventQueue:
    """
    Multi-producer, single-consumer unbounded queue for PPSSPP events.
    Essentially a closeable ``queue.SimpleQueue[BaseEvent]``.
    """

    # Note: Python doesn't support queue shutdown until Python 3.13.
    # And they only added it to 'queue.Queue', which combines the APIs of Queue and WaitGroup =>
    # => here we have a custom implementation
    def __init__(self):
        self._queue: SimpleQueue[BaseEvent | None] = SimpleQueue()
        self._closed = False
        self._pill_inserted = False

    def put(self, event: BaseEvent):
        """
        Tries to put an event into the queue. If the queue is closed, raises QueueClosedError.
        :param event: the item to be inserted
        :return:
        """
        if self._closed:
            raise QueueClosedError

        assert event is not None
        self._queue.put(event)

    def _extract(self, timeout: float | None) -> BaseEvent | None:
        # If the poison pill wasn't inserted, then block
        if not self._pill_inserted:
            return self._queue.get(True, timeout)
        # Otherwise we know there won't be any more items
        try:
            return self._queue.get_nowait()
        except Empty:
            # Someone called 'get' after getting a poison pill, let's feed them with another pill
            return None

    def get(self, timeout: float | None = None) -> BaseEvent:
        """
        Tries to fetch an event from the queue. If queue is empty and closed, raises ``QueueClosedError``.
        Otherwise, blocks until the event is available.
        If a timeout is specified, raises ``Empty`` if unable to fetch an event in specified timeout.
        :param timeout: timeout in seconds or None (no timeout)
        :return:
        """
        item = self._extract(timeout)
        if item is None:
            # Poison pill
            raise QueueClosedError

        return item

    def close(self):
        """
        Closes the queue: it won't accept new items anymore. If necessary, the only consumer will be notified.
        :return:
        """
        self._closed = True
        if self._pill_inserted:
            return

        # Poison pill
        self._queue.put(None)
        self._pill_inserted = True


class EventQueueReader:
    """
    A proxy over the ``EventQueue`` that only exposes the extraction operations (``get``).
    """
    def __init__(self, queue: EventQueue):
        self._queue = queue

    def get(self, timeout: float | None = None):
        """
        Tries to fetch an event from the queue. If queue is empty and closed, raises ``QueueClosedError``.
        Otherwise, blocks until the event is available.
        If a timeout is specified, raises ``Empty`` if unable to fetch an event in specified timeout.
        :param timeout: timeout in seconds or None (no timeout)
        :return:
        """
        return self._queue.get(timeout)
