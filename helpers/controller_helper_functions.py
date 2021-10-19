import math
from math import sqrt, sin, cos, asin, acos, atan,atan2, radians, degrees


class ControllerMath:
    RADIUS_EARTH = 6371e3

    @staticmethod
    def haversine(source_lat: float, source_long: float, target_lat: float, target_long: float):
        """Calculate distance in metres between 2 coordinates using the haversine formula"""
        source_lat = radians(source_lat)
        source_long = radians(source_long)
        target_lat = radians(target_lat)
        target_long = radians(target_long)

        delta_lat = abs(source_lat - target_lat)
        delta_long = abs(source_long - target_long)

        distance = 2*ControllerMath.RADIUS_EARTH*asin(sqrt(sin(delta_lat/2)**2  + cos(source_lat)*cos(target_lat)
                                                    *sin(delta_long/2)**2 ))

        return distance

    @staticmethod
    def determine_azimuth_difference(source_lat: float, source_long: float, target_lat: float, target_long: float):
        source_lat = radians(source_lat)
        source_long = radians(source_long)
        target_lat = radians(target_lat)
        target_long = radians(target_long)

        delta_lat = source_lat - target_lat
        delta_long = target_long - source_long

        azimuth = atan2((cos(target_lat)*sin(delta_long)),(cos(source_lat)*sin(target_lat) - sin(source_lat)*cos(target_lat)*cos(delta_long)))
        azimuth_degrees = degrees(azimuth) # add 180 degrees to reverse from source to dest
        return azimuth_degrees

    @staticmethod
    def determine_elevation_difference(source_alt: float, target_alt: float, distance):
        delta_height = source_alt - target_alt
        elevation_degrees = degrees(atan(delta_height/distance))
        return elevation_degrees



if __name__ == "__main__":
    print(ControllerMath.determine_azimuth_difference(40.4970900,-74.9159100, 41.68112, -75.83867))