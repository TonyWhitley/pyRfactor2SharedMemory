"""
rF2 Memory Map

Inherit Python mapping of The Iron Wolf's rF2 Shared Memory Tools,
with player-synchronized accessing (by S.Victor)
and cross-platform Linux support (by Bernat)
"""

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

    mmap_name: mmap filename, ex. $rFactor2SMMP_Scoring$
    rf2_data: rf2 data class defined in rF2data, ex. rF2data.rF2Scoring
    rf2_pid: rf2 Process ID for accessing server data
    """

    def __init__(self, mmap_name: str, rf2_data) -> None:
        self.mmap_id = mmap_name.strip("$")
        self._mmap_name = mmap_name
        self._rf2_data = rf2_data
        self._mmap_instance = None
        self._mmap_output = None
        self._access_mode = 0
        self._buffer_sharing = False

    def create(self, access_mode: int = 0, rf2_pid: str = "") -> None:
        """Create mmap instance & initial accessible copy"""
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

    def __buffer_copy(self, skip_check=False) -> None:
        """Copy buffer access, check version before assign"""
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
        self.mmap_active = [self._scor, self._tele, self._ext, self._ffb]

    def create_mmap(self, access_mode: int, rf2_pid: str) -> None:
        """Create mmap instance"""
        for data in self.mmap_active:
            data.create(access_mode, rf2_pid)

    def close_mmap(self) -> None:
        """Close mmap instance"""
        for data in self.mmap_active:
            data.close()

    def update_mmap(self) -> None:
        """Update mmap data"""
        for data in self.mmap_active:
            data.update()

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
    """Synchronize data with player ID"""

    def __init__(self) -> None:
        self.dataset = MMapDataSet()
        self.updating = False
        self.update_thread = None
        self.paused = True
        self.event = threading.Event()

        self.override_player_index = False
        self.player_scor_index = INVALID_INDEX
        self.player_scor = None
        self.player_tele = None
        self.tele_idx_dict = {idx: idx for idx in range(128)}

    def copy_player_scor(self, index: int = INVALID_INDEX) -> None:
        """Copy scoring player data"""
        self.player_scor = copy.copy(self.dataset.scor.mVehicles[index])

    def copy_player_tele(self, index: int = INVALID_INDEX) -> None:
        """Copy telemetry player data"""
        self.player_tele = copy.copy(self.dataset.tele.mVehicles[index])

    def __local_scor_index(self) -> int:
        """Find local player scoring index

        Check last found index first.
        If not player, loop through all vehicles.
        """
        for scor_idx in range(MAX_VEHICLES):
            if self.dataset.scor.mVehicles[scor_idx].mIsPlayer:
                return scor_idx
        return INVALID_INDEX

    def __sync_player_data(self) -> bool:
        """Sync local player data"""
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
        key: Tele mID
        value: Tele index
        """
        for idx in range(num_vehicles):
            self.tele_idx_dict[self.dataset.tele.mVehicles[idx].mID] = idx

    def sync_tele_index(self, scor_idx: int) -> int:
        """Find & sync telemetry index

        Match scoring mID with telemetry mID in tele_idx_dict
        """
        return self.tele_idx_dict[self.dataset.scor.mVehicles[scor_idx].mID]

    def start(self, access_mode: int, rf2_pid: str) -> None:
        """Update & sync mmap data copy in separate thread"""
        if self.updating:
            logger.warning("sharedmemory: UPDATING: already started")
        else:
            self.updating = True
            self.event.clear()
            self.dataset.create_mmap(access_mode, rf2_pid)
            self.copy_player_scor()
            self.copy_player_tele()

            self.update_thread = threading.Thread(
                target=self.__update, daemon=True)
            self.update_thread.start()
            logger.info("sharedmemory: UPDATING: thread started")
            logger.info("sharedmemory: player index override: %s", self.override_player_index)
            logger.info("sharedmemory: server process ID: %s", rf2_pid if rf2_pid else "DISABLED")

    def stop(self) -> None:
        """Join and stop updating thread, close mmap"""
        if self.updating:
            self.event.set()
            self.updating = False
            self.update_thread.join()
            self.dataset.close_mmap()
        else:
            logger.warning("sharedmemory: UPDATING: already stopped")

    def __update(self) -> None:
        """Update synced player data"""
        last_version_update = 0  # store last data version update
        data_freezed = True      # whether data is freezed
        check_timer_start = 0
        reset_counter = 0
        update_delay = 0.5  # longer delay while inactive

        while not self.event.wait(update_delay):
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

            # Start checking data version update status
            if time.time() - check_timer_start > 5:
                if (not data_freezed
                    and last_version_update == self.dataset.scor.mVersionUpdateEnd):
                    update_delay = 0.5
                    data_freezed = True
                    self.paused = True
                    logger.info(
                        "sharedmemory: UPDATING: paused, data version %s",
                        last_version_update)
                last_version_update = self.dataset.scor.mVersionUpdateEnd
                check_timer_start = time.time()  # reset timer

            if (data_freezed
                and last_version_update != self.dataset.scor.mVersionUpdateEnd):
                update_delay = 0.01
                data_freezed = False
                self.paused = False
                logger.info(
                    "sharedmemory: UPDATING: resumed, data version %s",
                    self.dataset.scor.mVersionUpdateEnd)

        self.paused = False
        logger.info("sharedmemory: UPDATING: thread stopped")


