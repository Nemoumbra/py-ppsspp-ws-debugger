from src.ppsspp.ppsspp_request import PPSSPPRequest
from src.ppsspp.exceptions.request_build_error import RequestBuildError


class BaseRequestBuilder:
    def __init__(self):
        self._request_lookup_table = {}

    def make_request(self, name: str, /, **kwargs) -> PPSSPPRequest:
        if name not in self._request_lookup_table:
            raise RequestBuildError(f"Unknown request '{name}'")
        return self._request_lookup_table[name](**kwargs)
