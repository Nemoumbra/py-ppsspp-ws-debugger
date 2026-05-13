from dataclasses import dataclass


@dataclass(kw_only=True)
class MemoryBaseRequest:
    pass


# The most generic form
@dataclass(kw_only=True)
class MemoryDisasmRequest:
    thread: int | None = None
    address: int
    count: int | None = None
    end: int | None = None
    display_symbols: bool | None = None


@dataclass(kw_only=True)
class MemoryDisasmByCountRequest:
    thread: int | None = None
    address: int
    count: int
    display_symbols: bool | None = None


@dataclass(kw_only=True)
class MemoryDisasmByEndAddrRequest:
    thread: int | None = None
    address: int
    end: int
    display_symbols: bool | None = None


@dataclass(kw_only=True)
class MemorySearchDisasmRequest:
    thread: int | None = None
    address: int
    end: int | None = None
    match: str
    display_symbols: bool | None = None


@dataclass(kw_only=True)
class MemoryAssembleRequest:
    address: int
    code: str
