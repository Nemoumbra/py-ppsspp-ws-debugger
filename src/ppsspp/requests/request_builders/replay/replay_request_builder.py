from src.ppsspp.requests.base_request_builder import BaseRequestBuilder
from src.ppsspp.ppsspp_request import PPSSPPRequest
from src.ppsspp.exceptions.request_build_error import RequestBuildError


class ReplayRequestBuilder(BaseRequestBuilder):
    def __init__(self):
        BaseRequestBuilder.__init__(self)
        self._request_lookup_table = {
            "replay.begin": replay_begin,
            "replay.abort": replay_abort,
            "replay.flush": replay_flush,
            "replay.execute": replay_execute,
            "replay.status": replay_status,
            "replay.time.get": replay_time_get,
            "replay.time.set": replay_time_set,
        }


def replay_begin(**kwargs):
    event_name = "replay.begin"

    # Read the arguments
    try:
        raise NotImplementedError
    except KeyError as e:
        raise RequestBuildError(f"Missing {event_name} parameter", e) from None
    except ValueError as e:
        raise RequestBuildError(e) from None

    if kwargs:
        params = map(str, kwargs.keys())
        raise RequestBuildError(f"Unknown {event_name} parameters specified", f"{{{', '.join(params)}}}")
        
    # Now let's validate the data (client-side validation)
    raise NotImplementedError

    # Now we know there are no issues with the data we need, let's build the request!
    request = PPSSPPRequest(event_name)
    raise NotImplementedError
    
    return request
    

def replay_abort(**kwargs):
    event_name = "replay.abort"

    # Read the arguments
    try:
        raise NotImplementedError
    except KeyError as e:
        raise RequestBuildError(f"Missing {event_name} parameter", e) from None
    except ValueError as e:
        raise RequestBuildError(e) from None

    if kwargs:
        params = map(str, kwargs.keys())
        raise RequestBuildError(f"Unknown {event_name} parameters specified", f"{{{', '.join(params)}}}")
        
    # Now let's validate the data (client-side validation)
    raise NotImplementedError

    # Now we know there are no issues with the data we need, let's build the request!
    request = PPSSPPRequest(event_name)
    raise NotImplementedError
    
    return request
    

def replay_flush(**kwargs):
    event_name = "replay.flush"

    # Read the arguments
    try:
        raise NotImplementedError
    except KeyError as e:
        raise RequestBuildError(f"Missing {event_name} parameter", e) from None
    except ValueError as e:
        raise RequestBuildError(e) from None

    if kwargs:
        params = map(str, kwargs.keys())
        raise RequestBuildError(f"Unknown {event_name} parameters specified", f"{{{', '.join(params)}}}")
        
    # Now let's validate the data (client-side validation)
    raise NotImplementedError

    # Now we know there are no issues with the data we need, let's build the request!
    request = PPSSPPRequest(event_name)
    raise NotImplementedError
    
    return request
    

def replay_execute(**kwargs):
    event_name = "replay.execute"

    # Read the arguments
    try:
        raise NotImplementedError
    except KeyError as e:
        raise RequestBuildError(f"Missing {event_name} parameter", e) from None
    except ValueError as e:
        raise RequestBuildError(e) from None

    if kwargs:
        params = map(str, kwargs.keys())
        raise RequestBuildError(f"Unknown {event_name} parameters specified", f"{{{', '.join(params)}}}")
        
    # Now let's validate the data (client-side validation)
    raise NotImplementedError

    # Now we know there are no issues with the data we need, let's build the request!
    request = PPSSPPRequest(event_name)
    raise NotImplementedError
    
    return request
    

def replay_status(**kwargs):
    event_name = "replay.status"

    # Read the arguments
    try:
        raise NotImplementedError
    except KeyError as e:
        raise RequestBuildError(f"Missing {event_name} parameter", e) from None
    except ValueError as e:
        raise RequestBuildError(e) from None

    if kwargs:
        params = map(str, kwargs.keys())
        raise RequestBuildError(f"Unknown {event_name} parameters specified", f"{{{', '.join(params)}}}")
        
    # Now let's validate the data (client-side validation)
    raise NotImplementedError

    # Now we know there are no issues with the data we need, let's build the request!
    request = PPSSPPRequest(event_name)
    raise NotImplementedError
    
    return request
    

def replay_time_get(**kwargs):
    event_name = "replay.time.get"

    # Read the arguments
    try:
        raise NotImplementedError
    except KeyError as e:
        raise RequestBuildError(f"Missing {event_name} parameter", e) from None
    except ValueError as e:
        raise RequestBuildError(e) from None

    if kwargs:
        params = map(str, kwargs.keys())
        raise RequestBuildError(f"Unknown {event_name} parameters specified", f"{{{', '.join(params)}}}")
        
    # Now let's validate the data (client-side validation)
    raise NotImplementedError

    # Now we know there are no issues with the data we need, let's build the request!
    request = PPSSPPRequest(event_name)
    raise NotImplementedError
    
    return request
    

def replay_time_set(**kwargs):
    event_name = "replay.time.set"

    # Read the arguments
    try:
        raise NotImplementedError
    except KeyError as e:
        raise RequestBuildError(f"Missing {event_name} parameter", e) from None
    except ValueError as e:
        raise RequestBuildError(e) from None

    if kwargs:
        params = map(str, kwargs.keys())
        raise RequestBuildError(f"Unknown {event_name} parameters specified", f"{{{', '.join(params)}}}")
        
    # Now let's validate the data (client-side validation)
    raise NotImplementedError

    # Now we know there are no issues with the data we need, let's build the request!
    request = PPSSPPRequest(event_name)
    raise NotImplementedError
    
    return request
    
