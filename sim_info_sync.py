"""
sharedMemoryAPI with player-synced methods

Inherit Python mapping of The Iron Wolf's rF2 Shared Memory Tools
and add access functions to it.
"""
import ctypes
import mmap
import time
import threading
import copy
import platform
import logging

try:
    from . import rF2data
except ImportError:  # standalone, not package
    import rF2data

PLATFORM = platform.system()
MAX_VEHICLES = rF2data.rFactor2Constants.MAX_MAPPED_VEHICLES
INVALID_INDEX = -1


class rF2MMap:
    """Create mmap for accessing rF2 shared memory"""

    def __init__(self, logger=__name__):
        self._logger = logging.getLogger(logger)
        self._rf2_pid = ""
        self._rf2_scor = None
        self._rf2_tele = None
        self._rf2_ext = None
        self._rf2_ffb = None
        self._data_scor = None
        self._data_tele = None
        self._data_ext = None
        self._data_ffb = None
        self._player_scor = None
        self._player_tele = None

    def start_mmap(self):
        """Start memory mapping"""
        self._rf2_scor = self.platform_mmap(
            name="$rFactor2SMMP_Scoring$",
            size=ctypes.sizeof(rF2data.rF2Scoring),
            pid=self._rf2_pid
        )
        self._rf2_tele = self.platform_mmap(
            name="$rFactor2SMMP_Telemetry$",
            size=ctypes.sizeof(rF2data.rF2Telemetry),
            pid=self._rf2_pid
        )
        self._rf2_ext = self.platform_mmap(
            name="$rFactor2SMMP_Extended$",
            size=ctypes.sizeof(rF2data.rF2Extended),
            pid=self._rf2_pid
        )
        self._rf2_ffb = self.platform_mmap(
            name="$rFactor2SMMP_ForceFeedback$",
            size=ctypes.sizeof(rF2data.rF2ForceFeedback),
        )
        self._logger.info("sharedmemory mapping started")

    def direct_access_mmap(self):
        """Direct access memory mapping data

        Direct accessing mmap data instance by using from_buffer.
        This may result unexpected data interruption or desync issue.
        """
        self._data_scor = rF2data.rF2Scoring.from_buffer(self._rf2_scor)
        self._data_tele = rF2data.rF2Telemetry.from_buffer(self._rf2_tele)
        self._data_ext = rF2data.rF2Extended.from_buffer(self._rf2_ext)
        self._data_ffb = rF2data.rF2ForceFeedback.from_buffer(self._rf2_ffb)

    def copy_mmap(self):
        """Copy memory mapping data

        Accessing shared memory data by using from_buffer_copy on mmap data instance,
        which ensures that orginal constantly updated mmap instance
        would not unexpectedly interrupt data verification and synchronizing.
        """
        self._data_scor = rF2data.rF2Scoring.from_buffer_copy(self._rf2_scor)
        self._data_tele = rF2data.rF2Telemetry.from_buffer_copy(self._rf2_tele)
        self._data_ext = rF2data.rF2Extended.from_buffer_copy(self._rf2_ext)
        self._data_ffb = rF2data.rF2ForceFeedback.from_buffer_copy(self._rf2_ffb)

    def copy_mmap_player(self):
        """Copy memory mapping player data

        Maintain a separate copy of synchronized local player's data
        which avoids data interruption or desync in case of player index changes.
        """
        self._player_scor = copy.deepcopy(self._data_scor.mVehicles[INVALID_INDEX])
        self._player_tele = copy.deepcopy(self._data_tele.mVehicles[INVALID_INDEX])

    def close_mmap(self):
        """Close memory mapping"""
        try:
            self._rf2_tele.close()
            self._rf2_scor.close()
            self._rf2_ext.close()
            self._rf2_ffb.close()
            self._logger.info("sharedmemory mapping closed")
        except BufferError:  # "cannot close exported pointers exist"
            self._logger.error("failed to close mmap")

    def platform_mmap(self, name, size, pid=""):
        """Platform memory mapping"""
        if PLATFORM == "Windows":
            return self.windows_mmap(name, size, pid)
        return self.linux_mmap(name, size)

    @staticmethod
    def windows_mmap(name, size, pid):
        """Windows memory mapping"""
        return mmap.mmap(-1, size, f"{name}{pid}")

    @staticmethod
    def linux_mmap(name, size):
        """Linux memory mapping"""
        file = open("/dev/shm/" + name, "a+")
        if file.tell() == 0:
            file.write("\0" * size)
            file.flush()
        return mmap.mmap(file.fileno(), size)

    @property
    def rf2PID(self):
        """rF2 process id"""
        return self._rf2_pid

    @rf2PID.setter
    def rf2PID(self, pid):
        """Set rF2 process id"""
        self._rf2_pid = pid


