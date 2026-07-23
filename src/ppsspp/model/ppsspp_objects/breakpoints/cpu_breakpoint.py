
from dataclasses import dataclass


@dataclass
class CpuBreakpoint:
    address: int
    enabled: bool
    log: bool
    condition: str | None
    log_format: str | None
    symbol: str | None
    code: str
