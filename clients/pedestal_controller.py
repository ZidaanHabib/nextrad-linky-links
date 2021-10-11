from clients.gps_client import GPSClient
from types.gps_location import GPSLocation
from clients.hand_controller_serial_client import SynscanSerialClient
from interfaces.serial_interface import SerialInterface
from configparser import ConfigParser


class PedestalController:

    def __init__(self, serial_client: SerialInterface, gps_client):
        self._serial_client = serial_client
        self._gps_client = gps_client

        self._location: GPSLocation = gps_client.get_location()
        self._altitude: float = gps_client.get_altitude()

        self._az_offset: float = self._serial_client.get_azimuth()
        self._el_offset: float = self._serial_client.get_elevation()

        self.az_current = 0.0
        self.el_Current = 0.0

        self._az_limits = [-1, -1]
        self._el_limits = [-1, -1]
        self._slew_rate_limit = 100000

    def set_location(self, latitude: float, lat_dir: chr, longitude: float, long_dir: chr) -> None:
        """ Manually set location if GPS device not funcitonning correctly"""
        self._location = GPSLocation(latitude, lat_dir, longitude, long_dir)

    def set_altitude(self, altitude: float):
        """ Manually set altitude if GPS device not functioning correctly"""
        self._altitude = altitude

    def set_az_limits(self, az_limit: [float]):
        self._az_limits = az_limit

    def set_el_limits(self, el_limits: [float]):
        self._el_limits = el_limits

    def set_slew_rate_limit(self, limit: float):
        self._slew_rate_limit = limit

