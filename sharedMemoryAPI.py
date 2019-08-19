"""
Inherit Python mapping of The Iron Wolf's rF2 Shared Memory Tools
and add access functions to it.
"""
# pylint: disable=bad-indentation
# pylint: disable=invalid-name

import psutil

try:
    from . import rF2data
except: # standalone, not package
    import rF2data

class SimInfoAPI(rF2data.SimInfo):
  """
  API for rF2 shared memory
  """
  def __init__(self):
    rF2data.SimInfo.__init__(self)
    self.player = 0
    self.minimumSupportedVersionParts = ['3', '6', '0', '0']
    self.versionCheckMsg = self.versionCheck()

  def isRF2running(self):
    """ 
    Both "rFactor 2 Launcher" and "rf2" processes are found
    whether it's the launcher or the game that's running BUT
    rfactor2.exe is only present if the game is running.
    """
    for pid in psutil.pids():
        try:
            p = psutil.Process(pid)
        except psutil.NoSuchProcess:
            continue
        if p.name().lower().startswith('rfactor2.exe'):
            return True

    return False

  def versionCheck(self):
    """
    Lifted from
    https://gitlab.com/mr_belowski/CrewChiefV4/blob/master/CrewChiefV4/RF2/RF2GameStateMapper.cs
    and translated.
    """
    versionStr = Cbytestring2Python(self.Rf2Ext.mVersion)
    msg = ''

    if versionStr == '':
        msg = "\nrFactor 2 Shared Memory not present.\n" \
            "Shared Memory is installed by Crew Chief or you can install it yourself, see\n" \
            "https://forum.studio-397.com/index.php?threads/rf2-shared-memory-tools-for-developers.54282/"
        return msg

    versionParts = versionStr.split('.')
    if len(versionParts) != 4:
        msg = "Corrupt or leaked rFactor 2 Shared Memory.  Version string: " + versionStr
        return msg

    smVer = 0
    minVer = 0
    partFactor = 1
    for i in range(3, 0, -1):
        versionPart = 0
        try:
          versionPart = int(versionParts[i])
        except: # pylint: disable=bare-except
            msg = "Corrupt or leaked rFactor 2 Shared Memory version.  Version string: " \
                + versionStr
            return msg

        smVer += (versionPart * partFactor)
        minVer += (int(self.minimumSupportedVersionParts[i]) * partFactor)
        partFactor *= 100

    if self.Rf2Ext.is64bit == 0:
        msg = "Only 64bit version of rFactor 2 is supported."
    elif smVer < minVer:
        minVerStr = ".".join(self.minimumSupportedVersionParts)
        msg = "Unsupported rFactor 2 Shared Memory version: " \
            + versionStr \
            + "  Minimum supported version is: " \
            + minVerStr \
            + "  Please update rFactor2SharedMemoryMapPlugin64.dll"
    else:
        msg = "\nrFactor 2 Shared Memory\nversion: " + versionStr + " 64bit."
        if self.Rf2Ext.mDirectMemoryAccessEnabled:
            if self.Rf2Ext.mSCRPluginEnabled:
                msg += "  Stock Car Rules plugin enabled. (DFT:%d" % \
                    self.Rf2Ext.mSCRPluginDoubleFileType
            else:
                msg += "  DMA enabled."

    # Only verify once.
    return msg


  ###########################################################
  # Access functions
  def isSharedMemoryAvailable(self):
    """
    True: rF2 is running and the memory map is loaded
    """
    version = Cbytestring2Python(self.Rf2Ext.mVersion)
    # 2019/04/23:  3.5.0.9
    return version != ''

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
    return self.Rf2Scor.mVehicles[self.player].mControl == 1
    # who's in control: -1=nobody (shouldn't get this), 0=local player,
    # 1=local AI, 2=remote, 3=replay (shouldn't get this)

    # didn't work self.Rf2Ext.mPhysics.mAIControl

  def driverName(self):
    """
    Get the player's name
    """
    return Cbytestring2Python(self.Rf2Scor.mVehicles[self.player].mDriverName)

  def playersVehicleTelemetry(self):
    """ Find the player's driver number """
    for player in range(50): #self.Rf2Tele.mVehicles[0].mNumVehicles:
      if self.Rf2Scor.mVehicles[player].mIsPlayer:
        self.player = player
        break
    # Get the variable for the player's vehicle
    return self.Rf2Tele.mVehicles[self.player]

  def playersVehicleScoring(self):
    """ Get the variable for the player's vehicle """
    return self.Rf2Scor.mVehicles[self.player]

  def close(self):
    # This didn't help with the errors
    try:
      self._rf2_tele.close()
      self._rf2_scor.close()
      self._rf2_ext.close()
    except BufferError: # "cannot close exported pointers exist"
      pass

  def __del__(self):
    self.close()

def Cbytestring2Python(bytestring):
    """
    C string to Python string
    """
    return bytes(bytestring).partition(b'\0')[0].decode().rstrip()

def test_main():
    # pylint: disable=E,W,R,C
    # Example usage
    info = SimInfoAPI()
    print(info.versionCheckMsg)
    clutch = info.playersVehicleTelemetry().mUnfilteredClutch # 1.0 clutch down, 0 clutch up
    info.playersVehicleTelemetry().mGear = 1
    gear   = info.playersVehicleTelemetry().mGear  # -1 to 6
    assert info.playersVehicleTelemetry().mGear == 1
    info.playersVehicleTelemetry().mGear = 2
    assert info.playersVehicleTelemetry().mGear == 2
    gear   = info.playersVehicleTelemetry().mGear  # -1 to 6
    info.playersVehicleTelemetry().mGear = 1
    assert info.playersVehicleTelemetry().mGear == 1

    driver = Cbytestring2Python(info.playersVehicleScoring().mDriverName)
    print('%s Gear: %d, Clutch position: %d' % (driver, gear, clutch))

    _vehicleName = Cbytestring2Python(info.playersVehicleScoring().mVehicleName)
    trackName = Cbytestring2Python(info.Rf2Scor.mScoringInfo.mTrackName)
    _vehicleClass = Cbytestring2Python(info.playersVehicleScoring().mVehicleClass)

    started = info.Rf2Ext.mSessionStarted
    realtime = info.Rf2Ext.mInRealtimeFC

    version = Cbytestring2Python(info.Rf2Ext.mVersion)
    # 2019/04/23:  3.5.0.9
    print(version)

    if info.isRF2running():
        print('rfactor2.exe is running')

    if info.isSharedMemoryAvailable():
      print('Memory map is loaded')
    else:
      print('Memory map is not loaded')

    if info.isTrackLoaded():
      trackName = Cbytestring2Python(info.Rf2Scor.mScoringInfo.mTrackName)
      print('%s is loaded' % trackName)
    else:
      print('Track is not loaded')

    if info.isOnTrack():
      driver = Cbytestring2Python(info.playersVehicleScoring().mDriverName)
      print('Driver "%s" is on track' % driver)
    else:
      print('Driver is not on track')

    if info.isAiDriving():
      print('AI is driving the car')
    else:
      print('Car not under AI control')

    return 'OK'


if __name__ == '__main__':
  test_main()
