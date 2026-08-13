
# Python websocket debugger for PPSSPP
This library provides low- and middle-level primitives for interacting with PPSSPP's remote websocket debugger API.

## Installation
Right now there's no distribution available at pypi.org, so you'll have to install it from here:
```
pip install git+https://github.com/Nemoumbra/py-ppsspp-ws-debugger.git@master
```
Pip is smart enough to install from GitHub. Alternatively, you can clone the repository and do a local installation.
This package is using `setuptools` so make sure it's present and not too old.

---
If your PyCharm is struggling with the package installed as editable, try reinstalling with this command instead:
```
pip install -e /path/to/cloned/repo --config-settings editable_mode=compat
```

## PPSSPP API
The only documentation available is located in comments in PPSSPP's source code.
The description of the system is [here](https://github.com/hrydgard/ppsspp/blob/master/Core/Debugger/WebSocket.cpp). The detailed info on the available
requests and expected responses is documented in the `.cpp` files inside [this directory](https://github.com/hrydgard/ppsspp/tree/master/Core/Debugger/WebSocket).
This library doesn't force you to operate on JSONs, instead, serialization and deserialization is used.
PPSSPP registers its websocket debugger on `report.ppsspp.org`. The endpoint `report.ppsspp.org/match/list` returns a JSON array of objects representing the PPSSPP instances.
For instance, `[{"ip":"1.2.3.4","p":54321,"t":1771360769}]`. To access the debugger, you have to substitute the IP and the port into `ws://{0}:{1}/debugger`.

You can also check out the Node.js [SDK](https://github.com/unknownbrackets/ppsspp-api-samples/tree/master/js) (written by Unknownbrackets)
to learn further details about this system and how to enable the remote debugger in PPSSPP.

## Model
The objects in the model are defined as dataclasses.
* `ppsspp.model.requests` contains the request templates for the modern request sending API (more on that [later](#issuing-requests-to-PPSSPP)).
* `ppsspp.model.ppsspp_objects` contains the building blocks for many PPSSPP events (often sent as responses to requests, but sometimes broadcast randomly).
* `ppsspp.model.events` contains the actual event bodies. There is a special event that PPSSPP sends if it's unable to process the request: `ErrorEvent`.
All events inherit from the base class `BaseEvent`, which stores the string name of the event and the optional ticket.

This library uses [adaptix](https://github.com/reagento/adaptix) for data model conversions.

## Usage
The library presents a full-fledged asynchronous API (`asyncio` and [websockets](https://github.com/python-websockets/websockets))
and also hard-to-use synchronous API (also [websockets](https://github.com/python-websockets/websockets)).
The following docs focus on the async API. The details on the sync API are listed [at the end](#sync-API).

The classes you need are `AsyncSession` and `AsyncConnection`.

### AsyncConnection
`AsyncConnection` encapsulates the connection from your device to PPSSPP. This library does not provide any means of acquiring the correct URI for connecting to PPSSPP.
It is entirely up to you: read it from your config file or let the user decide.
Perhaps, contact `report.ppsspp.org/match/list` by using your favorite HTTP library.

You can attempt to connect by awaiting a call to `connect(uri)`. You can also provide a callback `set_on_disconnected_handler`.
```py
# Returns whether the connection was reestablished
AsyncOnDisconnectedHandler = Callable[['AsyncPpssppConnection'], Awaitable[bool]]
```
It's a perfect opportunity to report the connection error to the user and reconnect. You can use a different URI this time, by the way.
The default handler just returns `False` to signify that the connection is dead for good. There's also a decorator for you:
```py
uri = ...

@connection.on_disconnected
async def on_disconnected(conn: AsyncPpssppConnection):
    if conn.closed_ok:
        notify_user("connection closed")
        return False

    notify_user("connection closed with error")
    try:
        await conn.connect(uri)
        return True
    except:
        return False
```
The handler may be called multiple times: once for every `send` or `recv` operation currently scheduled.
If you wish to make sure the handler's code is only executed by one task/coroutine at a time, use `asyncio.Lock`.
Furthermore, if the connection is reestablished, the pending failed operations may still invoke the handler (because of asyncio).
This problem of spurious disconnects can be solved by checking that `conn.close_info` is not `None` before doing anything.

If `close_info` is not `None`, it contains the `ConnectionClosed` exception from `websockets`.
Refer to their [documentation](https://websockets.readthedocs.io/en/stable/reference/exceptions.html#websockets.exceptions.ConnectionClosed) for details.
The field `conn.closed_ok` reports whether the connection has ended normally or due to an error.
```py
uri = ...
lock = asyncio.Lock()
first_time = True

@connection.on_disconnected
async def on_disconnected(conn: AsyncPpssppConnection):
    nonlocal lock, first_time
    async with lock:
        if conn.close_info is None:
            # Must've been the wind
            return True

        print(f"We disconnected: {conn.closed_ok=}, {conn.close_info=}")

        if first_time:
            first_time = False
            await conn.connect(uri)
            print("Reconnected!")
            return True
        return False
```

### AsyncSession
This is the actual facade you have to use for communicating with PPSSPP. Create an instance, then await a call to `run(connection)`.
The code assumes that the connection has been opened prior to calling `run`. This kicks off the internal tasks of the session
which recv from the connection, deserialize the events coming from PPSSPP, store them for later processing into a queue,
drain the queue and invoke event handlers if necessary.

Call `await session.stop()` to fully shut down the internals and the connection. Of course, it will trigger the `on_disconnected` handler. Reconnecting is meaningless at that point:
the internal queue will be closed by then, so the session will shut down nonetheless. Just return `False`.

---

#### Issuing requests to PPSSPP:
There are 2 groups of methods: one with the `_raw` suffix and one without. The methods without it accept request classes
inherited from `RequestBase` and ending on `Request` (such as `CpuStepIntoRequest`). The "raw" methods accept
an instance of `PPSSPPRequest`; they are more or less low-level, because `PPSSPPRequest` requires manually filling in
the request parameters, including the exact request name. The request classes are dataclasses with predefined fields
and auto-generated request name, so they should be safer to use. Other than that, these interfaces are identical.
The following code snippet will show both ways.

The most basic method is `session.send_request{_raw}`. It simply sends the request to PPSSPP.

```py
async def install_breakpoint(session: AsyncSession, address: int):
    # Check the source code for PPSSPPRequest creation API.
    request = PPSSPPRequest("cpu.breakpoint.add")
    request.add(address=address, enabled=True)
    await session.send_request_raw(request)

    modern_request = CpuBreakPointAddRequest(address=address, enabled=False)
    await session.send_request(modern_request)
```
However, there is also a second argument, defaulting to `None`, which is a response handler.
If a handler is provided and request contains a ticket, schedules the handler once PPSSPP echoes the same ticket in one of the events.
If a handler is provided with no ticket, the session generates a ticket automatically.
```py
AsyncEventHandler = Callable[[BaseEvent], Awaitable[bool | None]]
```
The mid-level API is `session.execute_unchecked{_raw}(request)`. This returns the event sent in response to your request (maybe `ErrorEvent`).
> [!WARNING]
> PPSSPP may not respond to certain events at all! In this case, `execute_unchecked` will hang!
>
> So far there are only [2 such commands](https://github.com/hrydgard/ppsspp/blob/master/Core/Debugger/WebSocket/CPUCoreSubscriber.cpp): `cpu.resume` and `cpu.stepping`.
So don't use `execute_unchecked` for them, use the low-level API.

Lastly, there is `session.execute{_raw}(request)`. It raises `RequestFailedError` if the returned event happens to be `ErrorEvent`.
This way is kind of more Pythonic than operating on error objects.
You can inspect the fields `error` for the error event and `failed_request` for the request that failed
(which is either `PPSSPPRequest` or a class derived from `BaseRequest`).

---

#### Reacting to PPSSPP events
The ticket system, which powers the `execute_unchecked{_raw}` and `execute{_raw}` methods (and also `send_request{_raw}` if you manually supply a handler),
covers almost a half of use-cases. Then there are unexpected broadcast events... They are divided into 4 groups.
1) Logging events: `LogEvent`. Sent for each PPSSPP's log.
2) Game events: `GameStartEvent`, `GamePauseEvent`, `GameQuitEvent`, `GameResumeEvent`. Sent when the emulator's game status is changed.
3) Input events: `InputAnalogEvent`, `InputButtonsEvent`. Sent in response to user's interaction with the PSP controls.
4) Stepping info events: `CpuSteppingEvent`, `CpuResumeEvent`. Sent once PPSSPP detects that the CPU status has changed.

You can subscribe to these groups by using the session's decorators.
```py
@session.log_handler()
async def log_broadcast(event: BaseEvent):
    event = cast(LogEvent, event)
    print(f"{event.timestamp}: {event.message}")
```

Lastly, there are events which are broadcast by PPSSPP as a feed response to a request. So far the only instance of this
behavior is the `gpu.stats.feed` request. To support this and also give you more control over how to handle
events in general, there is one last decorator: `session.listen_for(target)`
```py
@session.listen_for(GpuStatsGetEvent)
async def listener(event: BaseEvent):
    assert isinstance(event, GpuStatsGetEvent)
    report_stats(event)
```
Pass `None` for the target to install a so-called promiscuous listener that will be shown ALL events coming from PPSSPP.
> [!TIP]
> Return `True` from any handler to remove it from the list of handlers.
> This is not necessary for the ticket subscribers as they get removed automatically once PPSSPP answers.

### Sync API
The `AsyncConnection` is replaced by `Connection` with the same semantics and `AsyncSession` is replaced by `Session`.
The difference between `AsyncSession`'s and `Session`'s methods is that the latter doesn't let you register callbacks.
Instead, you can acquire an instance of class `QueueReader[BaseEvent]` by calling `session.get_queue()`.

You are supposed to manually react to the incoming events and implement your own state machine / observer to run handlers.
This is mostly because of the problems which arise from using `threading` in Python - it doesn't scale well.

`queue_reader.get()` (with optional timeout) returns the next item from the queue, `session.send_request{_raw}` methods
mimic the methods from `AsyncSession`, except they don't accept handlers.

## Tests
The unit tests can be run with `pytest`. I personally run them as `pytest . --asyncio-mode=auto`.
And when I want coverage, I do `pytest . --asyncio-mode=auto --cov --cov-report=html`.

## Contributing
PRs and Issues are always welcome! It also would mean a lot to me if anyone simply gives this library a try and
checks if it's convenient to use.