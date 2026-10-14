"""
Python mapping of The Iron Wolf's rF2 Shared Memory Plugin interface for rFactor 2

This library is based on:
- rFactor 2 InternalsPlugin header file by S397.
- The Iron Wolf's rF2 Shared Memory Plugin: https://github.com/TheIronWolfModding/rF2SharedMemoryMapPlugin

Type hints & annotation:
- Annotate "ctypes type" as "Python type" according to table from:
  https://docs.python.org/3/library/ctypes.html#fundamental-data-types
- Annotate array object as list[type].
"""

from __future__ import annotations

import ctypes
import mmap

from ._common import _t, typedstruct


# Constants
class rFactor2Constants:
    """rFactor 2 constants"""

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
    INVALID_CAR_INDEX: int = -1

    RFACTOR2_PROCESS_NAME: str = "rFactor2"
    RFACTOR2_DEVMODE_PROCESS_NAME: str = "rFactor2 Mod Mode"
    RFACTOR2_DEDICATED_PROCESS_NAME: str = "rFactor2 Dedicated"


# InternalsPlugin & rF2data
@typedstruct(pack=4)
class rF2Vec3(ctypes.Structure):
    """Mapping of 'TelemVect3' from InternalsPlugin.hpp"""

    __slots__ = ()

    x: float = _t(ctypes.c_double)
    y: float = _t(ctypes.c_double)
    z: float = _t(ctypes.c_double)


@typedstruct(pack=4)
class rF2Wheel(ctypes.Structure):
    """Mapping of 'TelemWheelV01' from InternalsPlugin.hpp

    Attributes:
        mSuspensionDeflection: meters
        mRideHeight: meters
        mSuspForce: pushrod load in Newtons
        mBrakeTemp: Celsius
        mBrakePressure: currently 0.0-1.0, depending on driver input and brake balance; will convert to true brake pressure (kPa) in future
        mRotation: radians/sec
        mLateralPatchVel: lateral velocity at contact patch
        mLongitudinalPatchVel: longitudinal velocity at contact patch
        mLateralGroundVel: lateral velocity at contact patch
        mLongitudinalGroundVel: longitudinal velocity at contact patch
        mCamber: radians (positive is left for left-side wheels, right for right-side wheels)
        mLateralForce: Newtons
        mLongitudinalForce: Newtons
        mTireLoad: Newtons
        mGripFract: an approximation of what fraction of the contact patch is sliding
        mPressure: kPa (tire pressure)
        mTemperature: Kelvin (subtract 273.15 to get Celsius) left/center/right (not to be confused with inside/center/outside!)
        mWear: wear (0.0-1.0, fraction of maximum) ... this is not necessarily proportional with grip loss
        mTerrainName: the material prefixes from the TDF file
        mSurfaceType: 0=dry, 1=wet, 2=grass, 3=dirt, 4=gravel, 5=rumblestrip, 6 = special
        mFlat: whether tire is flat
        mDetached: whether wheel is detached
        mStaticUndeflectedRadius: tire radius in centimeters
        mVerticalTireDeflection: how much is tire deflected from its (speed-sensitive) radius
        mWheelYLocation: wheel's y location relative to vehicle y location
        mToe: current toe angle w.r.t. the vehicle
        mTireCarcassTemperature: rough average of temperature samples from carcass (Kelvin)
        mTireInnerLayerTemperature: rough average of temperature samples from innermost layer of rubber (before carcass) (Kelvin)
        mExpansion: for future use
    """

    __slots__ = ()

    mSuspensionDeflection: float = _t(ctypes.c_double)
    mRideHeight: float = _t(ctypes.c_double)
    mSuspForce: float = _t(ctypes.c_double)
    mBrakeTemp: float = _t(ctypes.c_double)
    mBrakePressure: float = _t(ctypes.c_double)
    mRotation: float = _t(ctypes.c_double)
    mLateralPatchVel: float = _t(ctypes.c_double)
    mLongitudinalPatchVel: float = _t(ctypes.c_double)
    mLateralGroundVel: float = _t(ctypes.c_double)
    mLongitudinalGroundVel: float = _t(ctypes.c_double)
    mCamber: float = _t(ctypes.c_double)
    mLateralForce: float = _t(ctypes.c_double)
    mLongitudinalForce: float = _t(ctypes.c_double)
    mTireLoad: float = _t(ctypes.c_double)
    mGripFract: float = _t(ctypes.c_double)
    mPressure: float = _t(ctypes.c_double)
    mTemperature: list[float] = _t(ctypes.c_double * 3)
    mWear: float = _t(ctypes.c_double)
    mTerrainName: bytes = _t(ctypes.c_char * 16)
    mSurfaceType: int = _t(ctypes.c_ubyte)
    mFlat: bool = _t(ctypes.c_bool)
    mDetached: bool = _t(ctypes.c_bool)
    mStaticUndeflectedRadius: int = _t(ctypes.c_ubyte)
    mVerticalTireDeflection: float = _t(ctypes.c_double)
    mWheelYLocation: float = _t(ctypes.c_double)
    mToe: float = _t(ctypes.c_double)
    mTireCarcassTemperature: float = _t(ctypes.c_double)
    mTireInnerLayerTemperature: list[float] = _t(ctypes.c_double * 3)
    mExpansion: list[int] = _t(ctypes.c_ubyte * 24)


