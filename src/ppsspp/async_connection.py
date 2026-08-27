import json
from collections.abc import Callable, Awaitable

import websockets
from websockets import ConnectionClosedOK, ConnectionClosed
from websockets.asyncio.client import ClientConnection

from ppsspp.abstract_async_connection import AbstractAsyncPpssppConnection
from ppsspp.exceptions.connection_terminated import ConnectionTerminated


class AsyncPpssppConnection(AbstractAsyncPpssppConnection):
    def __init__(self):
        super().__init__()
        self._ws: ClientConnection | None = None
        self.closed_ok = True
        self.close_info: ConnectionClosed | None = None

    async def connect(self, uri: str):
        """
        Attempts to connect to the provided URI, raises on failure.
        :param uri: the URI to be used for the connection
        :return: None
        """
        self._ws = await websockets.connect(uri, max_size=None)
        # I surely hope that no one can recv or send between these 2 lines.
        self.close_info = None

    async def _execute_action(self, action: Callable[[], Awaitable]):
        while True:
            try:
                return await action()

            # Using the properties 'close_code' or 'close_reason' is bad practice: it corresponds to the reader's
            # (client's) perspective, which may be misleading. Like if the app sends the close frame first,
            # then the server sends EOF and the event loop registers this as "connection closed" and
            # tells that to the websocket => you get ABNORMAL_CLOSURE.
            except ConnectionClosed as e:
                self.closed_ok = isinstance(e, ConnectionClosedOK)
                self.close_info = e
                if not await self._on_disconnected(self):
                    raise ConnectionTerminated from None

    async def recv(self):
        """
        Attempts to receive the next websockets message and parse it as JSON.
        Might trigger the `on_disconnected` handler
        :return: whatever the message deserializes to from JSON
        """
        data = await self._execute_action(lambda: self._ws.recv())
        return json.loads(data)

    async def send(self, data: str):
        """
        Attempts to send the data into the websocket connection
        Might trigger the `on_disconnect` handler
        :param data: the text data to be sent
        :return: None
        """
        await self._execute_action(lambda: self._ws.send(data))

    async def close(self):
        """
        Closes the underlying websockets connection (performs the closing handshake)
        :return:
        """
        if self._ws:
            await self._ws.close()
