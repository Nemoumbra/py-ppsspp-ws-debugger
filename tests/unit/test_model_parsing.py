import asyncio
import dataclasses
from dataclasses import dataclass

from ppsspp import AsyncSession, PPSSPPRequest
from ppsspp.model.events.base_event import BaseEvent
from ppsspp.model.events.error_event import ErrorEvent
from ppsspp.model.ppsspp_objects.breakpoints.cpu_breakpoint import CpuBreakpoint
from ppsspp.model.ppsspp_objects.breakpoints.memory_breakpoint import MemoryBreakpoint
from ppsspp.model.ppsspp_objects.cpu.register import RegisterCategory
from ppsspp.model.ppsspp_objects.disassembly.branches import BranchGuide, BranchInfo
from ppsspp.model.ppsspp_objects.disassembly.disasm_line import (
    DisasmLine, DataSymbol, DisasmLineBreakpoint, DisasmLineRelevantData, DisasmLineDataAccess
)
from ppsspp.model.ppsspp_objects.game.game_info import GameInfo
from ppsspp.model.ppsspp_objects.gpu.gpu_stats import FpsInfo, TimingInfo, VblankCyclesInfo
from ppsspp.model.ppsspp_objects.hle.function_symbol import FunctionSymbolInfo
from ppsspp.model.ppsspp_objects.hle.stack_frame import StackFrameInfo
from ppsspp.model.ppsspp_objects.hle.thread import ThreadInfo
from ppsspp.model.ppsspp_objects.hle.user_module import UserModuleInfo
from ppsspp.model.ppsspp_objects.input.analog_stick import AnalogStick
from ppsspp.model.ppsspp_objects.input.button import Button
from ppsspp.model.ppsspp_objects.input.buttons_state import ButtonsState
from ppsspp.model.ppsspp_objects.logs.log_level import LogLevel
from ppsspp.model.ppsspp_objects.memory.memory_block_info import MemoryBlockInfo
from ppsspp.model.ppsspp_objects.memory.memory_range import MemoryRangeInfo
from ppsspp.model.ppsspp_objects.memory.memory_tag_type import MemoryTagType
from tests.unit.utils import MockConnection

from ppsspp.model.events.other.broadcast_config import (
    BroadcastConfigGetEvent, BroadcastConfigSetEvent
)
from ppsspp.model.events.breakpoints.cpu import (
    CpuBreakpointAddEvent, CpuBreakpointUpdateEvent, CpuBreakpointRemoveEvent, CpuBreakpointListEvent
)
from ppsspp.model.events.cpu.common import (
    CpuSteppingEvent, CpuResumeEvent, CpuStatusEvent, CpuEvaluateEvent
)
from ppsspp.model.events.cpu.registers import (
    CpuGetRegEvent, CpuSetRegEvent, CpuGetAllRegsEvent
)
from ppsspp.model.events.game.common import (
    GameResetEvent, GameStatusEvent, GamePauseEvent, GameResumeEvent, GameStartEvent, GameQuitEvent
)
from ppsspp.model.events.gpu.common import (
    GpuRecordDumpEvent, GpuStatsGetEvent
)
from ppsspp.model.events.gpu.buffer import (
    GpuBufferScreenshotUriEvent, GpuBufferScreenshotB64Event,
    GpuBufferRenderColorUriEvent, GpuBufferRenderColorB64Event,
    GpuBufferRenderDepthUriEvent, GpuBufferRenderDepthB64Event,
    GpuBufferRenderStencilUriEvent, GpuBufferRenderStencilB64Event,
    GpuBufferTextureUriEvent, GpuBufferTextureB64Event,
    GpuBufferClutUriEvent, GpuBufferClutB64Event
)
from ppsspp.model.events.hle.thread import (
    HleThreadListEvent, HleThreadStopEvent, HleThreadWakeEvent
)
from ppsspp.model.events.hle.func import (
    HleFuncListEvent, HleFuncAddEvent, HleFuncRemoveEvent,
    HleFuncRemoveRangeEvent, HleFuncRenameEvent, HleFuncScanEvent
)
from ppsspp.model.events.hle.common import (
    HleModuleListEvent, HleBacktraceEvent
)
from ppsspp.model.events.input.buttons import (
    InputButtonsEvent, InputButtonsSendEvent, InputButtonsPressEvent
)
from ppsspp.model.events.input.analog import (
    InputAnalogEvent, InputAnalogSendEvent
)
from ppsspp.model.events.other.log import LogEvent
from ppsspp.model.events.breakpoints.memory import (
    MemoryBreakpointAddEvent, MemoryBreakpointUpdateEvent, MemoryBreakpointRemoveEvent, MemoryBreakpointListEvent
)
from ppsspp.model.events.disassembly.common import (
    MemoryBaseEvent, MemoryDisasmEvent, MemorySearchDisasmEvent, MemoryAssembleEvent, DisasmRange
)
from ppsspp.model.events.memory.common import (
    MemoryReadU8Event, MemoryReadU16Event, MemoryReadU32Event, MemoryReadEvent,
    MemoryReadStringUtf8Event, MemoryReadStringB64Event,
    MemoryWriteU8Event, MemoryWriteU16Event, MemoryWriteU32Event, MemoryWriteEvent
)
from ppsspp.model.events.memory.memory_info import (
    MemoryMappingEvent,
    MemoryInfoConfigEvent, MemoryInfoSetEvent, MemoryInfoListEvent, MemoryInfoSearchEvent
)
from ppsspp.model.events.replay.common import (
    ReplayBeginEvent, ReplayAbortEvent, ReplayFlushEvent, ReplayExecuteEvent, ReplayStatusEvent
)
from ppsspp.model.events.replay.time import (
    ReplayTimeGetEvent, ReplayTimeSetEvent
)
from ppsspp.model.events.other.version import VersionEvent


