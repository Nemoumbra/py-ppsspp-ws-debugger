
from dataclasses import dataclass

@dataclass
class UserModuleInfo:
    name: str
    address: int
    size: int
    is_active: bool
