from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class GpuRecordDumpRequest(BaseRequest):
    pass


@dataclass(kw_only=True)
class GpuStatsGetRequest(BaseRequest):
    pass


@dataclass(kw_only=True)
class GpuStatsFeedRequest(BaseRequest):
    enable: bool | None = None
