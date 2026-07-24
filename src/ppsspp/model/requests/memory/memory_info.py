from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class MemoryMappingRequest(BaseRequest):
    pass


@dataclass(kw_only=True)
class MemoryInfoConfigRequest(BaseRequest):
    detailed: bool | None = None


@dataclass(kw_only=True)
class MemoryInfoSetRequest(BaseRequest):
    address: int
    size: int
    type: str
    tag: str | None = None
    pc: int | None = None


@dataclass(kw_only=True)
class MemoryInfoListRequest(BaseRequest):
    address: int
    size: int
    type: str | None = None


@dataclass(kw_only=True)
class MemoryInfoSearchRequest(BaseRequest):
    address: int | None = None
    end: int | None = None
    match: str
    type: str | None = None
