from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class ReplayTimeGetRequest(BaseRequest):
    pass


@dataclass(kw_only=True)
class ReplayTimeSetRequest(BaseRequest):
    value: int
