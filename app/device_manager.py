"""Manage Devices locally in the client side with overlapping UUIDs."""
from logger.logging_config import get_logger

# Set Main Logger
LOG = get_logger()

class DeviceManager():
    
    def __init__(self, db_location):
        self.db_location = db_location # local file to persist data, can implement sql or else
        self.devices = set() # Unique elements only
        self.__parse_db_location_local_file()
        LOG.info("Loaded local device manager")

    def __repr__(self):
        """Device manager repr"""
        return "DeviceManager: {} active devices".format(len(self.devices))

    def __read_local_file(self):
        """Read local file lines into readlines().
        Returns: list of lines in file."""
        try:
            with open (self.db_location, "r") as f:
                lines = f.readlines()
                return lines
        except FileNotFoundError as e:
            LOG.warning("File not found. Creating...")
            try:
                with open (self.db_location, "w") as f:
                    return
            except Exception as e:
                LOG.error("Error creating file")
                return

    def __write_local_file(self, append=False):
        """Write our local file as append.
        append: If true will append content instead of overwriting
        NOTE: This might need some after cleaning of duplicates. The read is safe because it reads into a set.
        """
        # Verbose syntax to demonstrate operation
        if append:
            op = "a+"
        else:
            op = "w"
        with open (self.db_location, op) as f:
            f.writelines(f"{x}\n" for x in self.devices)
        

    def __parse_db_location_local_file(self):
        LOG.debug("Loading device manager file: %s", self.db_location)
        
        local_devices = self.__read_local_file() # Creates file if doesn't exist
        print(local_devices)

        # No devices in the file (empty)
        if len(local_devices) <= 0:
            LOG.info("No devices in device manager file: %s", self.db_location)
            return

        # Add found devices in file to our local devices set
        for device in local_devices: # equivalent of: for lines in file
            if str(device) in self.devices:
                LOG.warning("could not add device: %s" % device)
            else:
                self.devices.add(str(device))
                LOG.debug("device added: %s" % device)

        LOG.info("Loaded %i devices in device manager file: %s", len(self.devices), self.db_location)


    def update_cache(self):
        """Read from local file into our devices"""
        for dev in self.__read_local_file():
            self.devices.add(dev)

    def sync_cache(self):
        """Read from local file into our devices. Then write our version."""
        for dev in self.__read_local_file():
            self.devices.add(dev)
        self.__write_local_file()

    def force_cache(self):
        """Write our version."""
        self.__write_local_file()

    def upgrade_cache(self):
        """Write our version with append."""
        self.__write_local_file(append=True)

    def add_device(self, user_id):
        """user_id: UUID
        returns: Bool True if device was added
        """
        # Adding appends our user to local file.

        # Check if user is connected
        if not self._is_connected(user_id):
            self.devices.add(user_id)
            self.update_cache() # Update local db (append)
            LOG.debug("Added device to device list: %s", user_id)
            return True
        LOG.debug("Device already in device list: %s", user_id)
        return False

    def remove_device(self, user_id):
        """user_id: UUID
        returns: Bool True if device was removed
        """
        # Removing involves reading local file first to see if there were any changes and adding those
        # devices that we don't have into our devices.
        # Then we remove the devices that we want and overwrite the file.

        # Check if user is connected
        if self._is_connected(user_id):
            self.update_cache()  # read
            self.devices.remove(user_id)
            self.force_cache() # Update local db
            LOG.debug("Removed device from device list: %s", user_id)
            return True
        LOG.debug("Device not in device list: %s", user_id)
        return False
    
    def _is_connected(self, user_id):
        return user_id in self.devices
    
    def get_devices(self):
        "Returns list of devices loaded in DeviceManager"
        return list(self.devices)
