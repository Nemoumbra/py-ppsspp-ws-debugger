from dataclasses import dataclass


@dataclass(kw_only=True)
class MemoryReadU8Request:
    address: int


@dataclass(kw_only=True)
class MemoryReadU16Request:
    address: int


@dataclass(kw_only=True)
class MemoryReadU32Request:
    address: int


@dataclass(kw_only=True)
class MemoryReadRequest:
    address: int
    size: int
    replacements: bool | None = None


@dataclass(kw_only=True)
class MemoryReadStringRequest:
    address: int
    # TODO: 2 options here, maybe duplicate?
    type: str | None = None


@dataclass(kw_only=True)
class MemoryWriteU8Request:
    address: int
    value: int


@dataclass(kw_only=True)
class MemoryWriteU16Request:
    address: int
    value: int


@dataclass(kw_only=True)
class MemoryWriteU32Request:
    address: int
    value: int


@dataclass(kw_only=True)
class MemoryWriteRequest:
    address: int
    base64: str

