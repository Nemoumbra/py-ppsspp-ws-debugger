
from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.model.ppsspp_objects.breakpoints.cpu_breakpoint import CpuBreakpoint


@dataclass(kw_only=True)
class CpuBreakpointAddEvent(BaseEvent):
    pass

@dataclass(kw_only=True)
class CpuBreakpointUpdateEvent(BaseEvent):
    pass

@dataclass(kw_only=True)
class CpuBreakpointRemoveEvent(BaseEvent):
    pass


@dataclass(kw_only=True)
class CpuBreakpointListEvent(BaseEvent):
    breakpoints: list[CpuBreakpoint]
