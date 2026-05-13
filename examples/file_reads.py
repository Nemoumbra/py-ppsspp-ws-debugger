from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from typing import cast, Awaitable, Coroutine
from logging import getLogger
import asyncio

from ppsspp.async_connection import AsyncPpssppConnection
from ppsspp.async_session import AsyncSession
from ppsspp.exceptions.request_failed_error import RequestFailedError
from ppsspp.model.events.base_event import BaseEvent
from ppsspp.model.events.cpu.common import CpuSteppingEvent
from ppsspp.model.events.cpu.registers import CpuGetRegEvent
from ppsspp.model.events.error_event import ErrorEvent
from ppsspp.model.events.hle.func import HleFuncListEvent
from ppsspp.model.events.memory.common import MemoryReadStringUtf8Event, MemoryReadU32Event
from ppsspp.model.ppsspp_objects.hle.function_symbol import FunctionSymbolInfo
from ppsspp.ppsspp_request import PPSSPPRequest


logger = getLogger("ppsspp.file_manager")

# Return False to remain stepping
SteppingHandler = Callable[[], Awaitable[bool | None]]


def decode_ioctl(cmd: int):
    return (
        ((cmd >> 20) & 0xFF),
        bool((cmd >> 17) & 1),
        bool((cmd >> 16) & 1),
        bool((cmd >> 15) & 1),
        bool((cmd >> 14) & 1),
        ((cmd >> 12) & 3),
        (cmd & 0x7FF),
    )


@dataclass
class FilePosition:
    from_end: bool
    position: int

    def __str__(self):
        if self.from_end:
            return f"end-0x{self.position:X}"
        else:
            return f"0x{self.position:X}"

    def advance(self, value):
        if not self.from_end:
            self.position += value
        else:
            self.position -= value


class FileAsyncState(Enum):
    PendingOpen = 0
    PendingClose = auto()
    PendingSeek = auto()
    PendingRead = auto()
    PendingIoctl = auto()

    PendingOther = auto()
    NoAsync = auto()


@dataclass
class FileState:
    name: str
    fd: int
    pos: FilePosition
    async_state: FileAsyncState = FileAsyncState.NoAsync

    # Can't do any better than that
    async_args: tuple = ()

    def info(self):
        return f"{self.name} (fd=0x{self.fd:X})"


class FileSeekType(Enum):
    Set = 0
    Cur = auto()
    End = auto()


class IoctlCommand(Enum):
    IsoFsRead = 0x01030008
    IsoFsSeek = 0x01010005
    UmdFsRead = 0x01f30003
    UmdFsSeek = 0x01F100A6


def format_ioctl_cmd(cmd: IoctlCommand):
    pass


class SteppingManager:
    def __init__(self):
        self.began_stepping = asyncio.Event()
        self.stepping_requested = False

    async def wait(self):
        self.stepping_requested = True
        await self.began_stepping.wait()

    def on_stepping(self):
        # returns whether stepping was requested
        if self.stepping_requested:
            # Wake up yourself
            self.began_stepping.set()
            self.began_stepping.clear()
            self.stepping_requested = False
            return True
        return False

class IoAsyncManager:
    def __init__(self):
        self.async_handles: dict[int, FileAsyncOp] = {}

        # sceIoWaitAsync blocks until error (<0) or 0
        # sceIoPollAsync returns error (<0), 1 (not yet) or 0



