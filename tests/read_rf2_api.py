"""
Test & read data from The Iron Wolf's rF2 Shared Memory Plugin interface
"""

from __future__ import annotations

import ctypes
import sys

sys.path.append(__file__.split("pyRfactor2SharedMemory")[0])
from pyRfactor2SharedMemory import rf2_data, rf2_enum


def find_player_index(data: rf2_data.rF2VehicleScoring):
    for player_index, player_data in enumerate(data):
        if player_data.mIsPlayer:
            return player_index
    return -1


def verify_struct_size(s_class: ctypes.Structure, size_origin: int):
    size = ctypes.sizeof(s_class)
    print(f"{s_class.__name__:<24} Size: {size:<10} ORG: {size_origin:<10} Match: {size_origin == size}")
    if size_origin != size:
        raise ValueError("Structure size mismatch.")


def compare_struct_size():
    print("Verify Struct Size:")
    verify_struct_size(rf2_data.rF2Vec3, 24)
    verify_struct_size(rf2_data.rF2Wheel, 260)
    verify_struct_size(rf2_data.rF2VehicleTelemetry, 1888)
    verify_struct_size(rf2_data.rF2ScoringInfo, 548)
    verify_struct_size(rf2_data.rF2VehicleScoring, 584)
    verify_struct_size(rf2_data.rF2PhysicsOptions, 40)
    verify_struct_size(rf2_data.rF2TrackRulesAction, 16)
    verify_struct_size(rf2_data.rF2TrackRulesParticipant, 332)
    verify_struct_size(rf2_data.rF2TrackRules, 716)
    verify_struct_size(rf2_data.rF2PitMenu, 332)
    verify_struct_size(rf2_data.rF2WeatherControlInfo, 616)
    verify_struct_size(rf2_data.rF2MappedBufferVersionBlock, 8)
    verify_struct_size(rf2_data.rF2MappedBufferVersionBlockWithSize, 12)
    verify_struct_size(rf2_data.rF2Telemetry, 241680)
    verify_struct_size(rf2_data.rF2Scoring, 75312)
    verify_struct_size(rf2_data.rF2Rules, 45272)
    verify_struct_size(rf2_data.rF2ForceFeedback, 16)
    verify_struct_size(rf2_data.rF2GraphicsInfo, 264)
    verify_struct_size(rf2_data.rF2Graphics, 272)
    verify_struct_size(rf2_data.rF2PitInfo, 340)
    verify_struct_size(rf2_data.rF2Weather, 632)
    verify_struct_size(rf2_data.rF2TrackedDamage, 16)
    verify_struct_size(rf2_data.rF2VehScoringCapture, 8)
    verify_struct_size(rf2_data.rF2SessionTransitionCapture, 1036)
    verify_struct_size(rf2_data.rF2Extended, 10152)
    verify_struct_size(rf2_data.rF2HWControl, 116)
    verify_struct_size(rf2_data.rF2WeatherControl, 628)
    verify_struct_size(rf2_data.rF2RulesControl, 45272)
    verify_struct_size(rf2_data.rF2PluginControl, 20)


def generic_info(data: rf2_data.rF2Extended):
    print("Plugin info:")
    print("Version:", data.mVersion)
    print("is64bit:", data.is64bit)
    print("Unsubscribed buffers:", rf2_enum.SubscribedBuffer(data.mUnsubscribedBuffersMask))


def scoring_info(data: rf2_data.rF2ScoringInfo):
    print("Scoring info:")
    print("Track name:", data.mTrackName)
    print("Local player name:", data.mPlayerName)
    print("Setting name:", data.mPlrFileName)
    print("Total vehicles:", data.mNumVehicles)


def player_scoring_info(data: rf2_data.rF2VehicleScoring):
    print("Selected Player scoring info:")
    print("Slot ID:", data.mID)
    print("Driver name:", data.mDriverName)
    print("VEH file:", data.mVehFilename)
    print("Is local player:", data.mIsPlayer)


def player_telemetry_info(data: rf2_data.rF2VehicleTelemetry):
    print("Selected player telemetry info:")
    print("Slot ID:", data.mID)
    print("Vehicle:", data.mVehicleName)
    print("Gear:", data.mGear)
    print("Throttle:", data.mUnfilteredThrottle)
    print("Brake:", data.mUnfilteredBrake)
    print("Clutch:", data.mUnfilteredClutch)


def player_wheel_info(data: list[rf2_data.rF2Wheel]):
    for index in range(4):
        print(rf2_enum.rF2WheelIndex(index).name, "Wheel Info:")
        print("mBrakeTemp:", data[index].mBrakeTemp)
        print("mPressure:", data[index].mPressure)
        print("mTireLoad:", data[index].mTireLoad)


def vehicle_model_info(data: list[rf2_data.rF2VehicleScoring], total_vehicles: int):
    print("Available vehicle model list from session:")
    for model in {data[i].mVehFilename for i in range(total_vehicles)}:
        print(model)


def list_zero_data(data, source):
    print("List of zero data:", source.__name__)
    for var, _ in source._fields_:
        value = getattr(data, var)
        if not value:
            print(var, value)


def test_data(info: rf2_data.SimInfo, player_index, selected_player_index):
    """Example usage"""
    separator = "-" * 40

    print(separator)

    print("Player Index:")
    print("Local player index:", player_index)
    print("Selected player index:", selected_player_index)

    print(separator)

    generic_info(info.RF2Ext)

    print(separator)

    scoring_info(info.RF2Scor.mScoringInfo)

    print(separator)

    player_scoring_info(info.RF2Scor.mVehicles[selected_player_index])

    print(separator)

    player_telemetry_info(info.RF2Tele.mVehicles[selected_player_index])

    print(separator)

    player_wheel_info(info.RF2Tele.mVehicles[selected_player_index].mWheels)

    print(separator)

    vehicle_model_info(info.RF2Scor, info.RF2Scor.mScoringInfo.mNumVehicles)


def test_enum():
    separator = "-" * 40

    print(separator)

    GAME_PHASE = rf2_enum.enum_map(rf2_enum.rF2GamePhase)
    SURFACE_TYPE = rf2_enum.enum_map(rf2_enum.rF2SurfaceType)
    SESSION = rf2_enum.enum_map(rf2_enum.rF2Session)

    print("Enum:")
    print(rf2_enum.rF2GamePhase(0))
    print(rf2_enum.rF2SurfaceType(1))
    print(rf2_enum.rF2Session(7))

    print(separator)

    print("Dict (fast lookup):")
    print(GAME_PHASE(0))
    print(SURFACE_TYPE(1))
    print(SESSION(7))


def verify_data(info: rf2_data.SimInfo, player_index):
    separator = "-" * 40

    print(separator)

    list_zero_data(info.RF2Scor.mScoringInfo, rf2_data.rF2ScoringInfo)

    print(separator)

    list_zero_data(info.RF2Scor.mVehicles[player_index], rf2_data.rF2VehicleScoring)

    print(separator)

    list_zero_data(info.RF2Tele.mVehicles[player_index], rf2_data.rF2VehicleTelemetry)

    print(separator)

    list_zero_data(info.RF2Tele.mVehicles[player_index].mWheels[0], rf2_data.rF2Wheel)


if __name__ == "__main__":
    compare_struct_size()

    info = rf2_data.SimInfo(server_pid="")

    player_index = find_player_index(info.RF2Scor.mVehicles)
    selected_player_index = player_index

    test_data(info, player_index, selected_player_index)

    test_enum()

    verify_data(info, selected_player_index)
