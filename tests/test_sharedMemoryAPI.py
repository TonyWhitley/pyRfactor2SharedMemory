import unittest

from sharedMemoryAPI import test_main, SimInfoAPI, Cbytestring2Python

VERSION_STRING = '3.6.0.0     '
TRACK_NAME = 'Test Track'


def str_to_byte_array(string):
    x = bytearray(string, 'utf-8')
    byte_array = bytearray()
    for i, ch in enumerate(x):
        byte_array[i] = ch
    return byte_array


class Test_sharedMemoryAPI(unittest.TestCase):
    def test_sharedMemoryAPI_main_runs(self):
        """ Preliminary test - does main run? """
        root = test_main()
        assert root is not None

    def test_pokeMemoryMap(self):
        info = SimInfoAPI()
        x = bytearray(VERSION_STRING, 'utf-8')
        for i, ch in enumerate(x):
            info.Rf2Ext.mVersion[i] = ch
        #info.Rf2Ext.mVersion = str_to_byte_array(VERSION_STRING)
        __ = VERSION_STRING.encode()
        info.Rf2Ext.is64bit = 1
        print(info.isSharedMemoryAvailable())
        assert info.isSharedMemoryAvailable() is not None

    def test_is_track_loaded(self):
        info = SimInfoAPI()
        info.Rf2Ext.mSessionStarted = 1
        assert info.isTrackLoaded()

    def test_track_name(self):
        info = SimInfoAPI()
        x = bytearray(TRACK_NAME, 'utf-8')
        for i, ch in enumerate(x):
            info.Rf2Scor.mScoringInfo.mTrackName[i] = ch
        trackName = Cbytestring2Python(
            info.Rf2Scor.mScoringInfo.mTrackName)
        assert trackName

    def test_is_on_track(self):
        info = SimInfoAPI()
        info.Rf2Ext.mInRealtimeFC = 1
        assert info.isOnTrack()


if __name__ == '__main__':
    unittest.main(exit=False)
