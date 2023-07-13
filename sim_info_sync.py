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
    """Create mmap for accessing rF2 shared memory

    mmap_name: mmap filename, ex. $rFactor2SMMP_Scoring$
    rf2_data: rf2 data class defined in rF2data.py, ex. rF2data.rF2Scoring
    rf2_pid: rf2 Process ID for server
    logger: logger name
    """

    def __init__(self, mmap_name, rf2_data, logger=__name__):
        self._logger = logging.getLogger(logger)
        self._mmap_name = mmap_name
        self._rf2_data = rf2_data
        self._mmap_inst = None
        self._mmap_data = None
        self._access_mode = 0
        self._direct_access_active = False

    def create(self, access_mode=0, rf2_pid=""):
        """Create mmap instance"""
        self._access_mode = access_mode
        self._mmap_inst = self.platform_mmap(
            name=self._mmap_name,
            size=ctypes.sizeof(self._rf2_data),
            pid=rf2_pid
        )
        mode_text = "Direct" if access_mode else "Copy"
        self._logger.info(
            "sharedmemory - %s > ACTIVE: %s Access",
            self._mmap_name.strip("$"), mode_text
        )

    def close(self):
        """Close memory mapping

        Create a final accessible mmap data copy before closing mmap instance.
        """
        self.copy_access()
        self._direct_access_active = False
        try:
            self._mmap_inst.close()
            self._logger.info("sharedmemory - %s > CLOSE", self._mmap_name.strip("$"))
        except BufferError:
            self._logger.error("sharedmemory - failed to close mmap")

    @staticmethod
    def version_check(data):
        """Data version check"""
        return data.mVersionUpdateEnd == data.mVersionUpdateBegin

    def direct_access(self):
        """Direct access memory map

        Direct accessing mmap data instance.
        May result data desync or interruption.
        """
        if self._direct_access_active:
            return None
        self._mmap_data = self._rf2_data.from_buffer(self._mmap_inst)
        self._direct_access_active = True

    def copy_access(self):
        """Copy access memory map

        Accessing mmap data by copying mmap instance
        and using version check to avoid data desync or interruption.
        """
        data_temp = self._rf2_data.from_buffer_copy(self._mmap_inst)
        if self.version_check(data_temp):
            self._mmap_data = data_temp
        elif not self._mmap_data:
            self._mmap_data = data_temp

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

    def update(self):
        """Update rF2 mmap data"""
        if self._access_mode:
            self.direct_access()
        else:
            self.copy_access()

    @property
    def data(self):
        """Access rF2 mmap data"""
        return self._mmap_data


