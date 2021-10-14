import pynmea2 as nmea
from dtypes.gps_location import GPSLocation

class FakeGPSClient:

    def get_location(self):
