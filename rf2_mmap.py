"""
rF2 Memory Map Control for accessing The Iron Wolf's rF2 Shared Memory Plugin interface

Memory map control (author: Xiang)
Cross-platform Linux support (author: Bernat)
"""

from __future__ import annotations

import ctypes
import logging
import mmap
import sys

from . import rf2_data
from ._common import get_root_logger_name

logger = logging.getLogger(get_root_logger_name())


def platform_mmap(name: str, size: int, pid: str = "") -> mmap.mmap:
    """Platform memory mapping"""
    if sys.platform == "win32":
        return windows_mmap(name, size, pid)
    return linux_mmap(name, size, pid)


def windows_mmap(name: str, size: int, pid: str) -> mmap.mmap:
    """Windows mmap"""
    return mmap.mmap(-1, size, f"{name}{pid}")


def linux_mmap(name: str, size: int, pid: str) -> mmap.mmap | None:
    """Linux mmap - read data from '/dev/shm/filename' if available"""
    with open(f"/dev/shm/{name}{pid}", "a+b") as file:
        stream_pos = file.tell()
        if stream_pos == 0:  # file is empty
            file.write(b"\0" * size)
            file.flush()
        elif stream_pos != size:  # file size doesn't match struct size
            file.seek(0)
            file.truncate(0)  # clear all data
            file.seek(0)
            file.write(b"\0" * size)
            file.flush()
        return mmap.mmap(file.fileno(), size)


class MMapControl:
    """Memory map control"""

    __slots__ = (
        "_buffer",
        "_mmap_buffer",
        "_mmap_name",
        "_struct",
        "_version",
        "data",
        "update",
    )

    def __init__(self, mmap_name: str, data_struct: ctypes.Structure) -> None:
        """Initialize memory map setting

        Args:
            mmap_name: mmap filename, ex. $rFactor2SMMP_Scoring$.
            data_struct: ctypes data structure, ex. rF2data.rF2Scoring.
        """
        self._buffer = bytearray()
        self._mmap_buffer = None
        self._mmap_name = mmap_name
        self._struct = data_struct
        self._version = None
        self.update = None
        self.data = None

    def __del__(self):
        logger.info("sharedmemory: GC: MMap %s", self._mmap_name)

    def create(self, access_mode: int = 0, server_pid: str = "") -> None:
        """Create mmap instance & initial accessible copy

        Args:
            access_mode: 0 = copy access, 1 = direct access.
            server_pid: rF2 Process ID for accessing server data.
        """
        self._mmap_buffer = platform_mmap(
            name=self._mmap_name,
            size=ctypes.sizeof(self._struct),
            pid=server_pid
        )

        if access_mode:
            self.data = self._struct.from_buffer(self._mmap_buffer)
            self.update = self.__buffer_share
        else:
            self._buffer[:] = self._mmap_buffer
            self.data = self._struct.from_buffer(self._buffer)
            self._version = rf2_data.rF2MappedBufferVersionBlock.from_buffer(self._mmap_buffer)
            self.update = self.__buffer_copy

        mode = "Direct" if access_mode else "Copy"
        logger.info("sharedmemory: ACTIVE: %s (%s Access)", self._mmap_name, mode)

    def close(self) -> None:
        """Close memory mapping

        Create a final accessible mmap data copy before closing mmap instance.
        """
        self.data = self._struct.from_buffer_copy(self._mmap_buffer)
        self._version = None
        try:
            self._mmap_buffer.close()
            logger.info("sharedmemory: CLOSED: %s", self._mmap_name)
        except BufferError:
            logger.error("sharedmemory: buffer error while closing %s", self._mmap_name)
        self.update = None  # unassign update method (for proper garbage collection)

    def __buffer_share(self) -> None:
        """Share buffer access, may result data desync"""

    def __buffer_copy(self) -> None:
        """Copy buffer access, helps avoid data desync"""
        # Copy if data version changed
        if self.data.mVersionUpdateEnd != self._version.mVersionUpdateEnd == self._version.mVersionUpdateBegin:
            self._buffer[:] = self._mmap_buffer
