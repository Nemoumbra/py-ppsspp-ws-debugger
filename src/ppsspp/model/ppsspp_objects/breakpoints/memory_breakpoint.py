
from dataclasses import dataclass


@dataclass(kw_only=True)
class MemoryBreakpoint:
    address: int
    size: int
    enabled: bool
    log: bool
    read: bool
    write: bool
    change: bool
    hits: int
    condition: str | None
    log_format: str | None
    symbol: str | None
