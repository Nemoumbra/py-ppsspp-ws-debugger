from src.ppsspp.requests.base_request_builder import BaseRequestBuilder
from src.ppsspp.ppsspp_request import PPSSPPRequest
from src.ppsspp.exceptions.request_build_error import RequestBuildError


class CPURequestBuilder(BaseRequestBuilder):
    def __init__(self):
        BaseRequestBuilder.__init__(self)
        self._request_lookup_table = {
            "cpu.stepping": cpu_stepping,
            "cpu.resume": cpu_resume,
            "cpu.status": cpu_status,
            "cpu.getAllRegs": cpu_getAllRegs,
            "cpu.getReg": cpu_getReg,
            "cpu.setReg": cpu_setReg,
            "cpu.evaluate": cpu_evaluate,
            "cpu.breakpoint.add": cpu_breakpoint_add,
            "cpu.breakpoint.update": cpu_breakpoint_update,
            "cpu.breakpoint.remove": cpu_breakpoint_remove,
            "cpu.breakpoint.list": cpu_breakpoint_list,
            "cpu.stepInto": cpu_stepInto,
            "cpu.stepOver": cpu_stepOver,
            "cpu.stepOut": cpu_stepOut,
            "cpu.runUntil": cpu_runUntil,
            "cpu.nextHLE": cpu_nextHLE,
        }


def cpu_stepping(**kwargs):
    event_name = "cpu.stepping"

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
    

def cpu_resume(**kwargs):
    event_name = "cpu.resume"

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
    

def cpu_status(**kwargs):
    event_name = "cpu.status"

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
    

def cpu_getAllRegs(**kwargs):
    event_name = "cpu.getAllRegs"

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
    

def cpu_getReg(**kwargs):
    event_name = "cpu.getReg"

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
    

def cpu_setReg(**kwargs):
    event_name = "cpu.setReg"

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
    

def cpu_evaluate(**kwargs):
    event_name = "cpu.evaluate"

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
    

def cpu_breakpoint_add(**kwargs):
    event_name = "cpu.breakpoint.add"

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
    

def cpu_breakpoint_update(**kwargs):
    event_name = "cpu.breakpoint.update"

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
    

def cpu_breakpoint_remove(**kwargs):
    event_name = "cpu.breakpoint.remove"

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
    

def cpu_breakpoint_list(**kwargs):
    event_name = "cpu.breakpoint.list"

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
    

def cpu_stepInto(**kwargs):
    event_name = "cpu.stepInto"

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
    

def cpu_stepOver(**kwargs):
    event_name = "cpu.stepOver"

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
    

def cpu_stepOut(**kwargs):
    event_name = "cpu.stepOut"

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
    

def cpu_runUntil(**kwargs):
    event_name = "cpu.runUntil"

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
    

def cpu_nextHLE(**kwargs):
    event_name = "cpu.nextHLE"

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
    