@typedstruct(pack=4)
class rF2VehicleTelemetry(ctypes.Structure):
    """Mapping of 'TelemInfoV01' from InternalsPlugin.hpp

    Attributes:
        mID: slot ID (note that it can be re-used in multiplayer after someone leaves)
        mDeltaTime: time since last update (seconds)
        mElapsedTime: game session time
        mLapNumber: current lap number
        mLapStartET: time this lap was started
        mVehicleName: current vehicle name
        mTrackName: current track name
        mPos: world position in meters
        mLocalVel: velocity (meters/sec) in local vehicle coordinates
        mLocalAccel: acceleration (meters/sec^2) in local vehicle coordinates
        mOri: rows of orientation matrix (use TelemQuat conversions if desired) also converts local
        mLocalRot: rotation (radians/sec) in local vehicle coordinates
        mLocalRotAccel: rotational acceleration (radians/sec^2) in local vehicle coordinates
        mGear: -1=reverse, 0=neutral, 1+ = forward gears
        mEngineRPM: engine RPM
        mEngineWaterTemp: Celsius
        mEngineOilTemp: Celsius
        mClutchRPM: clutch RPM
        mUnfilteredThrottle: ranges  0.0-1.0
        mUnfilteredBrake: ranges  0.0-1.0
        mUnfilteredSteering: ranges -1.0-1.0 (left to right)
        mUnfilteredClutch: ranges  0.0-1.0
        mFilteredThrottle: ranges  0.0-1.0
        mFilteredBrake: ranges  0.0-1.0
        mFilteredSteering: ranges -1.0-1.0 (left to right)
        mFilteredClutch: ranges  0.0-1.0
        mSteeringShaftTorque: torque around steering shaft (used to be mSteeringArmForce, but that is not necessarily accurate for feedback purposes)
        mFront3rdDeflection: deflection at front 3rd spring
        mRear3rdDeflection: deflection at rear 3rd spring
        mFrontWingHeight: front wing height
        mFrontRideHeight: front ride height
        mRearRideHeight: rear ride height
        mDrag: drag
        mFrontDownforce: front downforce
        mRearDownforce: rear downforce
        mFuel: amount of fuel (liters)
        mEngineMaxRPM: rev limit
        mScheduledStops: number of scheduled pitstops
        mOverheating: whether overheating icon is shown
        mDetached: whether any parts (besides wheels) have been detached
        mHeadlights: whether headlights are on
        mDentSeverity: dent severity at 8 locations around the car (0=none, 1=some, 2=more)
        mLastImpactET: time of last impact
        mLastImpactMagnitude: magnitude of last impact
        mLastImpactPos: location of last impact
        mEngineTorque: current engine torque (including additive torque) (used to be mEngineTq, but there's little reason to abbreviate it)
        mCurrentSector: the current sector (zero-based) with the pitlane stored in the sign bit (example: entering pits from third sector gives 0x80000002)
        mSpeedLimiter: whether speed limiter is on
        mMaxGears: maximum forward gears
        mFrontTireCompoundIndex: index within brand
        mRearTireCompoundIndex: index within brand
        mFuelCapacity: capacity in liters
        mFrontFlapActivated: whether front flap is activated
        mRearFlapActivated: whether rear flap is activated
        mRearFlapLegalStatus: 0=disallowed, 1=criteria detected but not allowed quite yet, 2 = allowed
        mIgnitionStarter: 0=off 1=ignition 2 = ignition+starter
        mFrontTireCompoundName: name of front tire compound
        mRearTireCompoundName: name of rear tire compound
        mSpeedLimiterAvailable: whether speed limiter is available
        mAntiStallActivated: whether (hard) anti-stall is activated
        mUnused: unused
        mVisualSteeringWheelRange: the *visual* steering wheel range
        mRearBrakeBias: fraction of brakes on rear
        mTurboBoostPressure: current turbo boost pressure if available
        mPhysicsToGraphicsOffset: offset from static CG to graphical center
        mPhysicalSteeringWheelRange: the *physical* steering wheel range
        mDeltaBest: (omitted in error by S397)
        mBatteryChargeFraction: Battery charge as fraction [0.0-1.0]
        mElectricBoostMotorTorque: current torque of boost motor (can be negative when in regenerating mode)
        mElectricBoostMotorRPM: current rpm of boost motor
        mElectricBoostMotorTemperature: current temperature of boost motor
        mElectricBoostWaterTemperature: current water temperature of boost motor cooler if present (0 otherwise)
        mElectricBoostMotorState: 0=unavailable 1=inactive, 2=propulsion, 3=regeneration
        mExpansion: for future use (note that the slot ID has been moved to mID above)
        mWheels: wheel info (front left, front right, rear left, rear right)
    """

    __slots__ = ()

    mID: int = _t(ctypes.c_int)
    mDeltaTime: float = _t(ctypes.c_double)
    mElapsedTime: float = _t(ctypes.c_double)
    mLapNumber: int = _t(ctypes.c_int)
    mLapStartET: float = _t(ctypes.c_double)
    mVehicleName: bytes = _t(ctypes.c_char * 64)
    mTrackName: bytes = _t(ctypes.c_char * 64)
    mPos: rF2Vec3 = _t(rF2Vec3)
    mLocalVel: rF2Vec3 = _t(rF2Vec3)
    mLocalAccel: rF2Vec3 = _t(rF2Vec3)
    mOri: list[rF2Vec3] = _t(rF2Vec3 * 3)
    mLocalRot: rF2Vec3 = _t(rF2Vec3)
    mLocalRotAccel: rF2Vec3 = _t(rF2Vec3)
    mGear: int = _t(ctypes.c_int)
    mEngineRPM: float = _t(ctypes.c_double)
    mEngineWaterTemp: float = _t(ctypes.c_double)
    mEngineOilTemp: float = _t(ctypes.c_double)
    mClutchRPM: float = _t(ctypes.c_double)
    mUnfilteredThrottle: float = _t(ctypes.c_double)
    mUnfilteredBrake: float = _t(ctypes.c_double)
    mUnfilteredSteering: float = _t(ctypes.c_double)
    mUnfilteredClutch: float = _t(ctypes.c_double)
    mFilteredThrottle: float = _t(ctypes.c_double)
    mFilteredBrake: float = _t(ctypes.c_double)
    mFilteredSteering: float = _t(ctypes.c_double)
    mFilteredClutch: float = _t(ctypes.c_double)
    mSteeringShaftTorque: float = _t(ctypes.c_double)
    mFront3rdDeflection: float = _t(ctypes.c_double)
    mRear3rdDeflection: float = _t(ctypes.c_double)
    mFrontWingHeight: float = _t(ctypes.c_double)
    mFrontRideHeight: float = _t(ctypes.c_double)
    mRearRideHeight: float = _t(ctypes.c_double)
    mDrag: float = _t(ctypes.c_double)
    mFrontDownforce: float = _t(ctypes.c_double)
    mRearDownforce: float = _t(ctypes.c_double)
    mFuel: float = _t(ctypes.c_double)
    mEngineMaxRPM: float = _t(ctypes.c_double)
    mScheduledStops: int = _t(ctypes.c_ubyte)
    mOverheating: bool = _t(ctypes.c_bool)
    mDetached: bool = _t(ctypes.c_bool)
    mHeadlights: bool = _t(ctypes.c_bool)
    mDentSeverity: list[int] = _t(ctypes.c_ubyte * 8)
    mLastImpactET: float = _t(ctypes.c_double)
    mLastImpactMagnitude: float = _t(ctypes.c_double)
    mLastImpactPos: rF2Vec3 = _t(rF2Vec3)
    mEngineTorque: float = _t(ctypes.c_double)
    mCurrentSector: int = _t(ctypes.c_int)
    mSpeedLimiter: int = _t(ctypes.c_ubyte)
    mMaxGears: int = _t(ctypes.c_ubyte)
    mFrontTireCompoundIndex: int = _t(ctypes.c_ubyte)
    mRearTireCompoundIndex: int = _t(ctypes.c_ubyte)
    mFuelCapacity: float = _t(ctypes.c_double)
    mFrontFlapActivated: int = _t(ctypes.c_ubyte)
    mRearFlapActivated: int = _t(ctypes.c_ubyte)
    mRearFlapLegalStatus: int = _t(ctypes.c_ubyte)
    mIgnitionStarter: int = _t(ctypes.c_ubyte)
    mFrontTireCompoundName: bytes = _t(ctypes.c_char * 18)
    mRearTireCompoundName: bytes = _t(ctypes.c_char * 18)
    mSpeedLimiterAvailable: int = _t(ctypes.c_ubyte)
    mAntiStallActivated: int = _t(ctypes.c_ubyte)
    mUnused: list[int] = _t(ctypes.c_ubyte * 2)
    mVisualSteeringWheelRange: float = _t(ctypes.c_float)
    mRearBrakeBias: float = _t(ctypes.c_double)
    mTurboBoostPressure: float = _t(ctypes.c_double)
    mPhysicsToGraphicsOffset: list[float] = _t(ctypes.c_float * 3)
    mPhysicalSteeringWheelRange: float = _t(ctypes.c_float)
    mDeltaBest: float = _t(ctypes.c_double)
    mBatteryChargeFraction: float = _t(ctypes.c_double)
    mElectricBoostMotorTorque: float = _t(ctypes.c_double)
    mElectricBoostMotorRPM: float = _t(ctypes.c_double)
    mElectricBoostMotorTemperature: float = _t(ctypes.c_double)
    mElectricBoostWaterTemperature: float = _t(ctypes.c_double)
    mElectricBoostMotorState: int = _t(ctypes.c_ubyte)
    mExpansion: list[int] = _t(ctypes.c_ubyte * 103)
    mWheels: list[rF2Wheel] = _t(rF2Wheel * 4)