class SimInfoSync(rF2MMap):
    """
    API for rF2 shared memory

    Player-Synced data.
    """

    def __init__(self, logger=__name__):
        super().__init__(logger)
        self._stopped = True
        self._updating = False
        self._restarting = False
        self._paused = True
        self._player_scor_index = INVALID_INDEX
        self._player_tele_index = INVALID_INDEX
        self._player_scor_mid = 0

    @staticmethod
    def __find_local_scor_index(data_scor):
        """Find local player scoring index"""
        for idx_scor in range(MAX_VEHICLES):
            if data_scor.mVehicles[idx_scor].mIsPlayer:
                return idx_scor
        return INVALID_INDEX

    @staticmethod
    def __find_local_tele_index(data_tele, mid_scor):
        """Find local player telemetry index

        Telemetry index can be different from scoring index.
        Use mID matching to find telemetry index.
        """
        for idx_tele in range(MAX_VEHICLES):
            if data_tele.mVehicles[idx_tele].mID == mid_scor:
                return idx_tele
        return INVALID_INDEX

    def __sync_local_player_data(self, data_scor, data_tele):
        """Sync local player data

        1. Find scoring index, break if not found.
        2. Update scoring index, mID, copy scoring data.
        3. Find telemetry index, break if not found.
        4. Update telemetry index, copy telemetry data.
        """
        idx_scor = self.__find_local_scor_index(data_scor)
        if idx_scor == INVALID_INDEX:
            return False
        self._player_scor_index = idx_scor
        self._player_scor_mid = data_scor.mVehicles[idx_scor].mID
        self._player_scor = copy.deepcopy(data_scor.mVehicles[idx_scor])

        idx_tele = self.__find_local_tele_index(data_tele, self._player_scor_mid)
        if idx_tele == INVALID_INDEX:
            return True  # found 1 index
        self._player_tele_index = idx_tele
        self._player_tele = copy.deepcopy(data_tele.mVehicles[idx_tele])
        return True  # found 2 index

    def find_player_index_tele(self, index_scor):
        """Find player index using mID"""
        scor_mid = self._data_scor.mVehicles[index_scor].mID
        for index in range(MAX_VEHICLES):
            if self._data_tele.mVehicles[index].mID == scor_mid:
                return index
        return INVALID_INDEX

    @staticmethod
    def ver_check(data):
        """Update version check"""
        return data.mVersionUpdateEnd == data.mVersionUpdateBegin

    def __update(self):
        """Update synced player data"""
        last_version_update = 0  # store last data version update
        data_freezed = True      # whether data is freezed
        check_timer_start = 0
        reset_counter = 0
        update_delay = 0.5  # longer delay while inactive

        while self._updating:
            data_scor = rF2data.rF2Scoring.from_buffer_copy(self._rf2_scor)
            data_tele = rF2data.rF2Telemetry.from_buffer_copy(self._rf2_tele)
            self._data_ext = rF2data.rF2Extended.from_buffer_copy(self._rf2_ext)
            self._data_ffb = rF2data.rF2ForceFeedback.from_buffer_copy(self._rf2_ffb)
            # Update player data & index
            if (not data_freezed
                and self.ver_check(data_scor)
                and self.ver_check(data_tele)):
                self._data_scor = data_scor
                self._data_tele = data_tele
                # Get player data
                data_synced = self.__sync_local_player_data(data_scor, data_tele)
                # Pause if local player index no longer exists, 5 tries
                if not data_synced and reset_counter < 6:
                    reset_counter += 1
                elif data_synced:
                    reset_counter = 0
                    self._paused = False
                # Activate pause
                if reset_counter == 5:
                    self._paused = True
                    self._logger.info("sharedmemory mapping player data paused")

            # Start checking data version update status
            if time.time() - check_timer_start > 5:
                if (not data_freezed
                    and last_version_update == data_scor.mVersionUpdateEnd):
                    update_delay = 0.5
                    data_freezed = True
                    self._paused = True
                    self._logger.info(
                        "sharedmemory mapping data paused, version %s",
                        last_version_update
                    )
                last_version_update = data_scor.mVersionUpdateEnd
                check_timer_start = time.time()  # reset timer

            if (data_freezed
                and last_version_update != data_scor.mVersionUpdateEnd):
                update_delay = 0.01
                data_freezed = False
                self._paused = False
                self._logger.info(
                    "sharedmemory mapping data unpaused, version %s",
                    data_scor.mVersionUpdateEnd
                )

            time.sleep(update_delay)

        self._stopped = True
        self._paused = False
        self._logger.info("sharedmemory data updating thread stopped")

    def start(self):
        """Start data updating thread

        Update & sync mmap data copy in separate thread.
        """
        if not self._stopped:
            return None
        self.start_mmap()
        self.copy_mmap()
        self.copy_mmap_player()
        self._updating = True
        self._stopped = False
        self._thread = threading.Thread(target=self.__update, daemon=True)
        self._thread.start()
        self._logger.info("sharedmemory data updating thread started")

    def stop(self):
        """Stop data updating thread"""
        self._updating = False
        self._thread.join()
        self.close_mmap()

    def restart(self):
        """Redtart data updating thread"""
        if self._restarting:
            return None
        self._restarting = True
        self.stop()
        self.start()
        self._restarting = False

    @property
    def rf2Scor(self):
        """rF2 vehicle scoring data"""
        return self._data_scor

    @property
    def rf2Tele(self):
        """rF2 vehicle telemetry data"""
        return self._data_tele

    @property
    def rf2Ext(self):
        """rF2 extended data"""
        return self._data_ext

    @property
    def rf2Ffb(self):
        """rF2 force feedback data"""
        return self._data_ffb

    @property
    def playerTele(self):
        """rF2 local player's vehicle telemetry data"""
        return self._player_tele

    @property
    def playerScor(self):
        """rF2 local player's vehicle scoring data"""
        return self._player_scor

    @property
    def playerTeleIndex(self):
        """rF2 local player's telemetry index"""
        return self._player_tele_index

    @property
    def playerScorIndex(self):
        """rF2 local player's scoring index"""
        return self._player_scor_index

    @property
    def paused(self):
        """Check whether data stopped updating"""
        return self._paused

    @staticmethod
    def cbytes2str(bytestring):
        """Convert bytes to string"""
        if type(bytestring) == bytes:
            return bytestring.decode(errors="replace").rstrip()
        return ""


if __name__ == "__main__":
    # Add logger
    logger = logging.getLogger(__name__)
    test_handler = logging.StreamHandler()
    logger.setLevel(logging.INFO)
    logger.addHandler(test_handler)

    # Example usage
    info = SimInfoSync(__name__)
    info.start()
    time.sleep(0.5)
    version = info.cbytes2str(info.rf2Ext.mVersion)
    clutch = info.rf2Tele.mVehicles[0].mUnfilteredClutch # 1.0 clutch down, 0 clutch up
    gear = info.rf2Tele.mVehicles[0].mGear  # -1 to 6
    print(f"API version: {version if version else 'unknown'}\n"
          f"Gear: {gear}\nClutch position: {clutch}")
    print("Test - API restart")
    info.restart()
    print("Test - API quit")
    info.stop()
