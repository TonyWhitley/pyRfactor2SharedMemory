"""
rF2 API data type hints & annotation

Helper classes with type hints & annotation reference to rF2data.py for IDE & type checker.

Annotate "ctypes type" as "Python type" according to table from:
https://docs.python.org/3/library/ctypes.html#fundamental-data-types

Annotate array object as tuple[type, ...] to specify number of elements contained.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class _NOINIT(ABC):
    """Disable instantiate"""

    @abstractmethod
    def _(self): ...


class rF2Vec3(_NOINIT):
    x: float
    y: float
    z: float


class rF2Wheel(_NOINIT):
    mSuspensionDeflection: float
    mRideHeight: float
    mSuspForce: float
    mBrakeTemp: float
    mBrakePressure: float
    mRotation: float
    mLateralPatchVel: float
    mLongitudinalPatchVel: float
    mLateralGroundVel: float
    mLongitudinalGroundVel: float
    mCamber: float
    mLateralForce: float
    mLongitudinalForce: float
    mTireLoad: float
    mGripFract: float
    mPressure: float
    mTemperature: tuple[float, float, float]
    mWear: float
    mTerrainName: bytes
    mSurfaceType: int
    mFlat: bool
    mDetached: bool
    mStaticUndeflectedRadius: int
    mVerticalTireDeflection: float
    mWheelYLocation: float
    mToe: float
    mTireCarcassTemperature: float
    mTireInnerLayerTemperature: tuple[float, float, float]
    mExpansion: tuple[int, ...]


class rF2VehicleTelemetry(_NOINIT):
    mID: int
    mDeltaTime: float
    mElapsedTime: float
    mLapNumber: int
    mLapStartET: float
    mVehicleName: bytes
    mTrackName: bytes
    mPos: rF2Vec3
    mLocalVel: rF2Vec3
    mLocalAccel: rF2Vec3
    mOri: tuple[rF2Vec3, rF2Vec3, rF2Vec3]
    mLocalRot: rF2Vec3
    mLocalRotAccel: rF2Vec3
    mGear: int
    mEngineRPM: float
    mEngineWaterTemp: float
    mEngineOilTemp: float
    mClutchRPM: float
    mUnfilteredThrottle: float
    mUnfilteredBrake: float
    mUnfilteredSteering: float
    mUnfilteredClutch: float
    mFilteredThrottle: float
    mFilteredBrake: float
    mFilteredSteering: float
    mFilteredClutch: float
    mSteeringShaftTorque: float
    mFront3rdDeflection: float
    mRear3rdDeflection: float
    mFrontWingHeight: float
    mFrontRideHeight: float
    mRearRideHeight: float
    mDrag: float
    mFrontDownforce: float
    mRearDownforce: float
    mFuel: float
    mEngineMaxRPM: float
    mScheduledStops: int
    mOverheating: bool
    mDetached: bool
    mHeadlights: bool
    mDentSeverity: tuple[int, int, int, int, int, int, int, int]
    mLastImpactET: float
    mLastImpactMagnitude: float
    mLastImpactPos: rF2Vec3
    mEngineTorque: float
    mCurrentSector: int
    mSpeedLimiter: int
    mMaxGears: int
    mFrontTireCompoundIndex: int
    mRearTireCompoundIndex: int
    mFuelCapacity: float
    mFrontFlapActivated: int
    mRearFlapActivated: int
    mRearFlapLegalStatus: int
    mIgnitionStarter: int
    mFrontTireCompoundName: bytes
    mRearTireCompoundName: bytes
    mSpeedLimiterAvailable: int
    mAntiStallActivated: int
    mUnused: tuple[int, int]
    mVisualSteeringWheelRange: float
    mRearBrakeBias: float
    mTurboBoostPressure: float
    mPhysicsToGraphicsOffset: tuple[float, float, float]
    mPhysicalSteeringWheelRange: float
    mDeltaBest: float
    mBatteryChargeFraction: float
    mElectricBoostMotorTorque: float
    mElectricBoostMotorRPM: float
    mElectricBoostMotorTemperature: float
    mElectricBoostWaterTemperature: float
    mElectricBoostMotorState: int
    mExpansion: tuple[int, ...]
    mWheels: tuple[rF2Wheel, rF2Wheel, rF2Wheel, rF2Wheel]


class rF2ScoringInfo(_NOINIT):
    mTrackName: bytes
    mSession: int
    mCurrentET: float
    mEndET: float
    mMaxLaps: int
    mLapDist: float
    mResultsStreamPointer: tuple[int, ...]
    mNumVehicles: int
    mGamePhase: int
    mYellowFlagState: int
    mSectorFlag: tuple[int, int, int]
    mStartLight: int
    mNumRedLights: int
    mInRealtime: bool
    mPlayerName: bytes
    mPlrFileName: bytes
    mDarkCloud: float
    mRaining: float
    mAmbientTemp: float
    mTrackTemp: float
    mWind: rF2Vec3
    mMinPathWetness: float
    mMaxPathWetness: float
    mGameMode: int
    mIsPasswordProtected: bool
    mServerPort: int
    mServerPublicIP: int
    mMaxPlayers: int
    mServerName: bytes
    mStartET: float
    mAvgPathWetness: float
    mExpansion: tuple[int, ...]
    mVehiclePointer: tuple[int, ...]


class rF2VehicleScoring(_NOINIT):
    mID: int
    mDriverName: bytes
    mVehicleName: bytes
    mTotalLaps: int
    mSector: int
    mFinishStatus: int
    mLapDist: float
    mPathLateral: float
    mTrackEdge: float
    mBestSector1: float
    mBestSector2: float
    mBestLapTime: float
    mLastSector1: float
    mLastSector2: float
    mLastLapTime: float
    mCurSector1: float
    mCurSector2: float
    mNumPitstops: int
    mNumPenalties: int
    mIsPlayer: bool
    mControl: int
    mInPits: bool
    mPlace: int
    mVehicleClass: bytes
    mTimeBehindNext: float
    mLapsBehindNext: int
    mTimeBehindLeader: float
    mLapsBehindLeader: int
    mLapStartET: float
    mPos: rF2Vec3
    mLocalVel: rF2Vec3
    mLocalAccel: rF2Vec3
    mOri: tuple[rF2Vec3, rF2Vec3, rF2Vec3]
    mLocalRot: rF2Vec3
    mLocalRotAccel: rF2Vec3
    mHeadlights: int
    mPitState: int
    mServerScored: int
    mIndividualPhase: int
    mQualification: int
    mTimeIntoLap: float
    mEstimatedLapTime: float
    mPitGroup: bytes
    mFlag: int
    mUnderYellow: bool
    mCountLapFlag: int
    mInGarageStall: bool
    mUpgradePack: tuple[int, ...]
    mPitLapDist: float
    mBestLapSector1: float
    mBestLapSector2: float
    mSteamID: int
    mVehFilename: bytes
    mAttackMode: int
    mFuelFraction: int
    mDRSState: bool
    mExpansion: tuple[int, ...]


class rF2PhysicsOptions(_NOINIT):
    mTractionControl: int
    mAntiLockBrakes: int
    mStabilityControl: int
    mAutoShift: int
    mAutoClutch: int
    mInvulnerable: int
    mOppositeLock: int
    mSteeringHelp: int
    mBrakingHelp: int
    mSpinRecovery: int
    mAutoPit: int
    mAutoLift: int
    mAutoBlip: int
    mFuelMult: int
    mTireMult: int
    mMechFail: int
    mAllowPitcrewPush: int
    mRepeatShifts: int
    mHoldClutch: int
    mAutoReverse: int
    mAlternateNeutral: int
    mAIControl: int
    mUnused1: int
    mUnused2: int
    mManualShiftOverrideTime: float
    mAutoShiftOverrideTime: float
    mSpeedSensitiveSteering: float
    mSteerRatioSpeed: float


class rF2TrackRulesAction(_NOINIT):
    mCommand: int
    mID: int
    mET: float


class rF2TrackRulesParticipant(_NOINIT):
    mID: int
    mFrozenOrder: int
    mPlace: int
    mYellowSeverity: float
    mCurrentRelativeDistance: float
    mRelativeLaps: int
    mColumnAssignment: int
    mPositionAssignment: int
    mPitsOpen: int
    mUpToSpeed: bool
    mUnused: tuple[bool, bool]
    mGoalRelativeDistance: float
    mMessage: bytes
    mExpansion: tuple[int, ...]


class rF2TrackRules(_NOINIT):
    mCurrentET: float
    mStage: int
    mPoleColumn: int
    mNumActions: int
    mActionPointer: tuple[int, ...]
    mNumParticipants: int
    mYellowFlagDetected: bool
    mYellowFlagLapsWasOverridden: int
    mSafetyCarExists: bool
    mSafetyCarActive: bool
    mSafetyCarLaps: int
    mSafetyCarThreshold: float
    mSafetyCarLapDist: float
    mSafetyCarLapDistAtStart: float
    mPitLaneStartDist: float
    mTeleportLapDist: float
    mInputExpansion: tuple[int, ...]
    mYellowFlagState: int
    mYellowFlagLaps: int
    mSafetyCarInstruction: int
    mSafetyCarSpeed: float
    mSafetyCarMinimumSpacing: float
    mSafetyCarMaximumSpacing: float
    mMinimumColumnSpacing: float
    mMaximumColumnSpacing: float
    mMinimumSpeed: float
    mMaximumSpeed: float
    mMessage: bytes
    mParticipantPointer: tuple[int, ...]
    mInputOutputExpansion: tuple[int, ...]


class rF2PitMenu(_NOINIT):
    mCategoryIndex: int
    mCategoryName: bytes
    mChoiceIndex: int
    mChoiceString: bytes
    mNumChoices: int
    mExpansion: tuple[int, ...]


class rF2WeatherControlInfo(_NOINIT):
    mET: float
    mRaining: tuple[float, float, float, float, float, float, float, float, float]
    mCloudiness: float
    mAmbientTempK: float
    mWindMaxSpeed: float
    mApplyCloudinessInstantly: bool
    mUnused1: bool
    mUnused2: bool
    mUnused3: bool
    mExpansion: tuple[int, ...]


class rF2MappedBufferVersionBlock(_NOINIT):
    mVersionUpdateBegin: int
    mVersionUpdateEnd: int


class rF2MappedBufferVersionBlockWithSize(_NOINIT):
    mVersionUpdateBegin: int
    mVersionUpdateEnd: int
    mBytesUpdatedHint: int


class rF2Telemetry(_NOINIT):
    mVersionUpdateBegin: int
    mVersionUpdateEnd: int
    mBytesUpdatedHint: int
    mNumVehicles: int
    mVehicles: tuple[rF2VehicleTelemetry, ...]


class rF2Scoring(_NOINIT):
    mVersionUpdateBegin: int
    mVersionUpdateEnd: int
    mBytesUpdatedHint: int
    mScoringInfo: rF2ScoringInfo
    mVehicles: tuple[rF2VehicleScoring, ...]


class rF2Rules(_NOINIT):
    mVersionUpdateBegin: int
    mVersionUpdateEnd: int
    mBytesUpdatedHint: int
    mTrackRules: rF2TrackRules
    mActions: tuple[rF2TrackRulesAction, ...]
    mParticipants: tuple[rF2TrackRulesParticipant, ...]


class rF2ForceFeedback(_NOINIT):
    mVersionUpdateBegin: int
    mVersionUpdateEnd: int
    mForceValue: float


class rF2GraphicsInfo(_NOINIT):
    mCamPos: rF2Vec3
    mCamOri: tuple[rF2Vec3, rF2Vec3, rF2Vec3]
    mHWND: tuple[int, ...]
    mAmbientRed: float
    mAmbientGreen: float
    mAmbientBlue: float
    mID: int
    mCameraType: int
    mExpansion: tuple[int, ...]


class rF2Graphics(_NOINIT):
    mVersionUpdateBegin: int
    mVersionUpdateEnd: int
    mGraphicsInfo: rF2GraphicsInfo


class rF2PitInfo(_NOINIT):
    mVersionUpdateBegin: int
    mVersionUpdateEnd: int
    mPitMenu: rF2PitMenu


class rF2Weather(_NOINIT):
    mVersionUpdateBegin: int
    mVersionUpdateEnd: int
    mTrackNodeSize: float
    mWeatherInfo: rF2WeatherControlInfo


class rF2TrackedDamage(_NOINIT):
    mMaxImpactMagnitude: float
    mAccumulatedImpactMagnitude: float


class rF2VehScoringCapture(_NOINIT):
    mID: int
    mPlace: int
    mIsPlayer: bool
    mFinishStatus: int


class rF2SessionTransitionCapture(_NOINIT):
    mGamePhase: int
    mSession: int
    mNumScoringVehicles: int
    mScoringVehicles: tuple[rF2VehScoringCapture, ...]


class rF2Extended(_NOINIT):
    mVersionUpdateBegin: int
    mVersionUpdateEnd: int
    mVersion: bytes
    is64bit: bool
    mPhysics: rF2PhysicsOptions
    mTrackedDamages: tuple[rF2TrackedDamage, ...]
    mInRealtimeFC: bool
    mMultimediaThreadStarted: bool
    mSimulationThreadStarted: bool
    mSessionStarted: bool
    mTicksSessionStarted: int
    mTicksSessionEnded: int
    mSessionTransitionCapture: rF2SessionTransitionCapture
    mDisplayedMessageUpdateCapture: bytes
    mDirectMemoryAccessEnabled: bool
    mTicksStatusMessageUpdated: int
    mStatusMessage: bytes
    mTicksLastHistoryMessageUpdated: int
    mLastHistoryMessage: bytes
    mCurrentPitSpeedLimit: float
    mSCRPluginEnabled: bool
    mSCRPluginDoubleFileType: int
    mTicksLSIPhaseMessageUpdated: int
    mLSIPhaseMessage: bytes
    mTicksLSIPitStateMessageUpdated: int
    mLSIPitStateMessage: bytes
    mTicksLSIOrderInstructionMessageUpdated: int
    mLSIOrderInstructionMessage: bytes
    mTicksLSIRulesInstructionMessageUpdated: int
    mLSIRulesInstructionMessage: bytes
    mUnsubscribedBuffersMask: int
    mHWControlInputEnabled: bool
    mWeatherControlInputEnabled: bool
    mRulesControlInputEnabled: bool


class rF2HWControl(_NOINIT):
    mVersionUpdateBegin: int
    mVersionUpdateEnd: int
    mLayoutVersion: int
    mControlName: bytes
    mfRetVal: float


class rF2WeatherControl(_NOINIT):
    mVersionUpdateBegin: int
    mVersionUpdateEnd: int
    mLayoutVersion: int
    mWeatherInfo: rF2WeatherControlInfo


class rF2RulesControl(_NOINIT):
    mVersionUpdateBegin: int
    mVersionUpdateEnd: int
    mLayoutVersion: int
    mTrackRules: rF2TrackRules
    mActions: tuple[rF2TrackRulesAction, ...]
    mParticipants: tuple[rF2TrackRulesParticipant, ...]


class rF2PluginControl(_NOINIT):
    mVersionUpdateBegin: int
    mVersionUpdateEnd: int
    mLayoutVersion: int
    mRequestEnableBuffersMask: int
    mRequestHWControlInput: int
    mRequestWeatherControlInput: int
    mRequestRulesControlInput: int
