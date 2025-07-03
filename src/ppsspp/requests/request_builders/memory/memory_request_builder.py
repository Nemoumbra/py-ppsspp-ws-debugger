from src.ppsspp.requests.base_request_builder import BaseRequestBuilder
from src.ppsspp.ppsspp_request import PPSSPPRequest
from src.ppsspp.exceptions.request_build_error import RequestBuildError


class MemoryRequestBuilder(BaseRequestBuilder):
    def __init__(self):
        BaseRequestBuilder.__init__(self)
        self._request_lookup_table = {
            "memory.read_u8": memory_read_u8,
            "memory.read_u16": memory_read_u16,
            "memory.read_u32": memory_read_u32,
            "memory.read": memory_read,
            "memory.readString": memory_readString,
            "memory.write_u8": memory_write_u8,
            "memory.write_u16": memory_write_u16,
            "memory.write_u32": memory_write_u32,
            "memory.write": memory_write,
            "memory.mapping": memory_mapping,
            "memory.info.config": memory_info_config,
            "memory.info.set": memory_info_set,
            "memory.info.list": memory_info_list,
            "memory.info.search": memory_info_search,
            "memory.base": memory_base,
            "memory.disasm": memory_disasm,
            "memory.searchDisasm": memory_searchDisasm,
            "memory.assemble": memory_assemble,
            "memory.breakpoint.add": memory_breakpoint_add,
            "memory.breakpoint.update": memory_breakpoint_update,
            "memory.breakpoint.remove": memory_breakpoint_remove,
            "memory.breakpoint.list": memory_breakpoint_list,
        }


def memory_read_u8(**kwargs):
    event_name = "memory.read_u8"

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
    

def memory_read_u16(**kwargs):
    event_name = "memory.read_u16"

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
    

def memory_read_u32(**kwargs):
    event_name = "memory.read_u32"

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
    

def memory_read(**kwargs):
    event_name = "memory.read"

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
    

def memory_readString(**kwargs):
    event_name = "memory.readString"

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
    

def memory_write_u8(**kwargs):
    event_name = "memory.write_u8"

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
    

def memory_write_u16(**kwargs):
    event_name = "memory.write_u16"

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
    

def memory_write_u32(**kwargs):
    event_name = "memory.write_u32"

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
    

def memory_write(**kwargs):
    event_name = "memory.write"

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
    

def memory_mapping(**kwargs):
    event_name = "memory.mapping"

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
    

def memory_info_config(**kwargs):
    event_name = "memory.info.config"

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
    

def memory_info_set(**kwargs):
    event_name = "memory.info.set"

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
    

def memory_info_list(**kwargs):
    event_name = "memory.info.list"

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
    

def memory_info_search(**kwargs):
    event_name = "memory.info.search"

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
    

def memory_base(**kwargs):
    event_name = "memory.base"

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
    

def memory_disasm(**kwargs):
    event_name = "memory.disasm"

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
    

def memory_searchDisasm(**kwargs):
    event_name = "memory.searchDisasm"

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
    

def memory_assemble(**kwargs):
    event_name = "memory.assemble"

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
    

def memory_breakpoint_add(**kwargs):
    event_name = "memory.breakpoint.add"

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
    

def memory_breakpoint_update(**kwargs):
    event_name = "memory.breakpoint.update"

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
    

def memory_breakpoint_remove(**kwargs):
    event_name = "memory.breakpoint.remove"

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
    

def memory_breakpoint_list(**kwargs):
    event_name = "memory.breakpoint.list"

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
    
