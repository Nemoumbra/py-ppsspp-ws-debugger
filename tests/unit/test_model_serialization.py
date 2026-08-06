import asyncio
import dataclasses

from ppsspp import AsyncSession
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
from ppsspp.model.requests.disassembly.common import (
    MemoryDisasmRequest, MemoryDisasmByCountRequest, MemoryDisasmByEndAddrRequest,
    MemorySearchDisasmRequest, MemoryAssembleRequest
)
from ppsspp.model.requests.game.common import GameResetRequest, GameStatusRequest
from ppsspp.model.requests.gpu.buffer import (
    GpuBufferScreenshotUriRequest, GpuBufferScreenshotBase64Request, GpuBufferScreenshotRequest,
    GpuBufferRenderColorRequest, GpuBufferRenderColorUriRequest, GpuBufferRenderColorBase64Request,
    GpuBufferRenderDepthRequest, GpuBufferRenderDepthUriRequest, GpuBufferRenderDepthBase64Request,
    GpuBufferRenderStencilRequest, GpuBufferRenderStencilUriRequest, GpuBufferRenderStencilBase64Request,
    GpuBufferTextureRequest, GpuBufferTextureUriRequest, GpuBufferTextureBase64Request, GpuBufferClutRequest,
    GpuBufferClutUriRequest, GpuBufferClutBase64Request
)
from ppsspp.model.requests.gpu.common import (
    GpuRecordDumpRequest, GpuStatsGetRequest, GpuStatsFeedRequest
)
from ppsspp.model.requests.hle.common import HleModuleListRequest, HleBacktraceRequest
from ppsspp.model.requests.hle.func import (
    HleFuncListRequest, HleFuncAddRequest, HleFuncRemoveRequest, HleFuncRemoveRangeRequest,
    HleFuncRenameRequest, HleFuncScanRequest
)
from ppsspp.model.requests.hle.thread import HleThreadListRequest, HleThreadWakeRequest, HleThreadStopRequest
from ppsspp.model.requests.input.analog import InputAnalogSendRequest
from ppsspp.model.requests.input.buttons import InputButtonsSendRequest, InputButtonsPressRequest
from ppsspp.model.requests.memory.common import (
    MemoryReadU8Request, MemoryReadU16Request, MemoryReadU32Request, MemoryReadRequest,
    MemoryReadStringRequest, MemoryReadStringUtf8Request, MemoryReadStringBase64Request,
    MemoryWriteU8Request, MemoryWriteU16Request, MemoryWriteU32Request, MemoryWriteRequest
)
from ppsspp.model.requests.memory.memory_info import (
    MemoryMappingRequest, MemoryInfoConfigRequest, MemoryInfoSetRequest,
    MemoryInfoListRequest, MemoryInfoSearchRequest
)
from ppsspp.model.requests.other.broadcast_config import BroadcastConfigGetRequest, BroadcastConfigSetRequest

from ppsspp.model.requests.other.version import VersionRequest
from ppsspp.model.requests.replay.common import (
    ReplayBeginRequest, ReplayAbortRequest, ReplayFlushRequest, ReplayExecuteRequest, ReplayStatusRequest
)
from ppsspp.model.requests.replay.time import ReplayTimeGetRequest, ReplayTimeSetRequest

from tests.unit.utils import MockStepByStepConnection


# TODO: fixture?

