
from websockets import connect, ClientConnection

class AsyncPpssppConnection:
    def __init__(self):
        self._ws: ClientConnection | None = None

    async def connect(self):
        pass

    async def recv(self):
        pass

    async def send(self, data: str):
        pass

    async def close(self):
        pass
