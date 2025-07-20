
from src.ppsspp.model.ppsspp_objects.logs.log_level import LogLevel
from src.ppsspp.model.events.base_event import BaseEvent

from dataclasses import dataclass

kErrorEvent = "error"

@dataclass(kw_only=True)
class ErrorEvent(BaseEvent):
    message: str
    level: int
    # TODO: implement LogLevel

