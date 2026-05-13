from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class HleThreadListRequest(BaseRequest):
    pass


@dataclass(kw_only=True)
class HleThreadWakeRequest(BaseRequest):
    thread: int


@dataclass(kw_only=True)
class HleThreadStopRequest(BaseRequest):
    thread: int
