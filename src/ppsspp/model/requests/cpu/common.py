from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class CpuSteppingRequest(BaseRequest):
    pass


@dataclass(kw_only=True)
class CpuResumeRequest(BaseRequest):
    pass


@dataclass(kw_only=True)
class CpuStatusRequest(BaseRequest):
    pass


@dataclass(kw_only=True)
class CpuEvaluateRequest(BaseRequest):
    thread: int | None = None
    expression: str
