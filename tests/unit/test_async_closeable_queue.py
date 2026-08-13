
import pytest

from ppsspp.util.async_closeable_queue import AsyncCloseableQueue
from ppsspp.exceptions.queue_closed_error import QueueClosedError


async def test_queue_basic():
    queue = AsyncCloseableQueue[int]()
    await queue.put(43)
    value = await queue.get()
    assert value == 43

    await queue.close()
    with pytest.raises(QueueClosedError):
        await queue.get()
    with pytest.raises(QueueClosedError):
        await queue.put(0)


async def test_queue_fifo():
    queue = AsyncCloseableQueue[int]()
    await queue.put(1)
    await queue.put(2)
    await queue.put(3)
    assert await queue.get() == 1
    assert await queue.get() == 2
    assert await queue.get() == 3


async def test_closing():
    queue = AsyncCloseableQueue[int]()
    await queue.put(101)
    await queue.put(102)
    await queue.close()
    await queue.close()
    assert await queue.get() == 101
    assert await queue.get() == 102
    with pytest.raises(QueueClosedError):
        await queue.get()
    with pytest.raises(QueueClosedError):
        await queue.get()


async def test_empty():
    queue = AsyncCloseableQueue[int]()
    await queue.close()
    with pytest.raises(QueueClosedError):
        await queue.get()
    with pytest.raises(QueueClosedError):
        await queue.put(0)
