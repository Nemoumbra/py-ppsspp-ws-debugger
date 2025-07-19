
from queue import SimpleQueue
from src.ppsspp.events.base_event import BaseEvent
from src.ppsspp.exceptions.queue_closed_error import QueueClosedError

class EventQueue:
    def __init__(self):
        self.queue: SimpleQueue[BaseEvent | None] = SimpleQueue()
        self.closed = False

    def put(self, event: BaseEvent):
        if self.closed:
            raise QueueClosedError

        self.queue.put(event)

    def get(self):
        item = self.queue.get()
        if item is None:
            # Poison pill
            raise QueueClosedError

        return item

    def close(self):
        self.closed = True
        # Poison pill
        self.queue.put(None)
