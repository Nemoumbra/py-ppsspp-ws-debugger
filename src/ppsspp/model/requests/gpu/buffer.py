from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class GpuBufferScreenshotRequest(BaseRequest):
    type: str | None = None
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferScreenshotUriRequest(BaseRequest):
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferScreenshotBase64Request(BaseRequest):
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferRenderColorRequest(BaseRequest):
    type: str | None = None
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferRenderColorUriRequest(BaseRequest):
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferRenderColorBase64Request(BaseRequest):
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferRenderDepthRequest(BaseRequest):
    type: str | None = None
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferRenderDepthUriRequest(BaseRequest):
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferRenderDepthBase64Request(BaseRequest):
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferRenderStencilRequest(BaseRequest):
    type: str | None = None
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferRenderStencilUriRequest(BaseRequest):
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferRenderStencilBase64Request(BaseRequest):
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferTextureRequest(BaseRequest):
    type: str | None = None
    alpha: bool | None = None
    level: int | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferTextureUriRequest(BaseRequest):
    alpha: bool | None = None
    level: int | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferTextureBase64Request(BaseRequest):
    alpha: bool | None = None
    level: int | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferClutRequest(BaseRequest):
    type: str | None = None
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferClutUriRequest(BaseRequest):
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferClutBase64Request(BaseRequest):
    alpha: bool | None = None
    stack_width: int | None = None
