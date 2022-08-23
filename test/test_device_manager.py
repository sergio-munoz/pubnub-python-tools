"""Simple test file for device_manager.py."""
from app import device_manager
from logging import DEBUG
from logger.logging_config import set_logger
from unittest import TestCase
import os

# Create a logger if needed for testing cases
LOG = set_logger("test_device_manager", DEBUG)  # Defaults as INFO

class RunMainAppTests(TestCase):

    def test_init(self):
        """Tests __init__ function from device_manager.py."""
        LOG.info("Testing test_init")

        # Test variables
        LOCATION = "/Users/sergio.munoz/Data/Git/pubnub-python-tools/test/db/test_empty.db"
        dm = device_manager.DeviceManager(LOCATION)
        self.assertEqual(dm.db_location, LOCATION)

    def test_read_local_file(self):
        """Tests __read_local_file function from device_manager.py."""
        LOCATION = "/Users/sergio.munoz/Data/Git/pubnub-python-tools/test/db/test_read_one.db"
        dm = device_manager.DeviceManager(LOCATION)

        # There is only one device at file
        lines = dm._DeviceManager__read_local_file()
        self.assertEqual(len(lines), 1)

    def test_write_local_file(self):
        """Tests __write_local_file function from device_manager.py."""
        LOCATION = "/Users/sergio.munoz/Data/Git/pubnub-python-tools/test/db/test_write_two.db"
        dm = device_manager.DeviceManager(LOCATION)

        # Add a new device
        dm.devices.add("UUID-r01")
        dm.devices.add("UUID-r02")
        dm._DeviceManager__write_local_file()

        # There is only one device at file
        file1 = open(LOCATION, "r")
        lines = file1.readlines()
        self.assertEqual(len(lines), 2)

        # Cleanup!
        os.remove(LOCATION)


    def test_parse_db_location_local_file(self):
        """Tests __parse_db_location_local_file function from device_manager.py."""
        LOG.info("Testing test_parse_db_location_local_file")

        # DB File location
        LOCATION = "/Users/sergio.munoz/Data/Git/pubnub-python-tools/test/db/test_read_one.db"
        dm = device_manager.DeviceManager(LOCATION)

        # Assert 1 device found
        # The file `test_one_device.db` only contains 1 row (1 device)
        self.assertEqual(len(dm.devices), 1)

        # Assert device name
        # The file `test_one_device.db` contains 1 device "UUID-r01"
        self.assertEqual(dm.get_devices()[0], "UUID-r01")
    

