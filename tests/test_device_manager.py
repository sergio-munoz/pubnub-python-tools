"""Simple test file for device_manager.py."""
from pubnub_python_tools.app import device_manager
from pubnub_python_tools.logger.logging_config import set_logger
from logging import DEBUG
from unittest import TestCase
import os

# Create a logger if needed for testing cases
LOG = set_logger("test_device_manager", DEBUG)  # Defaults as INFO

# Global test folder
TEST_FOLDER = str(os.path.dirname(os.path.abspath(__file__)))

class RunMainAppTests(TestCase):

    def test_init(self):
        """Tests __init__ function from device_manager.py."""
        LOG.info("Testing __init__()")

        # Test variables
        LOCATION = TEST_FOLDER+"/db/test_empty.db"
        dm = device_manager.DeviceManager(LOCATION)
        self.assertEqual(dm.db_location, LOCATION)

    def test_read_local_file(self):
        """Tests __read_local_file function from device_manager.py."""
        LOG.info("Testing __read_local_file()")

        LOCATION = TEST_FOLDER+"/db/test_read_one.db"
        dm = device_manager.DeviceManager(LOCATION)

        # There is only one device at file
        lines = dm._DeviceManager__read_local_file()
        self.assertEqual(len(lines), 1)

    def test_write_local_file(self):
        """Tests __write_local_file function from device_manager.py."""
        LOG.info("Testing __write_local_file()")

        LOCATION = TEST_FOLDER+"/db/test_write_two.db"
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
        LOG.info("Testing test_parse_db_location_local_file()")

        # DB File location
        LOCATION = TEST_FOLDER+"/db/test_read_one.db"
        dm = device_manager.DeviceManager(LOCATION)

        # Assert 1 device found
        # The file `test_one_device.db` only contains 1 row (1 device)
        self.assertEqual(len(dm.devices), 1)

        # Assert device name
        # The file `test_one_device.db` contains 1 device "UUID-r01"
        self.assertEqual(dm.get_devices()[0], "UUID-r01")
    
    def test_is_connected(self):
        """Tests add_device function from device_manager.py."""
        LOG.info("Testing is_connected()")

        # DB File location
        LOCATION = TEST_FOLDER+"/db/test_empty.db"
        dm = device_manager.DeviceManager(LOCATION)

        # Assert is not connected
        self.assertFalse(dm.is_connected("UUID-r01"))

        # Add device
        dm.devices.add("UUID-r01")
        # Assert is connected
        self.assertTrue(dm.is_connected("UUID-r01"))

    def test_add_device(self):
        """Tests add_device function from device_manager.py."""
        LOG.info("Testing add_device()")

        # DB File location
        LOCATION = TEST_FOLDER+"/db/test_add_device.db"
        dm = device_manager.DeviceManager(LOCATION)

        # Add three devices
        dm.add_device("UUID-r01")
        dm.add_device("UUID-r02")
        dm.add_device("UUID-r03")

        # Assert three devices
        devices = list(dm.devices)
        self.assertEqual(len(devices), 3)

        # Cleanup!
        os.remove(LOCATION)

    def test_remove_device(self):
        """Tests remove_device function from device_manager.py."""
        LOG.info("Testing remove_device()")

        # DB File location
        LOCATION = TEST_FOLDER+"/db/test_remove_device.db"
        dm = device_manager.DeviceManager(LOCATION)

        # Add three devices
        dm.add_device("UUID-r01")
        dm.add_device("UUID-r02")
        dm.add_device("UUID-r03")

        # Assert three devices
        devices = list(dm.devices)
        self.assertEqual(len(devices), 3)

        # Remove two devices
        dm.remove_device("UUID-r01")
        dm.remove_device("UUID-r02")

        # Assert one devices
        devices = list(dm.devices)
        self.assertEqual(len(devices), 1)

        # Cleanup!
        os.remove(LOCATION)