class SimInfoSync():
    """
    API for rF2 shared memory

    Player-Synced data.
    Access mode: 0 = copy access, 1 = direct access
    """

    def __init__(self, logger=__name__):
        self._stopped = True
        self._updating = False
        self._restarting = False
        self._paused = True
        self._player_scor_index = INVALID_INDEX
        self._player_tele_index = INVALID_INDEX
        self._player_scor_mid = 0
        self._rf2_pid = ""
        self._access_mode = 0
        self._logger = logging.getLogger(logger)
        self.init_mmap(logger)

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
        scor_mid = self._info_scor.data.mVehicles[index_scor].mID
        for index in range(MAX_VEHICLES):
            if self._info_tele.data.mVehicles[index].mID == scor_mid:
                return index
        return INVALID_INDEX

    def __update(self):
        """Update synced player data"""
        last_version_update = 0  # store last data version update
        data_freezed = True      # whether data is freezed
        check_timer_start = 0
        reset_counter = 0
        update_delay = 0.5  # longer delay while inactive

        while self._updating:
            self.update_mmap()
            # Update player data & index
            if not data_freezed:
                # Get player data
                data_synced = self.__sync_local_player_data(
                    self._info_scor.data, self._info_tele.data)
                # Pause if local player index no longer exists, 5 tries
                if not data_synced and reset_counter < 6:
                    reset_counter += 1
                elif data_synced:
                    reset_counter = 0
                    self._paused = False
                # Activate pause
                if reset_counter == 5:
                    self._paused = True
                    self._logger.info("sharedmemory - player data paused")

            # Start checking data version update status
            if time.time() - check_timer_start > 5:
                if (not data_freezed
                    and last_version_update == self._info_scor.data.mVersionUpdateEnd):
                    update_delay = 0.5
                    data_freezed = True
                    self._paused = True
                    self._logger.info(
                        "sharedmemory - data paused, version %s",
                        last_version_update
                    )
                last_version_update = self._info_scor.data.mVersionUpdateEnd
                check_timer_start = time.time()  # reset timer

            if (data_freezed
                and last_version_update != self._info_scor.data.mVersionUpdateEnd):
                update_delay = 0.01
                data_freezed = False
                self._paused = False
                self._logger.info(
                    "sharedmemory - data unpaused, version %s",
                    self._info_scor.data.mVersionUpdateEnd
                )

            time.sleep(update_delay)

        self._stopped = True
        self._paused = False
        self._logger.info("sharedmemory - updating thread stopped")

    def start(self):
        """Start data updating thread

        Update & sync mmap data copy in separate thread.
        """
        if not self._stopped:
            return None

        self.create_mmap()
        self.update_mmap()
        self.copy_mmap_player()
        self._updating = True
        self._stopped = False
        self._thread = threading.Thread(target=self.__update, daemon=True)
        self._thread.start()
        self._logger.info("sharedmemory - updating thread started")

    def stop(self):
        """Stop data updating thread"""
        self._updating = False
        self._thread.join()
        self.close_mmap()

    def restart(self):
        """Restart data updating thread"""
        if self._restarting:
            return None
        self._restarting = True
        self.stop()
        self.start()
        self._restarting = False

    def init_mmap(self, logger):
        """Initialize mmap info"""
        self._info_scor = rF2MMap(
            "$rFactor2SMMP_Scoring$", rF2data.rF2Scoring, logger)
        self._info_tele = rF2MMap(
            "$rFactor2SMMP_Telemetry$", rF2data.rF2Telemetry, logger)
        self._info_ext = rF2MMap(
            "$rFactor2SMMP_Extended$", rF2data.rF2Extended, logger)
        self._info_ffb = rF2MMap(
            "$rFactor2SMMP_ForceFeedback$", rF2data.rF2ForceFeedback, logger)

    def create_mmap(self):
        """Create mmap instance"""
        self._info_scor.create(self._access_mode, self._rf2_pid)
        self._info_tele.create(self._access_mode, self._rf2_pid)
        self._info_ext.create(self._access_mode, self._rf2_pid)
        self._info_ffb.create(self._access_mode, self._rf2_pid)

    def close_mmap(self):
        """Close mmap instance"""
        self._info_scor.close()
        self._info_tele.close()
        self._info_ext.close()
        self._info_ffb.close()

    def update_mmap(self):
        """Update mmap data"""
        self._info_scor.update()
        self._info_tele.update()
        self._info_ext.update()
        self._info_ffb.update()

    def copy_mmap_player(self):
        """Copy memory mapping player data

        Maintain a separate copy of synchronized local player's data
        which avoids data interruption or desync in case of player index changes.
        """
        self._player_scor = copy.deepcopy(self._info_scor.data.mVehicles[INVALID_INDEX])
        self._player_tele = copy.deepcopy(self._info_tele.data.mVehicles[INVALID_INDEX])

    def setPID(self, pid=""):
        """Set rf2 PID"""
        self._rf2_pid = pid

    def setMode(self, mode=0):
        """Set rf2 mmap access mode"""
        self._access_mode = mode

    @property
    def rf2Scor(self):
        """rF2 vehicle scoring data"""
        return self._info_scor.data

    @property
    def rf2Tele(self):
        """rF2 vehicle telemetry data"""
        return self._info_tele.data

    @property
    def rf2Ext(self):
        """rF2 extended data"""
        return self._info_ext.data

    @property
    def rf2Ffb(self):
        """rF2 force feedback data"""
        return self._info_ffb.data

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
    info = SimInfoSync(logger=__name__)
    info.setMode(0) # optional, can be omitted
    info.setPID("") # optional, can be omitted
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
