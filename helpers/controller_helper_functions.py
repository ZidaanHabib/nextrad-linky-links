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

        distance = 2*ControllerMath.RADIUS_EARTH*asin(sqrt(sin(delta_lat/2)**2  +
                                                           cos(source_lat)*cos(target_lat)*sin(delta_long/2)**2 ))

        return distance

    @staticmethod
    def determine_azimuth_difference(source_lat: float, source_long: float, target_lat: float, target_long: float):
        """ Method to compute azimuth difference between the source and target location with respect to true north"""
        source_lat = radians(source_lat)
        source_long = radians(source_long)
        target_lat = radians(target_lat)
        target_long = radians(target_long)

        delta_lat = source_lat - target_lat
        delta_long = target_long - source_long

        azimuth = atan2((cos(target_lat)*sin(delta_long)), (cos(source_lat)*sin(target_lat) -
                                                            sin(source_lat)*cos(target_lat)*cos(delta_long)))
        azimuth_degrees = degrees(azimuth) # add 180 degrees to reverse from source to dest
        if azimuth_degrees < 0:
            azimuth_degrees += 360
        return round(azimuth_degrees,2)

    @staticmethod
    def determine_elevation_difference(source_alt: float, target_alt: float, distance):
        """ Method to compute elevation difference between the source and target location"""
        delta_height = source_alt - target_alt
        elevation_degrees = degrees(atan(delta_height/distance))
        return round(elevation_degrees,2)



if __name__ == "__main__":
    #print(ControllerMath.determine_azimuth_difference(-33.9586853, 18.4601156, -33.95898249833889,
     #                                                 18.470658926566475))  # output is correct
    #print(ControllerMath.determine_elevation_difference(88, 15, 973))  # output is correct @ 4.29
    #TODO check if pedestal rotates the long way around when moving to the (360 - 4.29)
    source_lat, source_long = -33.908109924189084, 18.395487481680284  # Twin towers
    target_lat, target_long = -33.90625351007551, 18.394488341295258
    #distance = ControllerMath.haversine(source_lat, source_long, target_lat, target_long)
    az = ControllerMath.determine_azimuth_difference(-33.9586853, 18.4601156, -33.9586853, 18.5000)
    #el = ControllerMath.determine_elevation_difference(4,0,2)
    print(az)