import pynmea2 as nmea
from dtypes.gps_location import GPSLocation


class FakeGPSClient:

    def get_location(self):
        return GPSLocation("33.924869", "S", "18.424055", "E")


    def get_altitude(self):
        return 100.0

