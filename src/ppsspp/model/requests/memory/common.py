from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class MemoryReadU8Request(BaseRequest):
    address: int


@dataclass(kw_only=True)
class MemoryReadU16Request(BaseRequest):
    address: int


@dataclass(kw_only=True)
class MemoryReadU32Request(BaseRequest):
    address: int


@dataclass(kw_only=True)
class MemoryReadRequest(BaseRequest):
    address: int
    size: int
    replacements: bool | None = None


@dataclass(kw_only=True)
class MemoryReadStringRequest(BaseRequest):
    address: int
    # TODO: 2 options here, maybe duplicate?
    type: str | None = None


@dataclass(kw_only=True)
class MemoryWriteU8Request(BaseRequest):
    address: int
    value: int


@dataclass(kw_only=True)
class MemoryWriteU16Request(BaseRequest):
    address: int
    value: int


@dataclass(kw_only=True)
class MemoryWriteU32Request(BaseRequest):
    address: int
    value: int


@dataclass(kw_only=True)
class MemoryWriteRequest(BaseRequest):
    address: int
    base64: str
