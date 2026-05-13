from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class InputAnalogSendRequest(BaseRequest):
    x: float
    y: float
    # TODO: decide what to do with AnalogState and Analog
    stick: str | None = None