@typedstruct(pack=4)
class rF2ScoringInfo(ctypes.Structure):
    """Mapping of 'ScoringInfoV01' from InternalsPlugin.hpp

    Attributes:
        mTrackName: current track name
        mSession: current session (0=testday 1-4=practice 5-8=qual 9=warmup 10-13 = race)
        mCurrentET: current time
        mEndET: ending time
        mMaxLaps: maximum laps
        mLapDist: distance around track
        mResultsStreamPointer: results stream pointer
        mNumVehicles: current number of vehicles
        mGamePhase: Game phases:
            - 0 Before session has begun
            - 1 Reconnaissance laps (race only)
            - 2 Grid walk-through (race only)
            - 3 Formation lap (race only)
            - 4 Starting-light countdown has begun (race only)
            - 5 Green flag
            - 6 Full course yellow / safety car
            - 7 Session stopped
            - 8 Session over
            - 9 Paused (tag.2015.09.14 - this is new, and indicates that this is a heartbeat call to the plugin)
        mYellowFlagState: Yellow flag states (applies to full-course only)
            - -1 Invalid
            - 0 None
            - 1 Pending
            - 2 Pits closed
            - 3 Pit lead lap
            - 4 Pits open
            - 5 Last lap
            - 6 Resume
            - 7 Race halt (not currently used)
        mSectorFlag: whether there are any local yellows at the moment in each sector (not sure if sector 0 is first or last, so test)
        mStartLight: start light frame (number depends on track)
        mNumRedLights: number of red lights in start sequence
        mInRealtime: in realtime as opposed to at the monitor
        mPlayerName: player name (including possible multiplayer override)
        mPlrFileName: may be encoded to be a legal filename
        mDarkCloud: cloud darkness? 0.0-1.0
        mRaining: raining severity 0.0-1.0
        mAmbientTemp: temperature (Celsius)
        mTrackTemp: temperature (Celsius)
        mWind: wind speed
        mMinPathWetness: minimum wetness on main path 0.0-1.0
        mMaxPathWetness: maximum wetness on main path 0.0-1.0
        mGameMode: 1 = server, 2 = client, 3 = server and client
        mIsPasswordProtected: is the server password protected
        mServerPort: the port of the server (if on a server)
        mServerPublicIP: the public IP address of the server (if on a server)
        mMaxPlayers: maximum number of vehicles that can be in the session
        mServerName: name of the server
        mStartET: start time (seconds since midnight) of the event
        mAvgPathWetness: average wetness on main path 0.0-1.0
        mExpansion: for future use
        mVehiclePointer: vehicle pointer
    """

    __slots__ = ()

    mTrackName: bytes = _t(ctypes.c_char * 64)
    mSession: int = _t(ctypes.c_int)
    mCurrentET: float = _t(ctypes.c_double)
    mEndET: float = _t(ctypes.c_double)
    mMaxLaps: int = _t(ctypes.c_int)
    mLapDist: float = _t(ctypes.c_double)
    mResultsStreamPointer: list[int] = _t(ctypes.c_ubyte * 8)
    mNumVehicles: int = _t(ctypes.c_int)
    mGamePhase: int = _t(ctypes.c_ubyte)
    mYellowFlagState: int = _t(ctypes.c_char)
    mSectorFlag: list[int] = _t(ctypes.c_ubyte * 3)
    mStartLight: int = _t(ctypes.c_ubyte)
    mNumRedLights: int = _t(ctypes.c_ubyte)
    mInRealtime: bool = _t(ctypes.c_bool)
    mPlayerName: bytes = _t(ctypes.c_char * 32)
    mPlrFileName: bytes = _t(ctypes.c_char * 64)
    mDarkCloud: float = _t(ctypes.c_double)
    mRaining: float = _t(ctypes.c_double)
    mAmbientTemp: float = _t(ctypes.c_double)
    mTrackTemp: float = _t(ctypes.c_double)
    mWind: rF2Vec3 = _t(rF2Vec3)
    mMinPathWetness: float = _t(ctypes.c_double)
    mMaxPathWetness: float = _t(ctypes.c_double)
    mGameMode: int = _t(ctypes.c_ubyte)
    mIsPasswordProtected: bool = _t(ctypes.c_bool)
    mServerPort: int = _t(ctypes.c_ushort)
    mServerPublicIP: int = _t(ctypes.c_uint)
    mMaxPlayers: int = _t(ctypes.c_int)
    mServerName: bytes = _t(ctypes.c_char * 32)
    mStartET: float = _t(ctypes.c_float)
    mAvgPathWetness: float = _t(ctypes.c_double)
    mExpansion: list[int] = _t(ctypes.c_ubyte * 200)
    mVehiclePointer: list[int] = _t(ctypes.c_ubyte * 8)


