
from dataclasses import dataclass

from ppsspp.model.events.base_event import BaseEvent
from ppsspp.model.ppsspp_objects.logs.log_level import LogLevel


@dataclass(kw_only=True)
class LogEvent(BaseEvent):
    timestamp: str
    header: str
    message: str
    level: LogLevel
    channel: str
