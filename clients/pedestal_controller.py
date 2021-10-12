from clients.gps_client import GPSClient
from dtypes.gps_location import GPSLocation
from clients.hand_controller_serial_client import SynscanSerialClient
from interfaces.serial_interface import SerialInterface
from configparser import ConfigParser
import os


class PedestalController:

    def __init__(self, serial_client: SerialInterface, gps_client):
        self._serial_client = serial_client
        self._gps_client = gps_client

        self._location: GPSLocation = gps_client.get_location()
        self._altitude: float = gps_client.get_altitude()

        self._az_offset: float = self._serial_client.get_azimuth()
        self._el_offset: float = self._serial_client.get_elevation()

        self._az_current = 0.0
        self._el_current = 0.0

        self._az_limits = [-1, -1]
        self._el_limits = [-1, -1]
        self._slew_rate_limit = 100000

    def controller_init(self) -> None:
        self._cf = ConfigParser("config.ini")
        self._az_limits = [self._cf["Constraints"]["MinAzimuth"], self._cf["Constraints"]["MaxAzimuth"]]
        self._el_limits = [self._cf["Constraints"]["MinElevation"], self._cf["Constraints"]["MaxElevation"]]
        self._slew_rate_limit = self._cf["Constraints"]["MaxSlewRate"]

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

    def set_el_limits(self, el_limits: [float]) -> None:
        """ Set elevation limits for pedestal"""
        self._el_limits = el_limits

    def set_slew_rate_limit(self, limit: float) -> None:
        """ Set slew rate limits for pedestal"""
        self._slew_rate_limit = limit

    """Getter methods:"""
    def get_location(self):
        return self._location.__repr__()

    def get_azimuth(self):
        return self._az_current

    def get_elevation(self):
        return self._el_current


if __name__ == "__main__":
    print("hello")
    print(os.getcwd())