@dataclass
class EventTest:
    raw: dict
    expected: BaseEvent

def get_event_tests():
    return [
        # The error event
        EventTest(
            raw={"event": "error", "message": "oh man", "level": LogLevel.ERROR.value},
            expected=ErrorEvent(event="error", message="oh man", level=LogLevel.ERROR)
        ),

        # Breakpoints
        EventTest(
            raw={"event": "cpu.breakpoint.add"},
            expected=CpuBreakpointAddEvent(event="cpu.breakpoint.add")
        ),
        EventTest(
            raw={"event": "cpu.breakpoint.update"},
            expected=CpuBreakpointUpdateEvent(event="cpu.breakpoint.update")
        ),
        EventTest(
            raw={"event": "cpu.breakpoint.remove"},
            expected=CpuBreakpointRemoveEvent(event="cpu.breakpoint.remove")
        ),
        EventTest(
            raw={"event": "cpu.breakpoint.list", "breakpoints": [
                {'address': 0, 'enabled': False, 'log': True, 'code': "ooops", 'condition': None, 'logFormat': None,
                 'symbol': None}
            ]},
            expected=CpuBreakpointListEvent(
                event="cpu.breakpoint.list",
                breakpoints=[
                    CpuBreakpoint(
                        address=0,
                        enabled=False,
                        log=True,
                        code="ooops",
                        condition=None,
                        log_format=None,
                        symbol=None
                    )
                ]
            )
        ),
        EventTest(
            raw={"event": "cpu.breakpoint.list", "breakpoints": [
                {'address': 0, 'enabled': False, 'log': True, 'code': "ooops", 'condition': "true",
                 'logFormat': "format text", 'symbol': "zz_func"}
            ]},
            expected=CpuBreakpointListEvent(
                event="cpu.breakpoint.list",
                breakpoints=[
                    CpuBreakpoint(
                        address=0,
                        enabled=False,
                        log=True,
                        code="ooops",
                        condition="true",
                        log_format="format text",
                        symbol="zz_func"
                    )
                ]
            )
        ),
        EventTest(
            raw={"event": "memory.breakpoint.add"},
            expected=MemoryBreakpointAddEvent(event="memory.breakpoint.add")
        ),
        EventTest(
            raw={"event": "memory.breakpoint.update"},
            expected=MemoryBreakpointUpdateEvent(event="memory.breakpoint.update")
        ),
        EventTest(
            raw={"event": "memory.breakpoint.remove"},
            expected=MemoryBreakpointRemoveEvent(event="memory.breakpoint.remove")
        ),
        EventTest(
            raw={"event": "memory.breakpoint.list", "breakpoints": [
                {'address': 0, 'size': 1, 'enabled': False, 'log': True, 'read': True, 'write': True, 'change': True,
                 'hits': -1, 'condition': None, 'logFormat': None, 'symbol': None}
            ]},
            expected=MemoryBreakpointListEvent(
                event="memory.breakpoint.list",
                breakpoints=[
                    MemoryBreakpoint(
                        address=0,
                        size=1,
                        enabled=False,
                        log=True,
                        read=True,
                        write=True,
                        change=True,
                        hits=-1,
                        condition=None,
                        log_format=None,
                        symbol=None
                    )
                ]
            )
        ),
        EventTest(
            raw={"event": "memory.breakpoint.list", "breakpoints": [
                {'address': 0, 'size': 1, 'enabled': False, 'log': True, 'read': True, 'write': True, 'change': True,
                 'hits': -1, 'condition': "true", 'logFormat': "format text", 'symbol': "zz_func"}
            ]},
            expected=MemoryBreakpointListEvent(
                event="memory.breakpoint.list",
                breakpoints=[
                    MemoryBreakpoint(
                        address=0,
                        size=1,
                        enabled=False,
                        log=True,
                        read=True,
                        write=True,
                        change=True,
                        hits=-1,
                        condition="true",
                        log_format="format text",
                        symbol="zz_func"
                    )
                ]
            )
        ),

        # CPU
        EventTest(
            raw={"event": "cpu.stepping", "pc": 0, "ticks": 1, "reason": None, "relatedAddress": None},
            expected=CpuSteppingEvent(event="cpu.stepping", pc=0, ticks=1, reason=None, related_address=None)
        ),
        EventTest(
            raw={"event": "cpu.stepping", "pc": 0, "ticks": 1, "reason": "nuh-uh", "relatedAddress": 11037},
            expected=CpuSteppingEvent(event="cpu.stepping", pc=0, ticks=1, reason="nuh-uh", related_address=11037)
        ),
        EventTest(
            raw={"event": "cpu.resume"},
            expected=CpuResumeEvent(event="cpu.resume")
        ),
        EventTest(
            raw={"event": "cpu.status", "stepping": True, "paused": True, "pc": 0, "ticks": 1.5},
            expected=CpuStatusEvent(event="cpu.status", stepping=True, paused=True, pc=0, ticks=1.5)
        ),
        EventTest(
            raw={"event": "cpu.evaluate", "uintValue": 1, "floatValue": "1.5"},
            expected=CpuEvaluateEvent(event="cpu.evaluate", uint_value=1, float_value="1.5")
        ),
        EventTest(
            raw={"event": "cpu.getReg", "category": 1, "register": 0, "uintValue": 1, "floatValue": "1.5"},
            expected=CpuGetRegEvent(event="cpu.getReg", category=1, register=0, uint_value=1, float_value="1.5")
        ),
        EventTest(
            raw={"event": "cpu.setReg", "category": 1, "register": 0, "uintValue": 1, "floatValue": "1.5"},
            expected=CpuSetRegEvent(event="cpu.setReg", category=1, register=0, uint_value=1, float_value="1.5")
        ),
        EventTest(
            raw={"event": "cpu.getAllRegs", "categories": [
                {'id': 0, 'name': "hi", 'registerNames': ["a0"], 'uintValues': [1], 'floatValues': ["1.5"]}
            ]},
            expected=CpuGetAllRegsEvent(
                event="cpu.getAllRegs",
                categories=[
                    RegisterCategory(
                        id=0,
                        name="hi",
                        register_names=["a0"],
                        uint_values=[1],
                        float_values=["1.5"]
                    )
                ]
            )
        ),

        # Disassembly
        EventTest(
            raw={"event": "memory.base", "addressHex": "0xdeadbeef"},
            expected=MemoryBaseEvent(event="memory.base", address_hex="0xdeadbeef")
        ),
        EventTest(
            raw={"event": "memory.disasm", "range": {"start": 0, "end": 1}, "lines": [
                 {'type': "", 'address': 1, 'addressSize': 1, 'encoding': 0, 'macroEncoding': None,
                  'backgroundColor': "red", 'name': "what", 'params': "", 'symbol': None, 'function': None,
                  'dataSymbol': None, 'breakpoint': None, 'isCurrentPC': False, 'branch': None, 'relevantData': None,
                  'conditionMet': None, 'dataAccess': None}
            ],
            "branchGuides": [
                 {'top': 5, 'bottom': 1, 'direction': "down", 'lane': 1}
            ]},
            expected=MemoryDisasmEvent(
                event="memory.disasm",
                range=DisasmRange(start=0, end=1),
                lines=[
                    DisasmLine(
                        type="",
                        address=1,
                        address_size=1,
                        encoding=0,
                        macro_encoding=None,
                        background_color="red",
                        name="what",
                        params="",
                        symbol=None,
                        function=None,
                        data_symbol=None,
                        breakpoint=None,
                        is_current_pc=False,
                        branch=None,
                        relevant_data=None,
                        condition_met=None,
                        data_access=None
                    )
                ],
                branch_guides=[
                    BranchGuide(top=5, bottom=1, direction="down", lane=1)
                ]
            )
        ),
        EventTest(
            raw={"event": "memory.disasm", "range": {"start": 0, "end": 1}, "lines": [
                 {'type': "", 'address': 1, 'addressSize': 1, 'encoding': 0, 'macroEncoding': [0],
                  'backgroundColor': "red", 'name': "what", 'params': "", 'symbol': "sym", 'function': "func",
                  'dataSymbol': {'start': 0, 'label': None},
                  'breakpoint': {'enabled': False, 'address': 1, 'condition': None}, 'isCurrentPC': False,
                  'branch': {'targetAddress': None, 'register': None, 'isLined': False, 'isLikely': False,
                             'symbol': None},
                  'relevantData': {'address': 0, 'uintValue': None, 'stringValue': None},
                  'conditionMet': True,
                  'dataAccess': {'address': 0, 'size': 1, 'uintValue': None, 'symbol': None, 'valueSymbol': None}}
            ],
            "branchGuides": [
                 {'top': 5, 'bottom': 1, 'direction': "down", 'lane': 1}
            ]},
            expected=MemoryDisasmEvent(
                event="memory.disasm",
                range=DisasmRange(start=0, end=1),
                lines=[
                    DisasmLine(
                        type="",
                        address=1,
                        address_size=1,
                        encoding=0,
                        macro_encoding=[0],
                        background_color="red",
                        name="what",
                        params="",
                        symbol="sym",
                        function="func",
                        data_symbol=DataSymbol(start=0, label=None),
                        breakpoint=DisasmLineBreakpoint(enabled=False, address=1, condition=None),
                        is_current_pc=False,
                        branch=BranchInfo(target_address=None, register=None, is_lined=False, is_likely=False, symbol=None),
                        relevant_data=DisasmLineRelevantData(address=0, uint_value=None, string_value=None),
                        condition_met=True,
                        data_access=DisasmLineDataAccess(address=0, size=1, uint_value=None, symbol=None, value_symbol=None)
                    )
                ],
                branch_guides=[
                    BranchGuide(top=5, bottom=1, direction="down", lane=1)
                ]
            )
        ),
        EventTest(
            raw={"event": "memory.disasm", "range": {"start": 0, "end": 1}, "lines": [
                 {'type': "", 'address': 1, 'addressSize': 1, 'encoding': 0, 'macroEncoding': [0],
                  'backgroundColor': "red", 'name': "what", 'params': "", 'symbol': "sym", 'function': "func",
                  'dataSymbol': {'start': 0, 'label': "lable"},
                  'breakpoint': {'enabled': False, 'address': 1, 'condition': "true"}, 'isCurrentPC': False,
                  'branch': {'targetAddress': 1, 'register': 0, 'isLined': False, 'isLikely': False,
                             'symbol': "sym"},
                  'relevantData': {'address': 0, 'uintValue': 1, 'stringValue': "value"},
                  'conditionMet': True,
                  'dataAccess': {'address': 0, 'size': 1, 'uintValue': 10, 'symbol': "sym", 'valueSymbol': "value_sym"}}
            ],
            "branchGuides": [
                 {'top': 5, 'bottom': 1, 'direction': "down", 'lane': 1}
            ]},
            expected=MemoryDisasmEvent(
                event="memory.disasm",
                range=DisasmRange(start=0, end=1),
                lines=[
                    DisasmLine(
                        type="",
                        address=1,
                        address_size=1,
                        encoding=0,
                        macro_encoding=[0],
                        background_color="red",
                        name="what",
                        params="",
                        symbol="sym",
                        function="func",
                        data_symbol=DataSymbol(start=0, label="lable"),
                        breakpoint=DisasmLineBreakpoint(enabled=False, address=1, condition="true"),
                        is_current_pc=False,
                        branch=BranchInfo(target_address=1, register=0, is_lined=False, is_likely=False, symbol="sym"),
                        relevant_data=DisasmLineRelevantData(address=0, uint_value=1, string_value="value"),
                        condition_met=True,
                        data_access=DisasmLineDataAccess(address=0, size=1, uint_value=10, symbol="sym", value_symbol="value_sym")
                    )
                ],
                branch_guides=[
                    BranchGuide(top=5, bottom=1, direction="down", lane=1)
                ]
            )
        ),
        EventTest(
            raw={"event": "memory.searchDisasm", "address": None},
            expected=MemorySearchDisasmEvent(event="memory.searchDisasm", address=None)
        ),
        EventTest(
            raw={"event": "memory.searchDisasm", "address": 1},
            expected=MemorySearchDisasmEvent(event="memory.searchDisasm", address=1)
        ),
        EventTest(
            raw={"event": "memory.assemble", "encoding": 0xcafe},
            expected=MemoryAssembleEvent(event="memory.assemble", encoding=0xcafe)
        ),

        # Game
        EventTest(
            raw={"event": "game.reset"},
            expected=GameResetEvent(event="game.reset")
        ),
        EventTest(
            raw={"event": "game.status", "game": None, "paused": False},
            expected=GameStatusEvent(event="game.status", game=None, paused=False)
        ),
        EventTest(
            raw={"event": "game.status", "game": {'id': "nmae", 'version': "0", 'title': "tilted"}, "paused": False},
            expected=GameStatusEvent(
                event="game.status",
                game=GameInfo(id="nmae", version="0", title="tilted"),
                paused=False
            )
        ),
        EventTest(
            raw={"event": "game.pause", "game": None},
            expected=GamePauseEvent(event="game.pause", game=None)
        ),
        EventTest(
            raw={"event": "game.pause", "game": {'id': "nmae", 'version': "0", 'title': "tilted"}},
            expected=GamePauseEvent(event="game.pause", game=GameInfo(id="nmae", version="0", title="tilted"))
        ),
        EventTest(
            raw={"event": "game.resume", "game": None},
            expected=GameResumeEvent(event="game.resume", game=None)
        ),
        EventTest(
            raw={"event": "game.resume", "game": {'id': "nmae", 'version': "0", 'title': "tilted"}},
            expected=GameResumeEvent(event="game.resume", game=GameInfo(id="nmae", version="0", title="tilted"))
        ),
        EventTest(
            raw={"event": "game.start", "game": None},
            expected=GameStartEvent(event="game.start", game=None)
        ),
        EventTest(
            raw={"event": "game.start", "game": {'id': "nmae", 'version': "0", 'title': "tilted"}},
            expected=GameStartEvent(event="game.start", game=GameInfo(id="nmae", version="0", title="tilted"))
        ),
        EventTest(
            raw={"event": "game.quit", "game": None},
            expected=GameQuitEvent(event="game.quit", game=None)
        ),

        # GPU
        EventTest(
            raw={"event": "gpu.buffer.screenshot", "width": 0, "height": 0, "isFramebuffer": None, "uri": "abc"},
            expected=GpuBufferScreenshotUriEvent(event="gpu.buffer.screenshot", width=0, height=0, is_framebuffer=None, uri="abc")
        ),
        EventTest(
            raw={"event": "gpu.buffer.screenshot", "width": 0, "height": 0, "isFramebuffer": False, "uri": "abc"},
            expected=GpuBufferScreenshotUriEvent(event="gpu.buffer.screenshot", width=0, height=0, is_framebuffer=False, uri="abc")
        ),
        EventTest(
            raw={"event": "gpu.buffer.screenshot", "width": 0, "height": 0, "isFramebuffer": None, "flipped": False,
             "format": "png", "base64": "xyz"},
            expected=GpuBufferScreenshotB64Event(event="gpu.buffer.screenshot", width=0, height=0, is_framebuffer=None, flipped=False, format="png", base64="xyz")
        ),
        EventTest(
            raw={"event": "gpu.buffer.screenshot", "width": 0, "height": 0, "isFramebuffer": False, "flipped": False,
             "format": "png", "base64": "xyz"},
            expected=GpuBufferScreenshotB64Event(event="gpu.buffer.screenshot", width=0, height=0, is_framebuffer=False, flipped=False, format="png", base64="xyz")
        ),
        EventTest(
            raw={"event": "gpu.buffer.renderColor", "width": 0, "height": 0, "isFramebuffer": None, "uri": "def"},
            expected=GpuBufferRenderColorUriEvent(event="gpu.buffer.renderColor", width=0, height=0, is_framebuffer=None, uri="def")
        ),
        EventTest(
            raw={"event": "gpu.buffer.renderColor", "width": 0, "height": 0, "isFramebuffer": None, "flipped": False,
             "format": "jpeg", "base64": "uvw"},
            expected=GpuBufferRenderColorB64Event(event="gpu.buffer.renderColor", width=0, height=0, is_framebuffer=None, flipped=False, format="jpeg", base64="uvw")
        ),
        EventTest(
            raw={"event": "gpu.buffer.renderDepth", "width": 0, "height": 0, "isFramebuffer": None, "uri": "ghi"},
            expected=GpuBufferRenderDepthUriEvent(event="gpu.buffer.renderDepth", width=0, height=0, is_framebuffer=None, uri="ghi")
        ),
        EventTest(
            raw={"event": "gpu.buffer.renderDepth", "width": 0, "height": 0, "isFramebuffer": False, "uri": "ghi"},
            expected=GpuBufferRenderDepthUriEvent(event="gpu.buffer.renderDepth", width=0, height=0, is_framebuffer=False, uri="ghi")
        ),
        EventTest(
            raw={"event": "gpu.buffer.renderDepth", "width": 0, "height": 0, "isFramebuffer": None, "flipped": False,
             "format": "png", "base64": "rst"},
            expected=GpuBufferRenderDepthB64Event(event="gpu.buffer.renderDepth", width=0, height=0, is_framebuffer=None, flipped=False, format="png", base64="rst")
        ),
        EventTest(
            raw={"event": "gpu.buffer.renderDepth", "width": 0, "height": 0, "isFramebuffer": False, "flipped": False,
             "format": "png", "base64": "rst"},
            expected=GpuBufferRenderDepthB64Event(event="gpu.buffer.renderDepth", width=0, height=0, is_framebuffer=False, flipped=False, format="png", base64="rst")
        ),
        EventTest(
            raw={"event": "gpu.buffer.renderStencil", "width": 0, "height": 0, "isFramebuffer": None, "uri": "jkl"},
            expected=GpuBufferRenderStencilUriEvent(event="gpu.buffer.renderStencil", width=0, height=0, is_framebuffer=None, uri="jkl")
        ),
        EventTest(
            raw={"event": "gpu.buffer.renderStencil", "width": 0, "height": 0, "isFramebuffer": False, "uri": "jkl"},
            expected=GpuBufferRenderStencilUriEvent(event="gpu.buffer.renderStencil", width=0, height=0, is_framebuffer=False, uri="jkl")
        ),
        EventTest(
            raw={"event": "gpu.buffer.renderStencil", "width": 0, "height": 0, "isFramebuffer": None, "flipped": False,
             "format": "bmp", "base64": "mno"},
            expected=GpuBufferRenderStencilB64Event(event="gpu.buffer.renderStencil", width=0, height=0, is_framebuffer=None, flipped=False, format="bmp", base64="mno")
        ),
        EventTest(
            raw={"event": "gpu.buffer.renderStencil", "width": 0, "height": 0, "isFramebuffer": False, "flipped": False,
             "format": "bmp", "base64": "mno"},
            expected=GpuBufferRenderStencilB64Event(event="gpu.buffer.renderStencil", width=0, height=0, is_framebuffer=False, flipped=False, format="bmp", base64="mno")
        ),
        EventTest(
            raw={"event": "gpu.buffer.texture", "width": 0, "height": 0, "isFramebuffer": None, "uri": "pqr"},
            expected=GpuBufferTextureUriEvent(event="gpu.buffer.texture", width=0, height=0, is_framebuffer=None, uri="pqr")
        ),
        EventTest(
            raw={"event": "gpu.buffer.texture", "width": 0, "height": 0, "isFramebuffer": False, "uri": "pqr"},
            expected=GpuBufferTextureUriEvent(event="gpu.buffer.texture", width=0, height=0, is_framebuffer=False, uri="pqr")
        ),
        EventTest(
            raw={"event": "gpu.buffer.texture", "width": 0, "height": 0, "isFramebuffer": None, "flipped": False,
             "format": "png", "base64": "stu"},
            expected=GpuBufferTextureB64Event(event="gpu.buffer.texture", width=0, height=0, is_framebuffer=None, flipped=False, format="png", base64="stu")
        ),
        EventTest(
            raw={"event": "gpu.buffer.texture", "width": 0, "height": 0, "isFramebuffer": False, "flipped": False,
             "format": "png", "base64": "stu"},
            expected=GpuBufferTextureB64Event(event="gpu.buffer.texture", width=0, height=0, is_framebuffer=False, flipped=False, format="png", base64="stu")
        ),
        EventTest(
            raw={"event": "gpu.buffer.clut", "width": 0, "height": 0, "isFramebuffer": None, "uri": "vwx"},
            expected=GpuBufferClutUriEvent(event="gpu.buffer.clut", width=0, height=0, is_framebuffer=None, uri="vwx")
        ),
        EventTest(
            raw={"event": "gpu.buffer.clut", "width": 0, "height": 0, "isFramebuffer": False, "uri": "vwx"},
            expected=GpuBufferClutUriEvent(event="gpu.buffer.clut", width=0, height=0, is_framebuffer=False, uri="vwx")
        ),
        EventTest(
            raw={"event": "gpu.buffer.clut", "width": 0, "height": 0, "isFramebuffer": None, "flipped": False,
             "format": "tiff", "base64": "yza"},
            expected=GpuBufferClutB64Event(event="gpu.buffer.clut", width=0, height=0, is_framebuffer=None, flipped=False, format="tiff", base64="yza")
        ),
        EventTest(
            raw={"event": "gpu.buffer.clut", "width": 0, "height": 0, "isFramebuffer": False, "flipped": False,
             "format": "tiff", "base64": "yza"},
            expected=GpuBufferClutB64Event(event="gpu.buffer.clut", width=0, height=0, is_framebuffer=False, flipped=False, format="tiff", base64="yza")
        ),
        EventTest(
            raw={"event": "gpu.record.dump", "uri": "0"},
            expected=GpuRecordDumpEvent(event="gpu.record.dump", uri="0")
        ),
        EventTest(
            raw={"event": "gpu.stats.get", "fps": {'actual': 1.5, 'target': 0.5},
            "vblanksPerSecond": {'actual': 1.5, 'target': 0.5},
            "info": "0", "timing": {'frames': [1.0], 'sleep': [0.0], 'pos': 7}
            },
            expected=GpuStatsGetEvent(
                event="gpu.stats.get",
                fps=FpsInfo(actual=1.5, target=0.5),
                vblanks_per_second=VblankCyclesInfo(actual=1.5, target=0.5),
                info="0",
                timing=TimingInfo(frames=[1.0], sleep=[0.0], pos=7)
            )
        ),

        # HLE
        EventTest(
            raw={"event": "hle.module.list", "modules": [
                {"name": "mod", "address": 0, "size": 0, "isActive": False}
            ]},
            expected=HleModuleListEvent(
                event="hle.module.list",
                modules=[UserModuleInfo(name="mod", address=0, size=0, is_active=False)]
            )
        ),
        EventTest(
            raw={"event": "hle.backtrace", "frames": [
                {"entry": 0, "pc": 0, "sp": 0, "stackSize": 0, "code": "abc"}
            ]},
            expected=HleBacktraceEvent(
                event="hle.backtrace",
                frames=[StackFrameInfo(entry=0, pc=0, sp=0, stack_size=0, code="abc")]
            )
        ),
        EventTest(
            raw={"event": "hle.func.list", "functions": [
                {"name": "func", "address": 0, "size": 0}
            ]},
            expected=HleFuncListEvent(
                event="hle.func.list",
                functions=[FunctionSymbolInfo(name="func", address=0, size=0)]
            )
        ),
        EventTest(
            raw={"event": "hle.func.add", "address": 0, "size": 0, "name": "func"},
            expected=HleFuncAddEvent(event="hle.func.add", address=0, size=0, name="func")
        ),
        EventTest(
            raw={"event": "hle.func.remove", "address": 0, "size": 0},
            expected=HleFuncRemoveEvent(event="hle.func.remove", address=0, size=0)
        ),
        EventTest(
            raw={"event": "hle.func.removeRange", "count": 0},
            expected=HleFuncRemoveRangeEvent(event="hle.func.removeRange", count=0)
        ),
        EventTest(
            raw={"event": "hle.func.rename", "address": 0, "size": 0, "name": "newname"},
            expected=HleFuncRenameEvent(event="hle.func.rename", address=0, size=0, name="newname")
        ),
        EventTest(
            raw={"event": "hle.func.scan"},
            expected=HleFuncScanEvent(event="hle.func.scan")
        ),
        EventTest(
            raw={"event": "hle.thread.list", "threads": [
                {"id": 0, "name": "thread", "status": 0, "statuses": ["running"], "pc": 0, "entry": 0,
                 "initialStackSize": 0, "currentStackSize": 0, "priority": 0, "waitType": 0, "isCurrent": False}
            ]},
            expected=HleThreadListEvent(
                event="hle.thread.list",
                threads=[
                    ThreadInfo(
                        id=0,
                        name="thread",
                        status=0,
                        statuses=["running"],
                        pc=0,
                        entry=0,
                        initial_stack_size=0,
                        current_stack_size=0,
                        priority=0,
                        wait_type=0,
                        is_current=False
                    )
                ]
            )
        ),
        EventTest(
            raw={"event": "hle.thread.wake", "thread": 0, "status": "wake"},
            expected=HleThreadWakeEvent(event="hle.thread.wake", thread=0, status="wake")
        ),
        EventTest(
            raw={"event": "hle.thread.stop", "thread": 0, "status": "stop"},
            expected=HleThreadStopEvent(event="hle.thread.stop", thread=0, status="stop")
        ),

        # Input
        EventTest(
            raw={"event": "input.analog", "stick": "left", "x": 1.0, "y": -1.0 },
            expected=InputAnalogEvent(event="input.analog", stick=AnalogStick.left, x=1.0, y=-1.0)
        ),
        EventTest(
            raw={"event": "input.analog.send"},
            expected=InputAnalogSendEvent(event="input.analog.send")
        ),
        EventTest(
            raw={"event": "input.buttons", "buttons": {
                "cross": False,  "circle": False, "triangle": False,"square": False, "up": False,
                "down": False, "left": False, "right": False, "start": False, "select": False,
                "home": False, "screen": False, "note": False, "ltrigger": False, "rtrigger": False,
                "hold": False, "wlan": False, "remote_hold": False, "vol_up": False, "vol_down": False,
                "disc": False, "memstick": False, "forward": False, "back": False, "playpause": False,
                "l2": False, "l3": False, "r2": False, "r3": False,
            },
            "changed": {"cross": False, "r3": False}
            },
            expected=InputButtonsEvent(
                event="input.buttons",
                buttons=ButtonsState(
                    cross=False, circle=False, triangle=False, square=False, up=False,
                    down=False, left=False, right=False, start=False, select=False,
                    home=False, screen=False, note=False, ltrigger=False, rtrigger=False,
                    hold=False, wlan=False, remote_hold=False, vol_up=False, vol_down=False,
                    disc=False, memstick=False, forward=False, back=False, playpause=False,
                    l2=False, l3=False, r2=False, r3=False
                ),
                changed={Button.cross: False, Button.r3: False}
            )
        ),
        EventTest(
            raw={"event": "input.buttons.send"},
            expected=InputButtonsSendEvent(event="input.buttons.send")
        ),
        EventTest(
            raw={"event": "input.buttons.press"},
            expected=InputButtonsPressEvent(event="input.buttons.press")
        ),

        # Memory
        EventTest(
            raw={"event": "memory.read_u8", "value": 0},
            expected=MemoryReadU8Event(event="memory.read_u8", value=0)
        ),
        EventTest(
            raw={"event": "memory.read_u16", "value": 0},
            expected=MemoryReadU16Event(event="memory.read_u16", value=0)
        ),
        EventTest(
            raw={"event": "memory.read_u32", "value": 0},
            expected=MemoryReadU32Event(event="memory.read_u32", value=0)
        ),
        EventTest(
            raw={"event": "memory.read", "base64": "abc"},
            expected=MemoryReadEvent(event="memory.read", base64="abc")
        ),
        EventTest(
            raw={"event": "memory.readString", "value": "hello"},
            expected=MemoryReadStringUtf8Event(event="memory.readString", value="hello")
        ),
        EventTest(
            raw={"event": "memory.readString", "base64": "xyz"},
            expected=MemoryReadStringB64Event(event="memory.readString", base64="xyz")
        ),
        EventTest(
            raw={"event": "memory.write_u8", "value": 0},
            expected=MemoryWriteU8Event(event="memory.write_u8", value=0)
        ),
        EventTest(
            raw={"event": "memory.write_u16", "value": 0},
            expected=MemoryWriteU16Event(event="memory.write_u16", value=0)
        ),
        EventTest(
            raw={"event": "memory.write_u32", "value": 0},
            expected=MemoryWriteU32Event(event="memory.write_u32", value=0)
        ),
        EventTest(
            raw={"event": "memory.write"},
            expected=MemoryWriteEvent(event="memory.write")
        ),
        EventTest(
            raw={"event": "memory.mapping", "ranges": [
                {"type": "", "subtype": "", "name": "sup", "address": 0, "size": 1}
            ]},
            expected=MemoryMappingEvent(
                event="memory.mapping",
                ranges=[MemoryRangeInfo(type="", subtype="", name="sup", address=0, size=1)]
            )
        ),
        EventTest(
            raw={"event": "memory.info.config", "detailed": False},
            expected=MemoryInfoConfigEvent(event="memory.info.config", detailed=False)
        ),
        EventTest(
            raw={"event": "memory.info.set"},
            expected=MemoryInfoSetEvent(event="memory.info.set")
        ),
        EventTest(
            raw={"event": "memory.info.list", "extents": [
                {'type': "subfree", 'address': 0, 'size': 1, 'ticks': 1.5, 'pc': 0, 'tag': "", 'allocated': False}
            ]},
            expected=MemoryInfoListEvent(
                event="memory.info.list",
                extents=[MemoryBlockInfo(type=MemoryTagType.subfree, address=0, size=1, ticks=1.5, pc=0, tag="", allocated=False)]
            )
        ),
        EventTest(
            raw={"event": "memory.info.search", "extent": None},
            expected=MemoryInfoSearchEvent(event="memory.info.search", extent=None)
        ),
        EventTest(
            raw={"event": "memory.info.search", "extent": {
                'type': "subfree", 'address': 0, 'size': 1, 'ticks': 1.5, 'pc': 0, 'tag': "", 'allocated': False
            }},
            expected=MemoryInfoSearchEvent(
                event="memory.info.search",
                extent=MemoryBlockInfo(type=MemoryTagType.subfree, address=0, size=1, ticks=1.5, pc=0, tag="", allocated=False)
            )
        ),

        # Replay
        EventTest(
            raw={"event": "replay.begin"},
            expected=ReplayBeginEvent(event="replay.begin")
        ),
        EventTest(
            raw={"event": "replay.abort"},
            expected=ReplayAbortEvent(event="replay.abort")
        ),
        EventTest(
            raw={"event": "replay.flush", "version": 0, "base64": "huh"},
            expected=ReplayFlushEvent(event="replay.flush", version=0, base64="huh")
        ),
        EventTest(
            raw={"event": "replay.execute"},
            expected=ReplayExecuteEvent(event="replay.execute")
        ),
        EventTest(
            raw={"event": "replay.status", "executing": False, "saving": False},
            expected=ReplayStatusEvent(event="replay.status", executing=False, saving=False)
        ),
        EventTest(
            raw={"event": "replay.time.get", "value": 0},
            expected=ReplayTimeGetEvent(event="replay.time.get", value=0)
        ),
        EventTest(
            raw={"event": "replay.time.set"},
            expected=ReplayTimeSetEvent(event="replay.time.set")
        ),

        # Other
        EventTest(
            raw={"event": "version", "name": "mock", "version": "0"},
            expected=VersionEvent(event="version", name="mock", version="0")
        ),
        EventTest(
            raw={"event": "log", "timestamp": "", "header": "", "message": "msg", "level": LogLevel.INFO.value, "channel": ""},
            expected=LogEvent(event="log", timestamp="", header="", message="msg", level=LogLevel.INFO, channel="")
        ),
        EventTest(
            raw={"event": "broadcast.config.get", "disallowed": {"what": False}},
            expected=BroadcastConfigGetEvent(event="broadcast.config.get", disallowed={"what": False})
        ),
        EventTest(
            raw={"event": "broadcast.config.set", "disallowed": {"sup": False}},
            expected=BroadcastConfigSetEvent(event="broadcast.config.set", disallowed={"sup": False})
        ),
    ]


