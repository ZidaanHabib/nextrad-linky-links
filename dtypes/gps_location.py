
class GPSLocation:

    """def __init__(self, latitude: str, lat_direction: chr, longitude: str, long_direction: chr):
        self._latitude = latitude
        self._lat_direction = lat_direction
        self._longitude = longitude
        self._long_direction = long_direction"""

    def __init__(self, latitude: float, longitude: float, altitude: float ):
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude

    def get_latitude(self):
        """ Method to get latitude"""
        return self._latitude


    def get_longitude(self):
        """ Method to get longitude"""
        return self._longitude

    def __repr__(self):
        """location_string = str(self._latitude) + ", " + self._lat_direction \
        + str(self._longitude) + ", " + self._long_direction"""
        location_string = str(self.get_latitude()) + ", " + str(self.get_longitude())
        return location_string