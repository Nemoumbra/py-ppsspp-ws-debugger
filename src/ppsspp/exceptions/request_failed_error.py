
from ppsspp.model.events.error_event import ErrorEvent
from ppsspp.model.requests.base_request import BaseRequest
from ppsspp.ppsspp_request import PPSSPPRequest


class RequestFailedError(Exception):
    def __init__(self, error: ErrorEvent, failed_request: PPSSPPRequest | BaseRequest):
        self.error = error
        self.failed_request = failed_request
        super().__init__(f"Request {failed_request} failed: '{error.message}'")
