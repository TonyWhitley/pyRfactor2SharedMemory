"""
Test rF2 Memory Map Control
"""

import logging
import sys

sys.path.append(__file__.split("pyRfactor2SharedMemory")[0])
from pyRfactor2SharedMemory import rf2_data, rf2_mmap


def test_api():
    # Add logger
    logger = logging.getLogger(__name__)
    test_handler = logging.StreamHandler()
    logger.setLevel(logging.INFO)
    logger.addHandler(test_handler)
    logger.info(__doc__)

    # Test run
    SEPARATOR = "=" * 50
    print("Test API - Start")
    scoring = rf2_mmap.MMapControl(rf2_data.rFactor2Constants.MM_SCORING_FILE_NAME, rf2_data.rF2Scoring)
    scoring.create(1)
    telemetry = rf2_mmap.MMapControl(rf2_data.rFactor2Constants.MM_TELEMETRY_FILE_NAME, rf2_data.rF2Telemetry)
    telemetry.create(1)
    extended = rf2_mmap.MMapControl(rf2_data.rFactor2Constants.MM_EXTENDED_FILE_NAME, rf2_data.rF2Extended)
    extended.create(1)

    print(SEPARATOR)
    print("Test API - Read")
    version = extended.data.mVersion.decode()
    track = scoring.data.mScoringInfo.mTrackName.decode(encoding="iso-8859-1")
    vehicles = telemetry.data.mNumVehicles
    print(f"plugin ver: {version if version else 'not running'}")
    print(f"track name: {track if version else 'not running'}")
    print(f"total cars: {vehicles if version else 'not running'}")

    print(SEPARATOR)
    print("Test API - Close")
    scoring.close()
    telemetry.close()
    extended.close()


if __name__ == "__main__":
    test_api()
