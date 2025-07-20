from src.ppsspp.model.events.base_event import BaseEvent


class ResumedEvent(BaseEvent):
    __slots__ = ()

    def __init__(self):
        BaseEvent.__init__(self, "cpu.resume")
