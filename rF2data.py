"""
Python mapping of The Iron Wolf's rF2 Shared Memory Tools
Auto-generated from rF2data.cs
"""
# pylint: disable=C,R,W

import ctypes
import mmap
from enum import Enum, Flag


class rFactor2Constants:
    MM_TELEMETRY_FILE_NAME: str = "$rFactor2SMMP_Telemetry$"
    MM_SCORING_FILE_NAME: str = "$rFactor2SMMP_Scoring$"
    MM_RULES_FILE_NAME: str = "$rFactor2SMMP_Rules$"
    MM_FORCE_FEEDBACK_FILE_NAME: str = "$rFactor2SMMP_ForceFeedback$"
    MM_GRAPHICS_FILE_NAME: str = "$rFactor2SMMP_Graphics$"
    MM_PITINFO_FILE_NAME: str = "$rFactor2SMMP_PitInfo$"
    MM_WEATHER_FILE_NAME: str = "$rFactor2SMMP_Weather$"
    MM_EXTENDED_FILE_NAME: str = "$rFactor2SMMP_Extended$"

    MM_HWCONTROL_FILE_NAME: str = "$rFactor2SMMP_HWControl$"
    MM_HWCONTROL_LAYOUT_VERSION: int = 1

    MM_WEATHER_CONTROL_FILE_NAME: str = "$rFactor2SMMP_WeatherControl$"
    MM_WEATHER_CONTROL_LAYOUT_VERSION: int = 1

    MM_RULES_CONTROL_FILE_NAME: str = "$rFactor2SMMP_RulesControl$"
    MM_RULES_CONTROL_LAYOUT_VERSION: int = 1

    MM_PLUGIN_CONTROL_FILE_NAME: str = "$rFactor2SMMP_PluginControl$"
    MM_PLUGIN_CONTROL_LAYOUT_VERSION: int = 1

    MAX_MAPPED_VEHICLES: int = 128
    MAX_MAPPED_IDS: int = 512
    MAX_STATUS_MSG_LEN: int = 128
    MAX_RULES_INSTRUCTION_MSG_LEN: int = 96
    MAX_HWCONTROL_NAME_LEN: int = 96

    RFACTOR2_PROCESS_NAME: str = "rFactor2"
    RFACTOR2_DEVMODE_PROCESS_NAME: str = "rFactor2 Mod Mode"
    RFACTOR2_DEDICATED_PROCESS_NAME: str = "rFactor2 Dedicated"


"""
# untranslated /*
rF2 internal state mapping structures.  Allows access to native C++ structs from C
# untranslated Must be kept in sync with Include\rF2State.h.
# untranslated See: MainForm.MainUpdate for sample on how to marshall from native in memory struct.
# untranslated Author: The Iron Wolf (vleonavicius@hotmail.com)
# untranslated Website: thecrewchief.org
# untranslated */
# untranslated using Newtonsoft.Json;
# untranslated using System;
# untranslated using System.Runtime.InteropServices;
# untranslated using System.Xml.Serialization;
# untranslated namespace rF2SharedMemory
class rFactor2Constants
    const byte RowX = 0;
    const byte RowY = 1;
    const byte RowZ = 2;
"""


class SubscribedBuffer(Flag):
    """Subscribed buffer flag"""

    Telemetry = 1
    Scoring = 2
    Rules = 4
    MultiRules = 8
    ForceFeedback = 16
    Graphics = 32
    PitInfo = 64
    Weather = 128
    All = 255


class rF2GamePhase(Enum):
    """
    Game phase states

    0=Before session has begun,
    1=Reconnaissance laps (race only),
    2=Grid walk-through (race only),
    3=Formation lap (race only),
    4=Starting-light countdown has begun (race only),
    5=Green flag,
    6=Full course yellow / safety car,
    7=Session stopped,
    8=Session over,
    9=Paused (tag.2015.09.14 - this is new, and indicates that this is a heartbeat call to the plugin)
    """

    Garage = 0
    WarmUp = 1
    GridWalk = 2
    Formation = 3
    Countdown = 4
    GreenFlag = 5
    FullCourseYellow = 6
    SessionStopped = 7
    SessionOver = 8
    PausedOrHeartbeat = 9


class rF2YellowFlagState(Enum):
    """
    Yellow flag states (applies to full-course only)

    -1=Invalid,
    0=None,
    1=Pending,
    2=Pits closed,
    3=Pit lead lap,
    4=Pits open,
    5=Last lap,
    6=Resume,
    7=Race halt (not currently used),
    """

    Invalid = -1
    NoFlag = 0
    Pending = 1
    PitClosed = 2
    PitLeadLap = 3
    PitOpen = 4
    LastLap = 5
    Resume = 6
    RaceHalt = 7


class rF2SurfaceType(Enum):
    """
    Surface type

    0=dry,
    1=wet,
    2=grass,
    3=dirt,
    4=gravel,
    5=rumblestrip,
    6=special
    """

    Dry = 0
    Wet = 1
    Grass = 2
    Dirt = 3
    Gravel = 4
    Kerb = 5
    Special = 6


class rF2Sector(Enum):
    """
    Sector index

    0=sector3,
    1=sector1,
    2=sector2 (don't ask why)
    """

    Sector3 = 0
    Sector1 = 1
    Sector2 = 2


class rF2FinishStatus(Enum):
    """Finish status

    0=none,
    1=finished,
    2=dnf,
    3=dq
    """

    _None = 0
    Finished = 1
    Dnf = 2
    Dq = 3


class rF2Control(Enum):
    """
    Who's in control

    -1=nobody (shouldn't get this),
    0=local player,
    1=local AI,
    2=remote,
    3=replay (shouldn't get this)
    """

    Nobody = -1
    Player = 0
    AI = 1
    Remote = 2
    Replay = 3


class rF2WheelIndex(Enum):
    """Wheel index

    front left=0,
    front right=1,
    rear left=2,
    rear right=3
    """

    FrontLeft = 0
    FrontRight = 1
    RearLeft = 2
    RearRight = 3


class rF2PitState(Enum):
    """Pit state

    0=none,
    1=request,
    2=entering,
    3=stopped,
    4=exiting
    """

    _None = 0
    Request = 1
    Entering = 2
    Stopped = 3
    Exiting = 4


class rF2PrimaryFlag(Enum):
    """
    Primary flag being shown to vehicle

    0=green,
    6=blue
    """

    Green = 0
    Blue = 6


class rF2CountLapFlag(Enum):
    """Count lap flag

    0=do not count lap or time,
    1=count lap but not time,
    2=count lap and time
    """

    DoNotCountLap = 0
    CountLapButNotTime = 1
    CountLapAndTime = 2


class rF2RearFlapLegalStatus(Enum):
    """
    Rear flap (DRS) status

    0=disallowed,
    1=criteria detected but not allowed quite yet,
    2=allowed
    """

    Disallowed = 0
    DetectedButNotAllowedYet = 1
    Alllowed = 2


