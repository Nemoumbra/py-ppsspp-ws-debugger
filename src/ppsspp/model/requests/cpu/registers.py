from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class CpuGetAllRegsRequest(BaseRequest):
    thread: int | None = None


# Obviously passing None for either 'category' or 'register' after passing None for 'name'
# won't be accepted by PPSSPP, but it's still a part of the model...
# TODO: maybe remove this generic request completely?
@dataclass(kw_only=True)
class CpuGetRegRequest(BaseRequest):
    thread: int | None = None
    name: str | None = None
    category: int | None = None
    register: int | None = None


@dataclass(kw_only=True)
class CpuGetRegByNameRequest(BaseRequest):
    thread: int | None = None
    name: str


@dataclass(kw_only=True)
class CpuGetRegByIdxAndCategoryRequest(BaseRequest):
    thread: int | None = None
    category: int
    register: int


# Obviously passing None for either 'category' or 'register' after passing None for 'name'
# won't be accepted by PPSSPP, but it's still a part of the model...
# TODO: maybe remove this generic request completely?
@dataclass(kw_only=True)
class CpuSetRegRequest(BaseRequest):
    thread: int | None = None
    name: str | None = None
    category: int | None = None
    register: int | None = None
    value: int | str | None = None


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
