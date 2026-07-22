from dataclasses import dataclass


# Fields like in CpuStatusEvent
@dataclass
class CPUStatus:
    stepping: bool
    paused: bool
    pc: int
    ticks: float
