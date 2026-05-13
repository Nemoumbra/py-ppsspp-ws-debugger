from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


# TODO: figure out how to make these requests work with 'uri' and 'base64' modes safely

@dataclass(kw_only=True)
class GpuBufferScreenshotRequest(BaseRequest):
    type: str | None = None
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferRenderColorRequest(BaseRequest):
    type: str | None = None
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferRenderDepthRequest(BaseRequest):
    type: str | None = None
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferRenderStencilRequest(BaseRequest):
    type: str | None = None
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferTextureRequest(BaseRequest):
    type: str | None = None
    alpha: bool | None = None
    level: int | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferClutRequest(BaseRequest):
    type: str | None = None
    alpha: bool | None = None
    stack_width: int | None = None
