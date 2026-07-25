import typing
from dataclasses import dataclass

from enum import Enum


# The fields are like in ReplayFlushEvent, but the data is decoded as bytes
@dataclass
class ReplayData:
    version: int
    raw: bytes


# Not providing the full code for handling the binary format, this should be a separate utility...
# But some basic structs can't hurt. The following applies for the version 1.

@dataclass
class ReplayFileHeader:
    magic: typing.Literal["PPREPLAY"]
    version: int
    reserved1: int
    reserved2: int
    reserved3: int
    rtcBaseSeconds: int


class ReplayAction(Enum):
    BUTTONS = 0x00,  # buttons
    ANALOG = 0x01,  # analog
    FILE_RENAME = 0x40,  # result
    FILE_REMOVE = 0x41,  # result
    FILE_READ = 0xC2,  # sidedata
    FILE_OPEN = 0x43,  # result
    FILE_SEEK = 0x44,  # result64
    FILE_INFO = 0xC5,  # sidedata
    FILE_LISTING = 0xC6,  # sidedata
    MKDIR = 0x47,  # result
    RMDIR = 0x48,  # result
    FREESPACE = 0x49,  # result64

    # Some masks
    MASK_FILE = 0x40,
    MASK_SIDEDATA = 0x80,


@dataclass
class ReplayItemHeader:
    action: ReplayAction
    timestamp: int
    # Then some int value, depending on the action
    # Could be 4 bytes with 4 padding or 8 bytes with no padding (see 'result', 'result64', 'sidedata' etc.)
    remaining_header: int

    # If the action has a sidedata, its size is encoded in the int value, then we have the raw bytes.
    # They can also be meaningfully decoded in certain situations.


@dataclass
class ReplayFileInfo:
    filename: str
    size: int
    access: int
    exists: int
    isDirectory: int
    atime: int
    ctime: int
    mtime: int


@dataclass
class ReplayFileRead:
    data: bytes


@dataclass
class ReplayFileListing:
    listing: list[ReplayFileInfo]
