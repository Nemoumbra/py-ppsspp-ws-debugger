
from ppsspp.model.events.error_event import ErrorEvent
from ppsspp.ppsspp_request import PPSSPPRequest


class RequestFailedError(Exception):
    def __init__(self, error: ErrorEvent, failed_request: PPSSPPRequest):
        self.error = error
        self.failed_request = failed_request
        Exception.__init__(self, error, failed_request)
