
from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent


@dataclass(kw_only=True)
class CpuSteppingEvent(BaseEvent):
    pc: int
    ticks: float
    reason: str | None = None
    related_address: int | None = None


@dataclass(kw_only=True)
class CpuResumeEvent(BaseEvent):
    pass


@dataclass(kw_only=True)
class CpuStatusEvent(BaseEvent):
    stepping: bool
    paused: bool
    pc: int
    ticks: float


@dataclass(kw_only=True)
class CpuEvaluateEvent(BaseEvent):
    uint_value: int
    float_value: str
