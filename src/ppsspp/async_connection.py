
from typing import Callable, Awaitable

import websockets
from websockets import ConnectionClosedOK, ConnectionClosedError
from websockets.asyncio.client import ClientConnection

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
        self._ws = await websockets.connect(uri)

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
        try:
            return await action()
        except ConnectionClosedOK:
            self.closed_ok = True
            self.closed_code = self._ws.close_code
            self.closed_reason = self._ws.close_reason
            await self._on_disconnected(self)
        except ConnectionClosedError:
            self.closed_ok = False
            self.closed_code = self._ws.close_code
            self.closed_reason = self._ws.close_reason
            await self._on_disconnected(self)

    async def recv(self):
        return await self._execute_action(lambda: self._ws.recv())

    async def send(self, data: str):
        await self._execute_action(lambda: self._ws.send(data))

    async def close(self):
        await self._ws.close()
