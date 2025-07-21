from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent


# Reading

@dataclass(kw_only=True)
class MemoryReadU8Event(BaseEvent):
    value: int

@dataclass(kw_only=True)
class MemoryReadU16Event(BaseEvent):
    value: int

@dataclass(kw_only=True)
class MemoryReadU32Event(BaseEvent):
    value: int

@dataclass(kw_only=True)
class MemoryReadEvent(BaseEvent):
    base64: str

@dataclass(kw_only=True)
class MemoryReadStringUtf8Event(BaseEvent):
    value: str

@dataclass(kw_only=True)
class MemoryReadStringB64Event(BaseEvent):
    base64: str



# Writing

@dataclass(kw_only=True)
class MemoryWriteU8Event(BaseEvent):
    value: int

@dataclass(kw_only=True)
class MemoryWriteU16Event(BaseEvent):
    value: int

@dataclass(kw_only=True)
class MemoryWriteU32Event(BaseEvent):
    value: int

@dataclass(kw_only=True)
class MemoryWriteEvent(BaseEvent):
    pass