class RF2SM:
    """
    RF2 shared memory data output

    Optional parameters:
        setMode: set access mode, 0 = copy access, 1 = direct access
        setPID: set process ID for connecting to server data (str)
        setPlayerOverride: enable player index override (bool)
        setPlayerIndex: manually set player index (int)
    """

    def __init__(self) -> None:
        self._sync = SyncData()
        self.access_mode = 0
        self.rf2_pid = ""

    def start(self) -> None:
        """Start data updating thread"""
        self._sync.start(self.access_mode, self.rf2_pid)

    def stop(self) -> None:
        """Stop data updating thread"""
        self._sync.stop()

    def setPID(self, pid: str = "") -> None:
        """Set rf2 PID"""
        self.rf2_pid = str(pid)

    def setMode(self, mode: int = 0) -> None:
        """Set rf2 mmap access mode"""
        self.access_mode = mode

    def setPlayerOverride(self, state: bool = False) -> None:
        """Set player index override state"""
        self._sync.override_player_index = state

    def setPlayerIndex(self, idx: int = INVALID_INDEX) -> None:
        """Set player index"""
        self._sync.player_scor_index = min(max(idx, INVALID_INDEX), MAX_VEHICLES - 1)

    @property
    def rf2ScorInfo(self):
        """rF2 scoring info data"""
        return self._sync.dataset.scor.mScoringInfo

    def rf2ScorVeh(self, index: int = None):
        """rF2 scoring vehicle data

        Specify index for specific player.
        None for local player.
        """
        if index is None:
            return self._sync.player_scor
        return self._sync.dataset.scor.mVehicles[index]

    def rf2TeleVeh(self, index: int = None):
        """rF2 telemetry vehicle data

        Specify index for specific player.
        None for local player.
        """
        if index is None:
            return self._sync.player_tele
        return self._sync.dataset.tele.mVehicles[self._sync.sync_tele_index(index)]

    @property
    def rf2Ext(self):
        """rF2 extended data"""
        return self._sync.dataset.ext

    @property
    def rf2Ffb(self):
        """rF2 force feedback data"""
        return self._sync.dataset.ffb

    @property
    def playerIndex(self) -> int:
        """rF2 local player's scoring index"""
        return self._sync.player_scor_index

    def isPlayer(self, idx: int) -> bool:
        """Check whether index is player"""
        if self._sync.override_player_index:
            return self._sync.player_scor_index == idx
        return self._sync.dataset.scor.mVehicles[idx].mIsPlayer

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
