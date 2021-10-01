
class GPSLocation:

    def __init__(self, latitude: float,lat_direction: chr, longitude: float, long_direction: chr ):
        self._latitude = latitude
        self._lat_direction = lat_direction
        self._longitude = longitude
        self._long_direction = long_direction

    def get_latitude(self):
        """ Method to get latitude"""
        return self._latitude

    def get_lat_direction(self):
        """ Method to get latitude direction"""
        return self._lat_direction

    def get_longitude(self):
        """ Method to get longitude"""
        return self._longitude

    def get_long_direction(self):
        """ Method to get longitude direction"""
        return self._long_direction

