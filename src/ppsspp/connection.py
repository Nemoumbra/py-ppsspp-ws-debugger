from websocket import (
    WebSocket, WebSocketConnectionClosedException, WebSocketException,
    ABNF, STATUS_STATUS_NOT_AVAILABLE
)
from typing import Callable

import json
from src.ppsspp.exceptions.connection_terminated import ConnectionTerminated


OnDisconnectedHandler = Callable[['PpssppConnection'], bool]


class PpssppConnection:
    def __init__(self):
        self._on_disconnected: OnDisconnectedHandler = lambda connection: False
        self._ws: WebSocket = WebSocket()

        self.close_code: int | None = None
        self.reason: str | None = None

    def set_disconnected_handler(self, handler: OnDisconnectedHandler):
        self._on_disconnected = handler

    def connect(self, uri: str):
        self._ws.connect(uri)

    def recv(self):
        while True:
            try:
                received: bytes
                opcode, received = self._ws.recv_data()
                if opcode == ABNF.OPCODE_TEXT:
                    # Text has to be decoded
                    data = received.decode("utf-8", errors="replace")
                    break
                elif opcode == ABNF.OPCODE_CLOSE:
                    # It's a close frame. Let's parse it:
                    if len(received) >= 2:
                        self.close_code = int.from_bytes(received[0:2])
                        self.reason = received[2:]
                    elif len(received) == 0:
                        # IDK if it's the correct behavior, but that's what some libs do
                        self.close_code = STATUS_STATUS_NOT_AVAILABLE
                        self.reason = None
                    else:
                        # len == 1, that's just malformed
                        self.close_code = None
                        self.reason = None

                    go_on = self._on_disconnected(self)
                    # Reset the fields
                    self.close_code = self.reason = None
                    if not go_on:
                        raise ConnectionTerminated()

                    # Okay, let's try it one more time
                    continue
                elif opcode == ABNF.OPCODE_BINARY:
                    # This really shouldn't happen with PPSSPP
                    raise RuntimeError("Unexpected binary data from the server!")

            except (OSError, ConnectionResetError, WebSocketConnectionClosedException):
                # I don't know why yet, but I got 'OSError: [WinError 10038]' twice
                # TODO: investigate the causes

                go_on = self._on_disconnected(self)
                # Reset the fields
                self.close_code = self.reason = None
                if not go_on:
                    raise
                continue

        # Successfully read the data

        # Note: this may raise if PPSSPP goes mad and sends us invalid JSON
        return json.loads(data)

    def send(self, data: str):
        while True:
            try:
                self._ws.send(data)
                return
            except WebSocketConnectionClosedException:
                reconnect = self._on_disconnected(self)
                if not reconnect:
                    raise

    def close(self):
        self._ws.close()