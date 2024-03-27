"""
rF2 Memory Map

Inherit Python mapping of The Iron Wolf's rF2 Shared Memory Tools,
with player-synchronized accessing (by S.Victor)
and cross-platform Linux support (by Bernat)
"""

from __future__ import annotations
import copy
import ctypes
import logging
import mmap
import platform
import time
import threading

try:
    from . import rF2data
except ImportError:  # standalone, not package
    import rF2data

PLATFORM = platform.system()
MAX_VEHICLES = rF2data.rFactor2Constants.MAX_MAPPED_VEHICLES
INVALID_INDEX = -1

logger = logging.getLogger(__name__)


def platform_mmap(name: str, size: int, pid: str = "") -> mmap:
    """Platform memory mapping"""
    if PLATFORM == "Windows":
        return windows_mmap(name, size, pid)
    return linux_mmap(name, size)


def windows_mmap(name: str, size: int, pid: str) -> mmap:
    """Windows mmap"""
    return mmap.mmap(-1, size, f"{name}{pid}")


def linux_mmap(name: str, size: int) -> mmap:
    """Linux mmap"""
    file = open("/dev/shm/" + name, "a+b")
    if file.tell() == 0:
        file.write(b"\0" * size)
        file.flush()
    return mmap.mmap(file.fileno(), size)


class RF2MMap:
    """Create rF2 Memory Map

    Attributes:
        mmap_id: mmap name string.
    """

    def __init__(self, mmap_name: str, rf2_data: object) -> None:
        """Initialize memory map setting

        Args:
            mmap_name: mmap filename, ex. $rFactor2SMMP_Scoring$.
            rf2_data: rF2 data class defined in rF2data, ex. rF2data.rF2Scoring.
        """
        self.mmap_id = mmap_name.strip("$")
        self._mmap_name = mmap_name
        self._rf2_data = rf2_data
        self._mmap_instance = None
        self._mmap_output = None
        self._access_mode = 0
        self._buffer_sharing = False

    def create(self, access_mode: int = 0, rf2_pid: str = "") -> None:
        """Create mmap instance & initial accessible copy

        Args:
            access_mode: 0 = copy access, 1 = direct access.
            rf2_pid: rF2 Process ID for accessing server data.
        """
        self._access_mode = access_mode
        self._mmap_instance = platform_mmap(
            name=self._mmap_name,
            size=ctypes.sizeof(self._rf2_data),
            pid=rf2_pid
        )
        self.__buffer_copy(True)
        mode = "Direct" if access_mode else "Copy"
        logger.info("sharedmemory: ACTIVE: %s (%s Access)", self.mmap_id, mode)

    def close(self) -> None:
        """Close memory mapping

        Create a final accessible mmap data copy before closing mmap instance.
        """
        self.__buffer_copy(True)
        self._buffer_sharing = False
        try:
            self._mmap_instance.close()
            logger.info("sharedmemory: CLOSED: %s", self.mmap_id)
        except BufferError:
            logger.error("sharedmemory: buffer error while closing mmap")

    def update(self) -> None:
        """Update mmap data"""
        if self._access_mode:
            self.__buffer_share()
        else:
            self.__buffer_copy()

    @property
    def data(self):
        """Output mmap data"""
        return self._mmap_output

    def __buffer_share(self) -> None:
        """Share buffer direct access, may result desync"""
        if not self._buffer_sharing:
            self._buffer_sharing = True
            self._mmap_output = self._rf2_data.from_buffer(self._mmap_instance)

    def __buffer_copy(self, skip_check: bool = False) -> None:
        """Copy buffer access, check version before assign new data copy

        Args:
            skip_check: skip data version check.
        """
        temp = self._rf2_data.from_buffer_copy(self._mmap_instance)
        if temp.mVersionUpdateEnd == temp.mVersionUpdateBegin or skip_check:
            self._mmap_output = temp


class MMapDataSet:
    """Create mmap data set"""

    def __init__(self) -> None:
        self._scor = RF2MMap("$rFactor2SMMP_Scoring$", rF2data.rF2Scoring)
        self._tele = RF2MMap("$rFactor2SMMP_Telemetry$", rF2data.rF2Telemetry)
        self._ext = RF2MMap("$rFactor2SMMP_Extended$", rF2data.rF2Extended)
        self._ffb = RF2MMap("$rFactor2SMMP_ForceFeedback$", rF2data.rF2ForceFeedback)

    def create_mmap(self, access_mode: int, rf2_pid: str) -> None:
        """Create mmap instance

        Args:
            access_mode: 0 = copy access, 1 = direct access.
            rf2_pid: rF2 Process ID for accessing server data.
        """
        self._scor.create(access_mode, rf2_pid)
        self._tele.create(access_mode, rf2_pid)
        self._ext.create(1, rf2_pid)
        self._ffb.create(1, rf2_pid)

    def close_mmap(self) -> None:
        """Close mmap instance"""
        self._scor.close()
        self._tele.close()
        self._ext.close()
        self._ffb.close()

    def update_mmap(self) -> None:
        """Update mmap data"""
        self._scor.update()
        self._tele.update()
        self._ext.update()
        self._ffb.update()

    @property
    def scor(self):
        """Scoring data"""
        return self._scor.data

    @property
    def tele(self):
        """Telemetry data"""
        return self._tele.data

    @property
    def ext(self):
        """Extended data"""
        return self._ext.data

    @property
    def ffb(self):
        """Force feedback data"""
        return self._ffb.data


