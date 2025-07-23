
from dataclasses import dataclass

@dataclass
class StackFrameInfo:
    entry: int
    pc: int
    sp: int
    stack_size: int
    code: str
