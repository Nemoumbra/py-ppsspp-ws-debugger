
from dataclasses import dataclass

@dataclass
class MemoryRangeInfo:
    type: str
    subtype: str
    name: str
    address: int
    size: int