@typedstruct(pack=4)
class rF2VehicleScoring(ctypes.Structure):
    """Mapping of 'VehicleScoringInfoV01' from InternalsPlugin.hpp

    Attributes:
        mID: slot ID (note that it can be re-used in multiplayer after someone leaves)
        mDriverName: driver name
        mVehicleName: vehicle name
        mTotalLaps: laps completed
        mSector: 0=sector3, 1=sector1, 2 = sector2 (don't ask why)
        mFinishStatus: 0=none, 1=finished, 2=dnf, 3 = dq
        mLapDist: current distance around track
        mPathLateral: lateral position with respect to *very approximate* "center" path
        mTrackEdge: track edge (w.r.t. "center" path) on same side of track as vehicle
        mBestSector1: best sector 1
        mBestSector2: best sector 2 (plus sector 1)
        mBestLapTime: best lap time
        mLastSector1: last sector 1
        mLastSector2: last sector 2 (plus sector 1)
        mLastLapTime: last lap time
        mCurSector1: current sector 1 if valid
        mCurSector2: current sector 2 (plus sector 1) if valid
        mNumPitstops: number of pitstops made
        mNumPenalties: number of outstanding penalties
        mIsPlayer: is this the player's vehicle
        mControl: who's in control: -1=nobody (shouldn't get this) 0=local player, 1=local AI, 2=remote, 3 = replay (shouldn't get this)
        mInPits: between pit entrance and pit exit (not always accurate for remote vehicles)
        mPlace: 1-based position
        mVehicleClass: vehicle class
        mTimeBehindNext: time behind vehicle in next higher place
        mLapsBehindNext: laps behind vehicle in next higher place
        mTimeBehindLeader: time behind leader
        mLapsBehindLeader: laps behind leader
        mLapStartET: time this lap was started
        mPos: world position in meters
        mLocalVel: velocity (meters/sec) in local vehicle coordinates
        mLocalAccel: acceleration (meters/sec^2) in local vehicle coordinates
        mOri: rows of orientation matrix (use TelemQuat conversions if desired) also converts local
        mLocalRot: rotation (radians/sec) in local vehicle coordinates
        mLocalRotAccel: rotational acceleration (radians/sec^2) in local vehicle coordinates
        mHeadlights: status of headlights
        mPitState: 0=none, 1=request, 2=entering, 3=stopped, 4 = exiting
        mServerScored: whether this vehicle is being scored by server (could be off in qualifying or racing heats)
        mIndividualPhase: game phases (described below) plus 9=after formation, 10=under yellow, 11 = under blue (not used)
        mQualification: 1-based, can be -1 when invalid
        mTimeIntoLap: estimated time into lap
        mEstimatedLapTime: estimated laptime used for "time behind" and "time into lap" (note: this may changed based on vehicle and setup!?)
        mPitGroup: pit group (same as team name unless pit is shared)
        mFlag: primary flag being shown to vehicle (currently only 0=green or 6 = blue)
        mUnderYellow: whether this car has taken a full-course caution flag at the start/finish line
        mCountLapFlag: 0 = do not count lap or time, 1 = count lap but not time, 2 = count lap and time
        mInGarageStall: appears to be within the correct garage stall
        mUpgradePack: Coded upgrades
        mPitLapDist: location of pit in terms of lap distance
        mBestLapSector1: sector 1 time from best lap (not necessarily the best sector 1 time)
        mBestLapSector2: sector 2 time from best lap (not necessarily the best sector 2 time)
        mSteamID: SteamID of the current driver (if any)
        mVehFilename: filename of veh file used to identify this vehicle.
        mAttackMode: FE attack mode state
        mFuelFraction: Percentage of fuel or battery left in vehicle. 0x00 = 0%; 0xFF = 100%
        mDRSState: DRS (RearFlap) state
        mExpansion: for future use
    """

    __slots__ = ()

    mID: int = _t(ctypes.c_int)
    mDriverName: bytes = _t(ctypes.c_char * 32)
    mVehicleName: bytes = _t(ctypes.c_char * 64)
    mTotalLaps: int = _t(ctypes.c_short)
    mSector: int = _t(ctypes.c_byte)
    mFinishStatus: int = _t(ctypes.c_byte)
    mLapDist: float = _t(ctypes.c_double)
    mPathLateral: float = _t(ctypes.c_double)
    mTrackEdge: float = _t(ctypes.c_double)
    mBestSector1: float = _t(ctypes.c_double)
    mBestSector2: float = _t(ctypes.c_double)
    mBestLapTime: float = _t(ctypes.c_double)
    mLastSector1: float = _t(ctypes.c_double)
    mLastSector2: float = _t(ctypes.c_double)
    mLastLapTime: float = _t(ctypes.c_double)
    mCurSector1: float = _t(ctypes.c_double)
    mCurSector2: float = _t(ctypes.c_double)
    mNumPitstops: int = _t(ctypes.c_short)
    mNumPenalties: int = _t(ctypes.c_short)
    mIsPlayer: bool = _t(ctypes.c_bool)
    mControl: int = _t(ctypes.c_byte)
    mInPits: bool = _t(ctypes.c_bool)
    mPlace: int = _t(ctypes.c_ubyte)
    mVehicleClass: bytes = _t(ctypes.c_char * 32)
    mTimeBehindNext: float = _t(ctypes.c_double)
    mLapsBehindNext: int = _t(ctypes.c_int)
    mTimeBehindLeader: float = _t(ctypes.c_double)
    mLapsBehindLeader: int = _t(ctypes.c_int)
    mLapStartET: float = _t(ctypes.c_double)
    mPos: rF2Vec3 = _t(rF2Vec3)
    mLocalVel: rF2Vec3 = _t(rF2Vec3)
    mLocalAccel: rF2Vec3 = _t(rF2Vec3)
    mOri: list[rF2Vec3] = _t(rF2Vec3 * 3)
    mLocalRot: rF2Vec3 = _t(rF2Vec3)
    mLocalRotAccel: rF2Vec3 = _t(rF2Vec3)
    mHeadlights: int = _t(ctypes.c_ubyte)
    mPitState: int = _t(ctypes.c_ubyte)
    mServerScored: int = _t(ctypes.c_ubyte)
    mIndividualPhase: int = _t(ctypes.c_ubyte)
    mQualification: int = _t(ctypes.c_int)
    mTimeIntoLap: float = _t(ctypes.c_double)
    mEstimatedLapTime: float = _t(ctypes.c_double)
    mPitGroup: bytes = _t(ctypes.c_char * 24)
    mFlag: int = _t(ctypes.c_ubyte)
    mUnderYellow: bool = _t(ctypes.c_bool)
    mCountLapFlag: int = _t(ctypes.c_ubyte)
    mInGarageStall: bool = _t(ctypes.c_bool)
    mUpgradePack: list[int] = _t(ctypes.c_ubyte * 16)
    mPitLapDist: float = _t(ctypes.c_float)
    mBestLapSector1: float = _t(ctypes.c_float)
    mBestLapSector2: float = _t(ctypes.c_float)
    mSteamID: int = _t(ctypes.c_ulonglong)
    mVehFilename: bytes = _t(ctypes.c_char * 32)
    mAttackMode: int = _t(ctypes.c_short)
    mFuelFraction: int = _t(ctypes.c_ubyte)
    mDRSState: bool = _t(ctypes.c_bool)
    mExpansion: list[int] = _t(ctypes.c_ubyte * 4)


@typedstruct(pack=4)
class rF2PhysicsOptions(ctypes.Structure):
    """Mapping of 'PhysicsOptionsV01' from InternalsPlugin.hpp

    Attributes:
        mTractionControl: 0 (off) - 3 (high)
        mAntiLockBrakes: 0 (off) - 2 (high)
        mStabilityControl: 0 (off) - 2 (high)
        mAutoShift: 0 (off) 1 (upshifts) 2 (downshifts) 3 (all)
        mAutoClutch: 0 (off) 1 (on)
        mInvulnerable: 0 (off) 1 (on)
        mOppositeLock: 0 (off) 1 (on)
        mSteeringHelp: 0 (off) - 3 (high)
        mBrakingHelp: 0 (off) - 2 (high)
        mSpinRecovery: 0 (off) 1 (on)
        mAutoPit: 0 (off) 1 (on)
        mAutoLift: 0 (off) 1 (on)
        mAutoBlip: 0 (off) 1 (on)
        mFuelMult: fuel multiplier (0x-7x)
        mTireMult: tire wear multiplier (0x-7x)
        mMechFail: mechanical failure setting; 0 (off) 1 (normal) 2 (timescaled)
        mAllowPitcrewPush: 0 (off) 1 (on)
        mRepeatShifts: accidental repeat shift prevention (0-5; see PLR file)
        mHoldClutch: for auto-shifters at start of race: 0 (off) 1 (on)
        mAutoReverse: 0 (off) 1 (on)
        mAlternateNeutral: Whether shifting up and down simultaneously equals neutral
        mAIControl: Whether player vehicle is currently under AI control
        mUnused1: unused
        mUnused2: unused
        mManualShiftOverrideTime: time before auto-shifting can resume after recent manual shift
        mAutoShiftOverrideTime: time before manual shifting can resume after recent auto shift
        mSpeedSensitiveSteering: 0.0 (off) - 1.0
        mSteerRatioSpeed: speed (m/s) under which lock gets expanded to full
    """

    __slots__ = ()

    mTractionControl: int = _t(ctypes.c_ubyte)
    mAntiLockBrakes: int = _t(ctypes.c_ubyte)
    mStabilityControl: int = _t(ctypes.c_ubyte)
    mAutoShift: int = _t(ctypes.c_ubyte)
    mAutoClutch: int = _t(ctypes.c_ubyte)
    mInvulnerable: int = _t(ctypes.c_ubyte)
    mOppositeLock: int = _t(ctypes.c_ubyte)
    mSteeringHelp: int = _t(ctypes.c_ubyte)
    mBrakingHelp: int = _t(ctypes.c_ubyte)
    mSpinRecovery: int = _t(ctypes.c_ubyte)
    mAutoPit: int = _t(ctypes.c_ubyte)
    mAutoLift: int = _t(ctypes.c_ubyte)
    mAutoBlip: int = _t(ctypes.c_ubyte)
    mFuelMult: int = _t(ctypes.c_ubyte)
    mTireMult: int = _t(ctypes.c_ubyte)
    mMechFail: int = _t(ctypes.c_ubyte)
    mAllowPitcrewPush: int = _t(ctypes.c_ubyte)
    mRepeatShifts: int = _t(ctypes.c_ubyte)
    mHoldClutch: int = _t(ctypes.c_ubyte)
    mAutoReverse: int = _t(ctypes.c_ubyte)
    mAlternateNeutral: int = _t(ctypes.c_ubyte)
    mAIControl: int = _t(ctypes.c_ubyte)
    mUnused1: int = _t(ctypes.c_ubyte)
    mUnused2: int = _t(ctypes.c_ubyte)
    mManualShiftOverrideTime: float = _t(ctypes.c_float)
    mAutoShiftOverrideTime: float = _t(ctypes.c_float)
    mSpeedSensitiveSteering: float = _t(ctypes.c_float)
    mSteerRatioSpeed: float = _t(ctypes.c_float)


