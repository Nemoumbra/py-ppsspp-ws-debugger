from dataclasses import dataclass

from ppsspp.model.requests.base_request import BaseRequest


@dataclass(kw_only=True)
class BroadcastConfigGetRequest(BaseRequest):
    pass

# TODO: maybe wrap the dicts into objects?

@dataclass(kw_only=True)
class BroadcastConfigSetRequest(BaseRequest):
    disallowed: dict[str, bool]
