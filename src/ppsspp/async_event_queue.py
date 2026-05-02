
from asyncio.queues import Queue, QueueEmpty
from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.exceptions.queue_closed_error import QueueClosedError

class AsyncEventQueue:
    """
    Multi-producer, single-consumer unbounded async queue for PPSSPP events.
    Essentially a closeable ``asyncio.queues.Queue[BaseEvent]``.
    """

    # Note: Python doesn't support queue shutdown until Python 3.13.
    def __init__(self):
        self._queue: Queue[BaseEvent | None] = Queue(maxsize=0)
        self._closed = False
        self._pill_inserted = False

    async def put(self, event: BaseEvent):
        """
        Tries to put an event into the queue. If the queue is closed, raises QueueClosedError.
        :param event: the item to be inserted
        :return:
        """
        if self._closed:
            raise QueueClosedError

        assert event is not None
        await self._queue.put(event)

    async def _extract(self) -> BaseEvent | None:
        # If the poison pill wasn't inserted, then wait
        if not self._pill_inserted:
            return await self._queue.get()
        # Otherwise we know there won't be any more items
        try:
            return self._queue.get_nowait()
        except QueueEmpty:
            # Someone called 'get' after getting a poison pill, let's feed them with another pill
            return None

    async def get(self) -> BaseEvent:
        """
        Tries to fetch an event from the queue. If queue is empty and closed, raises ``QueueClosedError``.
        Otherwise, awaits for the event to be inserted.
        :return:
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