@typedstruct(pack=4)
class rF2TrackRulesAction(ctypes.Structure):
    """Mapping of 'TrackRulesActionV01' from InternalsPlugin.hpp

    Attributes:
        mCommand: recommended action
        mID: slot ID if applicable
        mET: elapsed time that event occurred, if applicable
    """

    __slots__ = ()

    mCommand: int = _t(ctypes.c_int)
    mID: int = _t(ctypes.c_int)
    mET: float = _t(ctypes.c_double)


@typedstruct(pack=4)
class rF2TrackRulesParticipant(ctypes.Structure):
    """Mapping of 'TrackRulesParticipantV01' from InternalsPlugin.hpp

    Attributes:
        mID: slot ID
        mFrozenOrder: 0-based place when caution came out (not valid for formation laps)
        mPlace: 1-based place (typically used for the initialization of the formation lap track order)
        mYellowSeverity: a rating of how much this vehicle is contributing to a yellow flag (the sum of all vehicles is compared to TrackRulesV01::mSafetyCarThreshold)
        mCurrentRelativeDistance: equal to ( ( ScoringInfoV01::mLapDist * this->mRelativeLaps ) + VehicleScoringInfoV01::mLapDist )
        mRelativeLaps: current formation/caution laps relative to safety car (should generally be zero except when safety car crosses s/f line); this can be decremented to implement "wave around" or "beneficiary rule" (a.k.a. "lucky dog" or "free pass")
        mColumnAssignment: which column (line/lane) that participant is supposed to be in
        mPositionAssignment: 0-based position within column (line/lane) that participant is supposed to be located at (-1 is invalid)
        mPitsOpen: whether the rules allow this particular vehicle to enter pits right now (input is 2=false or 3=true; if you want to edit it, set to 0=false or 1 = true)
        mUpToSpeed: while in the frozen order, this flag indicates whether the vehicle can be followed (this should be false for somebody who has temporarily spun and hasn't gotten back up to speed yet)
        mUnused: unused
        mGoalRelativeDistance: calculated based on where the leader is, and adjusted by the desired column spacing and the column/position assignments
        mMessage: a message for this participant to explain what is going on it will get run through translator on client machines
        mExpansion: for future use
    """

    __slots__ = ()

    mID: int = _t(ctypes.c_int)
    mFrozenOrder: int = _t(ctypes.c_short)
    mPlace: int = _t(ctypes.c_short)
    mYellowSeverity: float = _t(ctypes.c_float)
    mCurrentRelativeDistance: float = _t(ctypes.c_double)
    mRelativeLaps: int = _t(ctypes.c_int)
    mColumnAssignment: int = _t(ctypes.c_int)
    mPositionAssignment: int = _t(ctypes.c_int)
    mPitsOpen: int = _t(ctypes.c_ubyte)
    mUpToSpeed: bool = _t(ctypes.c_bool)
    mUnused: list[bool] = _t(ctypes.c_bool * 2)
    mGoalRelativeDistance: float = _t(ctypes.c_double)
    mMessage: bytes = _t(ctypes.c_char * 96)
    mExpansion: list[int] = _t(ctypes.c_ubyte * 192)


@typedstruct(pack=4)
class rF2TrackRules(ctypes.Structure):
    """Mapping of 'TrackRulesV01' from InternalsPlugin.hpp

    Attributes:
        mCurrentET: current time
        mStage: current stage
        mPoleColumn: column assignment where pole position seems to be located
        mNumActions: number of recent actions
        mActionPointer: action pointer
        mNumParticipants: number of participants (vehicles)
        mYellowFlagDetected: whether yellow flag was requested or sum of participant mYellowSeverity's exceeds mSafetyCarThreshold
        mYellowFlagLapsWasOverridden: whether mYellowFlagLaps (below) is an admin request (0=no 1=yes 2 = clear yellow)
        mSafetyCarExists: whether safety car even exists
        mSafetyCarActive: whether safety car is active
        mSafetyCarLaps: number of laps
        mSafetyCarThreshold: the threshold at which a safety car is called out (compared to the sum of TrackRulesParticipantV01::mYellowSeverity for each vehicle)
        mSafetyCarLapDist: safety car lap distance
        mSafetyCarLapDistAtStart: where the safety car starts from
        mPitLaneStartDist: where the waypoint branch to the pits breaks off (this may not be perfectly accurate)
        mTeleportLapDist: the front of the teleport locations (a useful first guess as to where to throw the green flag)
        mInputExpansion: input expansion
        mYellowFlagState: see ScoringInfoV01 for values
        mYellowFlagLaps: suggested number of laps to run under yellow (may be passed in with admin command)
        mSafetyCarInstruction: 0=no change, 1=go active, 2 = head for pits
        mSafetyCarSpeed: maximum speed at which to drive
        mSafetyCarMinimumSpacing: minimum spacing behind safety car (-1 to indicate no limit)
        mSafetyCarMaximumSpacing: maximum spacing behind safety car (-1 to indicate no limit)
        mMinimumColumnSpacing: minimum desired spacing between vehicles in a column (-1 to indicate indeterminate/unenforced)
        mMaximumColumnSpacing: maximum desired spacing between vehicles in a column (-1 to indicate indeterminate/unenforced)
        mMinimumSpeed: minimum speed that anybody should be driving (-1 to indicate no limit)
        mMaximumSpeed: maximum speed that anybody should be driving (-1 to indicate no limit)
        mMessage: a message for everybody to explain what is going on (which will get run through translator on client machines)
        mParticipantPointer: participant pointer
        mInputOutputExpansion: input output expansion
    """

    __slots__ = ()

    mCurrentET: float = _t(ctypes.c_double)
    mStage: int = _t(ctypes.c_int)
    mPoleColumn: int = _t(ctypes.c_int)
    mNumActions: int = _t(ctypes.c_int)
    mActionPointer: list[int] = _t(ctypes.c_ubyte * 8)
    mNumParticipants: int = _t(ctypes.c_int)
    mYellowFlagDetected: bool = _t(ctypes.c_bool)
    mYellowFlagLapsWasOverridden: int = _t(ctypes.c_ubyte)
    mSafetyCarExists: bool = _t(ctypes.c_bool)
    mSafetyCarActive: bool = _t(ctypes.c_bool)
    mSafetyCarLaps: int = _t(ctypes.c_int)
    mSafetyCarThreshold: float = _t(ctypes.c_float)
    mSafetyCarLapDist: float = _t(ctypes.c_double)
    mSafetyCarLapDistAtStart: float = _t(ctypes.c_float)
    mPitLaneStartDist: float = _t(ctypes.c_float)
    mTeleportLapDist: float = _t(ctypes.c_float)
    mInputExpansion: list[int] = _t(ctypes.c_ubyte * 256)
    mYellowFlagState: int = _t(ctypes.c_byte)
    mYellowFlagLaps: int = _t(ctypes.c_short)
    mSafetyCarInstruction: int = _t(ctypes.c_int)
    mSafetyCarSpeed: float = _t(ctypes.c_float)
    mSafetyCarMinimumSpacing: float = _t(ctypes.c_float)
    mSafetyCarMaximumSpacing: float = _t(ctypes.c_float)
    mMinimumColumnSpacing: float = _t(ctypes.c_float)
    mMaximumColumnSpacing: float = _t(ctypes.c_float)
    mMinimumSpeed: float = _t(ctypes.c_float)
    mMaximumSpeed: float = _t(ctypes.c_float)
    mMessage: bytes = _t(ctypes.c_char * 96)
    mParticipantPointer: list[int] = _t(ctypes.c_ubyte * 8)
    mInputOutputExpansion: list[int] = _t(ctypes.c_ubyte * 256)


