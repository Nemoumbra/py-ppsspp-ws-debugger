import json

from adaptix import Retort, name_mapping, NameStyle, dumper, Chain

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
    MemoryBaseRequest, MemoryDisasmRequest, MemoryDisasmByCountRequest, MemoryDisasmByEndAddrRequest,
    MemorySearchDisasmRequest, MemoryAssembleRequest
)
from ppsspp.model.requests.game.common import (
    GameResetRequest, GameStatusRequest
)
from ppsspp.model.requests.gpu.buffer import (
    GpuBufferScreenshotRequest, GpuBufferRenderColorRequest, GpuBufferRenderDepthRequest,
    GpuBufferRenderStencilRequest, GpuBufferTextureRequest, GpuBufferClutRequest
)
from ppsspp.model.requests.gpu.common import (
    GpuRecordDumpRequest, GpuStatsGetRequest, GpuStatsFeedRequest
)
from ppsspp.model.requests.hle.common import (
    HleModuleListRequest, HleBacktraceRequest
)
from ppsspp.model.requests.hle.func import (
    HleFuncListRequest, HleFuncAddRequest, HleFuncRemoveRequest, HleFuncRemoveRangeRequest,
    HleFuncRenameRequest, HleFuncScanRequest
)
from ppsspp.model.requests.hle.thread import (
    HleThreadListRequest, HleThreadWakeRequest, HleThreadStopRequest
)
from ppsspp.model.requests.input.analog import (
    InputAnalogSendRequest
)
from ppsspp.model.requests.input.buttons import (
    InputButtonsSendRequest, InputButtonsPressRequest
)
from ppsspp.model.requests.memory.common import (
    MemoryReadU8Request, MemoryReadU16Request, MemoryReadU32Request, MemoryReadRequest,
    MemoryReadStringRequest, MemoryWriteU8Request, MemoryWriteU16Request, MemoryWriteU32Request,
    MemoryWriteRequest, MemoryReadStringUtf8Request, MemoryReadStringBase64Request
)
from ppsspp.model.requests.memory.memory_info import (
    MemoryMappingRequest, MemoryInfoConfigRequest, MemoryInfoSetRequest,
    MemoryInfoListRequest, MemoryInfoSearchRequest
)
from ppsspp.model.requests.other.broadcast_config import (
    BroadcastConfigSetRequest, BroadcastConfigGetRequest
)
from ppsspp.model.requests.other.version import (
    VersionRequest
)
from ppsspp.model.requests.replay.common import (
    ReplayBeginRequest, ReplayAbortRequest, ReplayFlushRequest, ReplayStatusRequest, ReplayExecuteRequest
)
from ppsspp.model.requests.replay.time import (
    ReplayTimeGetRequest, ReplayTimeSetRequest
)

from ppsspp.exceptions.request_build_error import RequestBuildError


