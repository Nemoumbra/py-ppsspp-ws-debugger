
from asyncio.queues import Queue, QueueEmpty
from ppsspp.model.events.base_event import BaseEvent
from ppsspp.exceptions.queue_closed_error import QueueClosedError

from typing import TypeVar, Generic
T = TypeVar('T')


class AsyncCloseableQueue(Generic[T]):
    """
    Multi-producer, single-consumer unbounded async queue.
    Essentially a closeable ``asyncio.queues.Queue[T]``.
    """

    # Note: Python doesn't support queue shutdown until Python 3.13.
    def __init__(self):
        self._queue: Queue[T | None] = Queue(maxsize=0)
        self._closed = False
        self._pill_inserted = False

    async def put(self, item: T):
        """
        Tries to put an object into the queue. If the queue is closed, raises QueueClosedError.
        :param item: the object to be inserted
        :return:
        """
        if self._closed:
            raise QueueClosedError

        assert item is not None
        await self._queue.put(item)

    async def _extract(self) -> T | None:
        # If the poison pill wasn't inserted, then wait
        if not self._pill_inserted:
            return await self._queue.get()
        # Otherwise we know there won't be any more items
        try:
            return self._queue.get_nowait()
        except QueueEmpty:
            # Someone called 'get' after getting a poison pill, let's feed them with another pill
            return None

    async def get(self) -> T:
        """
        Tries to fetch an item from the queue. If queue is empty and closed, raises ``QueueClosedError``.
        Otherwise, awaits for the item to be inserted.
        :return: the extracted item
        """
        item = await self._extract()
        if item is None:
            # Poison pill
            raise QueueClosedError

        return item

    async def close(self):
        """
        Closes the queue: it won't accept new items anymore. If necessary, the only consumer will be notified.
        :return:
        """
        self._closed = True
        if self._pill_inserted:
            return

        # Poison pill
        await self._queue.put(None)
        self._pill_inserted = True
