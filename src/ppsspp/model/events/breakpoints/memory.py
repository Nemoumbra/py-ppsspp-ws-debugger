
from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.model.ppsspp_objects.breakpoints.memory_breakpoint import MemoryBreakpoint


@dataclass(kw_only=True)
class MemoryBreakpointAddEvent(BaseEvent):
    pass

@dataclass(kw_only=True)
class MemoryBreakpointUpdateEvent(BaseEvent):
    pass

@dataclass(kw_only=True)
class MemoryBreakpointRemoveEvent(BaseEvent):
    pass

@dataclass(kw_only=True)
class MemoryBreakpointListEvent(BaseEvent):
    breakpoints: list[MemoryBreakpoint]
