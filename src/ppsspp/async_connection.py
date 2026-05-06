import json
from typing import Callable, Awaitable

import websockets
from websockets import ConnectionClosedOK, ConnectionClosedError
from websockets.asyncio.client import ClientConnection

from src.ppsspp.exceptions.connection_terminated import ConnectionTerminated

# Returns whether the connection was reestablished
AsyncOnDisconnectedHandler = Callable[['AsyncPpssppConnection'], Awaitable[bool]]

async def _default_on_disconnect_handler(connection: 'AsyncPpssppConnection'):
    return False

class AsyncPpssppConnection:
    def __init__(self):
        self._ws: ClientConnection | None = None
        self.closed_ok = True
        self.closed_code: int | None = None
        self.closed_reason: str | None = None

        self._on_disconnected: AsyncOnDisconnectedHandler = _default_on_disconnect_handler

    async def connect(self, uri: str):
        """
        Attempts to connect to the provided URI, raises on failure.
        :param uri: the URI to be used for the connection
        :return: None
        """
        self._ws = await websockets.connect(uri, max_size=None)

    def set_disconnected_handler(self, handler: AsyncOnDisconnectedHandler):
        self._on_disconnected = handler

    def on_disconnected(self, handler: AsyncOnDisconnectedHandler):
        # TODO: figure out why the wrong signature for the @ syntax doesn't trigger any warnings:
        # @connection.on_disconnected
        # def wrong(arg: int, value: str):
        #     return [1.5, 2.5]

        self.set_disconnected_handler(handler)
        return handler

    async def _execute_action(self, action: Callable[[], Awaitable]):
        while True:
            try:
                return await action()

            # TODO: actually look into 'e.sent', 'e.rcvd' and 'e.rcvd_then_sent' instead of ws properties
            # The latter seemingly corresponds to the reader's (client's) perspective, which may be misleading.
            # Like if the app sends the close frame first, then the server sends EOF and the event loop
            # registers this as "connection closed" and tells that to the websocket => you get ABNORMAL_CLOSURE.
            except ConnectionClosedOK as e:
                self.closed_ok = True
                self.closed_code = self._ws.close_code
                self.closed_reason = self._ws.close_reason
                if not await self._on_disconnected(self):
                    raise ConnectionTerminated from None
            except ConnectionClosedError as e:
                self.closed_ok = False
                self.closed_code = self._ws.close_code
                self.closed_reason = self._ws.close_reason
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
        await self._ws.close()
