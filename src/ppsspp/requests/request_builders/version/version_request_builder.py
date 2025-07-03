from src.ppsspp.requests.base_request_builder import BaseRequestBuilder
from src.ppsspp.ppsspp_request import PPSSPPRequest
from src.ppsspp.exceptions.request_build_error import RequestBuildError


class VersionRequestBuilder(BaseRequestBuilder):
    def __init__(self):
        BaseRequestBuilder.__init__(self)
        self._request_lookup_table = {
            "version": version
        }


def version(**kwargs):
    event_name = "version"

    # Read the arguments
    try:
        name_arg = kwargs.pop("name")
        version_arg = kwargs.pop("version")
    except KeyError as e:
        raise RequestBuildError(f"Missing {event_name} parameter", e) from None
    except ValueError as e:
        raise RequestBuildError(e) from None

    if kwargs:
        params = map(str, kwargs.keys())
        raise RequestBuildError(f"Unknown {event_name} parameters specified", f"{{{', '.join(params)}}}")

    # Now let's validate the data (client-side validation)

    if type(name_arg) is not str:
        raise RequestBuildError(f"{event_name} request parameter 'name' must be a string")
    if type(version_arg) is not str:
        raise RequestBuildError(f"{event_name} request parameter 'version' must be a string")

    # Now we know there are no issues with the data we need, let's build the request!
    request = PPSSPPRequest(event_name)
    request.add(name=name_arg, version=version_arg)
    return request
