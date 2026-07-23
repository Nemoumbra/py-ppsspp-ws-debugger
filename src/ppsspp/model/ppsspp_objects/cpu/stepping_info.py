from dataclasses import dataclass


# Fields like in CpuSteppingEvent
@dataclass
class SteppingInfo:
    pc: int
    ticks: float
    reason: str | None = None
    related_address: int | None = None
