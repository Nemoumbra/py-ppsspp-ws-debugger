
from dataclasses import dataclass

from src.ppsspp.model.events.base_event import BaseEvent
from src.ppsspp.model.ppsspp_objects.gpu.gpu_stats import FpsInfo, VblankCyclesInfo, TimingInfo


@dataclass(kw_only=True)
class GpuRecordDumpEvent(BaseEvent):
    uri: str


@dataclass(kw_only=True)
class GpuStatsGetEvent(BaseEvent):
    fps: FpsInfo
    vblanks_per_second: VblankCyclesInfo
    info: str
    timing: TimingInfo
