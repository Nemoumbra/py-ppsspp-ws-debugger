
from dataclasses import dataclass


@dataclass
class BaseEvent:
    event: str
    ticket: str | None = None

