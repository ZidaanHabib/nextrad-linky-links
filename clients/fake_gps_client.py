import pynmea2 as nmea
from dtypes.gps_location import GPSLocation
from interfaces.gps_interface import IGPSInterface


class FakeGPSClient(IGPSInterface):

    def get_location(self):
        return GPSLocation(-33.9586853, 18.4601156, 88)


    def get_altitude(self):
        return 88.0

