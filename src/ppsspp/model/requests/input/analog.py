from dataclasses import dataclass


@dataclass(kw_only=True)
class InputAnalogSendRequest:
    x: float
    y: float
    # TODO: decide what to do with AnalogState and Analog
    stick: str | None = None