def _make_retort():
    retort = Retort(recipe=[
        name_mapping(name_style=NameStyle.CAMEL, omit_default=True),

        # Here we actually inject the request names
        dumper(CpuBreakpointAddRequest, lambda x: x | {"event": "cpu.breakpoint.add"}, Chain.LAST),
        dumper(CpuBreakpointUpdateRequest, lambda x: x | {"event": "cpu.breakpoint.update"}, Chain.LAST),
        dumper(CpuBreakpointRemoveRequest, lambda x: x | {"event": "cpu.breakpoint.remove"}, Chain.LAST),
        dumper(CpuBreakpointListRequest, lambda x: x | {"event": "cpu.breakpoint.list"}, Chain.LAST),

        dumper(MemoryBreakpointAddRequest, lambda x: x | {"event": "memory.breakpoint.add"}, Chain.LAST),
        dumper(MemoryBreakpointUpdateRequest, lambda x: x | {"event": "memory.breakpoint.update"}, Chain.LAST),
        dumper(MemoryBreakpointRemoveRequest, lambda x: x | {"event": "memory.breakpoint.remove"}, Chain.LAST),
        dumper(MemoryBreakpointListRequest, lambda x: x | {"event": "memory.breakpoint.list"}, Chain.LAST),

        dumper(CpuSteppingRequest, lambda x: x | {"event": "cpu.stepping"}, Chain.LAST),
        dumper(CpuResumeRequest, lambda x: x | {"event": "cpu.resume"}, Chain.LAST),
        dumper(CpuStatusRequest, lambda x: x | {"event": "cpu.status"}, Chain.LAST),
        dumper(CpuEvaluateRequest, lambda x: x | {"event": "cpu.evaluate"}, Chain.LAST),

        dumper(CpuStepIntoRequest, lambda x: x | {"event": "cpu.stepInto"}, Chain.LAST),
        dumper(CpuStepOverRequest, lambda x: x | {"event": "cpu.stepOver"}, Chain.LAST),
        dumper(CpuStepOutRequest, lambda x: x | {"event": "cpu.stepOut"}, Chain.LAST),
        dumper(CpuRunUntilRequest, lambda x: x | {"event": "cpu.runUntil"}, Chain.LAST),
        dumper(CpuNextHleRequest, lambda x: x | {"event": "cpu.nextHLE"}, Chain.LAST),

        dumper(CpuGetAllRegsRequest, lambda x: x | {"event": "cpu.getAllRegs"}, Chain.LAST),
        dumper(CpuGetRegRequest, lambda x: x | {"event": "cpu.getReg"}, Chain.LAST),
        dumper(CpuGetRegByNameRequest, lambda x: x | {"event": "cpu.getReg"}, Chain.LAST),
        dumper(CpuGetRegByIdxAndCategoryRequest, lambda x: x | {"event": "cpu.getReg"}, Chain.LAST),
        dumper(CpuSetRegRequest, lambda x: x | {"event": "cpu.setReg"}, Chain.LAST),
        dumper(CpuSetRegByNameRequest, lambda x: x | {"event": "cpu.setReg"}, Chain.LAST),
        dumper(CpuSetRegByIdxAndCategoryRequest, lambda x: x | {"event": "cpu.setReg"}, Chain.LAST),

        dumper(MemoryBaseRequest, lambda x: x | {"event": "memory.base"}, Chain.LAST),
        dumper(MemoryDisasmRequest, lambda x: x | {"event": "memory.disasm"}, Chain.LAST),
        dumper(MemoryDisasmByCountRequest, lambda x: x | {"event": "memory.disasm"}, Chain.LAST),
        dumper(MemoryDisasmByEndAddrRequest, lambda x: x | {"event": "memory.disasm"}, Chain.LAST),
        dumper(MemorySearchDisasmRequest, lambda x: x | {"event": "memory.searchDisasm"}, Chain.LAST),
        dumper(MemoryAssembleRequest, lambda x: x | {"event": "memory.assemble"}, Chain.LAST),

        dumper(GameResetRequest, lambda x: x | {"event": "game.reset"}, Chain.LAST),
        dumper(GameStatusRequest, lambda x: x | {"event": "game.status"}, Chain.LAST),

        # These are still kinda TODO-ish
        dumper(GpuBufferScreenshotRequest, lambda x: x | {"event": "gpu.buffer.screenshot"}, Chain.LAST),
        dumper(GpuBufferRenderColorRequest, lambda x: x | {"event": "gpu.buffer.renderColor"}, Chain.LAST),
        dumper(GpuBufferRenderDepthRequest, lambda x: x | {"event": "gpu.buffer.renderDepth"}, Chain.LAST),
        dumper(GpuBufferRenderStencilRequest, lambda x: x | {"event": "gpu.buffer.renderStencil"}, Chain.LAST),
        dumper(GpuBufferTextureRequest, lambda x: x | {"event": "gpu.buffer.texture"}, Chain.LAST),
        dumper(GpuBufferClutRequest, lambda x: x | {"event": "gpu.buffer.clut"}, Chain.LAST),

        dumper(GpuRecordDumpRequest, lambda x: x | {"event": "gpu.record.dump"}, Chain.LAST),
        dumper(GpuStatsGetRequest, lambda x: x | {"event": "gpu.stats.get"}, Chain.LAST),
        dumper(GpuStatsFeedRequest, lambda x: x | {"event": "gpu.stats.feed"}, Chain.LAST),

        dumper(HleModuleListRequest, lambda x: x | {"event": "hle.module.list"}, Chain.LAST),
        dumper(HleBacktraceRequest, lambda x: x | {"event": "hle.backtrace"}, Chain.LAST),
        dumper(HleFuncListRequest, lambda x: x | {"event": "hle.func.list"}, Chain.LAST),
        dumper(HleFuncAddRequest, lambda x: x | {"event": "hle.func.add"}, Chain.LAST),
        dumper(HleFuncRemoveRequest, lambda x: x | {"event": "hle.func.remove"}, Chain.LAST),
        dumper(HleFuncRemoveRangeRequest, lambda x: x | {"event": "hle.func.removeRange"}, Chain.LAST),
        dumper(HleFuncRenameRequest, lambda x: x | {"event": "hle.func.rename"}, Chain.LAST),
        dumper(HleFuncScanRequest, lambda x: x | {"event": "hle.func.scan"}, Chain.LAST),
        dumper(HleThreadListRequest, lambda x: x | {"event": "hle.thread.list"}, Chain.LAST),
        dumper(HleThreadWakeRequest, lambda x: x | {"event": "hle.thread.wake"}, Chain.LAST),
        dumper(HleThreadStopRequest, lambda x: x | {"event": "hle.thread.stop"}, Chain.LAST),

        dumper(InputAnalogSendRequest, lambda x: x | {"event": "input.analog.send"}, Chain.LAST),
        dumper(InputButtonsSendRequest, lambda x: x | {"event": "input.buttons.send"}, Chain.LAST),
        dumper(InputButtonsPressRequest, lambda x: x | {"event": "input.buttons.press"}, Chain.LAST),

        dumper(MemoryReadU8Request, lambda x: x | {"event": "memory.read_u8"}, Chain.LAST),
        dumper(MemoryReadU16Request, lambda x: x | {"event": "memory.read_u16"}, Chain.LAST),
        dumper(MemoryReadU32Request, lambda x: x | {"event": "memory.read_u32"}, Chain.LAST),
        dumper(MemoryReadRequest, lambda x: x | {"event": "memory.read"}, Chain.LAST),

        dumper(MemoryReadStringRequest, lambda x: x | {"event": "memory.readString"}, Chain.LAST),
        dumper(MemoryReadStringUtf8Request, lambda x: x | {"event": "memory.readString"}, Chain.LAST),
        dumper(
            MemoryReadStringBase64Request,
            lambda x: x | {"event": "memory.readString", "type": "base64"}, Chain.LAST
        ),

        dumper(MemoryWriteU8Request, lambda x: x | {"event": "memory.write_u8"}, Chain.LAST),
        dumper(MemoryWriteU16Request, lambda x: x | {"event": "memory.write_u16"}, Chain.LAST),
        dumper(MemoryWriteU32Request, lambda x: x | {"event": "memory.write_u32"}, Chain.LAST),
        dumper(MemoryWriteRequest, lambda x: x | {"event": "memory.write"}, Chain.LAST),

        dumper(MemoryMappingRequest, lambda x: x | {"event": "memory.mapping"}, Chain.LAST),
        dumper(MemoryInfoConfigRequest, lambda x: x | {"event": "memory.info.config"}, Chain.LAST),
        dumper(MemoryInfoSetRequest, lambda x: x | {"event": "memory.info.set"}, Chain.LAST),
        dumper(MemoryInfoListRequest, lambda x: x | {"event": "memory.info.list"}, Chain.LAST),
        dumper(MemoryInfoSearchRequest, lambda x: x | {"event": "memory.info.search"}, Chain.LAST),

        dumper(BroadcastConfigGetRequest, lambda x: x | {"event": "broadcast.config.get"}, Chain.LAST),
        dumper(BroadcastConfigSetRequest, lambda x: x | {"event": "broadcast.config.set"}, Chain.LAST),

        dumper(VersionRequest, lambda x: x | {"event": "version"}, Chain.LAST),

        dumper(ReplayBeginRequest, lambda x: x | {"event": "replay.begin"}, Chain.LAST),
        dumper(ReplayAbortRequest, lambda x: x | {"event": "replay.abort"}, Chain.LAST),
        dumper(ReplayFlushRequest, lambda x: x | {"event": "replay.flush"}, Chain.LAST),
        dumper(ReplayExecuteRequest, lambda x: x | {"event": "replay.execute"}, Chain.LAST),
        dumper(ReplayStatusRequest, lambda x: x | {"event": "replay.status"}, Chain.LAST),
        dumper(ReplayTimeGetRequest, lambda x: x | {"event": "replay.time.get"}, Chain.LAST),
        dumper(ReplayTimeSetRequest, lambda x: x | {"event": "replay.time.set"}, Chain.LAST),
    ])

    return retort


class RequestDispatcher:
    def __init__(self):
        self._retort = _make_retort()

    def make_request(self, request: BaseRequest) -> str:
        raw = self._retort.dump(request)
        return json.dumps(raw)
