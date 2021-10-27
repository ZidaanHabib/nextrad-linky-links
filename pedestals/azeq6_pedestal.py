from interfaces.pedestal_device_interface import IPedestalDevice
from interfaces.connection_interface import ControllerInterface
from clients.pedestal_controller import PedestalController
from helpers.controller_helper_functions import ControllerMath
#testing:
from clients.hand_controller_serial_client import SynscanSerialClient
from clients.fake_gps_client import FakeGPSClient
from clients.fake_controller_client import FakeControllerClient
import time
import os
from threading import Thread
from clients.hand_controller_serial_client import SynscanSerialClient
from dtypes.gps_location import GPSLocation
from configparser import ConfigParser


class AZEQ6Pedestal(IPedestalDevice): #TODO add IPedestalDevice inheritance

    def __init__(self, sc: SynscanSerialClient, gps_client):
        #  client members:
        self._serial_client = sc
        self._gps_client = gps_client

        self._cf = ConfigParser()  # means of reading from config file
        self._cf.read("config.ini")

        #  geographic information:
        self._az_offset: float = float(self._cf["Navigation"]["True_North_Offset"])
        self._el_offset: float = float(self._cf["Navigation"]["Horizontal_Offset"])
        self._location: GPSLocation = gps_client.get_location()
        self._altitude: float = gps_client.get_altitude()

        self._az_limits: [float] = [float(self._cf["Constraints"]["MinAzimuth"]), float(self._cf["Constraints"]["MaxAzimuth"])]
        self._el_limits: [float] = [float(self._cf["Constraints"]["MinElevation"]), float(self._cf["Constraints"]["MaxElevation"])]
        self._slew_rate_limit: float = float(self._cf["Constraints"]["MaxSlewRate"])

        self._slew_rate = 150.0  #arcsec/sec
        self._slew_preset = 9

        self._moving = False

    def calibrate(self):
        """ Set current azimuth and elevation to be the 0,0 point"""
        self._serial_client.calibrate_command()

    def slew_to_location(self, target_lat, target_long, target_altitude):
        """ Method to slew to a target location entered in latitude and longitude"""
        src_lat = self._location.get_latitude()
        src_long = self._location.get_longitude()

        distance = ControllerMath.haversine(src_lat, src_long, target_lat, target_long)   # calculate distance between
                                                                                         # locations
        src_altitude = self._altitude
        elevation_diff = ControllerMath.determine_elevation_difference(src_altitude, target_altitude, distance)
        azimuth_diff = ControllerMath.determine_azimuth_difference(src_lat, src_long, target_lat, target_long)

        #  now we need to account for where the pedestal is already pointing:
        azimuth_final = 360 - (azimuth_diff + self._az_offset)
        elevation_final = 360 - (elevation_diff + self._el_offset)

        self.slew_to_az_el(round(azimuth_final), round(elevation_final))  # move

    def slew_positive_specific(self, axis: int, rate: float):
        if self.is_moving():  # make sure pedestal not already moving
            self.stop_slew(axis)  # stop pedestal if already moving
        self.set_moving(True)

        slew_rate = rate if rate <= self._slew_rate_limit else self._slew_rate_limit

        azimuth_diff = abs(self.get_azimuth() - self._az_limits[1])
        if azimuth_diff > 180:
            azimuth_diff = 360 - azimuth_diff

        elevation_diff = abs(self.get_elevation() - self._el_limits[1])
        if elevation_diff > 180:
            elevation_diff = 360 - elevation_diff

        self._serial_client.slew_positive_specific(axis, slew_rate, azimuth_diff, elevation_diff)

    def slew_positive_preset(self, axis):  #axis == 1: azimuth, 2: elevation
        if self._moving:  # make sure pedestal not already moving
            self.stop_slew(axis)  # stop pedestal if already moving
        self.set_moving(True)
        self._serial_client.slew_positive_fixed(axis, self._slew_preset)

    def slew_negative_preset(self, axis: int):
        if self.is_moving():  # make sure pedestal not already moving
            self.stop_slew(axis)  # stop pedestal if already moving
        self.set_moving(True)
        self._serial_client.slew_negative_fixed(axis, self._slew_preset)

    def slew_negative_specific(self, axis: int, rate: float):
        if self.is_moving():  # make sure pedestal not already moving
            self.stop_slew(axis)  # stop pedestal if already moving
        self.set_moving(True)

        slew_rate = rate if rate <= self._slew_rate_limit else self._slew_rate_limit

        azimuth_diff = abs(self.get_azimuth() - self._az_limits[1])
        if azimuth_diff > 180:
            azimuth_diff = 360 - azimuth_diff

        elevation_diff = abs(self.get_elevation() - self._el_limits[1])
        if elevation_diff > 180:
            elevation_diff = 360 - elevation_diff

        self._serial_client.slew_negative_specific(axis, slew_rate, azimuth_diff, elevation_diff)


    def stop_slew(self, axis: int):
        self._serial_client.stop_slew(axis)
        #self._pedestal_controller.set_moving(False)  #update moving status to false

    def slew_to_az_el(self, azimuth: float, elevation: float):
        if azimuth < 0:
            while azimuth < 0:
                azimuth += 360
        if elevation < 0:
            while elevation < 0:
                elevation += 360
        self._serial_client.goto_az_el(azimuth, elevation)

    def get_azimuth(self) -> float:
        az_string = self._serial_client.get_azimuth()
        az = float.fromhex(az_string)  # convert from hex string to decimal number
        az = round((az/16777216)*360, 2)  # convert to degrees
        return az

    def get_elevation(self):
        el_string = self._serial_client.get_elevation()
        el = float.fromhex(el_string)  # convert from hex string to decimal number
        el = round((el / 16777216) * 360, 2)  # convert to degrees
        if el >= 180:
            el = -1*(360 - el)  # use negative degrees instead
        return el

    def is_slew_az_el(self) -> bool:
        return self._serial_client.is_goto()

    def sweep_thread(self, stop_sweep):
        """ Method to continously sweep pedestal between the 2 azimuth limits"""
        elevation = self.get_elevation()
        azimuth = self.get_azimuth()
        #  Stop pedestal if already moving:
        self.stop_slew(1)
        self.stop_slew(2)

        az_min = self._az_limits[0]
        az_max = self._az_limits[1]
        delay = (az_max - az_min) / 3.1  # goto speed is approx 3 deg/sec
        if azimuth not in [az_min, az_max]:  # if current pos not in range, go to the max az to start sweep
            self.slew_to_az_el(az_max, elevation)
        while not stop_sweep:
            self.slew_to_az_el(self._az_limits[0], elevation)
            time.sleep(delay)
            self.slew_to_az_el(self._az_limits[1], elevation)

    def sweep_off(self):
        global stop_sweep
        stop_sweep = True  # stop sweep thread
        self.stop_slew(1)
        self.stop_slew(2)

    def sweep_on(self):
        global stop_sweep
        stop_sweep = False
        sweep_thread = Thread(target=self.sweep_thread, args=[stop_sweep])
        sweep_thread.daemon = True
        sweep_thread.start()

    """Setter methods"""
    def set_moving(self, status: bool):
        self._moving = status

    """Setter methods: """

    def set_location(self, latitude: float, lat_dir: chr, longitude: float, long_dir: chr) -> None:
        """ Manually set location if GPS device not functioning correctly"""
        self._location = GPSLocation(latitude, lat_dir, longitude, long_dir)  #TODO fix type

    def set_altitude(self, altitude: float) -> None:
        """ Manually set altitude if GPS device not functioning correctly"""
        self._altitude = altitude

    def set_az_limits(self, az_limit: [float]) -> None:
        """ Set azimuth limits for pedestal"""
        self._az_limits = az_limit
        #self._cf["Constraints"]["MinAzimuth"] = str(az_limit[0])
        #self._cf["Constraints"]["MinAzimuth"] = str(az_limit[1])
        # self.update_config_file()  # write changes back to config file

    def set_el_limits(self, el_limits: [float]) -> None:
        """ Set elevation limits for pedestal"""
        self._el_limits = el_limits
        # self.update_config_file()  # write changes back to config file

    def set_slew_rate_limit(self, limit: float) -> None:
        """ Set slew rate limits for pedestal"""
        self._slew_rate_limit = limit

    def set_slew_rate(self, rate):
        self._slew_rate = rate

    def set_slew_preset(self, preset):
        self._slew_preset = preset

    """Getter methods:"""

    def get_location_str(self):
        """ Method to return string representation of location"""
        return self._location.__repr__()

    def get_location(self):
        """Return instance location object """
        return self._location

    def get_altitude(self):
        return self._altitude

    def get_azimuth_limits(self):
        return self._az_limits

    def is_moving(self) -> bool:
        return self._moving

    def get_slew_preset(self):
        return self._slew_preset

    def get_tn_offset(self):
        """ MEthod to return true north offset"""
        return self._az_offset

    def get_horizontal_offset(self):
        return self._el_offset

if __name__ == "__main__":

    os.chdir("../")
    sc = SynscanSerialClient()
    pc = PedestalController(sc, FakeGPSClient())
    az = AZEQ6Pedestal(pc, sc)
   #pc.set_az_limits([0,30])
    #print(pc.get_azimuth_limits())
    print("Azimuth: " + str(az.get_azimuth()))
    print("Elevation: " + str(az.get_elevation()))
    #)
    #print(az.is_moving())
    #az.slew_positive_fixed(1)
    #print(az.is_slew_az_el())
    #time.sleep(1)
    #az.stop_slew(1)
    #print(az.is_moving())
    #print(sc.get_azimuth())
    #time.sleep(5)
    #az._serial_client.send_command("B12AB,12AB")
    """az.sweep_on()
    time.sleep(30)
    az.sweep_off()"""
    az.slew_to_az_el(180,0)