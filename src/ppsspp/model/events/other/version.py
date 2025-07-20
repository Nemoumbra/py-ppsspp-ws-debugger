from src.ppsspp.model.events.base_event import BaseEvent


class VersionEvent(BaseEvent):
    __slots__ = ("name", "version")

    def __init__(self):
        BaseEvent.__init__(self, "version")
        self.name: str = ""
        self.version: str = ""
