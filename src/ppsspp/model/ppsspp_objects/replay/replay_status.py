
from dataclasses import dataclass


# Fields like in ReplayStatusEvent
@dataclass
class ReplayStatus:
    executing: bool
    saving: bool
