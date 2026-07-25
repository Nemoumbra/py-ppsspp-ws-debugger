from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class ReplayBeginRequest(BaseRequest):
    pass


@dataclass(kw_only=True)
class ReplayAbortRequest(BaseRequest):
    pass


@dataclass(kw_only=True)
class ReplayFlushRequest(BaseRequest):
    pass


@dataclass(kw_only=True)
class ReplayExecuteRequest(BaseRequest):
    version: int
    base64: str


@dataclass(kw_only=True)
class ReplayStatusRequest(BaseRequest):
    pass
