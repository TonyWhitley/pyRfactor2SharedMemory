"""
rF2 Memory Map Control

Inherit Python mapping of The Iron Wolf's rF2 Shared Memory Tools

Memory map control (by S.Victor)
Cross-platform Linux support (by Bernat)
"""

from __future__ import annotations

import ctypes
import logging
import mmap
import platform

try:
    from . import rF2data
    from .rF2data import rFactor2Constants
except ImportError:  # standalone, not package
    import rF2data
    from rF2data import rFactor2Constants

PLATFORM = platform.system()
MAX_VEHICLES = rFactor2Constants.MAX_MAPPED_VEHICLES
INVALID_INDEX = -1


def get_root_logger_name():
    """Get root logger name"""
    for logger_name in logging.root.manager.loggerDict:
        return logger_name
    return __name__


logger = logging.getLogger(get_root_logger_name())


def platform_mmap(name: str, size: int, pid: str = "") -> mmap.mmap:
    """Platform memory mapping"""
    if PLATFORM == "Windows":
        return windows_mmap(name, size, pid)
    return linux_mmap(name, size)


def windows_mmap(name: str, size: int, pid: str) -> mmap.mmap:
    """Windows mmap"""
    return mmap.mmap(-1, size, f"{name}{pid}")


def linux_mmap(name: str, size: int) -> mmap.mmap:
    """Linux mmap"""
    file = open("/dev/shm/" + name, "a+b")
    if file.tell() == 0:
        file.write(b"\0" * size)
        file.flush()
    return mmap.mmap(file.fileno(), size)


class MMapControl:
    """Memory map control"""

    __slots__ = (
        "_mmap_name",
        "_mmap_buffer",
        "_struct",
        "_buffer",
        "_version",
        "update",
        "data",
    )

    def __init__(self, mmap_name: str, data_struct: ctypes.Structure) -> None:
        """Initialize memory map setting

        Args:
            mmap_name: mmap filename, ex. $rFactor2SMMP_Scoring$.
            data_struct: ctypes data structure, ex. rF2data.rF2Scoring.
        """
        self._mmap_name = mmap_name
        self._mmap_buffer = None
        self._struct = data_struct
        self._buffer = bytearray()
        self._version = None
        self.update = None
        self.data = None

    def __del__(self):
        logger.info("sharedmemory: GC: MMap %s", self._mmap_name)

    def create(self, access_mode: int = 0, rf2_pid: str = "") -> None:
        """Create mmap instance & initial accessible copy

        Args:
            access_mode: 0 = copy access, 1 = direct access.
            rf2_pid: rF2 Process ID for accessing server data.
        """
        self._mmap_buffer = platform_mmap(
            name=self._mmap_name,
            size=ctypes.sizeof(self._struct),
            pid=rf2_pid
        )

        if access_mode:
            self.data = self._struct.from_buffer(self._mmap_buffer)
            self.update = self.__buffer_share
        else:
            self._buffer[:] = self._mmap_buffer
            self.data = self._struct.from_buffer(self._buffer)
            self._version = rF2data.rF2MappedBufferVersionBlock.from_buffer(self._mmap_buffer)
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


def test_api():
    """API test run"""
    # Add logger
    test_handler = logging.StreamHandler()
    logger.setLevel(logging.INFO)
    logger.addHandler(test_handler)

    # Test run
    SEPARATOR = "=" * 50
    print("Test API - Start")
    scoring = MMapControl(rFactor2Constants.MM_SCORING_FILE_NAME, rF2data.rF2Scoring)
    scoring.create(1)
    telemetry = MMapControl(rFactor2Constants.MM_TELEMETRY_FILE_NAME, rF2data.rF2Telemetry)
    telemetry.create(1)
    extended = MMapControl(rFactor2Constants.MM_EXTENDED_FILE_NAME, rF2data.rF2Extended)
    extended.create(1)

    print(SEPARATOR)
    print("Test API - Read")
    version = extended.data.mVersion.decode()
    track = scoring.data.mScoringInfo.mTrackName.decode(encoding="iso-8859-1")
    vehicles = telemetry.data.mNumVehicles
    print(f"plugin ver: {version if version else 'not running'}")
    print(f"track name: {track if version else 'not running'}")
    print(f"total cars: {vehicles if version else 'not running'}")

    print(SEPARATOR)
    print("Test API - Close")
    scoring.close()
    telemetry.close()
    extended.close()


if __name__ == "__main__":
    test_api()
