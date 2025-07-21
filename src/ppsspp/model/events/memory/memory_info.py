from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.model.ppsspp_objects.memory.memory_block_info import MemoryBlockInfo
from src.ppsspp.model.ppsspp_objects.memory.memory_range import MemoryRangeInfo


@dataclass(kw_only=True)
class MemoryMappingEvent(BaseEvent):
    ranges: list[MemoryRangeInfo]


@dataclass(kw_only=True)
class MemoryInfoConfigEvent(BaseEvent):
    detailed: bool

@dataclass(kw_only=True)
class MemoryInfoSetEvent(BaseEvent):
    pass

@dataclass(kw_only=True)
class MemoryInfoListEvent(BaseEvent):
    extents: list[MemoryBlockInfo]

@dataclass(kw_only=True)
class MemoryInfoSearchEvent(BaseEvent):
    extent: MemoryBlockInfo | None