class rF2IgnitionStarterStatus(Enum):
    """
    Ignition starter status

    0=off,
    1=ignition,
    2=ignition+starter
    """

    Off = 0
    Ignition = 1
    IgnitionAndStarter = 2


class rF2SafetyCarInstruction(Enum):
    """Safety car instruction

    0=no change,
    1=go active,
    2=head for pits
    """

    NoChange = 0
    GoActive = 1
    HeadForPits = 2


class rF2TrackRulesCommand(Enum):
    AddFromTrack = 0
    AddFromPit = 1        # exited pit during full-course yellow
    AddFromUndq = 2       # during a full-course yellow, the admin reversed a disqualification
    RemoveToPit = 3       # entered pit during full-course yellow
    RemoveToDnf = 4       # vehicle DNF'd during full-course yellow
    RemoveToDq = 5        # vehicle DQ'd during full-course yellow
    RemoveToUnloaded = 6  # vehicle unloaded (possibly kicked out or banned) during full-course yellow
    MoveToBack = 7        # misbehavior during full-course yellow, resulting in the penalty of being moved to the back of their current line
    LongestTime = 8       # misbehavior during full-course yellow, resulting in the penalty of being moved to the back of the longest line
    Maximum = 9           # should be last


class rF2TrackRulesColumn(Enum):
    LeftLane = 0
    MidLefLane = 1      # mid-left
    MiddleLane = 2      # middle
    MidrRghtLane = 3    # mid-right
    RightLane = 4       # right (outside)
    MaxLanes = 5        # should be after the valid static lane choices
    Invalid = MaxLanes
    FreeChoice = 6      # free choice (dynamically chosen by driver)
    Pending = 7         # depends on another participant's free choice (dynamically set after another driver chooses)
    Maximum = 8         # should be last


class rF2TrackRulesStage(Enum):
    FormationInit = 0
    FormationUpdate = 1  # update of the formation lap
    Normal = 2           # normal (non-yellow) update
    CautionInit = 3      # initialization of a full-course yellow
    CautionUpdate = 4    # update of a full-course yellow
    Maximum = 5          # should be last

class IP_VehicleClass(Enum):
    Hypercar = 0x00,
    LMP2_ELMS = 0x02,
    LMP2 = 0x03,
    LMP3 = 0x04,
    GTE = 0x05,
    GT3 = 0x06,
    PaceCar = 0x08,
    Unknown = 0xFF

class IP_VehicleChampionship(Enum):
    WEC_2023 = 0x00, 
    WEC_2024 = 0x01, 
    WEC_2025 = 0x02,
    WEC_2026 = 0x03,
    ELMS_2025 = 0X10,
    ELMS_2026 = 0x11,
    Unknown = 0xFF

