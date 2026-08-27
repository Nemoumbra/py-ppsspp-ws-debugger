from abc import ABC, abstractmethod
from collections.abc import Callable, Awaitable

# Returns whether the connection was reestablished
AsyncOnDisconnectedHandler = Callable[['AsyncPpssppConnection'], Awaitable[bool]]


async def _default_on_disconnect_handler(connection: 'AbstractAsyncPpssppConnection'):
    return False


class AbstractAsyncPpssppConnection(ABC):
    def __init__(self):
        self._on_disconnected: AsyncOnDisconnectedHandler = _default_on_disconnect_handler

    def set_disconnected_handler(self, handler: AsyncOnDisconnectedHandler):
        self._on_disconnected = handler

    def on_disconnected(self, handler: AsyncOnDisconnectedHandler):
        # For some reason the wrong signature for the @ syntax doesn't trigger any warnings:
        # @connection.on_disconnected
        # def wrong(arg: int, value: str):
        #     return [1.5, 2.5]

        self.set_disconnected_handler(handler)
        return handler

    @abstractmethod
    def recv(self):
        """
        Attempts to receive the next websockets message and parse it as JSON.
        Might trigger the `on_disconnected` handler
        :return: whatever the message deserializes to from JSON
        """
        pass

    @abstractmethod
    def send(self, data):
        """
        Attempts to send the data into the websocket connection
        Might trigger the `on_disconnect` handler
        :param data: the text data to be sent
        :return: None
        """
        pass

    @abstractmethod
    def close(self):
        """
        Closes the underlying websockets connection (performs the closing handshake)
        :return:
        """
        pass