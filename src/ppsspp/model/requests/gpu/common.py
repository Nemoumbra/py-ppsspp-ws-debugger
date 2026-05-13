from dataclasses import dataclass


@dataclass(kw_only=True)
class GpuRecordDumpRequest:
    pass


@dataclass(kw_only=True)
class GpuStatsGetRequest:
    pass


@dataclass(kw_only=True)
class GpuStatsFeedRequest:
    enable: bool | None = None
