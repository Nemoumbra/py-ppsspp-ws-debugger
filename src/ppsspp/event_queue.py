
from queue import SimpleQueue
from src.ppsspp.events.base_event import BaseEvent
from src.ppsspp.exceptions.queue_closed_error import QueueClosedError

class EventQueue:
    def __init__(self):
        self.queue: SimpleQueue[BaseEvent] = SimpleQueue()
        self.closed = False


    def put(self, event: BaseEvent):
        if self.closed:
            raise QueueClosedError

        self.queue.put(event)

    def get(self):
        if not self.closed:
            return self.queue.get()

        # Queue's closed => no one can put new objects into the queue
        if self.queue.empty():
            raise QueueClosedError

        # There's still something, let's return it
        return self.queue.get()

    def close(self):
        self.closed = True