class SyncData:
    """Synchronize data with player ID

    Attributes:
        dataset: mmap data set.
        paused: Data update state (boolean).
        override_player_index: Player index override state (boolean).
        player_scor_index: Local player scoring index.
        player_scor: Local player scoring data.
        player_tele: Local player telemetry data.
    """

    def __init__(self) -> None:
        self._updating = False
        self._update_thread = None
        self._event = threading.Event()
        self._tele_idx_dict = {_index: _index for _index in range(128)}

        self.dataset = MMapDataSet()
        self.paused = False
        self.override_player_index = False
        self.player_scor_index = INVALID_INDEX
        self.player_scor = None
        self.player_tele = None

    def copy_player_scor(self, index: int = INVALID_INDEX) -> None:
        """Copy scoring player data from matching index"""
        self.player_scor = copy.copy(self.dataset.scor.mVehicles[index])

    def copy_player_tele(self, index: int = INVALID_INDEX) -> None:
        """Copy telemetry player data from matching index"""
        self.player_tele = copy.copy(self.dataset.tele.mVehicles[index])

    def __local_scor_index(self) -> int:
        """Find local player scoring index"""
        for scor_idx in range(MAX_VEHICLES):
            if self.dataset.scor.mVehicles[scor_idx].mIsPlayer:
                return scor_idx
        return INVALID_INDEX

    def __sync_player_data(self) -> bool:
        """Sync local player data

        Returns:
            False, if no valid player scoring index found.
            True, update player data copy.
        """
        if not self.override_player_index:
            # Update scoring index
            scor_idx = self.__local_scor_index()
            if scor_idx == INVALID_INDEX:
                return False  # index not found, not synced
            self.player_scor_index = scor_idx
        # Copy player data
        self.copy_player_scor(self.player_scor_index)
        self.copy_player_tele(self.sync_tele_index(self.player_scor_index))
        return True  # found index, synced

    def __update_tele_index_dict(self, num_vehicles: int) -> None:
        """Update telemetry player index dictionary for quick reference

        Telemetry index can be different from scoring index.
        Use mID matching to match telemetry index.

        _tele_idx_dict: Telemetry mID:index reference dictionary.

        Args:
            num_vehicles: Total number of vehicles.
        """
        for _index in range(num_vehicles):
            self._tele_idx_dict[self.dataset.tele.mVehicles[_index].mID] = _index

    def sync_tele_index(self, scor_idx: int) -> int:
        """Sync telemetry index

        Use scoring index to find scoring mID,
        then match with telemetry mID in tele_idx_dict
        to find telemetry index.

        Args:
            scor_idx: Player scoring index.

        Returns:
            Player telemetry index.
        """
        return self._tele_idx_dict.get(
            self.dataset.scor.mVehicles[scor_idx].mID, INVALID_INDEX)

    def start(self, access_mode: int, rf2_pid: str) -> None:
        """Update & sync mmap data copy in separate thread

        Args:
            access_mode: 0 = copy access, 1 = direct access.
            rf2_pid: rF2 Process ID for accessing server data.
        """
        if self._updating:
            logger.warning("sharedmemory: UPDATING: already started")
        else:
            self._updating = True
            # Initialize mmap data
            self.dataset.create_mmap(access_mode, rf2_pid)
            self.__update_tele_index_dict(self.dataset.tele.mNumVehicles)
            if not self.__sync_player_data():
                self.copy_player_scor()
                self.copy_player_tele()
            # Setup updating thread
            self._event.clear()
            self._update_thread = threading.Thread(
                target=self.__update, daemon=True)
            self._update_thread.start()
            logger.info("sharedmemory: UPDATING: thread started")
            logger.info("sharedmemory: player index override: %s", self.override_player_index)
            logger.info("sharedmemory: server process ID: %s", rf2_pid if rf2_pid else "DISABLED")

    def stop(self) -> None:
        """Join and stop updating thread, close mmap"""
        if self._updating:
            self._event.set()
            self._updating = False
            self._update_thread.join()
            self.dataset.close_mmap()
        else:
            logger.warning("sharedmemory: UPDATING: already stopped")

    def __update(self) -> None:
        """Update synced player data"""
        self.paused = False  # make sure initial pause state is false
        freezed_version = 0  # store freezed update version number
        last_version_update = 0  # store last update version number
        last_update_time = 0
        data_freezed = True  # whether data is freezed
        reset_counter = 0
        update_delay = 0.5  # longer delay while inactive

        while not self._event.wait(update_delay):
            self.dataset.update_mmap()
            self.__update_tele_index_dict(self.dataset.tele.mNumVehicles)
            # Update player data & index
            if not data_freezed:
                # Get player data
                data_synced = self.__sync_player_data()
                # Pause if local player index no longer exists, 5 tries
                if not data_synced and reset_counter < 6:
                    reset_counter += 1
                elif data_synced:
                    reset_counter = 0
                    self.paused = False
                # Activate pause
                if reset_counter == 5:
                    self.paused = True
                    logger.info("sharedmemory: UPDATING: player data paused")

            if last_version_update != self.dataset.scor.mVersionUpdateEnd:
                last_update_time = time.time()
                last_version_update = self.dataset.scor.mVersionUpdateEnd

            # Set freeze state if data stopped updating after 2s
            if not data_freezed and time.time() - last_update_time > 2:
                update_delay = 0.5
                data_freezed = True
                self.paused = True
                freezed_version = last_version_update
                logger.info(
                    "sharedmemory: UPDATING: paused, data version %s", freezed_version)

            if data_freezed and freezed_version != last_version_update:
                update_delay = 0.01
                data_freezed = False
                self.paused = False
                logger.info(
                    "sharedmemory: UPDATING: resumed, data version %s", last_version_update)

        logger.info("sharedmemory: UPDATING: thread stopped")


