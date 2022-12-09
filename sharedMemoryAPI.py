"""
Inherit Python mapping of The Iron Wolf's rF2 Shared Memory Tools
and add access functions to it.
"""
# pylint: disable=invalid-name
import time
import threading
import copy
import psutil

try:
    from . import rF2data
except ImportError:  # standalone, not package
    import rF2data


class SimInfoAPI(rF2data.SimInfo):
    """
    API for rF2 shared memory
    """
    __HELP = "\nShared Memory is installed by Crew Chief or you can install it yourself.\n" \
        "Please update rFactor2SharedMemoryMapPlugin64.dll, see\n" \
        "https://forum.studio-397.com/index.php?threads/rf2-shared-memory-tools-for-developers.54282/"

    sharedMemoryVerified = False
    minimumSupportedVersionParts = ['3', '6', '0', '0']
    rf2_pid = None          # Once we've found rF2 running
    rf2_pid_counter = 0     # Counter to check if running
    rf2_running = False

    def __init__(self, input_pid=""):
        rF2data.SimInfo.__init__(self, input_pid)
        self.versionCheckMsg = self.versionCheck()
        self.__find_rf2_pid()

        self.players_index = 99
        self.data_updating = False
        print("sharedmemory mapping started")

    def versionCheck(self):
        """
        Lifted from
        https://gitlab.com/mr_belowski/CrewChiefV4/blob/master/CrewChiefV4/RF2/RF2GameStateMapper.cs
        and translated.
        """
        self.sharedMemoryVerified = False    # Verify every time it is called.

        versionStr = Cbytestring2Python(self.Rf2Ext.mVersion)
        msg = ''

        if versionStr == '':
            msg = "\nrFactor 2 Shared Memory not present." + self.__HELP
            return msg

        versionParts = versionStr.split('.')
        if len(versionParts) != 4:
            msg = "Corrupt or leaked rFactor 2 Shared Memory.  Version string: " \
                + versionStr + self.__HELP
            return msg

        smVer = 0
        minVer = 0
        partFactor = 1
        for i in range(3, -1, -1):
            versionPart = 0
            try:
                versionPart = int(versionParts[i])
            except BaseException:
                msg = "Corrupt or leaked rFactor 2 Shared Memory version.  Version string: " \
                    + versionStr + self.__HELP
                return msg

            smVer += (versionPart * partFactor)
            minVer += (int(self.minimumSupportedVersionParts[i]) * partFactor)
            partFactor *= 100

        if smVer < minVer:
            minVerStr = ".".join(self.minimumSupportedVersionParts)
            msg = "Unsupported rFactor 2 Shared Memory version: " \
                + versionStr \
                + "  Minimum supported version is: " \
                + minVerStr + self.__HELP
        else:
            msg = "\nrFactor 2 Shared Memory\nversion: " + versionStr + " 64bit."
            if self.Rf2Ext.mDirectMemoryAccessEnabled:
                if self.Rf2Ext.mSCRPluginEnabled:
                    msg += "  Stock Car Rules plugin enabled. (DFT:%d" % \
                        self.Rf2Ext.mSCRPluginDoubleFileType
                else:
                    msg += "  DMA enabled."
            if self.Rf2Ext.is64bit == 0:
                msg += "\nOnly 64bit version of rFactor 2 is supported."
            else:
                self.sharedMemoryVerified = True

        return msg

    ###########################################################
    def __find_rf2_pid(self):
        """ Find the process ID for rfactor2.exe.  Takes a while """
        for pid in psutil.pids():
            try:
                p = psutil.Process(pid)
            except psutil.NoSuchProcess:
                continue
            if p.name().lower().startswith('rfactor2.exe'):
                self.rf2_pid = pid
                break

    def __playersDriverNum(self):
        """ Find the player's driver number """
        index_list = copy.deepcopy(self.Rf2Scor.mVehicles)
        for _player in range(127):
            if index_list[_player].mIsPlayer == 1:
                break
        return _player

    ###########################################################
    # Sync data for local player

    def __playerVerified(self, input_data):
        """ Check player index number on one same data piece """
        found = False  # return false if failed to find player index
        for _player in range(127):  # max 128 players supported by API
            if input_data.mVehicles[_player].mIsPlayer == 1:  # use 1 to avoid reading incorrect value
                self.players_index = _player
                found = True
                break
        return found

    @staticmethod
    def dataVerified(input_data):
        """ Verify data """
        return input_data.mVersionUpdateEnd == input_data.mVersionUpdateBegin

    def __infoUpdate(self):
        """ Update synced player data """
        players_mid = 0          # player mID
        last_version_update = 0  # store last data version update
        re_version_update = 0    # store restarted data version update
        mmap_restarted = True    # whether has restarted memory mapping
        check_counter = 0        # counter for data version update check
        restore_counter = 0      # counter for restoring mmap data to default

        while self.data_updating:
            data_scor = copy.deepcopy(self.Rf2Scor)  # use deepcopy to avoid data interruption
            data_tele = copy.deepcopy(self.Rf2Tele)
            self.LastExt = copy.deepcopy(self.Rf2Ext)
            self.LastFfb = copy.deepcopy(self.Rf2Ffb)

            # Only update if data verified and player index found
            if self.dataVerified(data_scor) and self.__playerVerified(data_scor):
                self.LastScor = copy.deepcopy(data_scor)  # use deepcopy to update scoring data
                players_mid = self.LastScor.mVehicles[self.players_index].mID  # update player mID

                # Only update if data verified and player mID matches
                if self.dataVerified(data_tele) and data_tele.mVehicles[self.players_index].mID == players_mid:
                    self.LastTele = copy.deepcopy(data_tele)  # use deepcopy to update synced telemetry data

            # Start checking data version update status
            check_counter += 1

            if check_counter > 70:  # active after around 1 seconds
                if not mmap_restarted and last_version_update > 0 and last_version_update == self.LastScor.mVersionUpdateEnd:
                    self.reset_mmap()
                    mmap_restarted = True
                    re_version_update = self.LastScor.mVersionUpdateEnd
                    print(f"sharedmemory mapping restarted - version:{last_version_update}")
                last_version_update = self.LastScor.mVersionUpdateEnd
                check_counter = 0  # reset counter

            if mmap_restarted:
                if re_version_update != self.LastScor.mVersionUpdateEnd:
                    mmap_restarted = False
                    restore_counter = 0  # reset counter
                elif restore_counter < 71:
                    restore_counter += 1

            if restore_counter == 70:  # active after around 1 seconds
                self.set_default_mmap()
                print("sharedmemory mapping data reset to default")

            #print(f"c1:{check_counter:03.0f} c2:{restore_counter:03.0f} now:{self.LastScor.mVersionUpdateEnd:07.0f} last:{last_version_update:07.0f} re:{re_version_update:07.0f} {mmap_restarted}", end="\r")

            time.sleep(0.01)
        else:
            print("sharedmemory synced player data updating thread stopped")

    def startUpdating(self):
        """ Start data updating thread """
        self.data_updating = True
        index_thread = threading.Thread(target=self.__infoUpdate)
        index_thread.setDaemon(True)
        index_thread.start()
        print("sharedmemory synced player data updating thread started")

    def stopUpdating(self):
        """ Stop data updating thread """
        self.data_updating = False
        time.sleep(0.2)

    def syncedVehicleTelemetry(self):
        """ Get the variable for the player's vehicle """
        return self.LastTele.mVehicles[self.players_index]

    def syncedVehicleScoring(self):
        """ Get the variable for the player's vehicle """
        return self.LastScor.mVehicles[self.players_index]

    ###########################################################
    # Access functions

    def isRF2running(self, find_counter=200, found_counter=5):
        """
        Both "rFactor 2 Launcher" and "rf2" processes are found
        whether it's the launcher or the game that's running BUT
        rfactor2.exe is only present if the game is running.
        Beacuse this takes some time, control how often it's checked using:
        find_counter: how often to check if rF2 is not running
        found_counter: how often to check once rF2 is running
        """
        if self.rf2_pid_counter == 0:  # first time
            self.rf2_pid_counter = find_counter
        if self.isSharedMemoryAvailable():
            # No need to check if Shared Memory is OK!
            self.rf2_running = True
        elif self.rf2_pid:
            if self.rf2_pid_counter >= found_counter:
                self.rf2_pid_counter = 0
                try:
                    p = psutil.Process(self.rf2_pid)
                except psutil.NoSuchProcess:
                    self.rf2_pid = None
                    return False
                if p.name().lower().startswith('rfactor2.exe'):
                    self.rf2_running = True
        else:
            if self.rf2_pid_counter >= find_counter:
                self.rf2_pid_counter = 0
                self.__find_rf2_pid()
                self.rf2_running = False
        self.rf2_pid_counter += 1
        return self.rf2_running

    def isSharedMemoryAvailable(self):
        """
        True: The correct memory map is loaded
        """
        self.versionCheck()
        return self.sharedMemoryVerified

    def isTrackLoaded(self):
        """
        True: rF2 is running and the track is loaded
        """
        started = self.Rf2Ext.mSessionStarted
        return started != 0

    def isOnTrack(self):
        """
        True: rF2 is running and the player is on track
        """
        realtime = self.Rf2Ext.mInRealtimeFC
        return realtime != 0

    def isAiDriving(self):
        """
        True: rF2 is running and the player is on track
        """
        return self.Rf2Scor.mVehicles[self.__playersDriverNum()].mControl == 1
        # who's in control: -1=nobody (shouldn't get this), 0=local player,
        # 1=local AI, 2=remote, 3=replay (shouldn't get this)

        # didn't work self.Rf2Ext.mPhysics.mAIControl

    def driverName(self):
        """ Get the player's name """
        return Cbytestring2Python(
            self.Rf2Scor.mVehicles[self.__playersDriverNum()].mDriverName)

    def playersVehicleTelemetry(self):
        """ Get the variable for the player's vehicle """
        return self.Rf2Tele.mVehicles[self.__playersDriverNum()]

    def playersVehicleScoring(self):
        """ Get the variable for the player's vehicle """
        return self.Rf2Scor.mVehicles[self.__playersDriverNum()]

    def vehicleName(self):
        """ Get the vehicle's name """
        return Cbytestring2Python(
            self.Rf2Scor.mVehicles[self.__playersDriverNum()].mVehicleName)