def get_requests() -> list[BaseRequest]:
    return [
        # Garbage data

        # Breakpoints
        CpuBreakpointAddRequest(address=0, enabled=None, log=None, condition=None, log_format=None),
        CpuBreakpointAddRequest(address=0, enabled=False, log=False, condition="true", log_format="0"),
        CpuBreakpointUpdateRequest(address=0, enabled=None, log=None, condition=None, log_format=None),
        CpuBreakpointUpdateRequest(address=0, enabled=False, log=False, condition="true", log_format="0"),
        CpuBreakpointRemoveRequest(address=0),
        CpuBreakpointListRequest(),
        MemoryBreakpointAddRequest(address=0, size=0, enabled=None, log=None, read=None, write=None, change=None,
                                   condition=None, log_format=None),
        MemoryBreakpointAddRequest(address=0, size=0, enabled=False, log=False, read=False, write=False, change=False,
                                   condition="true", log_format="0"),
        MemoryBreakpointUpdateRequest(address=0, size=0, enabled=None, log=None, read=None, write=None, change=None,
                                      condition=None, log_format=None),
        MemoryBreakpointUpdateRequest(address=0, size=0, enabled=False, log=False, read=False, write=False, change=False,
                                   condition="true", log_format="0"),
        MemoryBreakpointRemoveRequest(address=0, size=0),
        MemoryBreakpointListRequest(),

        # CPU
        CpuSteppingRequest(),
        CpuResumeRequest(),
        CpuStatusRequest(),
        CpuEvaluateRequest(thread=None, expression="expr"),
        CpuEvaluateRequest(thread=0, expression="expr"),
        CpuStepIntoRequest(thread=None),
        CpuStepIntoRequest(thread=0),
        CpuStepOverRequest(thread=None),
        CpuStepOverRequest(thread=0),
        CpuStepOutRequest(thread=None),
        CpuStepOutRequest(thread=0),
        CpuRunUntilRequest(address=0),
        CpuNextHleRequest(),

        CpuGetAllRegsRequest(thread=None),
        CpuGetAllRegsRequest(thread=0),
        CpuGetRegRequest(thread=None, name=None, category=None, register=None),
        CpuGetRegRequest(thread=0, name="name", category=0, register=0),
        CpuGetRegByNameRequest(thread=None, name="eax"),
        CpuGetRegByNameRequest(thread=0, name="eax"),
        CpuGetRegByIdxAndCategoryRequest(thread=None, category=0, register=0),
        CpuGetRegByIdxAndCategoryRequest(thread=0, category=0, register=0),
        CpuSetRegRequest(thread=None, name=None, category=None, register=None, value=0),
        CpuSetRegRequest(thread=0, name="name", category=0, register=0, value=0),
        CpuSetRegByNameRequest(thread=None, name="eax", value=0),
        CpuSetRegByNameRequest(thread=0, name="eax", value=0),
        CpuSetRegByIdxAndCategoryRequest(thread=None, category=0, register=0, value=0),
        CpuSetRegByIdxAndCategoryRequest(thread=0, category=0, register=0, value=0),

        # Disassembly
        MemoryDisasmRequest(thread=None, address=0, count=None, end=None, display_symbols=None),
        MemoryDisasmRequest(thread=0, address=0, count=0, end=0, display_symbols=False),
        MemoryDisasmByCountRequest(thread=None, address=0, count=0, display_symbols=None),
        MemoryDisasmByCountRequest(thread=0, address=0, count=0, display_symbols=False),
        MemoryDisasmByEndAddrRequest(thread=None, address=0, end=0, display_symbols=None),
        MemoryDisasmByEndAddrRequest(thread=0, address=0, end=0, display_symbols=False),
        MemorySearchDisasmRequest(thread=None, address=0, end=None, match="test", display_symbols=None),
        MemorySearchDisasmRequest(thread=0, address=0, end=0, match="test", display_symbols=False),
        MemoryAssembleRequest(address=0, code="nop"),

        # Game
        GameResetRequest(break_=None),
        GameResetRequest(break_=False),
        GameStatusRequest(),

        # GPU
        GpuBufferScreenshotRequest(type=None, alpha=None, stack_width=None),
        GpuBufferScreenshotRequest(type="uri", alpha=False, stack_width=0),
        GpuBufferScreenshotUriRequest(alpha=None, stack_width=None),
        GpuBufferScreenshotUriRequest(alpha=False, stack_width=0),
        GpuBufferScreenshotBase64Request(alpha=None, stack_width=None),
        GpuBufferScreenshotBase64Request(alpha=False, stack_width=0),
        GpuBufferRenderColorRequest(type=None, alpha=None, stack_width=None),
        GpuBufferRenderColorRequest(type="type", alpha=False, stack_width=0),
        GpuBufferRenderColorUriRequest(alpha=None, stack_width=None),
        GpuBufferRenderColorUriRequest(alpha=False, stack_width=0),
        GpuBufferRenderColorBase64Request(alpha=None, stack_width=None),
        GpuBufferRenderColorBase64Request(alpha=False, stack_width=0),
        GpuBufferRenderDepthRequest(type=None, alpha=None, stack_width=None),
        GpuBufferRenderDepthRequest(type="uri", alpha=False, stack_width=False),
        GpuBufferRenderDepthUriRequest(alpha=None, stack_width=None),
        GpuBufferRenderDepthUriRequest(alpha=False, stack_width=0),
        GpuBufferRenderDepthBase64Request(alpha=None, stack_width=None),
        GpuBufferRenderDepthBase64Request(alpha=False, stack_width=0),
        GpuBufferRenderStencilRequest(type=None, alpha=None, stack_width=None),
        GpuBufferRenderStencilRequest(type="uri", alpha=False, stack_width=0),
        GpuBufferRenderStencilUriRequest(alpha=None, stack_width=None),
        GpuBufferRenderStencilUriRequest(alpha=False, stack_width=0),
        GpuBufferRenderStencilBase64Request(alpha=None, stack_width=None),
        GpuBufferRenderStencilBase64Request(alpha=False, stack_width=0),
        GpuBufferTextureRequest(type=None, alpha=None, level=None, stack_width=None),
        GpuBufferTextureRequest(type="uri", alpha=False, level=0, stack_width=0),
        GpuBufferTextureUriRequest(alpha=None, level=None, stack_width=None),
        GpuBufferTextureUriRequest(alpha=False, level=0, stack_width=0),
        GpuBufferTextureBase64Request(alpha=None, level=None, stack_width=None),
        GpuBufferTextureBase64Request(alpha=False, level=0, stack_width=0),
        GpuBufferClutRequest(type=None, alpha=None, stack_width=None),
        GpuBufferClutRequest(type="uri", alpha=False, stack_width=0),
        GpuBufferClutUriRequest(alpha=None, stack_width=None),
        GpuBufferClutUriRequest(alpha=False, stack_width=0),
        GpuBufferClutBase64Request(alpha=None, stack_width=None),
        GpuBufferClutBase64Request(alpha=False, stack_width=0),
        GpuRecordDumpRequest(),
        GpuStatsGetRequest(),
        GpuStatsFeedRequest(enable=None),
        GpuStatsFeedRequest(enable=False),

        # HLE
        HleModuleListRequest(),
        HleBacktraceRequest(thread=None),
        HleBacktraceRequest(thread=0),
        HleFuncListRequest(),
        HleFuncAddRequest(address=0, size=None, name=None),
        HleFuncAddRequest(address=0, size=0, name="zz_func"),
        HleFuncRemoveRequest(address=0),
        HleFuncRemoveRangeRequest(address=0, size=0),
        HleFuncRenameRequest(address=0, name="new"),
        HleFuncScanRequest(address=0, size=0, remove=None),
        HleFuncScanRequest(address=0, size=0, remove=False),
        HleThreadListRequest(),
        HleThreadWakeRequest(thread=0),
        HleThreadStopRequest(thread=0),

        # Input
        InputAnalogSendRequest(x=0.0, y=0.0, stick=None),
        InputAnalogSendRequest(x=0.0, y=0.0, stick="left"),
        InputButtonsSendRequest(buttons={"A": False}),
        InputButtonsPressRequest(button="A", duration=None),
        InputButtonsPressRequest(button="A", duration=0),

        # Memory
        MemoryReadU8Request(address=0),
        MemoryReadU16Request(address=0),
        MemoryReadU32Request(address=0),
        MemoryReadRequest(address=0, size=0, replacements=None),
        MemoryReadRequest(address=0, size=0, replacements=False),
        MemoryReadStringRequest(address=0, type=None),
        MemoryReadStringRequest(address=0, type="utf8"),
        MemoryReadStringUtf8Request(address=0),
        MemoryReadStringBase64Request(address=0),
        MemoryWriteU8Request(address=0, value=0),
        MemoryWriteU16Request(address=0, value=0),
        MemoryWriteU32Request(address=0, value=0),
        MemoryWriteRequest(address=0, base64="abc"),
        MemoryMappingRequest(),
        MemoryInfoConfigRequest(detailed=None),
        MemoryInfoConfigRequest(detailed=False),
        MemoryInfoSetRequest(address=0, size=0, type="region", tag=None, pc=None),
        MemoryInfoSetRequest(address=0, size=0, type="region", tag="tag", pc=0),
        MemoryInfoListRequest(address=0, size=0, type=None),
        MemoryInfoListRequest(address=0, size=0, type="suballoc"),
        MemoryInfoSearchRequest(address=None, end=None, match="search", type=None),
        MemoryInfoSearchRequest(address=0, end=1, match="search", type="suballoc"),

        # Replay
        ReplayBeginRequest(),
        ReplayAbortRequest(),
        ReplayFlushRequest(),
        ReplayExecuteRequest(version=0, base64="abc"),
        ReplayStatusRequest(),
        ReplayTimeGetRequest(),
        ReplayTimeSetRequest(value=0),

        # Other
        VersionRequest(name=None, version=None),
        VersionRequest(name="me", version="first"),
        BroadcastConfigGetRequest(),
        BroadcastConfigSetRequest(disallowed={"key": False}),
    ]

# TODO: actually test all requests...


def with_ticket(request: BaseRequest, ticket: str):
    return dataclasses.replace(request, ticket=ticket)


async def test_serialization():
    # Sending requests

    session = AsyncSession()
    # No need for input
    connection = MockStepByStepConnection([], manual=True)
    await session.run(connection)

    requests = get_requests()
    ticket_requests = [with_ticket(req, f"TICKET{i}") for i, req in enumerate(requests)]

    for request in requests:
        await session.send_request(request)

    async def dummy_handler(ev: BaseEvent):
        pass

    for request in ticket_requests:
        await session.send_request(request, dummy_handler)

    await connection.close()
    pass
