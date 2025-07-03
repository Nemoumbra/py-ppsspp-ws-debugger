from src.ppsspp.requests.base_request_builder import BaseRequestBuilder
from src.ppsspp.ppsspp_request import PPSSPPRequest
from src.ppsspp.exceptions.request_build_error import RequestBuildError


class HLERequestBuilder(BaseRequestBuilder):
    def __init__(self):
        BaseRequestBuilder.__init__(self)
        self._request_lookup_table = {
            "hle.thread.list": hle_thread_list,
            "hle.thread.wake": hle_thread_wake,
            "hle.thread.stop": hle_thread_stop,
            "hle.func.list": hle_func_list,
            "hle.func.add": hle_func_add,
            "hle.func.remove": hle_func_remove,
            "hle.func.removeRange": hle_func_removeRange,
            "hle.func.rename": hle_func_rename,
            "hle.func.scan": hle_func_scan,
            "hle.module.list": hle_module_list,
            "hle.backtrace": hle_backtrace,
        }


def hle_thread_list(**kwargs):
    event_name = "hle.thread.list"

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
    

def hle_thread_wake(**kwargs):
    event_name = "hle.thread.wake"

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
    

def hle_thread_stop(**kwargs):
    event_name = "hle.thread.stop"

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
    

def hle_func_list(**kwargs):
    event_name = "hle.func.list"

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
    

def hle_func_add(**kwargs):
    event_name = "hle.func.add"

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
    

def hle_func_remove(**kwargs):
    event_name = "hle.func.remove"

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
    

def hle_func_removeRange(**kwargs):
    event_name = "hle.func.removeRange"

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
    

def hle_func_rename(**kwargs):
    event_name = "hle.func.rename"

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
    

def hle_func_scan(**kwargs):
    event_name = "hle.func.scan"

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
    

def hle_module_list(**kwargs):
    event_name = "hle.module.list"

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
    

def hle_backtrace(**kwargs):
    event_name = "hle.backtrace"

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
    