class FileManager:
    def __init__(self, debugger: 'Debugger', stepping_manager: SteppingManager):
        self.debugger = debugger
        self.stepping_manager = stepping_manager
        self.files: dict[int, FileState] = {}

        self.async_handles: dict[int, FileAsyncOp] = {}

    async def on_open(self):
        name_addr = await self.debugger.get_resister("a0")
        filename = await self.debugger.read_string(name_addr)
        await self.debugger.step_out()
        await self.stepping_manager.wait()
        fd = await self.debugger.get_resister("v0")
        if fd >= 0x8000_0000:
            print(f"File open failed for {filename}: error code {fd:X}")
            return

        file = FileState(filename, fd, FilePosition(False, 0))
        self.files[fd] = file

        print(f"Opened file {file.info()}")

    async def on_close(self):
        fd = await self.debugger.get_resister("a0")
        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_resister("v0")
        if fd not in self.files:
            print(f"Closing unknown file: {fd=}, {result=}")
            return
        file = self.files[fd]
        if result != 0:
            print(f"Failed to close {file.info()}: error code {result:X}")
            return
        print(f"Closed {file.info()}")
        del self.files[fd]

    def handle_successful_seek(self, seek_type: FileSeekType, file: FileState, offset: int, result: int):
        match seek_type:
            case FileSeekType.Set:
                file.pos = FilePosition(False, offset)
            case FileSeekType.End:
                file.pos = FilePosition(True, offset)
            case FileSeekType.Cur:
                file.pos.advance(offset)

        actual_new_pos = FilePosition(False, result)
        print(f"Seek in {file.info()}: expected pos {file.pos}, actual pos {actual_new_pos}")
        file.pos = actual_new_pos

    async def on_seek(self):
        fd = await self.debugger.get_resister("a0")
        offset = await self.debugger.get_longlong_register("a2", "a3")
        whence = await self.debugger.get_resister("t0")
        seek_type = FileSeekType(whence)

        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_longlong_register("v0", "v1")

        if fd not in self.files:
            print(f"Seek in unknown file: {fd=}, {offset=}, {seek_type=}, {result=}")
            return

        file = self.files[fd]
        if result >= 0x80000000_00000000:
            print(f"Seek in {file.info()} failed: {offset=}, {seek_type=}, error code = 0x{result:X}")
            return

        self.handle_successful_seek(seek_type, file, offset, result)

    # TODO: on_seek_32 for sceIoLseek32?

    # TODO: meaning of sceIoRead depends on the file path (UMD gets special treatment), same for UmdFsRead
    def handle_successful_read(self, file: FileState, count: int, result: int):
        old_pos = FilePosition(file.pos.from_end, file.pos.position)

        expected_pos = FilePosition(file.pos.from_end, file.pos.position)
        expected_pos.advance(count)
        expected_bounds = f"[{old_pos}; {expected_pos}) (0x{count:x} bytes)"

        file.pos.advance(result)
        actual_bounds = f"[{old_pos}; {file.pos}) (0x{result:x} bytes)"

        print(f"Read from {file.info()}: {expected_bounds}; actually {actual_bounds}")

    def handle_read(self, fd: int, count: int, result: int):
        if fd not in self.files:
            print(f"Read in unknown file: {fd=}, {count=}, {result=}")
            return

        file = self.files[fd]
        if result >= 0x8000_0000:
            print(f"Read from {file.info()} failed: {count=}, error code = 0x{result:X}")
            return

        self.handle_successful_read(file, count, result)

    async def on_read(self):
        fd = await self.debugger.get_resister("a0")
        count = await self.debugger.get_resister("a2")

        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_resister("v0")

        self.handle_read(fd, count, result)

    async def handle_iso_fs_read(self, fd: int, in_arg: int):
        count = await self.debugger.read_u32(in_arg)
        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_resister("v0")

        self.handle_read(fd, count, result)

    async def handle_iso_fs_seek(self, fd: int, in_arg: int):
        offset = await self.debugger.read_u64(in_arg)
        whence = await self.debugger.read_u32(in_arg + 12)
        seek_type = FileSeekType(whence)

        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_resister("v0")

        if fd not in self.files:
            print(f"Seek in unknown file: {fd=}, {offset=}, {seek_type=}, {result=}")
            return

        file = self.files[fd]
        if result >= 0x80000000:
            print(f"Seek in {file.info()} failed: {offset=}, {seek_type=}, error code = 0x{result:X}")
            return

        self.handle_successful_seek(seek_type, file, offset, result)

    async def handle_umd_fs_read(self, fd: int, in_arg: int):
        sectors_cnt = await self.debugger.read_u32(in_arg)
        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_resister("v0")

        # TODO: maybe call something else once the sectors are properly implemented?
        self.handle_read(fd, sectors_cnt, result)

    async def handle_umd_fs_seek(self, fd: int, in_arg: int):
        offset = await self.debugger.read_u64(in_arg)
        whence = await self.debugger.read_u32(in_arg + 12)
        seek_type = FileSeekType(whence)

        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_resister("v0")

        if fd not in self.files:
            print(f"Seek in unknown file: {fd=}, {offset=}, {seek_type=}, {result=}")
            return

        file = self.files[fd]
        if result >= 0x80000000:
            print(f"Seek in {file.info()} failed: {offset=}, {seek_type=}, error code = 0x{result:X}")
            return

        # TODO: maybe call something else once the sectors are properly implemented?
        self.handle_successful_seek(seek_type, file, offset, result)

    async def on_ioctl(self):
        fd = await self.debugger.get_resister("a0")
        cmd = await self.debugger.get_resister("a1")
        in_arg = await self.debugger.get_resister("a2")
        match cmd:
            case IoctlCommand.IsoFsRead:
                await self.handle_iso_fs_read(fd, in_arg)
            case IoctlCommand.IsoFsSeek:
                await self.handle_iso_fs_seek(fd, in_arg)
            case IoctlCommand.UmdFsRead:
                await self.handle_umd_fs_read(fd, in_arg)
            case IoctlCommand.UmdFsSeek:
                await self.handle_umd_fs_seek(fd, in_arg)
            case (_):
                # That's not interesting. I guess we didn't need to grab fd and in_arg, but alas.
                pass
        pass

    async def process_successful_async_result(self, file: FileState, fd: int, io_res_ptr: int):
        match file.async_state:
            case FileAsyncState.PendingOpen:
                # IoRes is the actual fd
                actual_fd = await self.debugger.read_u32(io_res_ptr)
                file.async_state = FileAsyncState.NoAsync
                # Re-register the file under the correct fd
                del self.files[fd]
                assert actual_fd not in self.files
                self.files[actual_fd] = file
                print(f"Opened file {file.info()}")
                return

            case FileAsyncState.PendingClose:
                # IoRes is the result of "close"
                close_result = await self.debugger.read_u32(io_res_ptr)
                if close_result != 0:
                    print(f"Failed to close {file.info()}: error code {close_result:X}")
                    file.async_state = FileAsyncState.NoAsync
                    return
                print(f"Closed {file.info()}")
                del self.files[fd]
                return

            case FileAsyncState.PendingSeek:
                # IoRes is the result of "seek"
                seek_result = await self.debugger.read_u64(io_res_ptr)
                offset: int = file.async_args[0]
                seek_type: FileSeekType = file.async_args[1]

                if seek_result >= 0x80000000_00000000:
                    print(f"Seek in {file.info()} failed: {offset=}, {seek_type=}, error code = 0x{seek_result:X}")
                    file.async_state = FileAsyncState.NoAsync
                    return

                self.handle_successful_seek(seek_type, file, offset, seek_result)
                file.async_state = FileAsyncState.NoAsync
                return

            case FileAsyncState.PendingRead:
                # IoRes is the result of "read"
                read_result = await self.debugger.read_u32(io_res_ptr)
                count: int = file.async_args[0]

                self.handle_successful_read(file, count, read_result)
                file.async_state = FileAsyncState.NoAsync

            case FileAsyncState.PendingIoctl:
                result = await self.debugger.read_u32(io_res_ptr)
                cmd = IoctlCommand(file.async_args[0])
                match cmd:
                    case IoctlCommand.IsoFsRead:
                        count: int = file.async_args[1]
                        # For some reason checks if the fd is known. Not sure if it's bad or not.
                        self.handle_read(fd, count, result)
                        file.async_state = FileAsyncState.NoAsync
                    case IoctlCommand.IsoFsSeek:
                        offset: int = file.async_args[1]
                        seek_type: FileSeekType = file.async_args[2]
                        file = self.files[fd]
                        if result >= 0x80000000:
                            print(f"Seek in {file.info()} failed: {offset=}, {seek_type=}, error code = 0x{result:X}")
                            file.async_state = FileAsyncState.NoAsync
                            return
                        self.handle_successful_seek(seek_type, file, offset, result)
                        file.async_state = FileAsyncState.NoAsync

                    case IoctlCommand.UmdFsRead:
                        sectors_cnt: int = file.async_args[1]
                        # For some reason checks if the fd is known. Not sure if it's bad or not.
                        self.handle_read(fd, sectors_cnt, result)
                        # TODO: maybe call something else once the sectors are properly implemented?
                        file.async_state = FileAsyncState.NoAsync

                    case IoctlCommand.UmdFsSeek:
                        offset: int = file.async_args[1]
                        seek_type: FileSeekType = file.async_args[2]
                        file = self.files[fd]
                        if result >= 0x80000000:
                            print(f"Seek in {file.info()} failed: {offset=}, {seek_type=}, error code = 0x{result:X}")
                            return
                        # TODO: maybe call something else once the sectors are properly implemented?
                        self.handle_successful_seek(seek_type, file, offset, result)
                        file.async_state = FileAsyncState.NoAsync
                pass

    async def on_wait_async(self):
        fd = await self.debugger.get_resister("a0")
        io_res_ptr = await self.debugger.get_resister("a1")
        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_resister("v0")
        if fd not in self.files:
            print(f"Async operation for unknown file: {fd=}, {result=}")
            return
        file = self.files[fd]
        if result >= 0x8000_0000:
            if file.async_state == FileAsyncState.PendingOpen:
                print(f"Async file open failed for {file.name}, error code {result:X}")
                return

            print(f"Async operation failed for {file.info()}, state={file.async_state}")
            return

        # Gonna assume 'result' is zero
        await self.process_successful_async_result(file, fd, io_res_ptr)

    async def on_poll_async(self):
        fd = await self.debugger.get_resister("a0")
        io_res_ptr = await self.debugger.get_resister("a1")
        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_resister("v0")
        if fd not in self.files:
            print(f"Async operation for unknown file: {fd=}, {result=}")
            return

        file = self.files[fd]
        if result >= 0x8000_0000:
            if file.async_state == FileAsyncState.PendingOpen:
                print(f"Async file open failed for {file.name}, error code {result:X}")
                return

            print(f"Async operation failed for {file.info()}, state={file.async_state}")
            return

        # if result == 1:
        #     # Async operation has not completed yet
        #     pass
        if result != 0:
            return

        await self.process_successful_async_result(file, fd, io_res_ptr)

    async def on_open_async(self):
        name_addr = await self.debugger.get_resister("a0")
        filename = await self.debugger.read_string(name_addr)
        await self.debugger.step_out()
        await self.stepping_manager.wait()
        async_fd = await self.debugger.get_resister("v0")
        if async_fd >= 0x8000_0000:
            print(f"Async file open failed for {filename}: error code {async_fd:X}")
            return

        # Okay, let's store the file even though we're not certain it'll be opened successfully
        file = FileState(filename, async_fd, FilePosition(False, 0), FileAsyncState.PendingOpen)
        assert async_fd not in self.files
        self.files[async_fd] = file

        # The actual info will be extracted from the IoRes.
        # If the request fails, the file will be removed from self.files
        pass

    async def on_close_async(self):
        fd = await self.debugger.get_resister("a0")
        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_resister("v0")

        if fd not in self.files:
            print(f"Closing unknown file: {fd=}, {result=}")
            return
        file = self.files[fd]

        if result >= 0x8000_0000:
            print(f"Async close failed for {file.info()}")
            return
        file.async_state = FileAsyncState.PendingClose
        # The actual info will be extracted from the IoRes.
        # If the request succeeds, the file will be removed from self.files

    async def on_seek_async(self):
        fd = await self.debugger.get_resister("a0")
        offset = await self.debugger.get_longlong_register("a2", "a3")
        whence = await self.debugger.get_resister("t0")
        seek_type = FileSeekType(whence)

        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_resister("v0")

        if fd not in self.files:
            print(f"Seek in unknown file: {fd=}, {offset=}, {seek_type=}, {result=}")
            return
        file = self.files[fd]
        if result >= 0x8000_0000:
            print(f"Async seek failed for {file.info()}")
            return

        file.async_state = FileAsyncState.PendingSeek
        file.async_args = (offset, seek_type)
        # The actual info will be extracted from the IoRes.

    # TODO: on_seek_32_async for async version of sceIoLseek32?

    async def on_read_async(self):
        fd = await self.debugger.get_resister("a0")
        count = await self.debugger.get_resister("a2")

        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_resister("v0")

        if fd not in self.files:
            print(f"Read in unknown file: {fd=}, {count=}, {result=}")
            return

        file = self.files[fd]
        if result >= 0x8000_0000:
            print(f"Async read from {file.info()} failed: {count=}, error code = 0x{result:X}")
            return

        file.async_state = FileAsyncState.PendingRead
        file.async_args = (count,)
        # The actual info will be extracted from the IoRes.

    # Honestly, the code is identical here between the ISO and UMD funcs except for error logging...
    # Meanwhile, 'handle_iso_fs_seek_async' and 'handle_umd_fs_seek_async' are actually identical...
    async def handle_iso_fs_read_async(self, fd: int, in_arg: int):
        count = await self.debugger.read_u32(in_arg)
        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_resister("v0")

        if fd not in self.files:
            print(f"Read in unknown file: {fd=}, {count=}, {result=}")
            return
        file = self.files[fd]
        if result >= 0x8000_0000:
            print(f"Async ioctl read from {file.info()} failed: {count=}, error code = 0x{result:X}")
            return
        file.async_state = FileAsyncState.PendingIoctl
        file.async_args = (IoctlCommand.IsoFsRead, count,)

    async def handle_iso_fs_seek_async(self, fd: int, in_arg: int):
        offset = await self.debugger.read_u64(in_arg)
        whence = await self.debugger.read_u32(in_arg + 12)
        seek_type = FileSeekType(whence)

        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_resister("v0")

        if fd not in self.files:
            print(f"Seek in unknown file: {fd=}, {offset=}, {seek_type=}, {result=}")
            return

        file = self.files[fd]
        if result >= 0x80000000:
            print(f"Async ioctl seek in {file.info()} failed: {offset=}, {seek_type=}, error code = 0x{result:X}")
            return

        file.async_state = FileAsyncState.PendingIoctl
        file.async_args = (IoctlCommand.IsoFsRead, offset, seek_type,)

    async def handle_umd_fs_read_async(self, fd: int, in_arg: int):
        sectors_cnt = await self.debugger.read_u32(in_arg)
        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_resister("v0")

        if fd not in self.files:
            print(f"Read in unknown file: {fd=}, {sectors_cnt=}, {result=}")
            return
        file = self.files[fd]
        if result >= 0x8000_0000:
            print(f"Async ioctl read from {file.info()} failed: {sectors_cnt=}, error code = 0x{result:X}")
            return

        file.async_state = FileAsyncState.PendingIoctl
        file.async_args = (IoctlCommand.IsoFsRead, sectors_cnt,)

    async def handle_umd_fs_seek_async(self, fd: int, in_arg: int):
        offset = await self.debugger.read_u64(in_arg)
        whence = await self.debugger.read_u32(in_arg + 12)
        seek_type = FileSeekType(whence)

        await self.debugger.step_out()
        await self.stepping_manager.wait()
        result = await self.debugger.get_resister("v0")

        if fd not in self.files:
            print(f"Seek in unknown file: {fd=}, {offset=}, {seek_type=}, {result=}")
            return

        file = self.files[fd]
        if result >= 0x80000000:
            print(f"Async ioctl seek in {file.info()} failed: {offset=}, {seek_type=}, error code = 0x{result:X}")
            return

        file.async_state = FileAsyncState.PendingIoctl
        file.async_args = (IoctlCommand.IsoFsRead, offset, seek_type,)

    async def on_ioctl_async(self):
        fd = await self.debugger.get_resister("a0")
        cmd = await self.debugger.get_resister("a1")
        in_arg = await self.debugger.get_resister("a2")

        match cmd:
            case IoctlCommand.IsoFsRead:
                await self.handle_iso_fs_read_async(fd, in_arg)
            case IoctlCommand.IsoFsSeek:
                await self.handle_iso_fs_seek_async(fd, in_arg)
            case IoctlCommand.UmdFsRead:
                await self.handle_umd_fs_read_async(fd, in_arg)
            case IoctlCommand.UmdFsSeek:
                await self.handle_umd_fs_seek_async(fd, in_arg)
            case (_):
                # That's not interesting. I guess we didn't need to grab fd and in_arg, but alas.
                pass

        pass

    # Apparently sceIoDevctl is useless (it only puts data into cache)

