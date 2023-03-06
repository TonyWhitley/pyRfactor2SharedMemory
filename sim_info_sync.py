"""
sharedMemoryAPI with player-synced methods

Inherit Python mapping of The Iron Wolf's rF2 Shared Memory Tools
and add access functions to it.
"""
# pylint: disable=invalid-name
import ctypes
import mmap
import time
import threading
import copy
import platform

try:
    from . import rF2data
except ImportError:  # standalone, not package
    import rF2data

from .sharedMemoryAPI import Cbytestring2Python

MAX_VEHICLES = 128  # max 128 players supported by API


class SimInfoSync():
    """
    API for rF2 shared memory

    Player-Synced data.
    """

    def __init__(self, input_pid=""):
        self.players_index = 99
        self.players_mid = 99
        self.data_updating = False
        self.stopped = True
        self._input_pid = input_pid

        self._rf2_tele = None  # map shared memory
        self._rf2_scor = None
        self._rf2_ext = None
        self._rf2_ffb = None

        self.LastTele = None  # synced copy of raw data
        self.LastScor = None
        self.LastExt = None
        self.LastFfb = None

        self.start_mmap()
        self.copy_mmap()
        print("sharedmemory mapping started")

    def start_mmap(self):
        """ Start memory mapping """
        if platform.system() == "Windows":
            self._rf2_tele = mmap.mmap(-1, ctypes.sizeof(rF2data.rF2Telemetry),
                                       f"$rFactor2SMMP_Telemetry${self._input_pid}")
            self._rf2_scor = mmap.mmap(-1, ctypes.sizeof(rF2data.rF2Scoring),
                                       f"$rFactor2SMMP_Scoring${self._input_pid}")
            self._rf2_ext = mmap.mmap(-1, ctypes.sizeof(rF2data.rF2Extended),
                                      f"$rFactor2SMMP_Extended${self._input_pid}")
            self._rf2_ffb = mmap.mmap(-1, ctypes.sizeof(rF2data.rF2ForceFeedback),
                                      "$rFactor2SMMP_ForceFeedback$")
        else:
            tele_file = open("/dev/shm/$rFactor2SMMP_Telemetry$", "r+")
            self._rf2_tele = mmap.mmap(tele_file.fileno(), ctypes.sizeof(rF2data.rF2Telemetry))
            scor_file = open("/dev/shm/$rFactor2SMMP_Scoring$", "r+")
            self._rf2_scor = mmap.mmap(scor_file.fileno(), ctypes.sizeof(rF2data.rF2Scoring))
            ext_file = open("/dev/shm/$rFactor2SMMP_Extended$", "r+")
            self._rf2_ext = mmap.mmap(ext_file.fileno(), ctypes.sizeof(rF2data.rF2Extended))
            ffb_file = open("/dev/shm/$rFactor2SMMP_ForceFeedback$", "r+")
            self._rf2_ffb = mmap.mmap(ffb_file.fileno(), ctypes.sizeof(rF2data.rF2ForceFeedback))

    def copy_mmap(self):
        """ Copy memory mapping data """
        self.LastTele = rF2data.rF2Telemetry.from_buffer_copy(self._rf2_tele)
        self.LastScor = rF2data.rF2Scoring.from_buffer_copy(self._rf2_scor)
        self.LastExt = rF2data.rF2Extended.from_buffer_copy(self._rf2_ext)
        self.LastFfb = rF2data.rF2ForceFeedback.from_buffer_copy(self._rf2_ffb)

    def reset_mmap(self):
        """ Reset memory mapping """
        self.close()  # close mmap first
        self.start_mmap()

    def close(self):
        """ Close memory mapping """
        # This didn't help with the errors
        try:
            # Close shared memory mapping
            self._rf2_tele.close()
            self._rf2_scor.close()
            self._rf2_ext.close()
            self._rf2_ffb.close()
            print("sharedmemory mapping closed")
        except BufferError:  # "cannot close exported pointers exist"
            print("BufferError")
            pass

    ###########################################################
    # Sync data for local player

    def __playerVerified(self, data):
        """ Check player index number on one same data piece """
        for index in range(MAX_VEHICLES):
            if data.mVehicles[index].mIsPlayer:
                self.players_index = index
                return True
        return False  # return false if failed to find player index

    @staticmethod
    def dataVerified(data):
        """ Verify data """
        return data.mVersionUpdateEnd == data.mVersionUpdateBegin

    def __infoUpdate(self):
        """ Update synced player data """
        last_version_update = 0  # store last data version update
        re_version_update = 0    # store restarted data version update
        data_freezed = True      # whether data is freezed
        check_counter = 0        # counter for data version update check

        while self.data_updating:
            data_scor = rF2data.rF2Scoring.from_buffer_copy(self._rf2_scor)  # use deepcopy to avoid data interruption
            data_tele = rF2data.rF2Telemetry.from_buffer_copy(self._rf2_tele)
            self.LastExt = rF2data.rF2Extended.from_buffer_copy(self._rf2_ext)
            self.LastFfb = rF2data.rF2ForceFeedback.from_buffer_copy(self._rf2_ffb)

            # Only update if data verified and player index found
            if not data_freezed and self.__playerVerified(data_scor):
                self.LastScor = copy.deepcopy(data_scor)  # synced scoring
                self.players_mid = self.LastScor.mVehicles[self.players_index].mID  # update player mID

                # Only update if data verified and player mID matches
                if data_tele.mVehicles[self.players_index].mID == self.players_mid:
                    self.LastTele = copy.deepcopy(data_tele)  # synced telemetry

            # Start checking data version update status
            check_counter += 1

            if check_counter > 200:  # active after around 1 seconds
                if (not data_freezed and last_version_update > 0
                    and last_version_update == data_scor.mVersionUpdateEnd):
                    self.reset_mmap()
                    data_freezed = True
                    re_version_update = data_scor.mVersionUpdateEnd
                    self.LastTele.mVehicles[self.players_index].mIgnitionStarter = 0
                    print(f"sharedmemory mapping restarted - version:{last_version_update}")
                last_version_update = data_scor.mVersionUpdateEnd
                check_counter = 0  # reset counter

            if data_freezed and re_version_update != data_scor.mVersionUpdateEnd:
                data_freezed = False

            time.sleep(0.01)

        self.stopped = True
        print("sharedmemory synced player data updating thread stopped")

    def startUpdating(self):
        """ Start data updating thread """
        self.data_updating = True
        self.stopped = False
        index_thread = threading.Thread(target=self.__infoUpdate)
        index_thread.daemon=True
        index_thread.start()
        print("sharedmemory synced player data updating thread started")

    def stopUpdating(self):
        """ Stop data updating thread """
        self.data_updating = False
        while not self.stopped:  # wait until stopped
            time.sleep(0.01)

    def syncedVehicleTelemetry(self):
        """ Get the variable for the player's vehicle """
        return self.LastTele.mVehicles[self.players_index]

    def syncedVehicleScoring(self):
        """ Get the variable for the player's vehicle """
        return self.LastScor.mVehicles[self.players_index]

    ###########################################################

    def __del__(self):
        self.close()

if __name__ == '__main__':
    # Example usage
    info = SimInfoSync()
    info.startUpdating()  # start Shared Memory updating thread
    version = info.LastExt.mVersion
    v = bytes(version).partition(b'\0')[0].decode().rstrip()
    clutch = info.LastTele.mVehicles[0].mUnfilteredClutch # 1.0 clutch down, 0 clutch up
    gear   = info.LastTele.mVehicles[0].mGear  # -1 to 6
    print(f"Map version: {v}\n"
          f"Gear: {gear}, Clutch position: {clutch}")

    info.stopUpdating()  # stop sharedmemory synced player data updating thread