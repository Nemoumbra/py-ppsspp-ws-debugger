
from dataclasses import dataclass

# from adaptix import Omittable, Omitted


@dataclass
class BaseRequest:
    # ticket: Omittable[str] = Omitted()
    ticket: str | None = None