def resolve_functions(expected_names: set[str], functions: list[FunctionSymbolInfo]):
    result: dict[str, int | None] = {}
    for func_info in functions:
        if func_info.name in expected_names:
            result[func_info.name] = func_info.address
            expected_names.discard(func_info.name)
            if not expected_names:
                return result
        pass
    # There may be unmatched functions
    result.update({name: None for name in expected_names})
    return result


class FuncManager:
    def __init__(self, debugger: 'Debugger'):
        self.debugger = debugger
        self.resolved_funcs: dict[str, int | None] = {}
        self.handlers: dict[int, SteppingHandler] = {}

    async def install_breakpoints(self, resolved: dict[str, int | None]):
        self.resolved_funcs = resolved
        async with asyncio.TaskGroup() as tg:
            for address in resolved.values():
                if address is not None:
                    tg.create_task(self.debugger.install_breakpoint(address))

    async def remove_breakpoints(self):
        async with asyncio.TaskGroup() as tg:
            for address in self.resolved_funcs.values():
                if address is not None:
                    tg.create_task(self.debugger.remove_breakpoint(address))

    def register_handlers(self, handlers: dict[str | int, SteppingHandler]):
        for func_info, handler in handlers.items():
            if isinstance(func_info, int):
                # Explicit address
                address = func_info
            else:
                # Name
                assert func_info in self.resolved_funcs

                address = self.resolved_funcs[func_info]
                if address is None:
                    # No handler for this func
                    continue
            self.handlers[address] = handler
        pass

    async def handle_stepping(self, stepping: CpuSteppingEvent):
        handler = self.handlers.get(stepping.pc)
        if handler is None:
            if self.debugger.stepping_manager.on_stepping():
                return

            # We don't know this breakpoint, it's none of our business
            logger.warning(f"Stepping at 0x{stepping.pc:x}, because '{stepping.reason}'")
            return

        result = await handler()
        if result is None or result:
            await self.debugger.resume()
        pass

