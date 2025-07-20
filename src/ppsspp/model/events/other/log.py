from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.model.ppsspp_objects.logs.log import PPSSPPLog


class LogEvent(BaseEvent):
    __slots__ = "log"

    def __init__(self):
        BaseEvent.__init__(self, "log")
        self.log = PPSSPPLog()
