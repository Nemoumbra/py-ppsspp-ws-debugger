import websockets.sync.client as websockets_sync
import websockets
from typing import Callable

import json
from ppsspp.exceptions.connection_terminated import ConnectionTerminated


# Returns whether the connection was reestablished
OnDisconnectedHandler = Callable[['PpssppConnection'], bool]


class PpssppConnection:
    def __init__(self):
        self._on_disconnected: OnDisconnectedHandler = lambda connection: False
        self._ws: websockets_sync.ClientConnection | None = None

        self.closed_ok = True
        self.close_info: websockets.ConnectionClosed | None = None

    def set_disconnected_handler(self, handler: OnDisconnectedHandler):
        self._on_disconnected = handler

    def on_disconnected(self, handler: OnDisconnectedHandler):
        # TODO: figure out why the wrong signature for the @ syntax doesn't trigger any warnings:
        # @connection.on_disconnected
        # def wrong(arg: int, value: str):
        #     return [1.5, 2.5]

        self.set_disconnected_handler(handler)
        return handler

    def connect(self, uri: str):
        self._ws = websockets_sync.connect(uri, max_size=None, ping_timeout=None)
        # I surely hope that no one can recv or send between these 2 lines.
        self.close_info = None

    def _execute_action(self, action: Callable):
        while True:
            try:
                return action()
            except websockets.ConnectionClosed as e:
                self.closed_ok = isinstance(e, websockets.ConnectionClosedOK)
                self.close_info = e
                if not self._on_disconnected(self):
                    raise ConnectionTerminated from None

    def recv(self):
        data = self._execute_action(lambda: self._ws.recv())
        # Note: this may raise if PPSSPP goes mad and sends us invalid JSON
        return json.loads(data)

    def send(self, data: str):
        self._execute_action(lambda: self._ws.send(data))

    def close(self):
        if self._ws:
            self._ws.close()
