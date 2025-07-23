
from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent


@dataclass(kw_only=True)
class GpuBufferScreenshotUriEvent(BaseEvent):
    width: int
    height: int
    is_framebuffer: bool | None = None
    uri: str

@dataclass(kw_only=True)
class GpuBufferScreenshotB64Event(BaseEvent):
    width: int
    height: int
    flipped: bool
    format: str
    is_framebuffer: bool | None = None
    base64: str


@dataclass(kw_only=True)
class GpuBufferRenderColorUriEvent(BaseEvent):
    width: int
    height: int
    is_framebuffer: bool | None = None
    uri: str

@dataclass(kw_only=True)
class GpuBufferRenderColorB64Event(BaseEvent):
    width: int
    height: int
    flipped: bool
    format: str
    is_framebuffer: bool | None = None
    base64: str


@dataclass(kw_only=True)
class GpuBufferRenderDepthUriEvent(BaseEvent):
    width: int
    height: int
    is_framebuffer: bool | None = None
    uri: str

@dataclass(kw_only=True)
class GpuBufferRenderDepthB64Event(BaseEvent):
    width: int
    height: int
    flipped: bool
    format: str
    is_framebuffer: bool | None = None
    base64: str


@dataclass(kw_only=True)
class GpuBufferRenderStencilUriEvent(BaseEvent):
    width: int
    height: int
    is_framebuffer: bool | None = None
    uri: str

@dataclass(kw_only=True)
class GpuBufferRenderStencilB64Event(BaseEvent):
    width: int
    height: int
    flipped: bool
    format: str
    is_framebuffer: bool | None = None
    base64: str


@dataclass(kw_only=True)
class GpuBufferTextureUriEvent(BaseEvent):
    width: int
    height: int
    is_framebuffer: bool | None = None
    uri: str

@dataclass(kw_only=True)
class GpuBufferTextureB64Event(BaseEvent):
    width: int
    height: int
    flipped: bool
    format: str
    is_framebuffer: bool | None = None
    base64: str


@dataclass(kw_only=True)
class GpuBufferClutUriEvent(BaseEvent):
    width: int
    height: int
    is_framebuffer: bool | None = None
    uri: str

@dataclass(kw_only=True)
class GpuBufferClutB64Event(BaseEvent):
    width: int
    height: int
    flipped: bool
    format: str
    is_framebuffer: bool | None = None
    base64: str