@typedstruct(pack=4)
class rF2PitMenu(ctypes.Structure):
    """Mapping of 'PitMenuV01' from InternalsPlugin.hpp

    Attributes:
        mCategoryIndex: index of the current category
        mCategoryName: name of the current category (untranslated)
        mChoiceIndex: index of the current choice (within the current category)
        mChoiceString: name of the current choice (may have some translated words)
        mNumChoices: total number of choices (0 < = mChoiceIndex < mNumChoices)
        mExpansion: for future use
    """

    __slots__ = ()

    mCategoryIndex: int = _t(ctypes.c_int)
    mCategoryName: bytes = _t(ctypes.c_char * 32)
    mChoiceIndex: int = _t(ctypes.c_int)
    mChoiceString: bytes = _t(ctypes.c_char * 32)
    mNumChoices: int = _t(ctypes.c_int)
    mExpansion: list[int] = _t(ctypes.c_ubyte * 256)


@typedstruct(pack=4)
class rF2WeatherControlInfo(ctypes.Structure):
    """Mapping of 'WeatherControlInfoV01' from InternalsPlugin.hpp

    Attributes:
        mET: when you want this weather to take effect
        mRaining: rain (0.0-1.0) at different nodes
        mCloudiness: general cloudiness (0.0=clear to 1.0 = dark)
        mAmbientTempK: ambient temperature (Kelvin)
        mWindMaxSpeed: maximum speed of wind (ground speed, but it affects how fast the clouds move, too)
        mApplyCloudinessInstantly: preferably we roll the new clouds in, but you can instantly change them now
        mUnused1: unused
        mUnused2: unused
        mUnused3: unused
        mExpansion: future use (humidity, pressure, air density, etc.)
    """

    __slots__ = ()

    mET: float = _t(ctypes.c_double)
    mRaining: list[float] = _t(ctypes.c_double * 9)
    mCloudiness: float = _t(ctypes.c_double)
    mAmbientTempK: float = _t(ctypes.c_double)
    mWindMaxSpeed: float = _t(ctypes.c_double)
    mApplyCloudinessInstantly: bool = _t(ctypes.c_bool)
    mUnused1: bool = _t(ctypes.c_bool)
    mUnused2: bool = _t(ctypes.c_bool)
    mUnused3: bool = _t(ctypes.c_bool)
    mExpansion: list[int] = _t(ctypes.c_ubyte * 508)


@typedstruct(pack=4)
class rF2MappedBufferVersionBlock(ctypes.Structure):
    """Mapping of 'rF2MappedBufferVersionBlock' from rF2Data.cs

    Attributes:
        mVersionUpdateBegin: Incremented right before buffer is written to.
        mVersionUpdateEnd: Incremented after buffer write is done.
    """

    __slots__ = ()

    mVersionUpdateBegin: int = _t(ctypes.c_uint)
    mVersionUpdateEnd: int = _t(ctypes.c_uint)


@typedstruct(pack=4)
class rF2MappedBufferVersionBlockWithSize(ctypes.Structure):
    """Mapping of 'rF2MappedBufferVersionBlockWithSize' from rF2Data.cs

    Attributes:
        mVersionUpdateBegin: Incremented right before buffer is written to.
        mVersionUpdateEnd: Incremented after buffer write is done.
        mBytesUpdatedHint: How many bytes of the structure were written during the last update.
    """

    __slots__ = ()

    mVersionUpdateBegin: int = _t(ctypes.c_uint)
    mVersionUpdateEnd: int = _t(ctypes.c_uint)
    mBytesUpdatedHint: int = _t(ctypes.c_int)


@typedstruct(pack=4)
class rF2Telemetry(ctypes.Structure):
    """Mapping of 'rF2Telemetry' from rF2Data.cs

    Attributes:
        mVersionUpdateBegin: Incremented right before buffer is written to.
        mVersionUpdateEnd: Incremented after buffer write is done.
        mBytesUpdatedHint: How many bytes of the structure were written during the last update.
        mNumVehicles: current number of vehicles
        mVehicles: vehicle telemetry data
    """

    __slots__ = ()

    mVersionUpdateBegin: int = _t(ctypes.c_uint)
    mVersionUpdateEnd: int = _t(ctypes.c_uint)
    mBytesUpdatedHint: int = _t(ctypes.c_int)
    mNumVehicles: int = _t(ctypes.c_int)
    mVehicles: list[rF2VehicleTelemetry] = _t(rF2VehicleTelemetry * rFactor2Constants.MAX_MAPPED_VEHICLES)


@typedstruct(pack=4)
class rF2Scoring(ctypes.Structure):
    """Mapping of 'rF2Scoring' from rF2Data.cs

    Attributes:
        mVersionUpdateBegin: Incremented right before buffer is written to.
        mVersionUpdateEnd: Incremented after buffer write is done.
        mBytesUpdatedHint: How many bytes of the structure were written during the last update.
        mScoringInfo: scoring info
        mVehicles: vehicle scoring data
    """

    __slots__ = ()

    mVersionUpdateBegin: int = _t(ctypes.c_uint)
    mVersionUpdateEnd: int = _t(ctypes.c_uint)
    mBytesUpdatedHint: int = _t(ctypes.c_int)
    mScoringInfo: rF2ScoringInfo = _t(rF2ScoringInfo)
    mVehicles: list[rF2VehicleScoring] = _t(rF2VehicleScoring * rFactor2Constants.MAX_MAPPED_VEHICLES)


@typedstruct(pack=4)
class rF2Rules(ctypes.Structure):
    """Mapping of 'rF2Rules' from rF2Data.cs

    Attributes:
        mVersionUpdateBegin: Incremented right before buffer is written to.
        mVersionUpdateEnd: Incremented after buffer write is done.
        mBytesUpdatedHint: How many bytes of the structure were written during the last update.
        mTrackRules: track rules
        mActions: track rules action data
        mParticipants: track rules participant data
    """

    __slots__ = ()

    mVersionUpdateBegin: int = _t(ctypes.c_uint)
    mVersionUpdateEnd: int = _t(ctypes.c_uint)
    mBytesUpdatedHint: int = _t(ctypes.c_int)
    mTrackRules: rF2TrackRules = _t(rF2TrackRules)
    mActions: list[rF2TrackRulesAction] = _t(rF2TrackRulesAction * rFactor2Constants.MAX_MAPPED_VEHICLES)
    mParticipants: list[rF2TrackRulesParticipant] = _t(rF2TrackRulesParticipant * rFactor2Constants.MAX_MAPPED_VEHICLES)


@typedstruct(pack=4)
class rF2ForceFeedback(ctypes.Structure):
    """Mapping of 'rF2ForceFeedback' from rF2Data.cs

    Attributes:
        mVersionUpdateBegin: Incremented right before buffer is written to.
        mVersionUpdateEnd: Incremented after buffer write is done.
        mForceValue: Current FFB value reported via InternalsPlugin::ForceFeedback.
    """

    __slots__ = ()

    mVersionUpdateBegin: int = _t(ctypes.c_uint)
    mVersionUpdateEnd: int = _t(ctypes.c_uint)
    mForceValue: float = _t(ctypes.c_double)


@typedstruct(pack=4)
class rF2GraphicsInfo(ctypes.Structure):
    """Mapping of 'GraphicsInfoV01' from InternalsPlugin.hpp

    Attributes:
        mCamPos: camera position
        mCamOri: rows of orientation matrix (use TelemQuat conversions if desired) also converts local
        mHWND: app handle
        mAmbientRed: ambient red
        mAmbientGreen: ambient green
        mAmbientBlue: ambient blue
        mID: slot ID being viewed (-1 if invalid)
        mCameraType: see above comments for possible values
        mExpansion: for future use (possibly camera name)
    """

    __slots__ = ()

    mCamPos: rF2Vec3 = _t(rF2Vec3)
    mCamOri: list[rF2Vec3] = _t(rF2Vec3 * 3)
    mHWND: list[int] = _t(ctypes.c_ubyte * 8)
    mAmbientRed: float = _t(ctypes.c_double)
    mAmbientGreen: float = _t(ctypes.c_double)
    mAmbientBlue: float = _t(ctypes.c_double)
    mID: int = _t(ctypes.c_int)
    mCameraType: int = _t(ctypes.c_int)
    mExpansion: list[int] = _t(ctypes.c_ubyte * 128)


