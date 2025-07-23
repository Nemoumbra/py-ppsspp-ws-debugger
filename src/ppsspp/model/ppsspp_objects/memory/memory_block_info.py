
from dataclasses import dataclass

@dataclass
class MemoryBlockInfo:
    type: str
    address: int
    size: int
    ticks: float
    pc: int
    tag: str
    allocated: bool
