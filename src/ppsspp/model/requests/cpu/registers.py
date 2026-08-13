from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class CpuGetAllRegsRequest(BaseRequest):
    thread: int | None = None


@dataclass(kw_only=True)
class CpuGetRegByNameRequest(BaseRequest):
    thread: int | None = None
    name: str


@dataclass(kw_only=True)
class CpuGetRegByIdxAndCategoryRequest(BaseRequest):
    thread: int | None = None
    category: int
    register: int


@dataclass(kw_only=True)
class CpuSetRegByNameRequest(BaseRequest):
    thread: int | None = None
    name: str
    value: int | str


@dataclass(kw_only=True)
class CpuSetRegByIdxAndCategoryRequest(BaseRequest):
    thread: int | None = None
    category: int
    register: int
    value: int | str
