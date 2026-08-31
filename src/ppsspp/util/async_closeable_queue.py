import asyncio
import collections
from asyncio.queues import Queue, QueueEmpty
from ppsspp.exceptions.queue_closed_error import QueueClosedError

from typing import TypeVar, Generic
T = TypeVar('T')


class _MPSCEvent:
    """
    Multi-producer single-consumer event (simplified ``asyncio.Event``).
    """
    def __init__(self):
        self._waiter = None
        self._value = False

    def set(self):
        """Set the internal flag to true. The coroutine waiting for it to
        become true is awakened. Coroutine that call wait() once the flag is
        true will not block at all.
        """
        if not self._value:
            self._value = True
            fut = self._waiter
            if fut is not None and not fut.done():
                fut.set_result(True)

    def clear(self):
        """Reset the internal flag to false. Subsequently, coroutines calling
        wait() will block until set() is called to set the internal flag
        to true again."""
        self._value = False

    async def wait(self):
        """Block until the internal flag is true.

        If the internal flag is true on entry, return True
        immediately.  Otherwise, block until another coroutine calls
        set() to set the flag to true, then return True.
        """
        if self._value:
            return True

        fut = asyncio.get_event_loop().create_future()
        self._waiter = fut
        try:
            await fut
            return True
        finally:
            self._waiter = None

class AsyncCloseableQueue(Generic[T]):
    """
        Multi-producer, single-consumer unbounded async queue.
        Essentially a closeable ``asyncio.queues.Queue[T]``.
        """

    # Note: Python doesn't support queue shutdown until Python 3.13.
    def __init__(self):
        self._buffer = collections.deque()
        self._modified = _MPSCEvent()
        self._closed = False

    async def put(self, item: T):
        """
        Tries to put an object into the queue. If the queue is closed, raises QueueClosedError.
        :param item: the object to be inserted
        :return:
        """
        if self._closed:
            raise QueueClosedError

        self._buffer.append(item)
        self._modified.set()

    async def get(self) -> T:
        """
        Tries to fetch an item from the queue. If queue is empty and closed, raises ``QueueClosedError``.
        Otherwise, awaits for the item to be inserted.
        :return: the extracted item
        """
        while not self._closed and not self._buffer:
            await self._modified.wait()
            self._modified.clear()
        if self._buffer:
            return self._buffer.popleft()
        raise QueueClosedError

    async def close(self):
        """
        Closes the queue: it won't accept new items anymore. If necessary, the only consumer will be notified.
        :return:
        """
        self._closed = True
        self._modified.set()
