
from queue import SimpleQueue, Empty
from ppsspp.model.events.base_event import BaseEvent
from ppsspp.exceptions.queue_closed_error import QueueClosedError

from typing import TypeVar, Generic
T = TypeVar('T')


class CloseableQueue(Generic[T]):
    """
    Multi-producer, single-consumer unbounded sync queue.
    Essentially a closeable ``queue.SimpleQueue[T]``.
    """

    # Note: Python doesn't support queue shutdown until Python 3.13.
    # And they only added it to 'queue.Queue', which combines the APIs
    # of Queue and WaitGroup => here we have a custom implementation
    def __init__(self):
        self._queue: SimpleQueue[T | None] = SimpleQueue()
        self._closed = False
        self._pill_inserted = False

    def put(self, item: T):
        """
        Tries to put an object into the queue. If the queue is closed, raises QueueClosedError.
        :param item: the object to be inserted
        :return:
        """
        if self._closed:
            raise QueueClosedError

        assert item is not None
        self._queue.put(item)

    def _extract(self, timeout: float | None) -> T | None:
        # If the poison pill wasn't inserted, then block
        if not self._pill_inserted:
            return self._queue.get(True, timeout)
        # Otherwise we know there won't be any more items
        try:
            return self._queue.get_nowait()
        except Empty:
            # Someone called 'get' after getting a poison pill, let's feed them with another pill
            return None

    def get(self, timeout: float | None = None) -> T:
        """
        Tries to fetch an item from the queue. If queue is empty and closed, raises ``QueueClosedError``.
        Otherwise, blocks until a new item is inserted.
        If a timeout is specified, raises ``Empty`` if unable to fetch an item in specified timeout.
        :param timeout: timeout in seconds or None (no timeout)
        :return: the extracted item
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


class QueueReader(Generic[T]):
    """
    A proxy over the ``CloseableQueue`` that only exposes the extraction operations (``get``).
    """
    def __init__(self, queue: CloseableQueue[T]):
        self._queue = queue

    def get(self, timeout: float | None = None) -> T:
        """
        Tries to fetch an item from the queue. If queue is empty and closed, raises ``QueueClosedError``.
        Otherwise, blocks until the item is available.
        If a timeout is specified, raises ``Empty`` if unable to fetch an item in specified timeout.
        :param timeout: timeout in seconds or None (no timeout)
        :return:
        """
        return self._queue.get(timeout)
