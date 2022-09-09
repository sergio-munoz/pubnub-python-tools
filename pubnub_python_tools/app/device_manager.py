"""Manage Devices locally in the client side with overlapping UUIDs."""
from ..logger.logging_config import get_logger

LOG = get_logger()  # Get logger if needed. Default: INFO


class DeviceManager():
    """Device Manager.
    Locally keep track of connected devices.
    """

    def __init__(self, db_location, on_request_callback=None, device_uuid=None):
        """Start DeviceManager.

        Args:
            db_location (str): Uri db file location.
            on_request_callback (function, optional): Add a on_request callback. Defaults to None.
            device_uuid (str, optional): User ID or UUID. Defaults to None.
        """
        LOG.info("Starting Device Manager.")
        self.db_location = db_location  # local file to persist data, can implement sql or else
        self.devices = set()  # Unique elements only
        self.__parse_db_location_local_file()
        self.on_request_callback = on_request_callback
        self.device_uuid = device_uuid
        LOG.info("Started Device Manager.")

    def __repr__(self):
        """Device manager repr."""
        return f'DeviceManager: {len(self.devices)} active devices'

    def __read_local_file(self):
        """Read local file lines into readlines().
        Returns: list of lines in file."""
        try:
            with open(self.db_location, "r") as f:
                lines = f.readlines()
                return lines
        except FileNotFoundError:
            LOG.warning("File not found. Creating...")
            try:
                with open(self.db_location, "w") as f:
                    return []  # Returns empty list
            except Exception:
                LOG.error("Error creating file")
                return []

    def __write_local_file(self, append=False):
        """Write our local file as append.
        append: If true will append content instead of overwriting
        NOTE: This might need some after cleaning of duplicates.
        NOTE: The read is safe because it reads into a set.
        """
        # Verbose syntax to demonstrate operation
        if append:
            op = "a+"
        else:
            op = "w"
        with open(self.db_location, op) as f:
            f.writelines(f"{x}\n" for x in self.devices)

    def __parse_db_location_local_file(self):
        """Parse local file"""
        LOG.debug("Loading device manager file: %s", self.db_location)
        
        local_devices = self.__read_local_file()  # Creates file if doesn't exist

        # No devices in the file (empty)
        if local_devices is None:
            LOG.info("No devices in device manager file: %s", self.db_location)
            return

        # devices in the file (empty)
        if len(local_devices) <= 0:
            LOG.info("No devices in device manager file: %s", self.db_location)
            return

        # Add found devices in file to our local devices set
        for device in local_devices:  # equivalent of: for lines in file
            if str(device) in self.devices:
                LOG.warning("already on device list: %s" % device)
            else:
                self.devices.add(str(device))
                LOG.debug("device added: %s" % device)

        LOG.info("Loaded %i devices in db file: %s", len(self.devices), self.db_location)

    def _add_on_request_callback(self, on_request_callback):
        """Add a on_request function callback"""
        self.on_request_callback = on_request_callback
        LOG.info("added on_request_callback.")

    def _add_device_uuid(self, device_uuid):
        """Add a on_request function callback"""
        self.device_uuid = device_uuid
        LOG.debug("registered device_uuid")

    def is_connected(self, user_id):
        """Checks if the device is registered.

        Args:
            user_id (str): User ID or UUID.

        Returns:
            bool: Returns true if the device is on the Device Manager database.
        """
        return user_id in self.devices

    def add_device(self, user_id):
        """Adding appends user to local set and writes to file.

        Args:
            user_id (str): User ID or UUID.

        Returns:
            bool: Returns true if the device was added to the Device Manager database.
        """
        # Check if user is connected
        if not self.is_connected(user_id):
            self.devices.add(user_id)
            self.__write_local_file() 
            LOG.debug("Added device to device list: %s", user_id)
            return True
        LOG.debug("Device already in device list: %s", user_id)
        return False

    def remove_device(self, user_id):
        """Removing deletes a user from local set and writes to file.

        Args:
            user_id (str): User ID or UUID.

        Returns:
            bool: Returns true if the device was removed from the Device Manager database.
        """
        # Removing involves reading local file first to see if there were any changes
        # devices that we don't have into our devices.
        # Then we remove the devices that we want and overwrite the file.

        # Check if user is connected
        if self.is_connected(user_id):
            self.__read_local_file()
            self.devices.remove(user_id)
            self.__write_local_file()
            LOG.debug("Removed device from device list: %s", user_id)
            return True
        LOG.debug("Device not in device list: %s", user_id)
        return False

    def get_devices(self):
        """Returns list of registered devices.

        Returns:
            list: devices loaded in the Device Manager database.
        """
        return list(self.devices)
