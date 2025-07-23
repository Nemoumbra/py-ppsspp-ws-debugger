
from dataclasses import dataclass


@dataclass
class FpsInfo:
    actual: float
    target: float


@dataclass
class VblankCyclesInfo:
    actual: float
    target: float


@dataclass
class TimingInfo:
    frames: list[float]
    sleep: list[float]
    pos: int
