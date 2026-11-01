"""
rF2 API Enums mapping, with fast dict lookup function
"""

from __future__ import annotations

import enum

from ._common import enum_map


class SubscribedBuffer(enum.Flag):
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


class rF2GamePhase(enum.Enum):
    """Game phase states (mGamePhase)

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


class rF2YellowFlagState(enum.Enum):
    """Yellow flag states (mYellowFlagState), applies to full-course only

    -1=Invalid,
    0=None,
    1=Pending,
    2=Pits closed,
    3=Pit lead lap,
    4=Pits open,
    5=Last lap,
    6=Resume,
    7=Race halt (not currently used)
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


class rF2SurfaceType(enum.Enum):
    """Surface type (mSurfaceType)"""

    Dry = 0
    Wet = 1
    Grass = 2
    Dirt = 3
    Gravel = 4
    Kerb = 5
    Special = 6


class rF2Session(enum.Enum):
    """Session type (mSession)"""

    TestDay = 0
    Practice1 = 1
    Practice2 = 2
    Practice3 = 3
    Practice4 = 4
    Qualifying1 = 5
    Qualifying2 = 6
    Qualifying3 = 7
    Qualifying4 = 8
    Warmup = 9
    Race1 = 10
    Race2 = 11
    Race3 = 12
    Race4 = 13


class rF2Sector(enum.Enum):
    """Sector index (mSector)

    0=sector3,
    1=sector1,
    2=sector2 (don't ask why)
    """

    Sector3 = 0
    Sector1 = 1
    Sector2 = 2


class rF2FinishStatus(enum.Enum):
    """Finish status (mFinishStatus)"""

    _None = 0
    Finished = 1
    Dnf = 2
    Dq = 3


class rF2Control(enum.Enum):
    """Who's in control (mControl)

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


class rF2PitState(enum.Enum):
    """Pit state (mPitState)"""

    _None = 0
    Request = 1
    Entering = 2
    Stopped = 3
    Exiting = 4


class rF2PrimaryFlag(enum.Enum):
    """Primary flag being shown to vehicle (mFlag)"""

    Green = 0
    Blue = 6


class rF2CountLapFlag(enum.Enum):
    """Count lap flag (mCountLapFlag)"""

    DoNotCountLap = 0
    CountLapButNotTime = 1
    CountLapAndTime = 2


class rF2RearFlapLegalStatus(enum.Enum):
    """Rear flap (DRS) status (mRearFlapLegalStatus)"""

    Disallowed = 0
    DetectedButNotAllowedYet = 1
    Alllowed = 2


class rF2IgnitionStarterStatus(enum.Enum):
    """Ignition starter status (mIgnitionStarter)"""

    Off = 0
    Ignition = 1
    IgnitionAndStarter = 2


class rF2WheelIndex(enum.Enum):
    """Wheel index reference for 'rF2Wheel'"""

    FrontLeft = 0
    FrontRight = 1
    RearLeft = 2
    RearRight = 3


class rF2SafetyCarInstruction(enum.Enum):
    """Safety car instruction

    0=no change,
    1=go active,
    2=head for pits
    """

    NoChange = 0
    GoActive = 1
    HeadForPits = 2


class rF2TrackRulesCommand(enum.Enum):
    """Track rules command"""

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


class rF2TrackRulesColumn(enum.Enum):
    """Track rules column"""

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


class rF2TrackRulesStage(enum.Enum):
    """Track rules stage"""

    FormationInit = 0
    FormationUpdate = 1  # update of the formation lap
    Normal = 2           # normal (non-yellow) update
    CautionInit = 3      # initialization of a full-course yellow
    CautionUpdate = 4    # update of a full-course yellow
    Maximum = 5          # should be last
