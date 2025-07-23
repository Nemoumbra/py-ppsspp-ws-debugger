
from dataclasses import dataclass

@dataclass
class ThreadInfo:
    id: int
    name: str
    status: int
    statuses: list[str]
    pc: int
    entry: int
    initial_stack_size: int
    current_stack_size: int
    priority: int
    wait_type: int
    is_current: bool
