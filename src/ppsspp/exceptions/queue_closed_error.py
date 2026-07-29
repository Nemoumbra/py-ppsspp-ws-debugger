
class QueueClosedError(Exception):
    def __init__(self):
        super().__init__("Queue was closed")
