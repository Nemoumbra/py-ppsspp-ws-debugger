from dataclasses import dataclass


# TODO: figure out how to make these requests work with 'uri' and 'base64' modes safely

@dataclass(kw_only=True)
class GpuBufferScreenshotRequest:
    type: str | None = None
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferRenderColorRequest:
    type: str | None = None
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferRenderDepthRequest:
    type: str | None = None
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferRenderStencilRequest:
    type: str | None = None
    alpha: bool | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferTextureRequest:
    type: str | None = None
    alpha: bool | None = None
    level: int | None = None
    stack_width: int | None = None


@dataclass(kw_only=True)
class GpuBufferClutRequest:
    type: str | None = None
    alpha: bool | None = None
    stack_width: int | None = None
