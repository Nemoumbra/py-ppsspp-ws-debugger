import asyncio
import dataclasses
from dataclasses import dataclass

from ppsspp import AsyncSession
from ppsspp.model.events.base_event import BaseEvent
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

from tests.unit.utils import MockRequestValidatorConnection


@dataclass
class RequestTest:
    value: BaseRequest
    expected: dict


def get_request_tests():
    return [
        # Garbage data?
        # TODO: make sure the requests can be constructed without explicitly passing None for optional args

        # Breakpoints
        RequestTest(
            value=CpuBreakpointAddRequest(address=0, enabled=None, log=None, condition=None, log_format=None),
            expected={"event": "cpu.breakpoint.add", "address": 0}
        ),
        RequestTest(
            value=CpuBreakpointAddRequest(address=0, enabled=False, log=False, condition="true", log_format="0"),
            expected={"event": "cpu.breakpoint.add", "address": 0, "enabled": False, "log": False, "condition": "true", "logFormat": "0"}
        ),
        RequestTest(
            value=CpuBreakpointUpdateRequest(address=0, enabled=None, log=None, condition=None, log_format=None),
            expected={"event": "cpu.breakpoint.update", "address": 0}
        ),
        RequestTest(
            value=CpuBreakpointUpdateRequest(address=0, enabled=False, log=False, condition="true", log_format="0"),
            expected={"event": "cpu.breakpoint.update", "address": 0, "enabled": False, "log": False, "condition": "true", "logFormat": "0"}
        ),
        RequestTest(
            value=CpuBreakpointRemoveRequest(address=0),
            expected={"event": "cpu.breakpoint.remove", "address": 0}
        ),
        RequestTest(
            value=CpuBreakpointListRequest(),
            expected={"event": "cpu.breakpoint.list"}
        ),
        RequestTest(
            value=MemoryBreakpointAddRequest(address=0, size=0, enabled=None, log=None, read=None, write=None, change=None, condition=None, log_format=None),
            expected={"event": "memory.breakpoint.add", "address": 0, "size": 0}
        ),
        RequestTest(
            value=MemoryBreakpointAddRequest(address=0, size=0, enabled=False, log=False, read=False, write=False, change=False, condition="true", log_format="0"),
            expected={"event": "memory.breakpoint.add", "address": 0, "size": 0, "enabled": False, "log": False, "read": False, "write": False, "change": False, "condition": "true", "logFormat": "0"}
        ),
        RequestTest(
            value=MemoryBreakpointUpdateRequest(address=0, size=0, enabled=None, log=None, read=None, write=None, change=None, condition=None, log_format=None),
            expected={"event": "memory.breakpoint.update", "address": 0, "size": 0}
        ),
        RequestTest(
            value=MemoryBreakpointUpdateRequest(address=0, size=0, enabled=False, log=False, read=False, write=False, change=False, condition="true", log_format="0"),
            expected={"event": "memory.breakpoint.update", "address": 0, "size": 0, "enabled": False, "log": False, "read": False, "write": False, "change": False, "condition": "true", "logFormat": "0"}
        ),
        RequestTest(
            value=MemoryBreakpointRemoveRequest(address=0, size=0),
            expected={"event": "memory.breakpoint.remove", "address": 0, "size": 0}
        ),
        RequestTest(
            value=MemoryBreakpointListRequest(),
            expected={"event": "memory.breakpoint.list"}
        ),

        # CPU
        RequestTest(
            value=CpuSteppingRequest(),
            expected={"event": "cpu.stepping"}
        ),
        RequestTest(
            value=CpuResumeRequest(),
            expected={"event": "cpu.resume"}
        ),
        RequestTest(
            value=CpuStatusRequest(),
            expected={"event": "cpu.status"}
        ),
        RequestTest(
            value=CpuEvaluateRequest(thread=None, expression="expr"),
            expected={"event": "cpu.evaluate", "expression": "expr"}
        ),
        RequestTest(
            value=CpuEvaluateRequest(thread=0, expression="expr"),
            expected={"event": "cpu.evaluate", "thread": 0, "expression": "expr"}
        ),
        RequestTest(
            value=CpuStepIntoRequest(thread=None),
            expected={"event": "cpu.stepInto"}
        ),
        RequestTest(
            value=CpuStepIntoRequest(thread=0),
            expected={"event": "cpu.stepInto", "thread": 0}
        ),
        RequestTest(
            value=CpuStepOverRequest(thread=None),
            expected={"event": "cpu.stepOver"}
        ),
        RequestTest(
            value=CpuStepOverRequest(thread=0),
            expected={"event": "cpu.stepOver", "thread": 0}
        ),
        RequestTest(
            value=CpuStepOutRequest(thread=None),
            expected={"event": "cpu.stepOut"}
        ),
        RequestTest(
            value=CpuStepOutRequest(thread=0),
            expected={"event": "cpu.stepOut", "thread": 0}
        ),
        RequestTest(
            value=CpuRunUntilRequest(address=0),
            expected={"event": "cpu.runUntil", "address": 0}
        ),
        RequestTest(
            value=CpuNextHleRequest(),
            expected={"event": "cpu.nextHLE"}
        ),

        RequestTest(
            value=CpuGetAllRegsRequest(thread=None),
            expected={"event": "cpu.getAllRegs"}
        ),
        RequestTest(
            value=CpuGetAllRegsRequest(thread=0),
            expected={"event": "cpu.getAllRegs", "thread": 0}
        ),
        RequestTest(
            value=CpuGetRegRequest(thread=None, name=None, category=None, register=None),
            expected={"event": "cpu.getReg"}
        ),
        RequestTest(
            value=CpuGetRegRequest(thread=0, name="name", category=0, register=0),
            expected={"event": "cpu.getReg", "thread": 0, "name": "name", "category": 0, "register": 0}
        ),
        RequestTest(
            value=CpuGetRegByNameRequest(thread=None, name="eax"),
            expected={"event": "cpu.getReg", "name": "eax"}
        ),
        RequestTest(
            value=CpuGetRegByNameRequest(thread=0, name="eax"),
            expected={"event": "cpu.getReg", "thread": 0, "name": "eax"}
        ),
        RequestTest(
            value=CpuGetRegByIdxAndCategoryRequest(thread=None, category=0, register=0),
            expected={"event": "cpu.getReg", "category": 0, "register": 0}
        ),
        RequestTest(
            value=CpuGetRegByIdxAndCategoryRequest(thread=0, category=0, register=0),
            expected={"event": "cpu.getReg", "thread": 0, "category": 0, "register": 0}
        ),
        RequestTest(
            value=CpuSetRegRequest(thread=None, name=None, category=None, register=None, value=0),
            expected={"event": "cpu.setReg", "value": 0}
        ),
        RequestTest(
            value=CpuSetRegRequest(thread=0, name="name", category=0, register=0, value=0),
            expected={"event": "cpu.setReg", "thread": 0, "name": "name", "category": 0, "register": 0, "value": 0}
        ),
        RequestTest(
            value=CpuSetRegByNameRequest(thread=None, name="eax", value=0),
            expected={"event": "cpu.setReg", "name": "eax", "value": 0}
        ),
        RequestTest(
            value=CpuSetRegByNameRequest(thread=0, name="eax", value=0),
            expected={"event": "cpu.setReg", "thread": 0, "name": "eax", "value": 0}
        ),
        RequestTest(
            value=CpuSetRegByIdxAndCategoryRequest(thread=None, category=0, register=0, value=0),
            expected={"event": "cpu.setReg", "category": 0, "register": 0, "value": 0}
        ),
        RequestTest(
            value=CpuSetRegByIdxAndCategoryRequest(thread=0, category=0, register=0, value=0),
            expected={"event": "cpu.setReg", "thread": 0, "category": 0, "register": 0, "value": 0}
        ),

        # Disassembly
        RequestTest(
            value=MemoryDisasmRequest(thread=None, address=0, count=None, end=None, display_symbols=None),
            expected={"event": "memory.disasm", "address": 0}
        ),
        RequestTest(
            value=MemoryDisasmRequest(thread=0, address=0, count=0, end=0, display_symbols=False),
            expected={"event": "memory.disasm", "thread": 0, "address": 0, "count": 0, "end": 0, "displaySymbols": False}
        ),
        RequestTest(
            value=MemoryDisasmByCountRequest(thread=None, address=0, count=0, display_symbols=None),
            expected={"event": "memory.disasm", "address": 0, "count": 0}
        ),
        RequestTest(
            value=MemoryDisasmByCountRequest(thread=0, address=0, count=0, display_symbols=False),
            expected={"event": "memory.disasm", "thread": 0, "address": 0, "count": 0, "displaySymbols": False}
        ),
        RequestTest(
            value=MemoryDisasmByEndAddrRequest(thread=None, address=0, end=0, display_symbols=None),
            expected={"event": "memory.disasm", "address": 0, "end": 0}
        ),
        RequestTest(
            value=MemoryDisasmByEndAddrRequest(thread=0, address=0, end=0, display_symbols=False),
            expected={"event": "memory.disasm", "thread": 0, "address": 0, "end": 0, "displaySymbols": False}
        ),
        RequestTest(
            value=MemorySearchDisasmRequest(thread=None, address=0, end=None, match="test", display_symbols=None),
            expected={"event": "memory.searchDisasm", "address": 0, "match": "test"}
        ),
        RequestTest(
            value=MemorySearchDisasmRequest(thread=0, address=0, end=0, match="test", display_symbols=False),
            expected={"event": "memory.searchDisasm", "thread": 0, "address": 0, "end": 0, "match": "test", "displaySymbols": False}
        ),
        RequestTest(
            value=MemoryAssembleRequest(address=0, code="nop"),
            expected={"event": "memory.assemble", "address": 0, "code": "nop"}
        ),

        # Game
        RequestTest(
            value=GameResetRequest(break_=None),
            expected={"event": "game.reset"}
        ),
        RequestTest(
            value=GameResetRequest(break_=False),
            expected={"event": "game.reset", "break": False}
        ),
        RequestTest(
            value=GameStatusRequest(),
            expected={"event": "game.status"}
        ),

        # GPU
        RequestTest(
            value=GpuBufferScreenshotRequest(type=None, alpha=None, stack_width=None),
            expected={"event": "gpu.buffer.screenshot"}
        ),
        RequestTest(
            value=GpuBufferScreenshotRequest(type="uri", alpha=False, stack_width=0),
            expected={"event": "gpu.buffer.screenshot", "type": "uri", "alpha": False, "stackWidth": 0}
        ),
        RequestTest(
            value=GpuBufferScreenshotUriRequest(alpha=None, stack_width=None),
            expected={"event": "gpu.buffer.screenshot"}
        ),
        RequestTest(
            value=GpuBufferScreenshotUriRequest(alpha=False, stack_width=0),
            expected={"event": "gpu.buffer.screenshot", "alpha": False, "stackWidth": 0}
        ),
        RequestTest(
            value=GpuBufferScreenshotBase64Request(alpha=None, stack_width=None),
            expected={"event": "gpu.buffer.screenshot", "type": "base64"}
        ),
        RequestTest(
            value=GpuBufferScreenshotBase64Request(alpha=False, stack_width=0),
            expected={"event": "gpu.buffer.screenshot", "alpha": False, "stackWidth": 0, "type": "base64"}
        ),
        RequestTest(
            value=GpuBufferRenderColorRequest(type=None, alpha=None, stack_width=None),
            expected={"event": "gpu.buffer.renderColor"}
        ),
        RequestTest(
            value=GpuBufferRenderColorRequest(type="uri", alpha=False, stack_width=0),
            expected={"event": "gpu.buffer.renderColor", "type": "uri", "alpha": False, "stackWidth": 0}
        ),
        RequestTest(
            value=GpuBufferRenderColorUriRequest(alpha=None, stack_width=None),
            expected={"event": "gpu.buffer.renderColor"}
        ),
        RequestTest(
            value=GpuBufferRenderColorUriRequest(alpha=False, stack_width=0),
            expected={"event": "gpu.buffer.renderColor", "alpha": False, "stackWidth": 0}
        ),
        RequestTest(
            value=GpuBufferRenderColorBase64Request(alpha=None, stack_width=None),
            expected={"event": "gpu.buffer.renderColor", "type": "base64"}
        ),
        RequestTest(
            value=GpuBufferRenderColorBase64Request(alpha=False, stack_width=0),
            expected={"event": "gpu.buffer.renderColor", "alpha": False, "stackWidth": 0, "type": "base64"}
        ),
        RequestTest(
            value=GpuBufferRenderDepthRequest(type=None, alpha=None, stack_width=None),
            expected={"event": "gpu.buffer.renderDepth"}
        ),
        RequestTest(
            value=GpuBufferRenderDepthRequest(type="uri", alpha=False, stack_width=False),
            expected={"event": "gpu.buffer.renderDepth", "type": "uri", "alpha": False, "stackWidth": False}
        ),
        RequestTest(
            value=GpuBufferRenderDepthUriRequest(alpha=None, stack_width=None),
            expected={"event": "gpu.buffer.renderDepth"}
        ),
        RequestTest(
            value=GpuBufferRenderDepthUriRequest(alpha=False, stack_width=0),
            expected={"event": "gpu.buffer.renderDepth", "alpha": False, "stackWidth": 0}
        ),
        RequestTest(
            value=GpuBufferRenderDepthBase64Request(alpha=None, stack_width=None),
            expected={"event": "gpu.buffer.renderDepth", "type": "base64"}
        ),
        RequestTest(
            value=GpuBufferRenderDepthBase64Request(alpha=False, stack_width=0),
            expected={"event": "gpu.buffer.renderDepth", "alpha": False, "stackWidth": 0, "type": "base64"}
        ),
        RequestTest(
            value=GpuBufferRenderStencilRequest(type=None, alpha=None, stack_width=None),
            expected={"event": "gpu.buffer.renderStencil"}
        ),
        RequestTest(
            value=GpuBufferRenderStencilRequest(type="uri", alpha=False, stack_width=0),
            expected={"event": "gpu.buffer.renderStencil", "type": "uri", "alpha": False, "stackWidth": 0}
        ),
        RequestTest(
            value=GpuBufferRenderStencilUriRequest(alpha=None, stack_width=None),
            expected={"event": "gpu.buffer.renderStencil"}
        ),
        RequestTest(
            value=GpuBufferRenderStencilUriRequest(alpha=False, stack_width=0),
            expected={"event": "gpu.buffer.renderStencil", "alpha": False, "stackWidth": 0}
        ),
        RequestTest(
            value=GpuBufferRenderStencilBase64Request(alpha=None, stack_width=None),
            expected={"event": "gpu.buffer.renderStencil", "type": "base64"}
        ),
        RequestTest(
            value=GpuBufferRenderStencilBase64Request(alpha=False, stack_width=0),
            expected={"event": "gpu.buffer.renderStencil", "alpha": False, "stackWidth": 0, "type": "base64"}
        ),
        RequestTest(
            value=GpuBufferTextureRequest(type=None, alpha=None, level=None, stack_width=None),
            expected={"event": "gpu.buffer.texture"}
        ),
        RequestTest(
            value=GpuBufferTextureRequest(type="uri", alpha=False, level=0, stack_width=0),
            expected={"event": "gpu.buffer.texture", "type": "uri", "alpha": False, "level": 0, "stackWidth": 0}
        ),
        RequestTest(
            value=GpuBufferTextureUriRequest(alpha=None, level=None, stack_width=None),
            expected={"event": "gpu.buffer.texture"}
        ),
        RequestTest(
            value=GpuBufferTextureUriRequest(alpha=False, level=0, stack_width=0),
            expected={"event": "gpu.buffer.texture", "alpha": False, "level": 0, "stackWidth": 0}
        ),
        RequestTest(
            value=GpuBufferTextureBase64Request(alpha=None, level=None, stack_width=None),
            expected={"event": "gpu.buffer.texture", "type": "base64"}
        ),
        RequestTest(
            value=GpuBufferTextureBase64Request(alpha=False, level=0, stack_width=0),
            expected={"event": "gpu.buffer.texture", "alpha": False, "level": 0, "stackWidth": 0, "type": "base64"}
        ),
        RequestTest(
            value=GpuBufferClutRequest(type=None, alpha=None, stack_width=None),
            expected={"event": "gpu.buffer.clut"}
        ),
        RequestTest(
            value=GpuBufferClutRequest(type="uri", alpha=False, stack_width=0),
            expected={"event": "gpu.buffer.clut", "type": "uri", "alpha": False, "stackWidth": 0}
        ),
        RequestTest(
            value=GpuBufferClutUriRequest(alpha=None, stack_width=None),
            expected={"event": "gpu.buffer.clut"}
        ),
        RequestTest(
            value=GpuBufferClutUriRequest(alpha=False, stack_width=0),
            expected={"event": "gpu.buffer.clut", "alpha": False, "stackWidth": 0}
        ),
        RequestTest(
            value=GpuBufferClutBase64Request(alpha=None, stack_width=None),
            expected={"event": "gpu.buffer.clut", "type": "base64"}
        ),
        RequestTest(
            value=GpuBufferClutBase64Request(alpha=False, stack_width=0),
            expected={"event": "gpu.buffer.clut", "alpha": False, "stackWidth": 0, "type": "base64"}
        ),
        RequestTest(
            value=GpuRecordDumpRequest(),
            expected={"event": "gpu.record.dump"}
        ),
        RequestTest(
            value=GpuStatsGetRequest(),
            expected={"event": "gpu.stats.get"}
        ),
        RequestTest(
            value=GpuStatsFeedRequest(enable=None),
            expected={"event": "gpu.stats.feed"}
        ),
        RequestTest(
            value=GpuStatsFeedRequest(enable=False),
            expected={"event": "gpu.stats.feed", "enable": False}
        ),

        # HLE
        RequestTest(
            value=HleModuleListRequest(),
            expected={"event": "hle.module.list"}
        ),
        RequestTest(
            value=HleBacktraceRequest(thread=None),
            expected={"event": "hle.backtrace"}
        ),
        RequestTest(
            value=HleBacktraceRequest(thread=0),
            expected={"event": "hle.backtrace", "thread": 0}
        ),
        RequestTest(
            value=HleFuncListRequest(),
            expected={"event": "hle.func.list"}
        ),
        RequestTest(
            value=HleFuncAddRequest(address=0, size=None, name=None),
            expected={"event": "hle.func.add", "address": 0}
        ),
        RequestTest(
            value=HleFuncAddRequest(address=0, size=0, name="zz_func"),
            expected={"event": "hle.func.add", "address": 0, "size": 0, "name": "zz_func"}
        ),
        RequestTest(
            value=HleFuncRemoveRequest(address=0),
            expected={"event": "hle.func.remove", "address": 0}
        ),
        RequestTest(
            value=HleFuncRemoveRangeRequest(address=0, size=0),
            expected={"event": "hle.func.removeRange", "address": 0, "size": 0}
        ),
        RequestTest(
            value=HleFuncRenameRequest(address=0, name="new"),
            expected={"event": "hle.func.rename", "address": 0, "name": "new"}
        ),
        RequestTest(
            value=HleFuncScanRequest(address=0, size=0, remove=None),
            expected={"event": "hle.func.scan", "address": 0, "size": 0}
        ),
        RequestTest(
            value=HleFuncScanRequest(address=0, size=0, remove=False),
            expected={"event": "hle.func.scan", "address": 0, "size": 0, "remove": False}
        ),
        RequestTest(
            value=HleThreadListRequest(),
            expected={"event": "hle.thread.list"}
        ),
        RequestTest(
            value=HleThreadWakeRequest(thread=0),
            expected={"event": "hle.thread.wake", "thread": 0}
        ),
        RequestTest(
            value=HleThreadStopRequest(thread=0),
            expected={"event": "hle.thread.stop", "thread": 0}
        ),

        # Input
        RequestTest(
            value=InputAnalogSendRequest(x=0.0, y=0.0, stick=None),
            expected={"event": "input.analog.send", "x": 0.0, "y": 0.0}
        ),
        RequestTest(
            value=InputAnalogSendRequest(x=0.0, y=0.0, stick="left"),
            expected={"event": "input.analog.send", "x": 0.0, "y": 0.0, "stick": "left"}
        ),
        RequestTest(
            value=InputButtonsSendRequest(buttons={"A": False}),
            expected={"event": "input.buttons.send", "buttons": {"A": False}}
        ),
        RequestTest(
            value=InputButtonsPressRequest(button="A", duration=None),
            expected={"event": "input.buttons.press", "button": "A"}
        ),
        RequestTest(
            value=InputButtonsPressRequest(button="A", duration=0),
            expected={"event": "input.buttons.press", "button": "A", "duration": 0}
        ),

        # Memory
        RequestTest(
            value=MemoryReadU8Request(address=0),
            expected={"event": "memory.read_u8", "address": 0}
        ),
        RequestTest(
            value=MemoryReadU16Request(address=0),
            expected={"event": "memory.read_u16", "address": 0}
        ),
        RequestTest(
            value=MemoryReadU32Request(address=0),
            expected={"event": "memory.read_u32", "address": 0}
        ),
        RequestTest(
            value=MemoryReadRequest(address=0, size=0, replacements=None),
            expected={"event": "memory.read", "address": 0, "size": 0}
        ),
        RequestTest(
            value=MemoryReadRequest(address=0, size=0, replacements=False),
            expected={"event": "memory.read", "address": 0, "size": 0, "replacements": False}
        ),
        RequestTest(
            value=MemoryReadStringRequest(address=0, type=None),
            expected={"event": "memory.readString", "address": 0}
        ),
        RequestTest(
            value=MemoryReadStringRequest(address=0, type="utf8"),
            expected={"event": "memory.readString", "address": 0, "type": "utf8"}
        ),
        RequestTest(
            value=MemoryReadStringUtf8Request(address=0),
            expected={"event": "memory.readString", "address": 0}
        ),
        RequestTest(
            value=MemoryReadStringBase64Request(address=0),
            expected={"event": "memory.readString", "address": 0, "type": "base64"}
        ),
        RequestTest(
            value=MemoryWriteU8Request(address=0, value=0),
            expected={"event": "memory.write_u8", "address": 0, "value": 0}
        ),
        RequestTest(
            value=MemoryWriteU16Request(address=0, value=0),
            expected={"event": "memory.write_u16", "address": 0, "value": 0}
        ),
        RequestTest(
            value=MemoryWriteU32Request(address=0, value=0),
            expected={"event": "memory.write_u32", "address": 0, "value": 0}
        ),
        RequestTest(
            value=MemoryWriteRequest(address=0, base64="abc"),
            expected={"event": "memory.write", "address": 0, "base64": "abc"}
        ),
        RequestTest(
            value=MemoryMappingRequest(),
            expected={"event": "memory.mapping"}
        ),
        RequestTest(
            value=MemoryInfoConfigRequest(detailed=None),
            expected={"event": "memory.info.config"}
        ),
        RequestTest(
            value=MemoryInfoConfigRequest(detailed=False),
            expected={"event": "memory.info.config", "detailed": False}
        ),
        RequestTest(
            value=MemoryInfoSetRequest(address=0, size=0, type="region", tag=None, pc=None),
            expected={"event": "memory.info.set", "address": 0, "size": 0, "type": "region"}
        ),
        RequestTest(
            value=MemoryInfoSetRequest(address=0, size=0, type="region", tag="tag", pc=0),
            expected={"event": "memory.info.set", "address": 0, "size": 0, "type": "region", "tag": "tag", "pc": 0}
        ),
        RequestTest(
            value=MemoryInfoListRequest(address=0, size=0, type=None),
            expected={"event": "memory.info.list", "address": 0, "size": 0}
        ),
        RequestTest(
            value=MemoryInfoListRequest(address=0, size=0, type="suballoc"),
            expected={"event": "memory.info.list", "address": 0, "size": 0, "type": "suballoc"}
        ),
        RequestTest(
            value=MemoryInfoSearchRequest(address=None, end=None, match="search", type=None),
            expected={"event": "memory.info.search", "match": "search"}
        ),
        RequestTest(
            value=MemoryInfoSearchRequest(address=0, end=1, match="search", type="suballoc"),
            expected={"event": "memory.info.search", "address": 0, "end": 1, "match": "search", "type": "suballoc"}
        ),

        # Replay
        RequestTest(
            value=ReplayBeginRequest(),
            expected={"event": "replay.begin"}
        ),
        RequestTest(
            value=ReplayAbortRequest(),
            expected={"event": "replay.abort"}
        ),
        RequestTest(
            value=ReplayFlushRequest(),
            expected={"event": "replay.flush"}
        ),
        RequestTest(
            value=ReplayExecuteRequest(version=0, base64="abc"),
            expected={"event": "replay.execute", "version": 0, "base64": "abc"}
        ),
        RequestTest(
            value=ReplayStatusRequest(),
            expected={"event": "replay.status"}
        ),
        RequestTest(
            value=ReplayTimeGetRequest(),
            expected={"event": "replay.time.get"}
        ),
        RequestTest(
            value=ReplayTimeSetRequest(value=0),
            expected={"event": "replay.time.set", "value": 0}
        ),

        # Other
        RequestTest(
            value=VersionRequest(name=None, version=None),
            expected={"event": "version"}
        ),
        RequestTest(
            value=VersionRequest(name="me", version="first"),
            expected={"event": "version", "name": "me", "version": "first"}
        ),
        RequestTest(
            value=BroadcastConfigGetRequest(),
            expected={"event": "broadcast.config.get"}
        ),
        RequestTest(
            value=BroadcastConfigSetRequest(disallowed={"key": False}),
            expected={"event": "broadcast.config.set", "disallowed": {"key": False}}
        ),
    ]


def with_ticket(request: BaseRequest, ticket: str):
    return dataclasses.replace(request, ticket=ticket)


def split_request_tests(request_tests: list[RequestTest]):
    values = []
    expected = []
    for test in request_tests:
        values.append(test.value)
        expected.append(test.expected)
    return values, expected


async def test_serialization():
    # Sending requests

    session = AsyncSession()
    # No need for input

    connection = MockRequestValidatorConnection([])
    await session.run(connection)

    request_tests = get_request_tests()
    raw_requests, expected = split_request_tests(request_tests)

    # Inject tickets
    ticket_requests = [with_ticket(req, f"TICKET{i}") for i, req in enumerate(raw_requests)]
    expected.extend([value | {"ticket": f"TICKET{i}"} for i, value in enumerate(expected)])

    for request in raw_requests:
        await session.send_request(request)

    async def dummy_handler(ev: BaseEvent):
        pass

    for request in ticket_requests:
        await session.send_request(request, dummy_handler)

    await connection.close()
    actual_requests = connection.get_requests()
    all_requests = raw_requests + ticket_requests

    assert len(actual_requests) == len(expected)

    for actual_request, expected_request, original in zip(actual_requests, expected, all_requests):
        assert actual_request == expected_request, f"{original}"
