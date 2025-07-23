
from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.model.ppsspp_objects.cpu.register import RegisterCategory


@dataclass(kw_only=True)
class CpuGetRegEvent(BaseEvent):
    category: int
    register: int
    uint_value: int
    float_value: str

@dataclass(kw_only=True)
class CpuSetRegEvent(BaseEvent):
    category: int
    register: int
    uint_value: int
    float_value: str

@dataclass(kw_only=True)
class CpuGetAllRegsEvent(BaseEvent):
    categories: list[RegisterCategory]
