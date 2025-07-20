
from src.ppsspp.model.ppsspp_objects.logs.log_level import LogLevel
from src.ppsspp.model.events.base_event import BaseEvent


kErrorEvent = "error"

class ErrorEvent(BaseEvent):
    __slots__ = ("message", "level")

    def __init__(self):
        BaseEvent.__init__(self, kErrorEvent)
        self.message = ""
        self.level: LogLevel = LogLevel.notice

    def to_dict(self):
        res = {
            "event": kErrorEvent,
            "message": self.message,
            "level": self.level.value
        }
        if self.ticket is not None:
            res["ticket"] = self.ticket
        return res

    def from_dict(self, dictionary: dict):
        try:
            if dictionary["event"] != kErrorEvent:
                raise ValueError("The event is not an error")
            self.message = dictionary["message"]
            self.level = LogLevel(dictionary["level"])  # may throw ValueError
            self.ticket = dictionary.get("ticket")
        except KeyError as e:
            raise ValueError("Error event missing parameter", e) from None
