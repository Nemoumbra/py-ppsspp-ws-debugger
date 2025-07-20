
class BaseEvent:
    __slots__ = ("event", "ticket")

    def __init__(self, event: str):
        self.event = event
        self.ticket: str | None = None
