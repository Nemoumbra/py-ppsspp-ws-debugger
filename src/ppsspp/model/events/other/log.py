
from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent


@dataclass(kw_only=True)
class LogEvent(BaseEvent):
    timestamp: str
    header: str
    message: str
    level: int
    channel: str