@typedstruct(pack=4)
class rF2Graphics(ctypes.Structure):
    """Mapping of 'rF2Graphics' from rF2Data.cs

    Attributes:
        mVersionUpdateBegin: Incremented right before buffer is written to.
        mVersionUpdateEnd: Incremented after buffer write is done.
        mGraphicsInfo: graphics info
    """

    __slots__ = ()

    mVersionUpdateBegin: int = _t(ctypes.c_uint)
    mVersionUpdateEnd: int = _t(ctypes.c_uint)
    mGraphicsInfo: rF2GraphicsInfo = _t(rF2GraphicsInfo)


@typedstruct(pack=4)
class rF2PitInfo(ctypes.Structure):
    """Mapping of 'rF2PitInfo' from rF2Data.cs

    Attributes:
        mVersionUpdateBegin: Incremented right before buffer is written to.
        mVersionUpdateEnd: Incremented after buffer write is done.
        mPitMenu: pit menu
    """

    __slots__ = ()

    mVersionUpdateBegin: int = _t(ctypes.c_uint)
    mVersionUpdateEnd: int = _t(ctypes.c_uint)
    mPitMenu: rF2PitMenu = _t(rF2PitMenu)


@typedstruct(pack=4)
class rF2Weather(ctypes.Structure):
    """Mapping of 'rF2Weather' from rF2Data.cs

    Attributes:
        mVersionUpdateBegin: Incremented right before buffer is written to.
        mVersionUpdateEnd: Incremented after buffer write is done.
        mTrackNodeSize: track node size
        mWeatherInfo: weather info
    """

    __slots__ = ()

    mVersionUpdateBegin: int = _t(ctypes.c_uint)
    mVersionUpdateEnd: int = _t(ctypes.c_uint)
    mTrackNodeSize: float = _t(ctypes.c_double)
    mWeatherInfo: rF2WeatherControlInfo = _t(rF2WeatherControlInfo)


@typedstruct(pack=4)
class rF2TrackedDamage(ctypes.Structure):
    """Mapping of 'rF2TrackedDamage' from rF2Data.cs

    Attributes:
        mMaxImpactMagnitude: Max impact magnitude. Tracked on every telemetry update, and reset on visit to pits or Session restart.
        mAccumulatedImpactMagnitude: Accumulated impact magnitude. Tracked on every telemetry update, and reset on visit to pits or Session restart.
    """

    __slots__ = ()

    mMaxImpactMagnitude: float = _t(ctypes.c_double)
    mAccumulatedImpactMagnitude: float = _t(ctypes.c_double)


@typedstruct(pack=4)
class rF2VehScoringCapture(ctypes.Structure):
    """Mapping of 'rF2VehScoringCapture' from rF2Data.cs

    Attributes:
        mID: slot ID (note that it can be re-used in multiplayer after someone leaves)
        mPlace: 1-based position
        mIsPlayer: is this the player's vehicle
        mFinishStatus: 0=none, 1=finished, 2=dnf, 3 = dq
    """

    __slots__ = ()

    mID: int = _t(ctypes.c_int)
    mPlace: int = _t(ctypes.c_ubyte)
    mIsPlayer: bool = _t(ctypes.c_bool)
    mFinishStatus: int = _t(ctypes.c_byte)


@typedstruct(pack=4)
class rF2SessionTransitionCapture(ctypes.Structure):
    """Mapping of 'rF2SessionTransitionCapture' from rF2Data.cs

    Attributes:
        mGamePhase: game phase
        mSession: session type
        mNumScoringVehicles: number of scoring vehicles
        mScoringVehicles: vehicle scoring capture data
    """

    __slots__ = ()

    mGamePhase: int = _t(ctypes.c_ubyte)
    mSession: int = _t(ctypes.c_int)
    mNumScoringVehicles: int = _t(ctypes.c_int)
    mScoringVehicles: list[rF2VehScoringCapture] = _t(rF2VehScoringCapture * rFactor2Constants.MAX_MAPPED_VEHICLES)


@typedstruct(pack=4)
class rF2Extended(ctypes.Structure):
    """Mapping of 'rF2Extended' from rF2Data.cs

    Attributes:
        mVersionUpdateBegin: Incremented right before buffer is written to.
        mVersionUpdateEnd: Incremented after buffer write is done.
        mVersion: API (plugin) version
        is64bit: Is 64bit plugin?
        mPhysics: physics options
        mTrackedDamages: list[rF2TrackedDamage] = _t(rF2TrackedDamage*rFactor2Constants.MAX_MAPPED_IDS)
        mInRealtimeFC: in realtime as opposed to at the monitor (reported via last EnterRealtime/ExitRealtime calls).
        mMultimediaThreadStarted: multimedia thread started (reported via ThreadStarted/ThreadStopped calls).
        mSimulationThreadStarted: simulation thread started (reported via ThreadStarted/ThreadStopped calls).
        mSessionStarted: Set to true on Session Started, set to false on Session Ended.
        mTicksSessionStarted: Ticks when session started.
        mTicksSessionEnded: Ticks when session ended.
        mSessionTransitionCapture: Contains partial internals capture at session transition time.
        mDisplayedMessageUpdateCapture: displayed message update capture
        mDirectMemoryAccessEnabled: is direct memory access enabled
        mTicksStatusMessageUpdated: Ticks when status message was updated;
        mStatusMessage: status message
        mTicksLastHistoryMessageUpdated: Ticks when last message history message was updated;
        mLastHistoryMessage: last history message
        mCurrentPitSpeedLimit: speed limit m/s.
        mSCRPluginEnabled: Is Stock Car Rules plugin enabled?
        mSCRPluginDoubleFileType: Stock Car Rules plugin DoubleFileType value, only meaningful if mSCRPluginEnabled is true.
        mTicksLSIPhaseMessageUpdated: Ticks when last LSI phase message was updated.
        mLSIPhaseMessage: LSI phase message
        mTicksLSIPitStateMessageUpdated: Ticks when last LSI pit state message was updated.
        mLSIPitStateMessage: LSI pit state message
        mTicksLSIOrderInstructionMessageUpdated: Ticks when last LSI order instruction message was updated.
        mLSIOrderInstructionMessage: LSI order instruction message
        mTicksLSIRulesInstructionMessageUpdated: Ticks when last FCY rules message was updated.  Currently, only SCR plugin sets that.
        mLSIRulesInstructionMessage: LSI rules instruction message
        mUnsubscribedBuffersMask: Currently active UnsbscribedBuffersMask value.  This will be allowed for clients to write to in the future, but not yet.
        mHWControlInputEnabled: HWControl input buffer is enabled.
        mWeatherControlInputEnabled: WeatherControl input buffer is enabled.
        mRulesControlInputEnabled: RulesControl input buffer is enabled.
    """

    __slots__ = ()

    mVersionUpdateBegin: int = _t(ctypes.c_uint)
    mVersionUpdateEnd: int = _t(ctypes.c_uint)
    mVersion: bytes = _t(ctypes.c_char * 12)
    is64bit: bool = _t(ctypes.c_bool)
    mPhysics: rF2PhysicsOptions = _t(rF2PhysicsOptions)
    mTrackedDamages: list[rF2TrackedDamage] = _t(rF2TrackedDamage * rFactor2Constants.MAX_MAPPED_IDS)
    mInRealtimeFC: bool = _t(ctypes.c_bool)
    mMultimediaThreadStarted: bool = _t(ctypes.c_bool)
    mSimulationThreadStarted: bool = _t(ctypes.c_bool)
    mSessionStarted: bool = _t(ctypes.c_bool)
    mTicksSessionStarted: int = _t(ctypes.c_ulonglong)
    mTicksSessionEnded: int = _t(ctypes.c_ulonglong)
    mSessionTransitionCapture: rF2SessionTransitionCapture = _t(rF2SessionTransitionCapture)
    mDisplayedMessageUpdateCapture: bytes = _t(ctypes.c_char * 128)
    mDirectMemoryAccessEnabled: bool = _t(ctypes.c_bool)
    mTicksStatusMessageUpdated: int = _t(ctypes.c_ulonglong)
    mStatusMessage: bytes = _t(ctypes.c_char * rFactor2Constants.MAX_STATUS_MSG_LEN)
    mTicksLastHistoryMessageUpdated: int = _t(ctypes.c_ulonglong)
    mLastHistoryMessage: bytes = _t(ctypes.c_char * rFactor2Constants.MAX_STATUS_MSG_LEN)
    mCurrentPitSpeedLimit: float = _t(ctypes.c_float)
    mSCRPluginEnabled: bool = _t(ctypes.c_bool)
    mSCRPluginDoubleFileType: int = _t(ctypes.c_int)
    mTicksLSIPhaseMessageUpdated: int = _t(ctypes.c_ulonglong)
    mLSIPhaseMessage: bytes = _t(ctypes.c_char * rFactor2Constants.MAX_RULES_INSTRUCTION_MSG_LEN)
    mTicksLSIPitStateMessageUpdated: int = _t(ctypes.c_ulonglong)
    mLSIPitStateMessage: bytes = _t(ctypes.c_char * rFactor2Constants.MAX_RULES_INSTRUCTION_MSG_LEN)
    mTicksLSIOrderInstructionMessageUpdated: int = _t(ctypes.c_ulonglong)
    mLSIOrderInstructionMessage: bytes = _t(ctypes.c_char * rFactor2Constants.MAX_RULES_INSTRUCTION_MSG_LEN)
    mTicksLSIRulesInstructionMessageUpdated: int = _t(ctypes.c_ulonglong)
    mLSIRulesInstructionMessage: bytes = _t(ctypes.c_char * rFactor2Constants.MAX_RULES_INSTRUCTION_MSG_LEN)
    mUnsubscribedBuffersMask: int = _t(ctypes.c_int)
    mHWControlInputEnabled: bool = _t(ctypes.c_bool)
    mWeatherControlInputEnabled: bool = _t(ctypes.c_bool)
    mRulesControlInputEnabled: bool = _t(ctypes.c_bool)


