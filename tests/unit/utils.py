import asyncio
import json
from collections import deque

from ppsspp.abstract_async_connection import AbstractAsyncPpssppConnection
from ppsspp.exceptions.connection_terminated import ConnectionTerminated


class MockConnection(AbstractAsyncPpssppConnection):
    def __init__(self, exhausted: asyncio.Event, events: list):
        super().__init__()

        self.gen = (event for event in events)
        self.exhausted = exhausted

    def _next(self):
        item = next(self.gen)
        return item

    async def recv(self):
        try:
            return self._next()
        except StopIteration:
            self.exhausted.set()
            raise ConnectionTerminated from None

    async def send(self, _):
        # Do nothing
        pass

    async def close(self):
        pass


class MockStepByStepConnection(AbstractAsyncPpssppConnection):
    def __init__(self, events: list, recv_requested: asyncio.Event | None = None, *, manual: bool):
        super().__init__()

        self.gen = (event for event in events)
        self.proceed_requested = asyncio.Event()
        self.recv_requested = recv_requested
        self.manual = manual

    def _next(self):
        item = next(self.gen)
        if isinstance(item, Exception):
            raise item
        return item

    async def recv(self):
        try:
            if self.recv_requested is not None:
                self.recv_requested.set()
            await self.proceed_requested.wait()
            self.proceed_requested.clear()
            return self._next()
        except StopIteration:
            raise ConnectionTerminated from None

    async def send(self, _):
        if self.manual:
            # Do nothing
            return
        self.proceed()

    def proceed(self):
        self.proceed_requested.set()

    async def close(self):
        self.proceed_requested.set()


class MockTicketMonitorConnection(AbstractAsyncPpssppConnection):
    def __init__(self, events: list[dict]):
        super().__init__()

        self.gen = (event for event in events)
        self.proceed_requested = asyncio.Event()
        self.tickets: deque[str] = deque()

    def _next(self):
        item = next(self.gen)
        return item

    async def recv(self) -> dict:
        try:
            await self.proceed_requested.wait()
            self.proceed_requested.clear()
            event = self._next()
            assert "ticket" not in event, "What are you doing with your tests?"
            # Inject the correct
            event["ticket"] = self.tickets.popleft()
            return event
        except StopIteration:
            raise ConnectionTerminated from None

    async def send(self, data: str):
        request = json.loads(data)
        assert isinstance(request, dict), "What are you doing with your tests?"
        assert "ticket" in request, "What are you doing with your tests?"
        ticket = request.get("ticket")
        assert ticket is not None, "What are you doing with your tests?"

        self.tickets.append(ticket)
        self.proceed()

    def proceed(self):
        self.proceed_requested.set()

    async def close(self):
        self.proceed_requested.set()


class MockRequestValidatorConnection(AbstractAsyncPpssppConnection):
    def __init__(self, events: list[dict]):
        super().__init__()

        self.gen = (event for event in events)
        self.proceed_requested = asyncio.Event()
        self.dict_requests = []

    def _next(self):
        item = next(self.gen)
        return item

    async def recv(self) -> dict:
        try:
            await self.proceed_requested.wait()
            self.proceed_requested.clear()
            event = self._next()
            return event
        except StopIteration:
            raise ConnectionTerminated from None

    async def send(self, data: str):
        request = json.loads(data)
        assert isinstance(request, dict), "What are you doing with your tests?"
        self.dict_requests.append(request)
        self.proceed()

    def proceed(self):
        self.proceed_requested.set()

    async def close(self):
        self.proceed_requested.set()

    def get_requests(self):
        return self.dict_requests
