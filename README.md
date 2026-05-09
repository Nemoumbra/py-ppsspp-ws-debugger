
# Python websocket debugger for PPSSPP
This library provides low- and middle-level primitives for interacting with PPSSPP's remote websocket debugger API.
*Note: the project is in its alpha stage.*

## Installation
Right now there's no distribution available at pypi.org, so you'll have to install it from here.
Either `pip install git+https://github.com/Nemoumbra/py-ppsspp-ws-debugger.git@master`
(pip is smart enough to install from GitHub) or clone the repository and do a local installation.
This package is using `setuptools` so make sure it's present and not too old.

---
If your PyCharm is struggling with the package installed as editable, try reinstalling with this command instead: `pip install -e /path/to/cloned/repo --config-settings editable_mode=compat`.

## PPSSPP API
The only documentation available is located in comments in PPSSPP's source code.
The description of the system is [here](https://github.com/hrydgard/ppsspp/blob/master/Core/Debugger/WebSocket.cpp). The detailed info on the available
requests and expected responses is documented in the `.cpp` files inside [this directory](https://github.com/hrydgard/ppsspp/tree/master/Core/Debugger/WebSocket).
This library doesn't force you to operate on JSONs, instead, serialization and deserialization is used.

## Model
The objects in the model are defined as dataclasses.
`ppsspp.model.ppsspp_objects` contains the building blocks for many PPSSPP events (often sent as responses to requests, but sometimes broadcast randomly).
`ppsspp.model.events` contains the actual event bodies. There is a special event that PPSSPP sends if it's unable to process the request: `ErrorEvent`.
All events inherit from the base class `BaseEvent`, which stores the string name of the event and the optional ticket.
This library uses [adaptix](https://github.com/reagento/adaptix) as a data model conversion library.

## Usage
The library presents an asynchronous API (`asyncio` and [websockets](https://github.com/python-websockets/websockets))
and also an incomplete synchronous API ([websocket-client](https://github.com/websocket-client/websocket-client)).
Let's focus on the async API.

The classes you need are `AsyncSession` and `AsyncConnection`.

### AsyncConnection
`AsyncConnection` encapsulates the connection from your device to PPSSPP. This library not provide any means of acquiring the correct URI for connecting to PPSSPP.
It is entirely up to you: read it from your config file or let the user decide.
Perhaps, contact `report.ppsspp.org/match/list` by using your favorite HTTP library? More on that later.

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
    else:
        notify_user("connection closed with error")
    try:
        await conn.connect(uri)
        return True
    except:
        return False
```
The connection has some public fields which are used to get the detailed info on the disconnect reasons. TODO: finalize the API.

### AsyncSession
This is the actual facade you have to use for communicating with PPSSPP. Create an instance, then await a call to `run(connection)`.
The code assumes that the connection has been opened prior to calling `run`. This kicks off the internal tasks of the session
which recv from the connection, deserialize the events coming from PPSSPP, store them for later processing into a queue,
drain the queue and invoke event handlers if necessary.

Call `await session.stop()` to fully shut down the internals and the connection. Of course, it will trigger the `on_disconnected` handler. Reconnecting is meaningless at that point:
the internal queue will be closed by then, so the session will shut down nonetheless. Just return `False`.

#### Issuing requests to PPSSPP:
The low-level method of sending requests to PPSSPP involves calling `session.send_request` with an instance of class `PPSSPPRequest`. Check the source code for its creation API.
```py
async def install_breakpoint(session: AsyncSession, address: int):
    request = PPSSPPRequest("cpu.breakpoint.add")
    request.add(address=address, enabled=True)

    await self.session.send_request(request)
```
There is also a second argument, defaulting to `None`, which is a response handler.
If a handler is provided and request contains a ticket, schedules the handler once PPSSPP echoes the same ticket in one of the events.
If a handler is provided with no ticket, the session generates a ticket automatically.
```py
AsyncEventHandler = Callable[[BaseEvent], Awaitable]
```
The mid-level API is `await session.execute_unchecked(request)`. This returns the event sent in response to your request (maybe `ErrorEvent`).
> [!WARNING]
> PPSSPP may not respond to certain events at all! This may cause `execute_unchecked` to hang!
So far there are only [2 such commands](https://github.com/hrydgard/ppsspp/blob/master/Core/Debugger/WebSocket/CPUCoreSubscriber.cpp): `cpu.resume` and `cpu.stepping`.
So don't use `execute_unchecked` for them, use the low-level API.

Lastly, there is `await session.execute(request)`. It raises `RequestFailedError` if the returned event happens to be `ErrorEvent`.
This way is kind of more Pythonic than operating on error objects.
You can inspect the fields `error` for the error event and `failed_request` to inspect the `PPSSPPRequest` that failed.