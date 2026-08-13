
import pytest

from ppsspp.util.closeable_queue import CloseableQueue, QueueReader
from ppsspp.exceptions.queue_closed_error import QueueClosedError


def test_queue_basic():
    queue = CloseableQueue[int]()
    queue.put(43)
    value = queue.get()
    assert value == 43

    queue.close()
    with pytest.raises(QueueClosedError):
        queue.get()
    with pytest.raises(QueueClosedError):
        queue.put(0)


def test_queue_fifo():
    queue = CloseableQueue[int]()
    queue.put(1)
    queue.put(2)
    queue.put(3)
    assert queue.get() == 1
    assert queue.get() == 2
    assert queue.get() == 3


def test_closing():
    queue = CloseableQueue[int]()
    queue.put(101)
    queue.put(102)
    queue.close()
    queue.close()
    assert queue.get() == 101
    assert queue.get() == 102
    with pytest.raises(QueueClosedError):
        queue.get()
    with pytest.raises(QueueClosedError):
        queue.get()


def test_empty():
    queue = CloseableQueue[int]()
    queue.close()
    with pytest.raises(QueueClosedError):
        queue.get()
    with pytest.raises(QueueClosedError):
        queue.put(0)


def test_queue_reader():
    queue = CloseableQueue[int]()
    queue.put(1)

    reader = QueueReader(queue)
    assert reader.get() == 1
