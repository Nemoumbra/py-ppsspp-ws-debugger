
from dataclasses import dataclass

@dataclass
class BranchGuide:
    top: int
    bottom: int
    direction: str
    lane: int


@dataclass
class BranchInfo:
    target_address: int | None
    register: int | None
    is_lined: bool
    is_likely: bool
    symbol: str | None
