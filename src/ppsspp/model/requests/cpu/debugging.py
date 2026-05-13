from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class CpuStepIntoRequest(BaseRequest):
    thread: int | None = None


@dataclass(kw_only=True)
class CpuStepOverRequest(BaseRequest):
    thread: int | None = None


@dataclass(kw_only=True)
class CpuStepOutRequest(BaseRequest):
    thread: int | None = None


@dataclass(kw_only=True)
class CpuRunUntilRequest(BaseRequest):
    address: int


@dataclass(kw_only=True)
class CpuNextHleRequest(BaseRequest):
    pass
