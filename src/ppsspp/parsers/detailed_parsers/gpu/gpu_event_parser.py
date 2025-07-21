
from src.ppsspp.parsers.base_event_parser import BaseEventParser
from src.ppsspp.model.events.gpu.common import (
    GpuRecordDumpEvent, GpuStatsGetEvent
)
from src.ppsspp.model.events.gpu.buffer import (
    GpuBufferScreenshotUriEvent, GpuBufferScreenshotB64Event,
    GpuBufferRenderColorUriEvent, GpuBufferRenderColorB64Event,
    GpuBufferRenderDepthUriEvent, GpuBufferRenderDepthB64Event,
    GpuBufferRenderStencilUriEvent, GpuBufferRenderStencilB64Event,
    GpuBufferTextureUriEvent, GpuBufferTextureB64Event,
    GpuBufferClutUriEvent, GpuBufferClutB64Event
)

class GPUEventParser(BaseEventParser):
    def __init__(self):
        lookup_table = {
            "gpu.record.dump": GpuRecordDumpEvent,
            "gpu.stats.get": GpuStatsGetEvent,
            "gpu.buffer.screenshot": GpuBufferScreenshotUriEvent | GpuBufferScreenshotB64Event,
            "gpu.buffer.renderColor": GpuBufferRenderColorUriEvent | GpuBufferRenderColorB64Event,
            "gpu.buffer.renderDepth": GpuBufferRenderDepthUriEvent | GpuBufferRenderDepthB64Event,
            "gpu.buffer.renderStencil": GpuBufferRenderStencilUriEvent | GpuBufferRenderStencilB64Event,
            "gpu.buffer.texture": GpuBufferTextureUriEvent | GpuBufferTextureB64Event,
            "gpu.buffer.clut": GpuBufferClutUriEvent | GpuBufferClutB64Event
        }

        BaseEventParser.__init__(self, lookup_table)
