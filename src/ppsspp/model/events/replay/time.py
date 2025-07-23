
from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent


@dataclass(kw_only=True)
class ReplayTimeGetEvent(BaseEvent):
    value: int

@dataclass(kw_only=True)
class ReplayTimeSetEvent(BaseEvent):
    pass
