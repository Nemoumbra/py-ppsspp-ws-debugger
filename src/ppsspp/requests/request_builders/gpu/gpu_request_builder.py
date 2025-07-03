from src.ppsspp.requests.base_request_builder import BaseRequestBuilder
from src.ppsspp.ppsspp_request import PPSSPPRequest
from src.ppsspp.exceptions.request_build_error import RequestBuildError


class GPURequestBuilder(BaseRequestBuilder):
    def __init__(self):
        BaseRequestBuilder.__init__(self)
        self._request_lookup_table = {
            "gpu.buffer.screenshot": gpu_buffer_screenshot,
            "gpu.buffer.renderColor": gpu_buffer_renderColor,
            "gpu.buffer.renderDepth": gpu_buffer_renderDepth,
            "gpu.buffer.renderStencil": gpu_buffer_renderStencil,
            "gpu.buffer.texture": gpu_buffer_texture,
            "gpu.buffer.clut": gpu_buffer_clut,
            "gpu.record.dump": gpu_record_dump,
            "gpu.stats.get": gpu_stats_get,
            "gpu.stats.feed": gpu_stats_feed,
        }


def gpu_buffer_screenshot(**kwargs):
    event_name = "gpu.buffer.screenshot"

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
    

def gpu_buffer_renderColor(**kwargs):
    event_name = "gpu.buffer.renderColor"

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
    

def gpu_buffer_renderDepth(**kwargs):
    event_name = "gpu.buffer.renderDepth"

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
    

def gpu_buffer_renderStencil(**kwargs):
    event_name = "gpu.buffer.renderStencil"

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
    

def gpu_buffer_texture(**kwargs):
    event_name = "gpu.buffer.texture"

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
    

def gpu_buffer_clut(**kwargs):
    event_name = "gpu.buffer.clut"

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
    

def gpu_record_dump(**kwargs):
    event_name = "gpu.record.dump"

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
    

def gpu_stats_get(**kwargs):
    event_name = "gpu.stats.get"

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
    

def gpu_stats_feed(**kwargs):
    event_name = "gpu.stats.feed"

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
    