class Debugger:
    def __init__(self):
        self.session: AsyncSession = AsyncSession()

        self.last_thread_name = ""
        self.stepping_manager = SteppingManager()
        self.func_manager = FuncManager(self)
        self.file_manager = FileManager(self, self.stepping_manager)

    async def get_resister(self, name: str):
        request = PPSSPPRequest("cpu.getReg")
        request.add(name=name)

        response = await self.session.execute_raw(request)

        return cast(CpuGetRegEvent, response).uint_value

    async def get_longlong_register(self, first: str, second: str):
        low = await self.get_resister(first)
        high = await self.get_resister(second)
        return low | (high << 32)

    async def read_string(self, address: int):
        request = PPSSPPRequest("memory.readString")
        request.add(address=address)

        response = await self.session.execute_raw(request)

        return cast(MemoryReadStringUtf8Event, response).value

    async def read_u32(self, address: int):
        request = PPSSPPRequest("memory.read_u32")
        request.add(address=address)

        response = await self.session.execute_raw(request)

        return cast(MemoryReadU32Event, response).value

    async def read_u64(self, address: int):
        # TODO: implement in PPSSPP for convenience
        low = await self.read_u32(address)
        high = await self.read_u32(address + 4)
        return low | (high << 32)

    async def step_out(self):
        request = PPSSPPRequest("cpu.stepOut")

        await self.session.send_request_raw(request)

    async def resume(self):
        request = PPSSPPRequest("cpu.resume")

        await self.session.send_request_raw(request)

    async def list_functions(self):
        request = PPSSPPRequest("hle.func.list")

        response = await self.session.execute_raw(request)
        return cast(HleFuncListEvent, response).functions

    def resolve_function_names(self, functions: list[FunctionSymbolInfo]):
        names = {
            "zz_sceIoOpen", "zz_sceIoRead", "zz_sceIoLseek", "zz_sceIoClose", "zz_sceIoIoctl",

            "zz_sceIoOpenAsync", "zz_sceIoWaitAsync", "zz_sceIoPollAsync", "zz_sceIoWaitAsyncCB",

            "zz_sceIoReadAsync", "zz_sceIoLseekAsync", "zz_sceIoCloseAsync", "zz_sceIoIoctlAsync"
        }
        resolved = resolve_functions(names, functions)
        return resolved

    async def on_stepping(self, event: BaseEvent):
        if type(event) is not CpuSteppingEvent:
            return
        event = cast(CpuSteppingEvent, event)

        await self.func_manager.handle_stepping(event)

    async def remove_breakpoint(self, address: int):
        request = PPSSPPRequest("cpu.breakpoint.remove")
        request.add(address=address)
        # I don't care about the confirmation here

        await self.session.send_request_raw(request)

    async def install_breakpoint(self, address: int):
        request = PPSSPPRequest("cpu.breakpoint.add")
        request.add(address=address, enabled=True)

        await self.session.send_request_raw(request)

    async def disable_ppsspp_logs(self):
        request = PPSSPPRequest("broadcast.config.set")
        request.add(disallowed={"logger": True})

        await self.session.execute_raw(request)

    async def execute_script(self):
        # Register the handler
        @self.session.stepping_handler()
        async def on_stepping(event: BaseEvent):
            event = cast(CpuSteppingEvent, event)
            await self.on_stepping(event)


        funcs = await self.list_functions()
        await self.disable_ppsspp_logs()
        resolved = self.resolve_function_names(funcs)
        await self.func_manager.install_breakpoints(resolved)
        self.func_manager.register_handlers({
            "zz_sceIoOpen": self.file_manager.on_open,
            "zz_sceIoRead": self.file_manager.on_read,
            "zz_sceIoLseek": self.file_manager.on_seek,
            "zz_sceIoClose": self.file_manager.on_close,
            "zz_sceIoIoctl": self.file_manager.on_ioctl,

            "zz_sceIoWaitAsync": self.file_manager.on_wait_async,
            "zz_sceIoWaitAsyncCB": self.file_manager.on_wait_async,
            "zz_sceIoPollAsync": self.file_manager.on_poll_async,

            "zz_sceIoOpenAsync": self.file_manager.on_open_async,
            "zz_sceIoReadAsync": self.file_manager.on_read_async,
            "zz_sceIoLseekAsync": self.file_manager.on_seek_async,
            "zz_sceIoCloseAsync": self.file_manager.on_close_async,
            "zz_sceIoIoctlAsync": self.file_manager.on_ioctl_async,
        })

    async def cleanup(self):
        # Might not even be installed, that doesn't matter
        await self.func_manager.remove_breakpoints()

    async def run(self, uri: str):
        connection = AsyncPpssppConnection()
        print("Connecting...")
        should_cleanup = False
        ending = False

        @connection.on_disconnected
        async def on_disconnected(conn: AsyncPpssppConnection):
            nonlocal should_cleanup, ending
            should_cleanup = False
            ending = True
            return False

        try:
            await connection.connect(uri)
            print("Connected!")
            should_cleanup = True

            await self.session.run(connection)
            await self.execute_script()
            while not ending:
                await asyncio.sleep(1)

        except (KeyboardInterrupt, asyncio.CancelledError):
            print("Exiting...")
            pass
        except RequestFailedError as e:
            logger.critical(f"Request {e.failed_request} failed: {e.error}")
        except ConnectionRefusedError as e:
            print(f"Connection refused: {e}")
            print("Exiting")

        if should_cleanup:
            await self.cleanup()

        await self.session.stop()


async def main():
    debugger = Debugger()

    # uri = "ws://192.168.1.134:55488/debugger"
    uri = "ws://127.0.0.1:55488/debugger"
    await debugger.run(uri)

    print("The debugger is stopped!")


if __name__ == "__main__":
    asyncio.run(main())
