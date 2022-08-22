"""Simple test file for device_manager.py."""
from app import device_manager
from logging import DEBUG
from logger.logging_config import set_logger
from unittest import TestCase

# Create a logger if needed for testing cases
LOG = set_logger("test_device_manager", DEBUG)  # Defaults as INFO

class RunMainAppTests(TestCase):

    def test_init(self):
        """Tests __init__ function from device_manager.py."""
        LOG.info("Testing test_init")

        # Test variables
        LOCATION = "/Users/sergio.munoz/Data/Git/pubnub-python-tools/test/db/test_device_manager.db"
        dm = device_manager.DeviceManager(LOCATION)
        self.assertEqual(dm.db_location, LOCATION)

        DEVICES = dm.devices
        print(DEVICES)
        # self.assertEqual(True, False)

    def test_read_local_file(self):
        pass

    def test_parse_db_location_local_file(self):
        """Tests __parse_db_location_local_file function from device_manager.py."""
        LOG.info("Testing test_parse_db_location_local_file")

        # DB File location
        LOCATION = "/Users/sergio.munoz/Data/Git/pubnub-python-tools/test/db/test_one_device.db"
        dm = device_manager.DeviceManager(LOCATION)

        # Assert 1 device found
        # The file `test_one_device.db` only contains 1 row (1 device)
        self.assertEqual(len(dm.devices), 1)

        # Assert device name
        # The file `test_one_device.db` contains 1 device "UUID-r01"
        self.assertEqual(dm.get_devices()[0], "UUID-r01")
    