@typedstruct(pack=4)
class rF2HWControl(ctypes.Structure):
    """Mapping of 'rF2HWControl' from rF2Data.cs

    Attributes:
        mVersionUpdateBegin: Incremented right before buffer is written to.
        mVersionUpdateEnd: Incremented after buffer write is done.
        mLayoutVersion: layout version
        mControlName: control name
        mfRetVal: float return value
    """

    __slots__ = ()

    mVersionUpdateBegin: int = _t(ctypes.c_uint)
    mVersionUpdateEnd: int = _t(ctypes.c_uint)
    mLayoutVersion: int = _t(ctypes.c_int)
    mControlName: bytes = _t(ctypes.c_char * rFactor2Constants.MAX_HWCONTROL_NAME_LEN)
    mfRetVal: float = _t(ctypes.c_double)


@typedstruct(pack=4)
class rF2WeatherControl(ctypes.Structure):
    """Mapping of 'rF2WeatherControl' from rF2Data.cs

    Attributes:
        mVersionUpdateBegin: Incremented right before buffer is written to.
        mVersionUpdateEnd: Incremented after buffer write is done.
        mLayoutVersion: layout version
        mWeatherInfo: weather control info
    """

    __slots__ = ()

    mVersionUpdateBegin: int = _t(ctypes.c_uint)
    mVersionUpdateEnd: int = _t(ctypes.c_uint)
    mLayoutVersion: int = _t(ctypes.c_int)
    mWeatherInfo: rF2WeatherControlInfo = _t(rF2WeatherControlInfo)


@typedstruct(pack=4)
class rF2RulesControl(ctypes.Structure):
    """Mapping of 'rF2RulesControl' from rF2Data.cs

    Attributes:
        mVersionUpdateBegin: Incremented right before buffer is written to.
        mVersionUpdateEnd: Incremented after buffer write is done.
        mLayoutVersion: layout version
        mTrackRules: track rules
        mActions: track rules action data
        mParticipants: track rules participant data
    """

    __slots__ = ()

    mVersionUpdateBegin: int = _t(ctypes.c_uint)
    mVersionUpdateEnd: int = _t(ctypes.c_uint)
    mLayoutVersion: int = _t(ctypes.c_int)
    mTrackRules: rF2TrackRules = _t(rF2TrackRules)
    mActions: list[rF2TrackRulesAction] = _t(rF2TrackRulesAction * rFactor2Constants.MAX_MAPPED_VEHICLES)
    mParticipants: list[rF2TrackRulesParticipant] = _t(rF2TrackRulesParticipant * rFactor2Constants.MAX_MAPPED_VEHICLES)


@typedstruct(pack=4)
class rF2PluginControl(ctypes.Structure):
    """Mapping of 'rF2PluginControl' from rF2Data.cs

    Attributes:
        mVersionUpdateBegin: Incremented right before buffer is written to.
        mVersionUpdateEnd: Incremented after buffer write is done.
        mLayoutVersion: layout version
        mRequestEnableBuffersMask: request enable buffers mask
        mRequestHWControlInput: request hwcontrol input
        mRequestWeatherControlInput: request weather control input
        mRequestRulesControlInput: request rules control input
    """

    __slots__ = ()

    mVersionUpdateBegin: int = _t(ctypes.c_uint)
    mVersionUpdateEnd: int = _t(ctypes.c_uint)
    mLayoutVersion: int = _t(ctypes.c_int)
    mRequestEnableBuffersMask: int = _t(ctypes.c_int)
    mRequestHWControlInput: int = _t(ctypes.c_ubyte)
    mRequestWeatherControlInput: int = _t(ctypes.c_ubyte)
    mRequestRulesControlInput: int = _t(ctypes.c_ubyte)


# Memory map
class SimInfo:
    """Simulation info from shared memory"""

    def __init__(self, server_pid: str = ""):
        self._rf2_tele = mmap.mmap(
            fileno=0,
            length=ctypes.sizeof(rF2Telemetry),
            tagname=f"{rFactor2Constants.MM_TELEMETRY_FILE_NAME}{server_pid}",
        )
        self.RF2Tele = rF2Telemetry.from_buffer(self._rf2_tele)

        self._rf2_scor = mmap.mmap(
            fileno=0,
            length=ctypes.sizeof(rF2Scoring),
            tagname=f"{rFactor2Constants.MM_SCORING_FILE_NAME}{server_pid}",
        )
        self.RF2Scor = rF2Scoring.from_buffer(self._rf2_scor)

        self._rf2_ext = mmap.mmap(
            fileno=0,
            length=ctypes.sizeof(rF2Extended),
            tagname=f"{rFactor2Constants.MM_EXTENDED_FILE_NAME}{server_pid}",
        )
        self.RF2Ext = rF2Extended.from_buffer(self._rf2_ext)

    def close(self):
        """Close memory map"""
        self.RF2Tele = None
        self.RF2Scor = None
        self.RF2Ext = None

        try:  # this did not help with the errors
            self._rf2_tele.close()
            self._rf2_scor.close()
            self._rf2_ext.close()
        except BufferError as e:
            print("Error:", e)

    def __del__(self):
        self.close()
