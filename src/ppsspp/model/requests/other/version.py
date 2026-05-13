from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class VersionRequest(BaseRequest):
    name: str | None = None
    version: str | None = None