async def test_garbage_parsing():
    # Parsing garbage data
    events = [
        {},
        {"event": 123},
        {"event": "unknown_event"},
        {"event": "memory.unknown_event"},
    ]
    # Inject tickets, cause why not
    events.extend([event | {"ticket": "000"} for event in events])

    session = AsyncSession()
    exhausted = asyncio.Event()
    connection = MockConnection(exhausted, events)
    await session.run(connection)

    await exhausted.wait()


def split_event_tests(event_tests: list[EventTest]):
    raw = []
    expected = []
    for test in event_tests:
        raw.append(test.raw)
        expected.append(test.expected)
    return raw, expected


def with_ticket(request: BaseEvent, ticket: str):
    return dataclasses.replace(request, ticket=ticket)


async def test_parsing():
    # Parsing events
    session = AsyncSession()
    event_tests = get_event_tests()
    raw_events, expected = split_event_tests(event_tests)
    # Inject tickets
    # TODO: actually, let's not do that for broadcasts
    raw_events.extend([event | {"ticket": f"TICKET{i}"} for i, event in enumerate(raw_events)])
    ticket_events = [with_ticket(ev, f"TICKET{i}") for i, ev in enumerate(expected)]
    expected.extend(ticket_events)

    connection = MockConnection(asyncio.Event(), raw_events)

    parsed = []
    count = 0
    done = asyncio.Event()
    # Promiscuous listener
    @session.listen_for(None)
    async def handle_all(ev: BaseEvent):
        nonlocal count
        count += 1
        parsed.append(ev)
        if count == len(expected):
            done.set()

    await session.run(connection)

    async def dummy_handler(ev: BaseEvent):
        pass

    # Register fake handlers for the runtime not to reject the tickets
    for event in ticket_events:
        req = PPSSPPRequest("")
        req.set_ticket(event.ticket)
        await session.send_request_raw(req, dummy_handler)

    await done.wait()

    # Implicitly asserted by the await above, but whatever
    assert len(parsed) == len(expected)

    for parsed_event, expected_event in zip(parsed, expected):
        assert parsed_event == expected_event