class RF2SM:
    """RF2 shared memory data output"""

    def __init__(self) -> None:
        self._sync = SyncData()
        self._access_mode = 0
        self._rf2_pid = ""

    def start(self) -> None:
        """Start data updating thread"""
        self._sync.start(self._access_mode, self._rf2_pid)

    def stop(self) -> None:
        """Stop data updating thread"""
        self._sync.stop()

    def setPID(self, pid: str = "") -> None:
        """Set rF2 process ID for connecting to server data"""
        self._rf2_pid = str(pid)

    def setMode(self, mode: int = 0) -> None:
        """Set rF2 mmap access mode

        Args:
            mode: 0 = copy access, 1 = direct access
        """
        self._access_mode = mode

    def setPlayerOverride(self, state: bool = False) -> None:
        """Enable player index override state"""
        self._sync.override_player_index = state

    def setPlayerIndex(self, index: int = INVALID_INDEX) -> None:
        """Manual override player index"""
        self._sync.player_scor_index = min(max(index, INVALID_INDEX), MAX_VEHICLES - 1)

    @property
    def rf2ScorInfo(self) -> object:
        """rF2 scoring info data"""
        return self._sync.dataset.scor.mScoringInfo

    def rf2ScorVeh(self, index: int | None = None) -> object:
        """rF2 scoring vehicle data

        Specify index for specific player.

        Args:
            index: None for local player.
        """
        if index is None:
            return self._sync.player_scor
        return self._sync.dataset.scor.mVehicles[index]

    def rf2TeleVeh(self, index: int | None = None) -> object:
        """rF2 telemetry vehicle data

        Specify index for specific player.

        Args:
            index: None for local player.
        """
        if index is None:
            return self._sync.player_tele
        return self._sync.dataset.tele.mVehicles[self._sync.sync_tele_index(index)]

    @property
    def rf2Ext(self) -> object:
        """rF2 extended data"""
        return self._sync.dataset.ext

    @property
    def rf2Ffb(self) -> object:
        """rF2 force feedback data"""
        return self._sync.dataset.ffb

    @property
    def playerIndex(self) -> int:
        """rF2 local player's scoring index"""
        return self._sync.player_scor_index

    def isPlayer(self, index: int) -> bool:
        """Check whether index is player"""
        if self._sync.override_player_index:
            return self._sync.player_scor_index == index
        return self._sync.dataset.scor.mVehicles[index].mIsPlayer

    @property
    def isPaused(self) -> bool:
        """Check whether data stopped updating"""
        return self._sync.paused


if __name__ == "__main__":
    # Add logger
    test_handler = logging.StreamHandler()
    logger.setLevel(logging.INFO)
    logger.addHandler(test_handler)

    # Test run
    SEPARATOR = "=" * 50
    print("Test API - Start")
    info = RF2SM()
    info.setMode(1)  # set direct access
    info.setPID("")
    info.setPlayerOverride(True)  # enable player override
    info.setPlayerIndex(0)  # set player index to 0
    info.start()
    time.sleep(0.2)

    print(SEPARATOR)
    print("Test API - Read")
    version = info.rf2Ext.mVersion.decode()
    driver = info.rf2ScorVeh(0).mDriverName.decode(encoding="iso-8859-1")
    track = info.rf2ScorInfo.mTrackName.decode(encoding="iso-8859-1")
    print(f"plugin version: {version if version else 'not running'}")
    print(f"driver name   : {driver if version else 'not running'}")
    print(f"track name    : {track if version else 'not running'}")

    print(SEPARATOR)
    print("Test API - Restart")
    info.stop()
    info.setMode(0)  # set copy access
    info.setPlayerOverride(False)  # disable player override
    info.start()

    print(SEPARATOR)
    print("Test API - Multi starts")
    info.start()
    info.start()
    info.start()
    info.start()

    print(SEPARATOR)
    print("Test API - Close")
    info.stop()

    print(SEPARATOR)
    print("Test API - Multi stop")
    info.stop()
    info.stop()
    info.stop()
