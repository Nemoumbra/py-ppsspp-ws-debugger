from dataclasses import dataclass


@dataclass(kw_only=True)
class CpuGetAllRegsRequest:
    thread: int | None = None


# The most generic form
@dataclass(kw_only=True)
class CpuGetRegRequest:
    thread: int | None = None
    name: str | None = None
    category: int | None = None
    register: int | None = None


@dataclass(kw_only=True)
class CpuGetRegByNameRequest:
    thread: int | None = None
    name: str


@dataclass(kw_only=True)
class CpuGetRegByIdxAndCategoryRequest:
    thread: int | None = None
    category: int
    register: int


# The most generic form
@dataclass(kw_only=True)
class CpuSetRegRequest:
    thread: int | None = None
    name: str | None = None
    category: int | None = None
    register: int | None = None
    value: int | str | None = None


@dataclass(kw_only=True)
class CpuSetRegByNameRequest:
    thread: int | None = None
    name: str
    value: int | str


@dataclass(kw_only=True)
class CpuSetRegByIdxAndCategoryRequest:
    thread: int | None = None
    category: int
    register: int
    value: int | str
