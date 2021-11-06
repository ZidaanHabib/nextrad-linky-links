"""Interfaces:"""
import threading

from interfaces.pedestal_device_interface import IPedestalDevice
from interfaces.connection_interface import ConnectionInterface
from interfaces.controller_interface import IControllerInterface
from interfaces.gps_interface import IGPSInterface
"""Clients:"""
from clients.pedestal_controller import PedestalController
from clients.hand_controller_serial_client import SynscanSerialClient
from clients.fake_gps_client import FakeGPSClient
from clients.fake_controller_client import FakeControllerClient

from helpers.controller_helper_functions import ControllerMath
#testing:
from dtypes.gps_location import GPSLocation
from configparser import ConfigParser
import time
import timeit
import os
from threading import Thread



class AZEQ6Pedestal(IPedestalDevice):

    def __init__(self, sc: IControllerInterface, gps_client:IGPSInterface):
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

        self._az_limits = []
        self._el_limits = []
        self.initialise_axes_limits()
        self._slew_rate_limit: float = float(self._cf["Constraints"]["MaxSlewRate"])

        self._slew_rate = 5   #degrees/sec
        self._slew_preset = 9

        self._moving = False
        self._DEBUG = False

    def initialise_axes_limits(self):
        """Read limits from config file, and check if they are negative"""
        self._az_limits: [float] = [float(self._cf["Constraints"]["MinAzimuth"]),
                                    float(self._cf["Constraints"]["MaxAzimuth"])]
        self._el_limits: [float] = [float(self._cf["Constraints"]["MinElevation"]),
                                    float(self._cf["Constraints"]["MaxElevation"])]
        for i in range(2):
            if self._az_limits[i] < 0:
                self._az_limits[i] = self._az_limits[i] + 360
            if self._el_limits[i] < 0:
                self._el_limits[i] = self._el_limits[i] + 360

    def calibrate(self):
        """ Set current azimuth and elevation to be the 0,0 point"""
        self._serial_client.calibrate_command()

    """Slewing methods: """
    def slew_to_az_el(self, azimuth: float, elevation: float):
        """ Method to slew to specific azimuth and elevation coordinates """

        start_time = timeit.default_timer()

        if azimuth < 0:
            while azimuth < 0:
                azimuth += 360
        if elevation < 0:
            while elevation < 0:
                elevation += 360
        if azimuth in range (int(self._az_limits[0]), int(self._az_limits[1])) or elevation in range(int(self._el_limits[0]), int(self._el_limits[1])):
            print("Target position out of specified limits.")
        else:
            self._serial_client.goto_az_el(azimuth, elevation)

        end_time = timeit.default_timer()
        if self._DEBUG:
            exec_time = (end_time - start_time)
            print("Time:{}".format(exec_time))
            return exec_time

    def slew_to_location(self, target_lat, target_long, target_altitude):
        """ Method to slew to a target location entered in latitude and longitude"""

        start_time = timeit.default_timer()

        src_lat = self._location.get_latitude()
        src_long = self._location.get_longitude()


        distance = ControllerMath.haversine(src_lat, src_long, target_lat, target_long)   # calculate distance between locations

        src_altitude = self._altitude
        elevation_diff = ControllerMath.determine_elevation_difference(src_altitude, target_altitude, distance)
        azimuth_diff = ControllerMath.determine_azimuth_difference(src_lat, src_long, target_lat, target_long)

        #  now we need to account for where the pedestal is already pointing:

        azimuth_final = azimuth_diff - self._az_offset
        elevation_final = elevation_diff - self._el_offset

        self.slew_to_az_el(round(azimuth_final, 2), round(elevation_final, 2))  # move

        end_time = timeit.default_timer()
        if self._DEBUG:
            exec_time = (end_time - start_time)
            print("Time:{}".format(exec_time))
            return exec_time

    def slew_thread(self, axis: int, dir: int):  # threaded method
        """ Threaded method to slew until limit is reached """
        if axis == 1:
            current_position = self.get_azimuth()
            if dir == 1:
                final_position = self._az_limits[1]
            else:
                final_position = self._az_limits[0]
        else:
            current_position = self.get_elevation()
            if dir == 1:
                final_position = self._el_limits[1]
            else:
                final_position = self._el_limits[0]
        diff = abs(current_position - final_position)
        wait = diff / self._slew_rate  # gives the number of seconds to delay before stopping slew
        slew_rate = self._slew_rate*3600  # convert degrees/sec to arcsec/sec
        self._serial_client.slew(axis, slew_rate, dir)
        time.sleep(wait)
        if self.is_moving():
            self.stop_slew(axis)
        else:
            pass

    def slew(self, axis, dir):
        """ Starts the slew thread"""
        start_time = timeit.default_timer()
        if self.is_moving():  # make sure pedestal not already moving
            self.stop_slew(axis)  # stop pedestal if already moving

        slew_thread = threading.Thread(target=self.slew_thread, args=[axis, dir])
        slew_thread.daemon = True

        self.set_moving(True)
        slew_thread.start()

        end_time = timeit.default_timer()
        if self._DEBUG:
            exec_time = (end_time - start_time)
            print("Time:{}".format(exec_time))
            return exec_time

    def slew_preset(self, axis, dir):  #axis == 1: azimuth, 2: elevation
        if self._moving:  # make sure pedestal not already moving
            self.stop_slew(axis)  # stop pedestal if already moving
        self.set_moving(True)
        self._serial_client.slew_fixed(axis, self._slew_preset, dir)


    def stop_slew(self, axis: int):
        """ Stop pedestal """
        start_time = timeit.default_timer()

        self.set_moving(False)
        self._serial_client.stop_slew(axis)
        #self._pedestal_controller.set_moving(False)  #update moving status to false

        end_time = timeit.default_timer()

        if self._DEBUG:
            exec_time = (end_time - start_time)
            print("Time:{}".format(exec_time))
            return exec_time

    #def sweep_thread(self, stop_sweep):
        """ Method to continously sweep pedestal between the 2 azimuth limits"""
        """elevation = self.get_elevation()
        azimuth = self.get_azimuth()
        #  Stop pedestal if already moving:
        self.stop_slew(1)
        self.stop_slew(2)

        az_min = self._az_limits[0]
        az_max = self._az_limits[1]
        delay = (az_max - az_min) / 3.1  # goto speed is approx 3 deg/sec
        if azimuth not in [az_min, az_max]:  # if current pos not in range, go to the max az to start sweep
            self.slew_to_az_el(az_max, elevation)
        while self._moving:
            self.slew_to_az_el(self._az_limits[0], elevation)
            time.sleep(delay)
            self.slew_to_az_el(self._az_limits[1], elevation)"""

    def sweep_thread(self):  # TODO tests this out
        """ Threaded method that continuously sweep back and forth between azimuth limits"""

        azimuth = self.get_azimuth()
        initial_wait = (azimuth - self._az_limits[0])/self._slew_rate
        wait = (self._az_limits[1] - self._az_limits[0]) / self._slew_rate
        slew_rate = self._slew_rate * 3600  # convert to arcsec/sec

        self._serial_client.slew(1, self._slew_rate, 2)  # initially go to smaller limit
        time.sleep(initial_wait)  # delay by time needed to get to lower limit

        while self.is_moving():
            self._serial_client.slew(1, slew_rate, 1)
            time.sleep(wait)
            if self.is_moving():
                self._serial_client.slew(1, slew_rate, 2)

    def sweep_on(self):
        """ Start sweep mode """
        start_time = timeit.default_timer()

        if self._moving:  # make sure pedestal not already moving
            self.stop_slew(1)  # stop pedestal if already moving
            self.stop_slew(2)
        self._moving = True

        sweep_thread = Thread(target=self.sweep_thread)
        sweep_thread.daemon = True
        sweep_thread.start()

        end_time = timeit.default_timer()
        if self._DEBUG:
            exec_time = (end_time - start_time)
            print("Time:{}".format(exec_time))
            return exec_time

    def slew_test(self, axis, dir):  # TODO tests this on the pedestal

        if axis == 1:
            azimuth = self.get_azimuth()
            while self._moving and azimuth < self._az_limits[1]:
                self._serial_client.slew_step(axis, dir, self._slew_rate)
                azimuth = self.get_azimuth()
        else:
            elevation = self.get_elevation()
            while self._moving and elevation < self._el_limits[1]:
                self._serial_client.slew_step(axis, dir, self._slew_rate)
                elevation = self.get_elevation()

    def start_slew_test(self, axis, dir):
        if self.is_moving():  # make sure pedestal not already moving
            self.stop_slew(axis)  # stop pedestal if already moving
        self.set_moving(True)

        thread = Thread(target=self.slew_test, args=[axis, dir])
        thread.daemon = True
        thread.start()

    """Get methods: """

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

    """Setter methods"""
    def set_moving(self, status: bool):
        self._moving = status

    def set_location(self, latitude: float, longitude: float, altitude: float) -> None:
        """ Manually set location if GPS device not functioning correctly"""
        self._location = GPSLocation(latitude, longitude, altitude)

    def set_altitude(self, altitude: float) -> None:
        """ Manually set altitude if GPS device not functioning correctly"""
        self._altitude = altitude

    def set_az_limits(self, az_limits: [float]) -> None:
        """ Set azimuth limits for pedestal and convert to pedestals coordinate system"""
        for i in range(2):
            if az_limits[i] < 0:
                az_limits[i] = az_limits[i] + 360
        self._az_limits = az_limits
        #self._cf["Constraints"]["MinAzimuth"] = str(az_limit[0])
        #self._cf["Constraints"]["MinAzimuth"] = str(az_limit[1])
        # self.update_config_file()  # write changes back to config file

    def set_el_limits(self, el_limits: [float]) -> None:
        """ Set elevation limits for pedestal and convert to pedestals coordinate system"""
        for i in range(2):
            if el_limits[i] < 0:
                el_limits[i] = el_limits[i] + 360
        self._el_limits = el_limits
        # self.update_config_file()  # write changes back to config file

    def set_slew_rate_limit(self, limit: float) -> None:
        """ Set slew rate limits for pedestal"""
        self._slew_rate_limit = limit

    def set_slew_rate(self, rate):  # degrees per sec
        self._slew_rate = rate

    def set_slew_preset(self, preset):
        self._slew_preset = preset

    def set_true_north_offset(self, offset):
        self._az_offset = offset

    def toggle_debug_mode(self):
        self._DEBUG = True

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