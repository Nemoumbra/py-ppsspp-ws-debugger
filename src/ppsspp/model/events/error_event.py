from ppsspp.model.ppsspp_objects.logs.log_level import LogLevel
from ppsspp.model.events.base_event import BaseEvent

from dataclasses import dataclass

kErrorEvent = "error"


@dataclass(kw_only=True)
class ErrorEvent(BaseEvent):
    message: str
    level: LogLevel  # However, it can't really be anything other than LogLevel.ERROR as of now
