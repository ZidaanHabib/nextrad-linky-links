from interfaces.pedestal_remote_interface import IPedestalRemote
from interfaces.controller_interface import ControllerInterface
from clients.pedestal_controller import PedestalController
from helpers.controller_helper_functions import ControllerMath
#testing:
from clients.hand_controller_serial_client import SynscanSerialClient
from clients.fake_gps_client import FakeGPSClient
from clients.fake_controller_client import FakeControllerClient
import time
import os
from threading import Thread

class AZEQ6Remote(): #TODO add IPedestalRemote inheritance


    def __init__(self, pc: PedestalController, sc: ControllerInterface):
        self._pedestal_controller = pc
        self._serial_client = sc

    def calibrate(self):
        """ Set current azimuth and elevation to be the 0,0 point"""
        self._serial_client.send_command("P" + chr(4) + chr(16) +
                                         chr(4) + chr(0) + chr(0) +
                                         chr(0) + chr(0))  # manufacturer command to set current azimuth as 0
        self._serial_client.send_command("P" + chr(4) + chr(17) +
                                         chr(4) + chr(0) + chr(0) +
                                         chr(0) + chr(0))  # manufacturer command to set current elevation as 0

    def slew_cw(self):
        pass

    def slew_ccw(self):
        pass

    def slew_to_location(self, target_lat, target_long, target_altitude):
        """ Method to slew to a target location entered in latitude and longitude"""
        src_lat = self._pedestal_controller.get_location().get_latitude()
        src_long = self._pedestal_controller.get_location().get_longitude()

        distance = ControllerMath.haversine(src_lat, src_long, target_lat, target_long)   # calculate distance between
                                                                                         # locations
        src_altitude = self._pedestal_controller.get_altitude()
        elevation_diff = ControllerMath.determine_elevation_difference(src_altitude, target_altitude)
        azimuth_diff = ControllerMath.determine_azimuth_difference(src_lat, src_long, target_lat, target_long)

        #  now we need to account for where the pedestal is already pointing:
        azimuth_final = 360 - (azimuth_diff + self._pedestal_controller.get_tn_offset())
        elevation_final = 360 - (elevation_diff + self._pedestal_controller.get_horizontal_offset())

        self.slew_to_az_el(round(azimuth_final), round(elevation_final))  # move

    def slew_positive_fixed(self, axis):  #axis == 1: azimuth, 2: elevation
        if self._pedestal_controller.is_moving():  # make sure pedestal not already moving
            self.stop_slew(axis)  # stop pedestal if already moving
        self._pedestal_controller.set_moving(True)
        axis_char = ""
        if axis == 1:
            axis_char = chr(16)
        else: # axis = 2
            axis_char = chr(17)
        msg: str = "P" + chr(2) + axis_char + chr(36) + chr(self._pedestal_controller.get_slew_preset()) + chr(0)*3
        self._serial_client.communicate(msg)

    def slew_positive_specific(self, axis: int, rate: float):
        if self._pedestal_controller.is_moving():  # make sure pedestal not already moving
            self.stop_slew(axis)  # stop pedestal if already moving
        self._pedestal_controller.set_moving(True)

        slew_rate = rate if rate <= self._pedestal_controller._slew_rate_limit else self._pedestal_controller._slew_rate_limit
        #  separate slew rate into high and low byte according to datasheet:
        #TODO move the below cmd string creation into the hand controller client
        slew_rate_whole = int((slew_rate * 4) // 256)
        slew_rate_rem = int((slew_rate * 4) % 256)

        azimuth_diff = abs(self.get_azimuth() - self._pedestal_controller._az_limits[1])
        if azimuth_diff > 180:
            azimuth_diff = 360 - azimuth_diff
        elevation_diff = abs(self.get_elevation() - self._pedestal_controller._el_limits[1])
        if elevation_diff > 180:
            elevation_diff = 360 - elevation_diff
        #  1 arcsec/sec = 0.000277778  degrees/sec

        axis_char = ""
        wait = 0
        if axis == 1:  # azimuth axis
            axis_char = chr(16)
            wait = azimuth_diff/(slew_rate * 0.000277778)
        else:  # axis = 2  , elevation axis
            axis_char = chr(17)
            wait = elevation_diff / (slew_rate * 0.000277778)
        cmd = "P" + chr(3) + axis_char + chr(6) + chr(slew_rate_whole) + chr(slew_rate_rem) + chr(0)*2
        time.sleep(wait)
        self.stop_slew(axis)




    def slew_negative_fixed(self, axis: int):
        if self._pedestal_controller.is_moving():  # make sure pedestal not already moving
            self.stop_slew(axis)  # stop pedestal if already moving
        self._pedestal_controller.set_moving(True)
        axis_char = ""
        if axis == 1:
            axis_char = chr(16)
        else:  # axis = 2
            axis_char = chr(17)
        msg: str = "P" + chr(2) + axis_char + chr(37) + chr(self._pedestal_controller.get_slew_preset()) + chr(0) * 3
        self._serial_client.send_command(msg)

    def stop_slew(self, axis: int):
        axis_char = ""
        if axis == 1:
            axis_char = chr(16)
        else:  # axis = 2
            axis_char = chr(17)
        msg = "P" + chr(2) + axis_char + chr(36) + chr(0) + chr(0) * 3
        self._serial_client.send_command(msg)
        self._pedestal_controller.set_moving(False)  #update moving status to false

    def slew_to_az_el(self, azimuth: float, elevation: float):
        if azimuth < 0:
            while azimuth < 0:
                azimuth += 360
        if elevation < 0:
            while elevation < 0:
                elevation += 360
        hex_azimuth = hex(round(azimuth*(16777216/360)))[2:]  # from datasheet, also ignore '0x'
        hex_elevation = hex(round(elevation * (16777216 / 360)))[2:]
        hex_elevation =  hex_elevation.upper()  # convert to uppercase
        hex_azimuth = hex_azimuth.upper()   # convert to uppercase
        if (len(hex_azimuth) < 6):
            hex_azimuth = "0"*(6 - len(hex_azimuth)) + hex_azimuth
        if (len(hex_elevation) < 6):
            hex_elevation = "0"*(6 - len(hex_elevation))  + hex_elevation

        cmd: str = "b" + hex_azimuth + "00" + "," + hex_elevation + "00"
        self._serial_client.send_command(cmd)


    def get_azimuth(self) -> float:
        response = self._serial_client.communicate("Z")
        #response = "12AB,12AB#"
        az_string = response.split(",")[0]  # get the azimuth portion of controller response
        az_string += "00"  # append 2 trailing zeros because 24 bit number
        az = float.fromhex(az_string)  # convert from hex string to decimal number
        az = round((az/16777216)*360, 2)  # convert to degrees
        return az

    def get_elevation(self):
        response = self._serial_client.communicate("Z")
        #response = "12AB,12AB#"
        el_string = response.split(",")[1]  # get the azimuth portion of controller response
        el_string = el_string[0:-1]
        el_string += "00"  # append 2 trailing zeros because 24 bit number
        el = float.fromhex(el_string)  # convert from hex string to decimal number
        el = round((el / 16777216) * 360, 2)  # convert to degrees
        if el >= 180:
            el = -1*(360 - el)  # use negative degrees instead
        return el

    def is_slew_az_el(self) -> bool:
        response = self._serial_client.communicate("L")
        #moving: bool = int(response[0:-1])
        response = response[0:-1]
        print("response: " + response)
        moving: bool = False
        if response == "0":
            moving = False
        elif response == "1":
            moving = True

        return moving

    def sweep_thread(self, stop_sweep):
        """ Method to continously sweep pedestal between the 2 azimuth limits"""
        elevation = self._pedestal_controller.get_elevation()
        azimuth = self._pedestal_controller.get_azimuth()
        #  Stop pedestal if already moving:
        self.stop_slew(1)
        self.stop_slew(2)
        #  make this a threaded function:

        """while not stop_sweep:
            while self.is_slew_az_el():
                pass   # block if already moving
                print("blocking")
            self.slew_to_az_el(self._pedestal_controller.get_azimuth_limits()[0], elevation)  # when stopped slewing, go to min azimuth
            print("slewing")
            while self.is_slew_az_el():
                pass  # block if already moving
            self.slew_to_az_el(self._pedestal_controller.get_azimuth_limits()[1],elevation )  # when stopped slewing, go to min azimuth
        print("thread exiting")"""
        az_min = self._pedestal_controller.get_azimuth_limits()[0]
        az_max = self._pedestal_controller.get_azimuth_limits()[1]
        delay = (az_max - az_min) / 3.1  # goto speed is approx 3 deg/sec
        if azimuth not in [az_min, az_max]: #if current pos not in range, go to the max az to start sweep
            self.slew_to_az_el(az_max, elevation)
        while not stop_sweep:
            self.slew_to_az_el(self._pedestal_controller.get_azimuth_limits()[0], elevation)
            time.sleep(delay)
            self.slew_to_az_el(self._pedestal_controller.get_azimuth_limits()[1], elevation)




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

    def sweep_test(self):
        elevation = self._pedestal_controller.get_elevation()
        az_min = self._pedestal_controller.get_azimuth_limits()[0]
        az_max = self._pedestal_controller.get_azimuth_limits()[1]
        delay = (az_max - az_min)/3.1  # goto speed is approx 3 deg/sec
        try:
            while True:
                self.slew_to_az_el(self._pedestal_controller.get_azimuth_limits()[0], elevation)
                time.sleep(delay)
                self.slew_to_az_el(self._pedestal_controller.get_azimuth_limits()[1], elevation)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":

    os.chdir("../")
    sc = SynscanSerialClient()
    pc = PedestalController(sc, FakeGPSClient())
    az = AZEQ6Remote(pc, sc)
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