
from dataclasses import dataclass

from ppsspp.model.ppsspp_objects.memory.memory_tag_type import MemoryTagType


@dataclass
class MemoryBlockInfo:
    type: MemoryTagType
    address: int
    size: int
    ticks: float
    pc: int
    tag: str
    allocated: bool
