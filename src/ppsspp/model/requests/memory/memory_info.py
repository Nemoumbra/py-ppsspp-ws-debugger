from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class MemoryMappingRequest(BaseRequest):
    pass


@dataclass(kw_only=True)
class MemoryInfoConfigRequest(BaseRequest):
    detailed: bool | None = None


# TODO (or maybe a note...): the tag is only optional if the 'type' is 'free' or 'subfree'...
# I CAN'T REPRESENT THIS IN THE MODEL!!!
@dataclass(kw_only=True)
class MemoryInfoSetRequest(BaseRequest):
    address: int
    size: int
    type: str
    tag: str | None = None
    pc: int | None = None


# Note: can't search for 'free' or 'subfree' ranges
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
