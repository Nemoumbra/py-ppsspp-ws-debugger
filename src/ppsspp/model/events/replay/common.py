
from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent

@dataclass(kw_only=True)
class ReplayBeginEvent(BaseEvent):
    pass

@dataclass(kw_only=True)
class ReplayAbortEvent(BaseEvent):
    pass

@dataclass(kw_only=True)
class ReplayFlushEvent(BaseEvent):
    version: int
    base64: str

@dataclass(kw_only=True)
class ReplayExecuteEvent(BaseEvent):
    pass

@dataclass(kw_only=True)
class ReplayStatusEvent(BaseEvent):
    executing: bool
    saving: bool