def Cbytestring2Python(bytestring):
    """
    C string to Python string
    """
    try:
        return bytes(bytestring).partition(b'\0')[0].decode('utf_8').rstrip()
    except BaseException:
        pass
    try:    # Codepage 1252 includes Scandinavian characters
        return bytes(bytestring).partition(b'\0')[0].decode('cp1252').rstrip()
    except BaseException:
        pass
    try:    # OK, struggling, just ignore errors
        return bytes(bytestring).partition(b'\0')[
            0].decode('utf_8', 'ignore').rstrip()
    except Exception as e:
        print('Trouble decoding a string')
        print(e)


def test_main():    # pylint: disable=too-many-statements
    """ Example usage """
    info = SimInfoAPI()
    if info.isRF2running():
        print('rfactor2.exe is running')
        print(info.versionCheckMsg, '\n')
        if info.isSharedMemoryAvailable():
            print('Memory map is loaded')
            version = Cbytestring2Python(info.Rf2Ext.mVersion)
            # 2019/04/23:  3.5.0.9
            print('Shared memory version:', version)

            if info.isTrackLoaded():
                trackName = Cbytestring2Python(
                    info.Rf2Scor.mScoringInfo.mTrackName)
                print('%s is loaded' % trackName)
                if info.isOnTrack():
                    driver = Cbytestring2Python(
                        info.playersVehicleScoring().mDriverName)
                    print('Driver "%s" is on track' % driver)
                    clutch = info.playersVehicleTelemetry().mUnfilteredClutch
                    # 1.0 clutch down, 0 clutch up

                    driver = Cbytestring2Python(
                        info.playersVehicleScoring().mDriverName)
                    gear = info.playersVehicleTelemetry().mGear
                    print('Driver: "%s", Gear: %d, Clutch position: %d' %
                          (driver, gear, clutch))

                    # Test that memory map can be poked
                    info.playersVehicleTelemetry().mGear = 1
                    gear = info.playersVehicleTelemetry().mGear  # -1 to 6
                    assert info.playersVehicleTelemetry().mGear == 1
                    info.playersVehicleTelemetry().mGear = 2
                    assert info.playersVehicleTelemetry().mGear == 2
                    gear = info.playersVehicleTelemetry().mGear  # -1 to 6
                    info.playersVehicleTelemetry().mGear = 1
                    assert info.playersVehicleTelemetry().mGear == 1

                    _vehicleName = Cbytestring2Python(
                        info.playersVehicleScoring().mVehicleName)
                    _vehicleClass = Cbytestring2Python(
                        info.playersVehicleScoring().mVehicleClass)

                    print('vehicleName:', _vehicleName)
                    print('vehicleClass:', _vehicleClass)

                    started = info.Rf2Ext.mSessionStarted
                    print('SessionStarted:', started)
                    realtime = info.Rf2Ext.mInRealtimeFC
                    print('InRealtimeFC:', realtime)
                    if info.isAiDriving():
                        print('AI is driving the car')
                    else:
                        print('Car not under AI control')
                else:
                    print('Driver is not on track')
            else:
                print('Track is not loaded')

            print('\nBreaking the version string...')
            info.Rf2Ext.mVersion[0] = 32

            assert not info.isSharedMemoryAvailable()
            print('\n' + info.versionCheck())
            info.Rf2Ext.mVersion[0] = 51  # restore it

            info.Rf2Ext.mVersion[0] = 50
            assert not info.isSharedMemoryAvailable()
            print('\n' + info.versionCheck())
            info.Rf2Ext.mVersion[0] = 51  # restore it

            info.Rf2Ext.mVersion[2] = 53
            assert not info.isSharedMemoryAvailable()
            print('\n' + info.versionCheck())
            info.Rf2Ext.mVersion[2] = 54  # restore it

            print('\nBreaking 64 bit info...')
            info.Rf2Ext.is64bit = 0
            assert not info.isSharedMemoryAvailable()
            print(info.versionCheck())
            info.Rf2Ext.is64bit = 1

            print('\nPit Menu')
            while True:
                if info.Rf2PitMenu.changed:
                    print(Cbytestring2Python(
                        info.Rf2PitMenu.mCategoryName))
                    info.Rf2PitMenu.changed = 0

            print('\nOK')
        else:
            print('Incorrect shared memory')
    else:
        print('rFactor 2 not running')

    s = bytearray(range(0xA1, 0xff))
    print(Cbytestring2Python(s))
    return 'OK'


if __name__ == '__main__':
    test_main()
