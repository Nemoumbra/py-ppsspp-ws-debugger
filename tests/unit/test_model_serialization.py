import asyncio
import dataclasses

from ppsspp import AsyncSession
from ppsspp.exceptions.connection_terminated import ConnectionTerminated
from ppsspp.model.events.base_event import BaseEvent
from ppsspp.model.ppsspp_objects.logs.log_level import LogLevel
from ppsspp.model.requests.base_request import BaseRequest
from ppsspp.model.requests.breakpoints.cpu import (
    CpuBreakpointAddRequest, CpuBreakpointUpdateRequest, CpuBreakpointRemoveRequest, CpuBreakpointListRequest
)
from ppsspp.model.requests.breakpoints.memory import (
    MemoryBreakpointAddRequest, MemoryBreakpointUpdateRequest, MemoryBreakpointRemoveRequest,
    MemoryBreakpointListRequest
)
from ppsspp.model.requests.cpu.common import (
    CpuSteppingRequest, CpuResumeRequest, CpuStatusRequest, CpuEvaluateRequest
)
from ppsspp.model.requests.cpu.debugging import (
    CpuStepIntoRequest, CpuStepOverRequest, CpuStepOutRequest, CpuRunUntilRequest, CpuNextHleRequest
)
from ppsspp.model.requests.cpu.registers import (
    CpuGetAllRegsRequest, CpuGetRegRequest, CpuGetRegByNameRequest, CpuGetRegByIdxAndCategoryRequest,
    CpuSetRegRequest, CpuSetRegByNameRequest, CpuSetRegByIdxAndCategoryRequest
)
from ppsspp.model.requests.other.version import VersionRequest


# TODO: find a better place for this class (it's duplicated)
class MockConnection:
    def __init__(self, exhausted: asyncio.Event, events: list):
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


# TODO: fixture?

def get_requests() -> list[BaseRequest]:
    return [
        # Garbage data

        # Breakpoints
        CpuBreakpointAddRequest(address=0, enabled=None, log=None, condition=None, log_format=None),
        CpuBreakpointUpdateRequest(address=0, enabled=None, log=None, condition=None, log_format=None),
        CpuBreakpointRemoveRequest(address=0),
        CpuBreakpointListRequest(),
        MemoryBreakpointAddRequest(address=0, size=0, enabled=None, log=None, read=None, write=None, change=None,
                                   condition=None, log_format=None),
        MemoryBreakpointUpdateRequest(address=0, size=0, enabled=None, log=None, read=None, write=None, change=None,
                                      condition=None, log_format=None),
        MemoryBreakpointRemoveRequest(address=0, size=0),
        MemoryBreakpointListRequest(),

        # CPU
        CpuSteppingRequest(),
        CpuResumeRequest(),
        CpuStatusRequest(),
        CpuEvaluateRequest(thread=None, expression="expr"),
        CpuStepIntoRequest(thread=None),
        CpuStepOverRequest(thread=None),
        CpuStepOutRequest(thread=None),
        CpuRunUntilRequest(address=0),
        CpuNextHleRequest(),
        CpuGetAllRegsRequest(thread=None),
        CpuGetRegRequest(thread=None, name=None, category=None, register=None),
        CpuGetRegByNameRequest(thread=None, name="eax"),
        CpuGetRegByIdxAndCategoryRequest(thread=None, category=0, register=0),
        CpuSetRegRequest(thread=None, name=None, category=None, register=None, value=0),
        CpuSetRegByNameRequest(thread=None, name="eax", value=0),
        CpuSetRegByIdxAndCategoryRequest(thread=None, category=0, register=0, value=0),

        # Disassembly

        # Game

        # GPU

        # HLE

        # Input
        # Memory

        # Replay


        # Other
        VersionRequest(name=None, version=None),
        VersionRequest(name="me", version="first"),

    ]

# TODO: actually test all requests...


def with_ticket(request: BaseRequest, ticket: str):
    return dataclasses.replace(request, ticket=ticket)


async def test_serialization():
    # Sending requests

    session = AsyncSession()
    # No need for input
    connection = MockConnection(asyncio.Event(), [])
    await session.run(connection)

    requests = get_requests()
    ticket_requests = [with_ticket(req, f"TICKET{i}") for i, req in enumerate(requests)]

    for request in requests:
        await session.send_request(request)

    async def dummy_handler(ev: BaseEvent):
        pass

    for request in ticket_requests:
        await session.send_request(request, dummy_handler)

    pass
