from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class MemoryBaseRequest(BaseRequest):
    pass


# The most generic form
@dataclass(kw_only=True)
class MemoryDisasmRequest(BaseRequest):
    thread: int | None = None
    address: int
    count: int | None = None
    end: int | None = None
    display_symbols: bool | None = None


@dataclass(kw_only=True)
class MemoryDisasmByCountRequest(BaseRequest):
    thread: int | None = None
    address: int
    count: int
    display_symbols: bool | None = None


@dataclass(kw_only=True)
class MemoryDisasmByEndAddrRequest(BaseRequest):
    thread: int | None = None
    address: int
    end: int
    display_symbols: bool | None = None


@dataclass(kw_only=True)
class MemorySearchDisasmRequest(BaseRequest):
    thread: int | None = None
    address: int
    end: int | None = None
    match: str
    display_symbols: bool | None = None


@dataclass(kw_only=True)
class MemoryAssembleRequest(BaseRequest):
    address: int
    code: str
