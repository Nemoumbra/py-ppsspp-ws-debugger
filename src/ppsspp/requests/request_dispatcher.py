from src.ppsspp.requests.base_request_builder import BaseRequestBuilder
from src.ppsspp.exceptions.request_build_error import RequestBuildError


class RequestDispatcher:
    def __init__(self, request_lookup_table: dict[str, BaseRequestBuilder]):
        self._request_lookup_table = request_lookup_table

    def make_request(self, name: str, /, **kwargs):
        request_group = name.split(".")[0]
        if request_group not in self._request_lookup_table:
            raise RequestBuildError(f"Unknown request type '{request_group}' (full name '{name}')")
        # We don't assign tickets here
        return self._request_lookup_table[request_group].make_request(name, **kwargs)