# untranslated namespace rFactor2Data
# untranslated [StructLayout(LayoutKind.Sequential, Pack = 4)]
class rF2Vec3(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("x", ctypes.c_double),
        ("y", ctypes.c_double),
        ("z", ctypes.c_double),
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2Wheel(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mSuspensionDeflection", ctypes.c_double),         # meters
        ("mRideHeight", ctypes.c_double),                   # meters
        ("mSuspForce", ctypes.c_double),                    # pushrod load in Newtons
        ("mBrakeTemp", ctypes.c_double),                    # Celsius
        ("mBrakePressure", ctypes.c_double),                # currently 0.0-1.0, depending on driver input and brake balance; will convert to true brake pressure (kPa) in future
        ("mRotation", ctypes.c_double),                     # radians/sec
        ("mLateralPatchVel", ctypes.c_double),              # lateral velocity at contact patch
        ("mLongitudinalPatchVel", ctypes.c_double),         # longitudinal velocity at contact patch
        ("mLateralGroundVel", ctypes.c_double),             # lateral velocity at contact patch
        ("mLongitudinalGroundVel", ctypes.c_double),        # longitudinal velocity at contact patch
        ("mCamber", ctypes.c_double),                       # radians (positive is left for left-side wheels, right for right-side wheels)
        ("mLateralForce", ctypes.c_double),                 # Newtons
        ("mLongitudinalForce", ctypes.c_double),            # Newtons
        ("mTireLoad", ctypes.c_double),                     # Newtons
        ("mGripFract", ctypes.c_double),                    # an approximation of what fraction of the contact patch is sliding
        ("mPressure", ctypes.c_double),                     # kPa (tire pressure)
        ("mTemperature", ctypes.c_double*3),                # Kelvin (subtract 273.15 to get Celsius), left/center/right (not to be confused with inside/center/outside!)
        ("mWear", ctypes.c_double),                         # wear (0.0-1.0, fraction of maximum) ... this is not necessarily proportional with grip loss
        ("mTerrainName", ctypes.c_char*16),                 # the material prefixes from the TDF file
        ("mSurfaceType", ctypes.c_ubyte),                   # 0=dry, 1=wet, 2=grass, 3=dirt, 4=gravel, 5=rumblestrip, 6 = special
        ("mFlat", ctypes.c_bool),                           # whether tire is flat
        ("mDetached", ctypes.c_bool),                       # whether wheel is detached
        ("mStaticUndeflectedRadius", ctypes.c_ubyte),       # tire radius in centimeters
        ("mVerticalTireDeflection", ctypes.c_double),       # how much is tire deflected from its (speed-sensitive) radius
        ("mWheelYLocation", ctypes.c_double),               # wheel's y location relative to vehicle y location
        ("mToe", ctypes.c_double),                          # current toe angle w.r.t. the vehicle
        ("mTireCarcassTemperature", ctypes.c_double),       # rough average of temperature samples from carcass (Kelvin)
        ("mTireInnerLayerTemperature", ctypes.c_double*3),  # rough average of temperature samples from innermost layer of rubber (before carcass) (Kelvin)
        ("mOptimalTemp", ctypes.c_float),
        ("mCompoundIndex", ctypes.c_ubyte),
        ("mCompoundType", ctypes.c_ubyte),
        ("mExpansion", ctypes.c_ubyte*18),
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2VehicleTelemetry(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mID", ctypes.c_int),                                # slot ID (note that it can be re-used in multiplayer after someone leaves)
        ("mDeltaTime", ctypes.c_double),                      # time since last update (seconds)
        ("mElapsedTime", ctypes.c_double),                    # game session time
        ("mLapNumber", ctypes.c_int),                         # current lap number
        ("mLapStartET", ctypes.c_double),                     # time this lap was started
        ("mVehicleName", ctypes.c_char*64),                   # current vehicle name
        ("mTrackName", ctypes.c_char*64),                     # current track name
        ("mPos", rF2Vec3),                                    # world position in meters
        ("mLocalVel", rF2Vec3),                               # velocity (meters/sec) in local vehicle coordinates
        ("mLocalAccel", rF2Vec3),                             # acceleration (meters/sec^2) in local vehicle coordinates
        ("mOri", rF2Vec3*3),                                  # rows of orientation matrix (use TelemQuat conversions if desired), also converts local
        ("mLocalRot", rF2Vec3),                               # rotation (radians/sec) in local vehicle coordinates
        ("mLocalRotAccel", rF2Vec3),                          # rotational acceleration (radians/sec^2) in local vehicle coordinates
        ("mGear", ctypes.c_int),                              # -1=reverse, 0=neutral, 1+ = forward gears
        ("mEngineRPM", ctypes.c_double),                      # engine RPM
        ("mEngineWaterTemp", ctypes.c_double),                # Celsius
        ("mEngineOilTemp", ctypes.c_double),                  # Celsius
        ("mClutchRPM", ctypes.c_double),                      # clutch RPM
        ("mUnfilteredThrottle", ctypes.c_double),             # ranges  0.0-1.0
        ("mUnfilteredBrake", ctypes.c_double),                # ranges  0.0-1.0
        ("mUnfilteredSteering", ctypes.c_double),             # ranges -1.0-1.0 (left to right)
        ("mUnfilteredClutch", ctypes.c_double),               # ranges  0.0-1.0
        ("mFilteredThrottle", ctypes.c_double),               # ranges  0.0-1.0
        ("mFilteredBrake", ctypes.c_double),                  # ranges  0.0-1.0
        ("mFilteredSteering", ctypes.c_double),               # ranges -1.0-1.0 (left to right)
        ("mFilteredClutch", ctypes.c_double),                 # ranges  0.0-1.0
        ("mSteeringShaftTorque", ctypes.c_double),            # torque around steering shaft (used to be mSteeringArmForce, but that is not necessarily accurate for feedback purposes)
        ("mFront3rdDeflection", ctypes.c_double),             # deflection at front 3rd spring
        ("mRear3rdDeflection", ctypes.c_double),              # deflection at rear 3rd spring
        ("mFrontWingHeight", ctypes.c_double),                # front wing height
        ("mFrontRideHeight", ctypes.c_double),                # front ride height
        ("mRearRideHeight", ctypes.c_double),                 # rear ride height
        ("mDrag", ctypes.c_double),                           # drag
        ("mFrontDownforce", ctypes.c_double),                 # front downforce
        ("mRearDownforce", ctypes.c_double),                  # rear downforce
        ("mFuel", ctypes.c_double),                           # amount of fuel (liters)
        ("mEngineMaxRPM", ctypes.c_double),                   # rev limit
        ("mScheduledStops", ctypes.c_ubyte),                  # number of scheduled pitstops
        ("mOverheating", ctypes.c_bool),                      # whether overheating icon is shown
        ("mDetached", ctypes.c_bool),                         # whether any parts (besides wheels) have been detached
        ("mHeadlights", ctypes.c_bool),                       # whether headlights are on
        ("mDentSeverity", ctypes.c_ubyte*8),                  # dent severity at 8 locations around the car (0=none, 1=some, 2=more)
        ("mLastImpactET", ctypes.c_double),                   # time of last impact
        ("mLastImpactMagnitude", ctypes.c_double),            # magnitude of last impact
        ("mLastImpactPos", rF2Vec3),                          # location of last impact
        ("mEngineTorque", ctypes.c_double),                   # current engine torque (including additive torque) (used to be mEngineTq, but there's little reason to abbreviate it)
        ("mCurrentSector", ctypes.c_int),                     # the current sector (zero-based) with the pitlane stored in the sign bit (example: entering pits from third sector gives 0x80000002)
        ("mSpeedLimiter", ctypes.c_ubyte),                    # whether speed limiter is on
        ("mMaxGears", ctypes.c_ubyte),                        # maximum forward gears
        ("mFrontTireCompoundIndex", ctypes.c_ubyte),          # index within brand
        ("mRearTireCompoundIndex", ctypes.c_ubyte),           # index within brand
        ("mFuelCapacity", ctypes.c_double),                   # capacity in liters
        ("mFrontFlapActivated", ctypes.c_ubyte),              # whether front flap is activated
        ("mRearFlapActivated", ctypes.c_ubyte),               # whether rear flap is activated
        ("mRearFlapLegalStatus", ctypes.c_ubyte),             # 0=disallowed, 1=criteria detected but not allowed quite yet, 2 = allowed
        ("mIgnitionStarter", ctypes.c_ubyte),                 # 0=off 1=ignition 2 = ignition+starter
        ("mFrontTireCompoundName", ctypes.c_char*18),         # name of front tire compound
        ("mRearTireCompoundName", ctypes.c_char*18),          # name of rear tire compound
        ("mSpeedLimiterAvailable", ctypes.c_ubyte),           # whether speed limiter is available
        ("mAntiStallActivated", ctypes.c_ubyte),              # whether (hard) anti-stall is activated
        ("mUnused", ctypes.c_ubyte*2),                        #
        ("mVisualSteeringWheelRange", ctypes.c_float),        # the *visual* steering wheel range
        ("mRearBrakeBias", ctypes.c_double),                  # fraction of brakes on rear
        ("mTurboBoostPressure", ctypes.c_double),             # current turbo boost pressure if available
        ("mPhysicsToGraphicsOffset", ctypes.c_float*3),       # offset from static CG to graphical center
        ("mPhysicalSteeringWheelRange", ctypes.c_float),      # the *physical* steering wheel range
        ("mDeltaBest", ctypes.c_double),                      # (omitted in error by S397)
        ("mBatteryChargeFraction", ctypes.c_double),          # Battery charge as fraction [0.0-1.0]
        ("mElectricBoostMotorTorque", ctypes.c_double),       # current torque of boost motor (can be negative when in regenerating mode)
        ("mElectricBoostMotorRPM", ctypes.c_double),          # current rpm of boost motor
        ("mElectricBoostMotorTemperature", ctypes.c_double),  # current temperature of boost motor
        ("mElectricBoostWaterTemperature", ctypes.c_double),  # current water temperature of boost motor cooler if present (0 otherwise)
        ("mElectricBoostMotorState", ctypes.c_ubyte),         # 0=unavailable 1=inactive, 2=propulsion, 3=regeneration
        ("mLapInvalidated", ctypes.c_bool),
        ("mABSActive", ctypes.c_bool),
        ("mTCActive", ctypes.c_bool),
        ("mSpeedLimiterActive", ctypes.c_bool),
        ("mWiperState", ctypes.c_ubyte),
        ("mTC", ctypes.c_ubyte),
        ('mTCMax', ctypes.c_ubyte),
        ('mTCSlip', ctypes.c_ubyte),
        ('mTCSlipMax', ctypes.c_ubyte),
        ('mTCCut', ctypes.c_ubyte),
        ('mTCCutMax', ctypes.c_ubyte),
        ('mABS', ctypes.c_ubyte),
        ('mABSMax', ctypes.c_ubyte),
        ('mMotorMap', ctypes.c_ubyte),
        ('mMotorMapMax', ctypes.c_ubyte),
        ('mMigration', ctypes.c_ubyte),
        ('mMigrationMax', ctypes.c_ubyte),
        ('mFrontAntiSway', ctypes.c_ubyte),
        ('mFrontAntiSwayMax', ctypes.c_ubyte),
        ('mRearAntiSway', ctypes.c_ubyte),
        ('mRearAntiSwayMax', ctypes.c_ubyte),
        ('mLiftAndCoastProgress', ctypes.c_ubyte),
        ('mTrackLimitsSteps', ctypes.c_ubyte), # Normalized track limits points (TrackLimitPoints * TrackLimitStepsPerPoint)
        ('mRegen', ctypes.c_float), #kW
        ('mSoC', ctypes.c_float),
        ('mVirtualEnergy', ctypes.c_float),
        ('mTimeGapCarAhead', ctypes.c_float),
        ('mTimeGapCarBehind', ctypes.c_float),
        ('mTimeGapPlaceAhead', ctypes.c_float),
        ('mTimeGapPlaceBehind', ctypes.c_float),
        ("mVehicleModel", ctypes.c_char*30),
        ("mVehicleClass", ctypes.c_ubyte),
        ("mVehicleChampionship", ctypes.c_ubyte),

        ("mExpansion", ctypes.c_ubyte*20), # for future use (note that the slot ID has been moved to mID above)
        ("mWheels", rF2Wheel*4),                              # wheel info (front left, front right, rear left, rear right)
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2ScoringInfo(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mTrackName", ctypes.c_char*64),         # current track name
        ("mSession", ctypes.c_int),               # current session (0=testday 1-4=practice 5-8=qual 9=warmup 10-13 = race)
        ("mCurrentET", ctypes.c_double),          # current time
        ("mEndET", ctypes.c_double),              # ending time
        ("mMaxLaps", ctypes.c_int),               # maximum laps
        ("mLapDist", ctypes.c_double),            # distance around track
        ("mResultsStreamPointer", ctypes.c_ubyte*8),
        ("mNumVehicles", ctypes.c_int),           # current number of vehicles
        ("mGamePhase", ctypes.c_ubyte),
        ("mYellowFlagState", ctypes.c_char),
        ("mSectorFlag", ctypes.c_ubyte*3),        # whether there are any local yellows at the moment in each sector (not sure if sector 0 is first or last, so test)
        ("mStartLight", ctypes.c_ubyte),          # start light frame (number depends on track)
        ("mNumRedLights", ctypes.c_ubyte),        # number of red lights in start sequence
        ("mInRealtime", ctypes.c_bool),           # in realtime as opposed to at the monitor
        ("mPlayerName", ctypes.c_char*32),        # player name (including possible multiplayer override)
        ("mPlrFileName", ctypes.c_char*64),       # may be encoded to be a legal filename
        ("mDarkCloud", ctypes.c_double),          # cloud darkness? 0.0-1.0
        ("mRaining", ctypes.c_double),            # raining severity 0.0-1.0
        ("mAmbientTemp", ctypes.c_double),        # temperature (Celsius)
        ("mTrackTemp", ctypes.c_double),          # temperature (Celsius)
        ("mWind", rF2Vec3),                       # wind speed
        ("mMinPathWetness", ctypes.c_double),     # minimum wetness on main path 0.0-1.0
        ("mMaxPathWetness", ctypes.c_double),     # maximum wetness on main path 0.0-1.0
        ("mGameMode", ctypes.c_ubyte),            # 1 = server, 2 = client, 3 = server and client
        ("mIsPasswordProtected", ctypes.c_bool),  # is the server password protected
        ("mServerPort", ctypes.c_ushort),         # the port of the server (if on a server)
        ("mServerPublicIP", ctypes.c_uint),       # the public IP address of the server (if on a server)
        ("mMaxPlayers", ctypes.c_int),            # maximum number of vehicles that can be in the session
        ("mServerName", ctypes.c_char*32),        # name of the server
        ("mStartET", ctypes.c_float),             # start time (seconds since midnight) of the event
        ("mAvgPathWetness", ctypes.c_double),     # average wetness on main path 0.0-1.0
        ("mSessionTimeRemaining", ctypes.c_float),
        ("mTimeOfDay", ctypes.c_float),
        ("mIsFixedSetup", ctypes.c_bool),
        ("mTrackGripLevel", ctypes.c_ubyte),
        ("mCloudCoverage", ctypes.c_ubyte),
        ("mTrackLimitsStepsPerPenalty", ctypes.c_ubyte),
        ("mTrackLimitsStepsPerPoint", ctypes.c_ubyte),

        ("mExpansion", ctypes.c_ubyte*187),
        ("mVehiclePointer", ctypes.c_ubyte*8),
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2VehicleScoring(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mID", ctypes.c_int),                   # slot ID (note that it can be re-used in multiplayer after someone leaves)
        ("mDriverName", ctypes.c_char*32),       # driver name
        ("mVehicleName", ctypes.c_char*64),      # vehicle name
        ("mTotalLaps", ctypes.c_short),          # laps completed
        ("mSector", ctypes.c_byte),              # 0=sector3, 1=sector1, 2 = sector2 (don't ask why)
        ("mFinishStatus", ctypes.c_byte),        # 0=none, 1=finished, 2=dnf, 3 = dq
        ("mLapDist", ctypes.c_double),           # current distance around track
        ("mPathLateral", ctypes.c_double),       # lateral position with respect to *very approximate* "center" path
        ("mTrackEdge", ctypes.c_double),         # track edge (w.r.t. "center" path) on same side of track as vehicle
        ("mBestSector1", ctypes.c_double),       # best sector 1
        ("mBestSector2", ctypes.c_double),       # best sector 2 (plus sector 1)
        ("mBestLapTime", ctypes.c_double),       # best lap time
        ("mLastSector1", ctypes.c_double),       # last sector 1
        ("mLastSector2", ctypes.c_double),       # last sector 2 (plus sector 1)
        ("mLastLapTime", ctypes.c_double),       # last lap time
        ("mCurSector1", ctypes.c_double),        # current sector 1 if valid
        ("mCurSector2", ctypes.c_double),        # current sector 2 (plus sector 1) if valid
        ("mNumPitstops", ctypes.c_short),        # number of pitstops made
        ("mNumPenalties", ctypes.c_short),       # number of outstanding penalties
        ("mIsPlayer", ctypes.c_bool),            # is this the player's vehicle
        ("mControl", ctypes.c_byte),             # who's in control: -1=nobody (shouldn't get this), 0=local player, 1=local AI, 2=remote, 3 = replay (shouldn't get this)
        ("mInPits", ctypes.c_bool),              # between pit entrance and pit exit (not always accurate for remote vehicles)
        ("mPlace", ctypes.c_ubyte),              # 1-based position
        ("mVehicleClass", ctypes.c_char*32),     # vehicle class
        ("mTimeBehindNext", ctypes.c_double),    # time behind vehicle in next higher place
        ("mLapsBehindNext", ctypes.c_int),       # laps behind vehicle in next higher place
        ("mTimeBehindLeader", ctypes.c_double),  # time behind leader
        ("mLapsBehindLeader", ctypes.c_int),     # laps behind leader
        ("mLapStartET", ctypes.c_double),        # time this lap was started
        ("mPos", rF2Vec3),                       # world position in meters
        ("mLocalVel", rF2Vec3),                  # velocity (meters/sec) in local vehicle coordinates
        ("mLocalAccel", rF2Vec3),                # acceleration (meters/sec^2) in local vehicle coordinates
        ("mOri", rF2Vec3*3),                     # rows of orientation matrix (use TelemQuat conversions if desired), also converts local
        ("mLocalRot", rF2Vec3),                  # rotation (radians/sec) in local vehicle coordinates
        ("mLocalRotAccel", rF2Vec3),             # rotational acceleration (radians/sec^2) in local vehicle coordinates
        ("mHeadlights", ctypes.c_ubyte),         # status of headlights
        ("mPitState", ctypes.c_ubyte),           # 0=none, 1=request, 2=entering, 3=stopped, 4 = exiting
        ("mServerScored", ctypes.c_ubyte),       # whether this vehicle is being scored by server (could be off in qualifying or racing heats)
        ("mIndividualPhase", ctypes.c_ubyte),    # game phases (described below) plus 9=after formation, 10=under yellow, 11 = under blue (not used)
        ("mQualification", ctypes.c_int),        # 1-based, can be -1 when invalid
        ("mTimeIntoLap", ctypes.c_double),       # estimated time into lap
        ("mEstimatedLapTime", ctypes.c_double),  # estimated laptime used for "time behind" and "time into lap" (note: this may changed based on vehicle and setup!?)
        ("mPitGroup", ctypes.c_char*24),         # pit group (same as team name unless pit is shared)
        ("mFlag", ctypes.c_ubyte),               # primary flag being shown to vehicle (currently only 0=green or 6 = blue)
        ("mUnderYellow", ctypes.c_bool),         # whether this car has taken a full-course caution flag at the start/finish line
        ("mCountLapFlag", ctypes.c_ubyte),       # 0 = do not count lap or time, 1 = count lap but not time, 2 = count lap and time
        ("mInGarageStall", ctypes.c_bool),       # appears to be within the correct garage stall
        ("mUpgradePack", ctypes.c_ubyte*16),     # Coded upgrades
        ("mPitLapDist", ctypes.c_float),         # location of pit in terms of lap distance
        ("mBestLapSector1", ctypes.c_float),     # sector 1 time from best lap (not necessarily the best sector 1 time)
        ("mBestLapSector2", ctypes.c_float),     # sector 2 time from best lap (not necessarily the best sector 2 time)
        ("mSteamID", ctypes.c_ulonglong),        # SteamID of the current driver (if any)
        ("mVehFilename", ctypes.c_char*32),      # filename of veh file used to identify this vehicle.
        ("mAttackMode", ctypes.c_short),
        ("mFuelFraction", ctypes.c_ubyte),       # Percentage of fuel or battery left in vehicle. 0x00 = 0%; 0xFF = 100%
        ("mDRSState", ctypes.c_bool),            # DRS (RearFlap) state
        ("mExpansion", ctypes.c_ubyte*4),        # for future use
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2PhysicsOptions(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mTractionControl", ctypes.c_ubyte),          # 0 (off) - 3 (high)
        ("mAntiLockBrakes", ctypes.c_ubyte),           # 0 (off) - 2 (high)
        ("mStabilityControl", ctypes.c_ubyte),         # 0 (off) - 2 (high)
        ("mAutoShift", ctypes.c_ubyte),                # 0 (off), 1 (upshifts), 2 (downshifts), 3 (all)
        ("mAutoClutch", ctypes.c_ubyte),               # 0 (off), 1 (on)
        ("mInvulnerable", ctypes.c_ubyte),             # 0 (off), 1 (on)
        ("mOppositeLock", ctypes.c_ubyte),             # 0 (off), 1 (on)
        ("mSteeringHelp", ctypes.c_ubyte),             # 0 (off) - 3 (high)
        ("mBrakingHelp", ctypes.c_ubyte),              # 0 (off) - 2 (high)
        ("mSpinRecovery", ctypes.c_ubyte),             # 0 (off), 1 (on)
        ("mAutoPit", ctypes.c_ubyte),                  # 0 (off), 1 (on)
        ("mAutoLift", ctypes.c_ubyte),                 # 0 (off), 1 (on)
        ("mAutoBlip", ctypes.c_ubyte),                 # 0 (off), 1 (on)
        ("mFuelMult", ctypes.c_ubyte),                 # fuel multiplier (0x-7x)
        ("mTireMult", ctypes.c_ubyte),                 # tire wear multiplier (0x-7x)
        ("mMechFail", ctypes.c_ubyte),                 # mechanical failure setting; 0 (off), 1 (normal), 2 (timescaled)
        ("mAllowPitcrewPush", ctypes.c_ubyte),         # 0 (off), 1 (on)
        ("mRepeatShifts", ctypes.c_ubyte),             # accidental repeat shift prevention (0-5; see PLR file)
        ("mHoldClutch", ctypes.c_ubyte),               # for auto-shifters at start of race: 0 (off), 1 (on)
        ("mAutoReverse", ctypes.c_ubyte),              # 0 (off), 1 (on)
        ("mAlternateNeutral", ctypes.c_ubyte),         # Whether shifting up and down simultaneously equals neutral
        ("mAIControl", ctypes.c_ubyte),                # Whether player vehicle is currently under AI control
        ("mUnused1", ctypes.c_ubyte),                  #
        ("mUnused2", ctypes.c_ubyte),                  #
        ("mManualShiftOverrideTime", ctypes.c_float),  # time before auto-shifting can resume after recent manual shift
        ("mAutoShiftOverrideTime", ctypes.c_float),    # time before manual shifting can resume after recent auto shift
        ("mSpeedSensitiveSteering", ctypes.c_float),   # 0.0 (off) - 1.0
        ("mSteerRatioSpeed", ctypes.c_float),          # speed (m/s) under which lock gets expanded to full
    ]


# untranslated [StructLayout(LayoutKind.Sequential, Pack = 4)]
class rF2TrackRulesAction(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mCommand", ctypes.c_int),  # recommended action
        ("mID", ctypes.c_int),       # slot ID if applicable
        ("mET", ctypes.c_double),    # elapsed time that event occurred, if applicable
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2TrackRulesParticipant(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mID", ctypes.c_int),                          # slot ID
        ("mFrozenOrder", ctypes.c_short),               # 0-based place when caution came out (not valid for formation laps)
        ("mPlace", ctypes.c_short),                     # 1-based place (typically used for the initialization of the formation lap track order)
        ("mYellowSeverity", ctypes.c_float),            # a rating of how much this vehicle is contributing to a yellow flag (the sum of all vehicles is compared to TrackRulesV01::mSafetyCarThreshold)
        ("mCurrentRelativeDistance", ctypes.c_double),  # equal to ( ( ScoringInfoV01::mLapDist * this->mRelativeLaps ) + VehicleScoringInfoV01::mLapDist )
        ("mRelativeLaps", ctypes.c_int),                # current formation/caution laps relative to safety car (should generally be zero except when safety car crosses s/f line); this can be decremented to implement "wave around" or "beneficiary rule" (a.k.a. "lucky dog" or "free pass")
        ("mColumnAssignment", ctypes.c_int),            # which column (line/lane) that participant is supposed to be in
        ("mPositionAssignment", ctypes.c_int),          # 0-based position within column (line/lane) that participant is supposed to be located at (-1 is invalid)
        ("mPitsOpen", ctypes.c_ubyte),                  # whether the rules allow this particular vehicle to enter pits right now (input is 2=false or 3=true; if you want to edit it, set to 0=false or 1 = true)
        ("mUpToSpeed", ctypes.c_bool),                  # while in the frozen order, this flag indicates whether the vehicle can be followed (this should be false for somebody who has temporarily spun and hasn't gotten back up to speed yet)
        ("mUnused", ctypes.c_bool*2),                   #
        ("mGoalRelativeDistance", ctypes.c_double),     # calculated based on where the leader is, and adjusted by the desired column spacing and the column/position assignments
        ("mMessage", ctypes.c_char*96),                 # a message for this participant to explain what is going on it will get run through translator on client machines
        ("mExpansion", ctypes.c_ubyte*192),
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2TrackRules(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mCurrentET", ctypes.c_double),                   # current time
        ("mStage", ctypes.c_int),                          # current stage
        ("mPoleColumn", ctypes.c_int),                     # column assignment where pole position seems to be located
        ("mNumActions", ctypes.c_int),                     # number of recent actions
        ("mActionPointer", ctypes.c_ubyte*8),
        ("mNumParticipants", ctypes.c_int),                # number of participants (vehicles)
        ("mYellowFlagDetected", ctypes.c_bool),            # whether yellow flag was requested or sum of participant mYellowSeverity's exceeds mSafetyCarThreshold
        ("mYellowFlagLapsWasOverridden", ctypes.c_ubyte),  # whether mYellowFlagLaps (below) is an admin request (0=no 1=yes 2 = clear yellow)
        ("mSafetyCarExists", ctypes.c_bool),               # whether safety car even exists
        ("mSafetyCarActive", ctypes.c_bool),               # whether safety car is active
        ("mSafetyCarLaps", ctypes.c_int),                  # number of laps
        ("mSafetyCarThreshold", ctypes.c_float),           # the threshold at which a safety car is called out (compared to the sum of TrackRulesParticipantV01::mYellowSeverity for each vehicle)
        ("mSafetyCarLapDist", ctypes.c_double),            # safety car lap distance
        ("mSafetyCarLapDistAtStart", ctypes.c_float),      # where the safety car starts from
        ("mPitLaneStartDist", ctypes.c_float),             # where the waypoint branch to the pits breaks off (this may not be perfectly accurate)
        ("mTeleportLapDist", ctypes.c_float),              # the front of the teleport locations (a useful first guess as to where to throw the green flag)
        ("mInputExpansion", ctypes.c_ubyte*256),
        ("mYellowFlagState", ctypes.c_byte),               # see ScoringInfoV01 for values
        ("mYellowFlagLaps", ctypes.c_short),               # suggested number of laps to run under yellow (may be passed in with admin command)
        ("mSafetyCarInstruction", ctypes.c_int),           # 0=no change, 1=go active, 2 = head for pits
        ("mSafetyCarSpeed", ctypes.c_float),               # maximum speed at which to drive
        ("mSafetyCarMinimumSpacing", ctypes.c_float),      # minimum spacing behind safety car (-1 to indicate no limit)
        ("mSafetyCarMaximumSpacing", ctypes.c_float),      # maximum spacing behind safety car (-1 to indicate no limit)
        ("mMinimumColumnSpacing", ctypes.c_float),         # minimum desired spacing between vehicles in a column (-1 to indicate indeterminate/unenforced)
        ("mMaximumColumnSpacing", ctypes.c_float),         # maximum desired spacing between vehicles in a column (-1 to indicate indeterminate/unenforced)
        ("mMinimumSpeed", ctypes.c_float),                 # minimum speed that anybody should be driving (-1 to indicate no limit)
        ("mMaximumSpeed", ctypes.c_float),                 # maximum speed that anybody should be driving (-1 to indicate no limit)
        ("mMessage", ctypes.c_char*96),                    # a message for everybody to explain what is going on (which will get run through translator on client machines)
        ("mParticipantPointer", ctypes.c_ubyte*8),
        ("mInputOutputExpansion", ctypes.c_ubyte*256),
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2PitMenu(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mCategoryIndex", ctypes.c_int),     # index of the current category
        ("mCategoryName", ctypes.c_char*32),  # name of the current category (untranslated)
        ("mChoiceIndex", ctypes.c_int),       # index of the current choice (within the current category)
        ("mChoiceString", ctypes.c_char*32),  # name of the current choice (may have some translated words)
        ("mNumChoices", ctypes.c_int),        # total number of choices (0 < = mChoiceIndex < mNumChoices)
        ("mExpansion", ctypes.c_ubyte*256),   # for future use
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2WeatherControlInfo(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mET", ctypes.c_double),                      # when you want this weather to take effect
        ("mRaining", ctypes.c_double*9),               # rain (0.0-1.0) at different nodes
        ("mCloudiness", ctypes.c_double),              # general cloudiness (0.0=clear to 1.0 = dark)
        ("mAmbientTempK", ctypes.c_double),            # ambient temperature (Kelvin)
        ("mWindMaxSpeed", ctypes.c_double),            # maximum speed of wind (ground speed, but it affects how fast the clouds move, too)
        ("mApplyCloudinessInstantly", ctypes.c_bool),  # preferably we roll the new clouds in, but you can instantly change them now
        ("mUnused1", ctypes.c_bool),
        ("mUnused2", ctypes.c_bool),
        ("mUnused3", ctypes.c_bool),
        ("mExpansion", ctypes.c_ubyte*508),            # future use (humidity, pressure, air density, etc.)
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2MappedBufferVersionBlock(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mVersionUpdateBegin", ctypes.c_uint),  # Incremented right before buffer is written to.
        ("mVersionUpdateEnd", ctypes.c_uint),    # Incremented after buffer write is done.
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2MappedBufferVersionBlockWithSize(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mVersionUpdateBegin", ctypes.c_uint),  # Incremented right before buffer is written to.
        ("mVersionUpdateEnd", ctypes.c_uint),    # Incremented after buffer write is done.
        ("mBytesUpdatedHint", ctypes.c_int),     # How many bytes of the structure were written during the last update.
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2Telemetry(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mVersionUpdateBegin", ctypes.c_uint),  # Incremented right before buffer is written to.
        ("mVersionUpdateEnd", ctypes.c_uint),    # Incremented after buffer write is done.
        ("mBytesUpdatedHint", ctypes.c_int),     # How many bytes of the structure were written during the last update.
        ("mNumVehicles", ctypes.c_int),          # current number of vehicles
        ("mVehicles", rF2VehicleTelemetry*rFactor2Constants.MAX_MAPPED_VEHICLES),
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2Scoring(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mVersionUpdateBegin", ctypes.c_uint),  # Incremented right before buffer is written to.
        ("mVersionUpdateEnd", ctypes.c_uint),    # Incremented after buffer write is done.
        ("mBytesUpdatedHint", ctypes.c_int),     # How many bytes of the structure were written during the last update.
        ("mScoringInfo", rF2ScoringInfo),
        ("mVehicles", rF2VehicleScoring*rFactor2Constants.MAX_MAPPED_VEHICLES),
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2Rules(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mVersionUpdateBegin", ctypes.c_uint),  # Incremented right before buffer is written to.
        ("mVersionUpdateEnd", ctypes.c_uint),    # Incremented after buffer write is done.
        ("mBytesUpdatedHint", ctypes.c_int),     # How many bytes of the structure were written during the last update.
        ("mTrackRules", rF2TrackRules),
        ("mActions", rF2TrackRulesAction*rFactor2Constants.MAX_MAPPED_VEHICLES),
        ("mParticipants", rF2TrackRulesParticipant*rFactor2Constants.MAX_MAPPED_VEHICLES),
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2ForceFeedback(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mVersionUpdateBegin", ctypes.c_uint),  # Incremented right before buffer is written to.
        ("mVersionUpdateEnd", ctypes.c_uint),    # Incremented after buffer write is done.
        ("mForceValue", ctypes.c_double),        # Current FFB value reported via InternalsPlugin::ForceFeedback.
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2GraphicsInfo(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mCamPos", rF2Vec3),                # camera position
        ("mCamOri", rF2Vec3*3),              # rows of orientation matrix (use TelemQuat conversions if desired), also converts local
        ("mHWND", ctypes.c_ubyte*8),         # app handle
        ("mAmbientRed", ctypes.c_double),
        ("mAmbientGreen", ctypes.c_double),
        ("mAmbientBlue", ctypes.c_double),
        ("mID", ctypes.c_int),               # slot ID being viewed (-1 if invalid)
        ("mCameraType", ctypes.c_int),       # see above comments for possible values
        ("mExpansion", ctypes.c_ubyte*128),  # for future use (possibly camera name)
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2Graphics(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mVersionUpdateBegin", ctypes.c_uint),  # Incremented right before buffer is written to.
        ("mVersionUpdateEnd", ctypes.c_uint),    # Incremented after buffer write is done.
        ("mGraphicsInfo", rF2GraphicsInfo),
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2PitInfo(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mVersionUpdateBegin", ctypes.c_uint),  # Incremented right before buffer is written to.
        ("mVersionUpdateEnd", ctypes.c_uint),    # Incremented after buffer write is done.
        ("mPitMenu", rF2PitMenu),
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2Weather(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mVersionUpdateBegin", ctypes.c_uint),  # Incremented right before buffer is written to.
        ("mVersionUpdateEnd", ctypes.c_uint),    # Incremented after buffer write is done.
        ("mTrackNodeSize", ctypes.c_double),
        ("mWeatherInfo", rF2WeatherControlInfo),
    ]


# untranslated [StructLayout(LayoutKind.Sequential, Pack = 4)]
class rF2TrackedDamage(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mMaxImpactMagnitude", ctypes.c_double),          # Max impact magnitude.  Tracked on every telemetry update, and reset on visit to pits or Session restart.
        ("mAccumulatedImpactMagnitude", ctypes.c_double),  # Accumulated impact magnitude.  Tracked on every telemetry update, and reset on visit to pits or Session restart.
    ]


# untranslated [StructLayout(LayoutKind.Sequential, Pack = 4)]
class rF2VehScoringCapture(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mID", ctypes.c_int),             # slot ID (note that it can be re-used in multiplayer after someone leaves)
        ("mPlace", ctypes.c_ubyte),
        ("mIsPlayer", ctypes.c_bool),
        ("mFinishStatus", ctypes.c_byte),  # 0=none, 1=finished, 2=dnf, 3 = dq
    ]


# untranslated [StructLayout(LayoutKind.Sequential, Pack = 4)]
class rF2SessionTransitionCapture(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mGamePhase", ctypes.c_ubyte),
        ("mSession", ctypes.c_int),
        ("mNumScoringVehicles", ctypes.c_int),
        ("mScoringVehicles", rF2VehScoringCapture*rFactor2Constants.MAX_MAPPED_VEHICLES),
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2Extended(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mVersionUpdateBegin", ctypes.c_uint),                             # Incremented right before buffer is written to.
        ("mVersionUpdateEnd", ctypes.c_uint),                               # Incremented after buffer write is done.
        ("mVersion", ctypes.c_char*12),                                     # API version
        ("is64bit", ctypes.c_bool),                                         # Is 64bit plugin?
        ("mPhysics", rF2PhysicsOptions),
        ("mTrackedDamages", rF2TrackedDamage*rFactor2Constants.MAX_MAPPED_IDS),
        ("mInRealtimeFC", ctypes.c_bool),                                   # in realtime as opposed to at the monitor (reported via last EnterRealtime/ExitRealtime calls).
        ("mMultimediaThreadStarted", ctypes.c_bool),                        # multimedia thread started (reported via ThreadStarted/ThreadStopped calls).
        ("mSimulationThreadStarted", ctypes.c_bool),                        # simulation thread started (reported via ThreadStarted/ThreadStopped calls).
        ("mSessionStarted", ctypes.c_bool),                                 # Set to true on Session Started, set to false on Session Ended.
        ("mTicksSessionStarted", ctypes.c_ulonglong),                       # Ticks when session started.
        ("mTicksSessionEnded", ctypes.c_ulonglong),                         # Ticks when session ended.
        ("mSessionTransitionCapture", rF2SessionTransitionCapture),         # Contains partial internals capture at session transition time.
        ("mDisplayedMessageUpdateCapture", ctypes.c_char*128),
        ("mDirectMemoryAccessEnabled", ctypes.c_bool),
        ("mTicksStatusMessageUpdated", ctypes.c_ulonglong),                 # Ticks when status message was updated;
        ("mStatusMessage", ctypes.c_char*rFactor2Constants.MAX_STATUS_MSG_LEN),
        ("mTicksLastHistoryMessageUpdated", ctypes.c_ulonglong),            # Ticks when last message history message was updated;
        ("mLastHistoryMessage", ctypes.c_char*rFactor2Constants.MAX_STATUS_MSG_LEN),
        ("mCurrentPitSpeedLimit", ctypes.c_float),                          # speed limit m/s.
        ("mSCRPluginEnabled", ctypes.c_bool),                               # Is Stock Car Rules plugin enabled?
        ("mSCRPluginDoubleFileType", ctypes.c_int),                         # Stock Car Rules plugin DoubleFileType value, only meaningful if mSCRPluginEnabled is true.
        ("mTicksLSIPhaseMessageUpdated", ctypes.c_ulonglong),               # Ticks when last LSI phase message was updated.
        ("mLSIPhaseMessage", ctypes.c_char*rFactor2Constants.MAX_RULES_INSTRUCTION_MSG_LEN),
        ("mTicksLSIPitStateMessageUpdated", ctypes.c_ulonglong),            # Ticks when last LSI pit state message was updated.
        ("mLSIPitStateMessage", ctypes.c_char*rFactor2Constants.MAX_RULES_INSTRUCTION_MSG_LEN),
        ("mTicksLSIOrderInstructionMessageUpdated", ctypes.c_ulonglong),    # Ticks when last LSI order instruction message was updated.
        ("mLSIOrderInstructionMessage", ctypes.c_char*rFactor2Constants.MAX_RULES_INSTRUCTION_MSG_LEN),
        ("mTicksLSIRulesInstructionMessageUpdated", ctypes.c_ulonglong),    # Ticks when last FCY rules message was updated.  Currently, only SCR plugin sets that.
        ("mLSIRulesInstructionMessage", ctypes.c_char*rFactor2Constants.MAX_RULES_INSTRUCTION_MSG_LEN),
        ("mUnsubscribedBuffersMask", ctypes.c_int),                         # Currently active UnsbscribedBuffersMask value.  This will be allowed for clients to write to in the future, but not yet.
        ("mHWControlInputEnabled", ctypes.c_bool),                          # HWControl input buffer is enabled.
        ("mWeatherControlInputEnabled", ctypes.c_bool),                     # WeatherControl input buffer is enabled.
        ("mRulesControlInputEnabled", ctypes.c_bool),                       # RulesControl input buffer is enabled.
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2HWControl(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mVersionUpdateBegin", ctypes.c_uint),  # Incremented right before buffer is written to.
        ("mVersionUpdateEnd", ctypes.c_uint),    # Incremented after buffer write is done.
        ("mLayoutVersion", ctypes.c_int),
        ("mControlName", ctypes.c_char*rFactor2Constants.MAX_HWCONTROL_NAME_LEN),
        ("mfRetVal", ctypes.c_double),
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2WeatherControl(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mVersionUpdateBegin", ctypes.c_uint),  # Incremented right before buffer is written to.
        ("mVersionUpdateEnd", ctypes.c_uint),    # Incremented after buffer write is done.
        ("mLayoutVersion", ctypes.c_int),
        ("mWeatherInfo", rF2WeatherControlInfo),
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2RulesControl(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mVersionUpdateBegin", ctypes.c_uint),  # Incremented right before buffer is written to.
        ("mVersionUpdateEnd", ctypes.c_uint),    # Incremented after buffer write is done.
        ("mLayoutVersion", ctypes.c_int),
        ("mTrackRules", rF2TrackRules),
        ("mActions", rF2TrackRulesAction*rFactor2Constants.MAX_MAPPED_VEHICLES),
        ("mParticipants", rF2TrackRulesParticipant*rFactor2Constants.MAX_MAPPED_VEHICLES),
    ]


# untranslated [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi, Pack = 4)]
class rF2PluginControl(ctypes.Structure):
    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mVersionUpdateBegin", ctypes.c_uint),  # Incremented right before buffer is written to.
        ("mVersionUpdateEnd", ctypes.c_uint),    # Incremented after buffer write is done.
        ("mLayoutVersion", ctypes.c_int),
        ("mRequestEnableBuffersMask", ctypes.c_int),
        ("mRequestHWControlInput", ctypes.c_ubyte),
        ("mRequestWeatherControlInput", ctypes.c_ubyte),
        ("mRequestRulesControlInput", ctypes.c_ubyte),
    ]


class SimInfo:
    """Simulation info from shared memory"""

    def __init__(self):
        self._rf2_tele = mmap.mmap(
            fileno=0,
            length=ctypes.sizeof(rF2Telemetry),
            tagname=rFactor2Constants.MM_TELEMETRY_FILE_NAME,
        )
        self.Rf2Tele = rF2Telemetry.from_buffer(self._rf2_tele)

        self._rf2_scor = mmap.mmap(
            fileno=0,
            length=ctypes.sizeof(rF2Scoring),
            tagname=rFactor2Constants.MM_SCORING_FILE_NAME,
        )
        self.Rf2Scor = rF2Scoring.from_buffer(self._rf2_scor)

        self._rf2_ext = mmap.mmap(
            fileno=0,
            length=ctypes.sizeof(rF2Extended),
            tagname=rFactor2Constants.MM_EXTENDED_FILE_NAME,
        )
        self.Rf2Ext = rF2Extended.from_buffer(self._rf2_ext)

    def close(self):
        """Close memory map"""
        self.Rf2Tele = None
        self.Rf2Scor = None
        self.Rf2Ext = None
        try:  # this did not help with the errors
            self._rf2_tele.close()
            self._rf2_scor.close()
            self._rf2_ext.close()
        except BufferError as e:
            print("Error:", e)

    def __del__(self):
        self.close()


def test():
    """Example usage"""
    info = SimInfo()

    scor_data = info.Rf2Scor
    tele_data = info.Rf2Tele
    ext_data = info.Rf2Ext

    selected_player_index = 0

    player_scor_data = scor_data.mVehicles[selected_player_index]
    player_tele_data = tele_data.mVehicles[selected_player_index]

    print("-"*40)
    print("Plugin info:")
    print("Version:", bytes(ext_data.mVersion).decode().rstrip())
    print("Unsubscribed buffers:", SubscribedBuffer(ext_data.mUnsubscribedBuffersMask))

    print("-"*40)
    print("Scoring info:")
    print("Track name:", scor_data.mScoringInfo.mTrackName)
    print("Local player name:", scor_data.mScoringInfo.mPlayerName)
    print("Setting name:", scor_data.mScoringInfo.mPlrFileName)
    print("Total vehicles:", scor_data.mScoringInfo.mNumVehicles)

    print("-"*40)
    print("Selected Player scoring info:")
    print("Slot ID:", player_scor_data.mID)
    print("Driver name:", player_scor_data.mDriverName)
    print("VEH file:", player_scor_data.mVehFilename)
    print("Is local player:", player_scor_data.mIsPlayer)
    print("SteamID:", player_scor_data.mSteamID)
    print("FuelFraction:", player_scor_data.mFuelFraction)


    print("-"*40)
    print("Selected player telemetry info:")
    print("Slot ID:", player_tele_data.mID)
    print("Gear:", player_tele_data.mGear)
    print("Throttle:", player_tele_data.mUnfilteredThrottle)
    print("Brake:", player_tele_data.mUnfilteredBrake)
    print("Clutch:", player_tele_data.mUnfilteredClutch)
    print("Virtual Energy:", player_tele_data.mVirtualEnergy)
    print("Regen:", player_tele_data.mRegen)
    print("State of Charge?:", player_tele_data.mSoC)
    print("Vehicle Model:", player_tele_data.mVehicleModel)

    player_scor_data = None
    player_tele_data = None
    scor_data = None
    tele_data = None
    ext_data = None


if __name__ == "__main__":
    test()
