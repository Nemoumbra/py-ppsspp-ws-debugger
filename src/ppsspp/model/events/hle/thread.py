
from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.model.ppsspp_objects.hle.thread import ThreadInfo


@dataclass(kw_only=True)
class HleThreadListEvent(BaseEvent):
    threads: list[ThreadInfo]

@dataclass(kw_only=True)
class HleThreadWakeEvent(BaseEvent):
    thread: int
    status: str

@dataclass(kw_only=True)
class HleThreadStopEvent(BaseEvent):
    thread: int
    status: str
