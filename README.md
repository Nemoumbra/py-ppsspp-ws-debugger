
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

## Usage
The library present an asynchronous API (`asyncio` and [websockets](https://github.com/python-websockets/websockets)) 
and also the incomplete synchronous API ([websocket-client](https://github.com/websocket-client/websocket-client)).
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
This is the actual facade you have to use for communicating with PPSSPP.