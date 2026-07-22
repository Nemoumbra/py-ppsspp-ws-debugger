from dataclasses import dataclass


# Fields like in CpuSteppingEvent
@dataclass(kw_only=True)
class SteppingInfo:
    pc: int
    ticks: float
    reason: str | None = None
    related_address: int | None = None
