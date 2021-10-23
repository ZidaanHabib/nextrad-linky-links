from clients.gps_client import GPSClient
from dtypes.gps_location import GPSLocation
from clients.hand_controller_serial_client import SynscanSerialClient
from interfaces.controller_interface import ControllerInterface
from configparser import ConfigParser
import os
from helpers.controller_helper_functions import ControllerMath


class PedestalController:

    def __init__(self, serial_client: ControllerInterface, gps_client): #TODO change tye to ControllerInterface or more accurately, IPedestalRemote
        self._serial_client: SynscanSerialClient = serial_client
        self._gps_client: GPSClient = gps_client

        self._location: GPSLocation = gps_client.get_location()
        self._altitude: float = gps_client.get_altitude()

        # DEFAULT VALUES:
        self._az_offset: float = 0
        self._el_offset: float = 0

        self._az_current: float = 0.0
        self._el_current: float = 0.0

        self._cf = ConfigParser()
        self._cf.read("config.ini")

        self._az_limits: [float] = [-1, -1]
        self._el_limits: [float] = [-1, -1]
        self._slew_rate_limit: float = 100000

        self._moving: bool = False
        self._slew_rate_preset: int = 9
        self.controller_init()

    def controller_init(self) -> None:
        self._az_limits = [self._cf["Constraints"]["MinAzimuth"], self._cf["Constraints"]["MaxAzimuth"]]
        self._el_limits = [self._cf["Constraints"]["MinElevation"], self._cf["Constraints"]["MaxElevation"]]
        self._slew_rate_limit = self._cf["Constraints"]["MaxSlewRate"]
        self._az_offset: float = self._serial_client.get_azimuth()
        self._el_offset: float = self._serial_client.get_elevation()

    def update_config_file(self) -> None:
        """ Update config.ini file """
        with open("config.ini", "w") as f:
            self._cf.write(f)

    """Setter methods: """
    def set_location(self, latitude: float, lat_dir: chr, longitude: float, long_dir: chr) -> None:
        """ Manually set location if GPS device not funcitonning correctly"""
        self._location = GPSLocation(latitude, lat_dir, longitude, long_dir)

    def set_altitude(self, altitude: float) -> None:
        """ Manually set altitude if GPS device not functioning correctly"""
        self._altitude = altitude

    def set_az_limits(self, az_limit: [float]) -> None:
        """ Set azimuth limits for pedestal"""
        self._az_limits = az_limit
        self._cf["Constraints"]["MinAzimuth"] = str(self._az_limits[0])
        self._cf["Constraints"]["MinAzimuth"] = str(self._az_limits[1])
        self.update_config_file()  # write changes back to config file


    def set_el_limits(self, el_limits: [float]) -> None:
        """ Set elevation limits for pedestal"""
        self._el_limits = el_limits
        self.update_config_file()  # write changes back to config file

    def set_slew_rate_limit(self, limit: float) -> None:
        """ Set slew rate limits for pedestal"""
        self._slew_rate_limit = limit
        self.update_config_file()  # write changes back to config file

    def set_moving(self, status: bool):
        self._moving = status

    """Getter methods:"""
    def get_location(self):
        return self._location.__repr__()

    def get_azimuth(self):
        return self._az_current

    def get_elevation(self):
        return self._el_current

    def get_azimuth_limits(self):
        return self._az_limits

    def is_moving(self) -> bool:
        return self._moving

    def get_slew_preset(self):
        return self._slew_rate_preset

if __name__ == "__main__":
    print("hello")
    print(os.getcwd())

