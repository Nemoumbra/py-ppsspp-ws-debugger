import asyncio

from ppsspp import AsyncSession, PPSSPPRequest
from ppsspp.exceptions.connection_terminated import ConnectionTerminated
from ppsspp.model.ppsspp_objects.gpu.gpu_stats import FpsInfo, VblankCyclesInfo, TimingInfo
from ppsspp.model.ppsspp_objects.logs.log_level import LogLevel
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

def get_events():
    return [
        # Garbage data
        {},
        {"event": 123},
        {"event": "unknown_event"},
        {"event": "memory.unknown_event"},

        # The error event
        {"event": "error", "message": "oh man", "level": LogLevel.ERROR.value},

        # Breakpoints
        {"event": "cpu.breakpoint.add"},
        {"event": "cpu.breakpoint.update"},
        {"event": "cpu.breakpoint.remove"},
        {"event": "cpu.breakpoint.list", "breakpoints": [
            {'address': 0, 'enabled': False, 'log': True, 'code': "ooops", 'condition': None, 'logFormat': None,
             'symbol': None}
        ]},
        {"event": "cpu.breakpoint.list", "breakpoints": [
            {'address': 0, 'enabled': False, 'log': True, 'code': "ooops", 'condition': "true",
             'logFormat': "format text", 'symbol': "zz_func"}
        ]},
        {"event": "memory.breakpoint.add"},
        {"event": "memory.breakpoint.update"},
        {"event": "memory.breakpoint.remove"},
        {"event": "memory.breakpoint.list", "breakpoints": [
            {'address': 0, 'size': 1, 'enabled': False, 'log': True, 'read': True, 'write': True, 'change': True,
             'hits': -1, 'condition': None, 'logFormat': None, 'symbol': None}
        ]},
        {"event": "memory.breakpoint.list", "breakpoints": [
            {'address': 0, 'size': 1, 'enabled': False, 'log': True, 'read': True, 'write': True, 'change': True,
             'hits': -1, 'condition': "true", 'logFormat': "format text", 'symbol': "zz_func"}
        ]},

        # CPU
        {"event": "cpu.stepping", "pc": 0, "ticks": 1, "reason": "nuh-uh", "relatedAddress": 11037},
        {"event": "cpu.stepping", "pc": 0, "ticks": 1, "reason": None, "relatedAddress": None},
        {"event": "cpu.resume"},
        {"event": "cpu.status", "stepping": True, "paused": True, "pc": 0, "ticks": 1.5},
        {"event": "cpu.evaluate", "uintValue": 1, "floatValue": "1.5"},

        {"event": "cpu.getReg", "category": 1, "register": 0, "uintValue": 1, "floatValue": "1.5"},
        {"event": "cpu.setReg", "category": 1, "register": 0, "uintValue": 1, "floatValue": "1.5"},
        {"event": "cpu.getAllRegs", "categories": [
            {'id': 0, 'name': "hi", 'registerNames': ["a0"], 'uintValues': [1], 'floatValues': ["1.5"]}
        ]},

        # Disassembly
        {"event": "memory.base", "addressHex": "0xdeadbeef"},
        {"event": "memory.disasm", "range": {"start": 0, "end": 1},
         "lines": [
             {'type': "", 'address': 1, 'addressSize': 1, 'encoding': 0, 'macroEncoding': None,
              'backgroundColor': "red", 'name': "what", 'params': "", 'symbol': None, 'function': None,
              'dataSymbol': None, 'breakpoint': None, 'isCurrentPC': False, 'branch': None, 'relevantData': None,
              'conditionMet': None, 'dataAccess': None}
         ],
         "branchGuides": [
             {'top': 5, 'bottom': 1, 'direction': "down", 'lane': 1}
         ]
         },

        {"event": "memory.disasm", "range": {"start": 0, "end": 1},
         "lines": [
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
         ]
         },
        # and another layer of "none"s...
        {"event": "memory.disasm", "range": {"start": 0, "end": 1},
         "lines": [
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
         ]
        },
        {"event": "memory.searchDisasm", "address": None},
        {"event": "memory.searchDisasm", "address": 1},
        {"event": "memory.assemble", "encoding": 0xcafe},

        # Game
        {"event": "game.reset"},
        {"event": "game.status", "game": None, "paused": False},
        {"event": "game.status", "game": {'id': "nmae", 'version': "0", 'title': "tilted"}, "paused": False},
        {"event": "game.pause", "game": None},
        {"event": "game.pause", "game": {'id': "nmae", 'version': "0", 'title': "tilted"}},
        {"event": "game.resume", "game": None},
        {"event": "game.resume", "game": {'id': "nmae", 'version': "0", 'title': "tilted"}},
        {"event": "game.start", "game": None},
        {"event": "game.start", "game": {'id': "nmae", 'version': "0", 'title': "tilted"}},
        {"event": "game.quit", "game": None},
        # {"event": "game.resume"},  # This also works! TODO: should it work?

        # GPU
        {"event": "gpu.buffer.screenshot", "width": 0, "height": 0, "isFramebuffer": None, "uri": "abc"},
        {"event": "gpu.buffer.screenshot", "width": 0, "height": 0, "isFramebuffer": False, "uri": "abc"},
        {"event": "gpu.buffer.screenshot", "width": 0, "height": 0, "isFramebuffer": None, "flipped": False,
         "format": "png", "base64": "xyz"},
        {"event": "gpu.buffer.screenshot", "width": 0, "height": 0, "isFramebuffer": False, "flipped": False,
         "format": "png", "base64": "xyz"},
        {"event": "gpu.buffer.renderColor", "width": 0, "height": 0, "isFramebuffer": None, "uri": "def"},
        {"event": "gpu.buffer.renderColor", "width": 0, "height": 0, "isFramebuffer": None, "flipped": False,
         "format": "jpeg", "base64": "uvw"},
        {"event": "gpu.buffer.renderDepth", "width": 0, "height": 0, "isFramebuffer": None, "uri": "ghi"},
        {"event": "gpu.buffer.renderDepth", "width": 0, "height": 0, "isFramebuffer": False, "uri": "ghi"},
        {"event": "gpu.buffer.renderDepth", "width": 0, "height": 0, "isFramebuffer": None, "flipped": False,
         "format": "png", "base64": "rst"},
        {"event": "gpu.buffer.renderDepth", "width": 0, "height": 0, "isFramebuffer": False, "flipped": False,
         "format": "png", "base64": "rst"},
        {"event": "gpu.buffer.renderStencil", "width": 0, "height": 0, "isFramebuffer": None, "uri": "jkl"},
        {"event": "gpu.buffer.renderStencil", "width": 0, "height": 0, "isFramebuffer": False, "uri": "jkl"},
        {"event": "gpu.buffer.renderStencil", "width": 0, "height": 0, "isFramebuffer": None, "flipped": False,
         "format": "bmp", "base64": "mno"},
        {"event": "gpu.buffer.renderStencil", "width": 0, "height": 0, "isFramebuffer": False, "flipped": False,
         "format": "bmp", "base64": "mno"},
        {"event": "gpu.buffer.texture", "width": 0, "height": 0, "isFramebuffer": None, "uri": "pqr"},
        {"event": "gpu.buffer.texture", "width": 0, "height": 0, "isFramebuffer": False, "uri": "pqr"},
        {"event": "gpu.buffer.texture", "width": 0, "height": 0, "isFramebuffer": None, "flipped": False,
         "format": "png", "base64": "stu"},
        {"event": "gpu.buffer.texture", "width": 0, "height": 0, "isFramebuffer": False, "flipped": False,
         "format": "png", "base64": "stu"},
        {"event": "gpu.buffer.clut", "width": 0, "height": 0, "isFramebuffer": None, "uri": "vwx"},
        {"event": "gpu.buffer.clut", "width": 0, "height": 0, "isFramebuffer": False, "uri": "vwx"},
        {"event": "gpu.buffer.clut", "width": 0, "height": 0, "isFramebuffer": None, "flipped": False,
         "format": "tiff", "base64": "yza"},
        {"event": "gpu.buffer.clut", "width": 0, "height": 0, "isFramebuffer": False, "flipped": False,
         "format": "tiff", "base64": "yza"},

        {"event": "gpu.record.dump", "uri": "0"},
        {"event": "gpu.stats.get", "fps": {'actual': 1.5, 'target': 0.5},
         "vblanksPerSecond": {'actual': 1.5, 'target': 0.5},
         "info": "0", "timing": {'frames': [1.0], 'sleep': [0.0], 'pos': 7}
         },

        # HLE
        {"event": "hle.module.list", "modules": [
            {"name": "mod", "address": 0, "size": 0, "isActive": False}
        ]},
        {"event": "hle.backtrace", "frames": [
            {"entry": 0, "pc": 0, "sp": 0, "stackSize": 0, "code": "abc"}
        ]},
        {"event": "hle.func.list", "functions": [
            {"name": "func", "address": 0, "size": 0}
        ]},
        {"event": "hle.func.add", "address": 0, "size": 0, "name": "func"},
        {"event": "hle.func.remove", "address": 0, "size": 0},
        {"event": "hle.func.removeRange", "count": 0},
        {"event": "hle.func.rename", "address": 0, "size": 0, "name": "newname"},
        {"event": "hle.func.scan"},
        {"event": "hle.thread.list", "threads": [
            {"id": 0, "name": "thread", "status": 0, "statuses": ["running"], "pc": 0, "entry": 0,
             "initialStackSize": 0, "currentStackSize": 0, "priority": 0, "waitType": 0, "isCurrent": False}
        ]},
        {"event": "hle.thread.wake", "thread": 0, "status": "wake"},
        {"event": "hle.thread.stop", "thread": 0, "status": "stop"},


        # Input

        # Memory

        # Replay

        # Other
        {"event": "version", "name": "mock", "version": "0"}
    ]


def get_requests():
    return {

    }

# TODO: actually test all events and requests...


async def test_serialization():
    # Sending requests

    session = AsyncSession()
    events = get_events()
    requests = get_requests()
    exhausted = asyncio.Event()
    connection = MockConnection(exhausted, events)

    await session.run(connection)

    # Low-level stuff, no ticket
    await session.send_request_raw(PPSSPPRequest("version"))
    await session.send_request(VersionRequest())

    pass


async def test_parsing():
    # Parsing events
    session = AsyncSession()
    events = get_events()
    exhausted = asyncio.Event()
    connection = MockConnection(exhausted, events)

    await session.run(connection)
    await exhausted.wait()
    pass
