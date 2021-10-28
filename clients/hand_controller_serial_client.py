import time

import serial
#from interfaces.connection_interface import ConnectionInterface
from time import sleep
from threading import Lock
from clients.serial_connection import SerialConnection
from interfaces.controller_interface import IControllerInterface

class SynscanSerialClient(IControllerInterface):

    def __init__(self, connection: SerialConnection ):
        super(SynscanSerialClient, self).__init__()
        self._serial_connection = connection

    def calibrate_command(self):
        self._serial_connection.send_command("P" + chr(4) + chr(16) +
                                         chr(4) + chr(0) + chr(0) +
                                         chr(0) + chr(0))  # manufacturer command to set current azimuth as 0
        self._serial_connection.send_command("P" + chr(4) + chr(17) +
                                         chr(4) + chr(0) + chr(0) +
                                         chr(0) + chr(0))  # manufacturer command to set current elevation as 0

    def goto_az_el(self, azimuth: float, elevation: float):
        hex_azimuth = hex(round(azimuth * (16777216 / 360)))[2:]  # from datasheet, also ignore '0x'
        hex_elevation = hex(round(elevation * (16777216 / 360)))[2:]
        hex_elevation = hex_elevation.upper()  # convert to uppercase
        hex_azimuth = hex_azimuth.upper()  # convert to uppercase
        if (len(hex_azimuth) < 6):
            hex_azimuth = "0" * (6 - len(hex_azimuth)) + hex_azimuth
        if (len(hex_elevation) < 6):
            hex_elevation = "0" * (6 - len(hex_elevation)) + hex_elevation

        cmd: str = "b" + hex_azimuth + "00" + "," + hex_elevation + "00"
        self._serial_connection.send_command(cmd)

    def is_goto(self):
        response = self._serial_connection.communicate("L")
        response = response[0:-1]
        print("response: " + response)
        moving: bool = False
        if response == "0":
            moving = False
        elif response == "1":
            moving = True

        return moving

    def slew_positive_fixed(self, axis, preset):  #axis == 1: azimuth, 2: elevation
        axis_char = ""
        if axis == 1:
            axis_char = chr(16)
        else:  # axis = 2
            axis_char = chr(17)
        msg: str = "P" + chr(2) + axis_char + chr(36) + chr(preset) + chr(0) * 3
        self._serial_connection.communicate(msg)

    def slew_negative_fixed(self, axis: int, preset: int):
        axis_char = ""
        if axis == 1:
            axis_char = chr(16)
        else:  # axis = 2
            axis_char = chr(17)
        msg: str = "P" + chr(2) + axis_char + chr(37) + chr(preset) + chr(0) * 3
        self._serial_connection.send_command(msg)

    def slew_positive_specific(self, axis: chr, slew_rate: float, azimuth_diff, elevation_diff ):  # rate is in arcseconds per sec
        """Slew in positive direction at a specific rate in arcseconds per sec"""
        slew_rate_whole = int((slew_rate * 4) // 256)
        slew_rate_rem = int((slew_rate * 4) % 256)
        axis_char = ""
        wait = 0
        if axis == 1:  # azimuth axis
            axis_char = chr(16)
            wait = azimuth_diff / (slew_rate * 0.000277778)  # 1 arcsec/sec = 0.000277778  degrees/sec
        else:  # axis = 2  , elevation axis
            axis_char = chr(17)
            wait = elevation_diff / (slew_rate * 0.000277778)
        cmd = "P" + chr(3) + axis_char + chr(6) + chr(slew_rate_whole) + chr(slew_rate_rem) + chr(0) * 2
        time.sleep(wait)
        self.stop_slew(axis)


    def slew_negative_specific(self, axis: chr, slew_rate: float,  azimuth_diff, elevation_diff ):  # rate is in arcseconds per sec
        """Slew in negative direction at a specific rate in arcseconds per sec"""
        slew_rate_whole = int((slew_rate * 4) // 256)
        slew_rate_rem = int((slew_rate * 4) % 256)
        axis_char = ""
        wait = 0
        if axis == 1:  # azimuth axis
            axis_char = chr(16)
            wait = azimuth_diff / (slew_rate * 0.000277778)  # 1 arcsec/sec = 0.000277778  degrees/sec
        else:  # axis = 2  , elevation axis
            axis_char = chr(17)
            wait = elevation_diff / (slew_rate * 0.000277778)
        cmd = "P" + chr(3) + axis_char + chr(7) + chr(slew_rate_whole) + chr(slew_rate_rem) + chr(0) * 2
        time.sleep(wait)
        self.stop_slew(axis)

    def stop_slew(self, axis):
        axis_char = ""
        if axis == 1:
            axis_char = chr(16)
        else:  # axis = 2
            axis_char = chr(17)
        msg = "P" + chr(2) + axis_char + chr(36) + chr(0) + chr(0) * 3
        self._serial_connection.send_command(msg)

    """def set_tracking(self, mode):
        msg = "T" + str(mode)
        self._serial_connection.send_command(msg)"""

    def slew_step(self, axis, direction, slew_rate):
        """ Method to slew pedestal by 1 degree"""
        slew_rate_whole = int((slew_rate * 4) // 256)
        slew_rate_rem = int((slew_rate * 4) % 256)
        delay = 3600.0/slew_rate   # 3600 arcsec = 1 degree

        axis_char = ""
        dir_char = ""

        if axis == 1:  # azimuth axis
            axis_char = chr(16)
        else:  # axis = 2 , # elevation axis
            axis_char = chr(17)
        if dir == 1:  # positive dir, cw
            axis_char = chr(6)
        else:  # axis = 2  # negative dir, ccw
            axis_char = chr(7)

        cmd = "P" + chr(3) + axis_char + dir_char + chr(slew_rate_whole) + chr(slew_rate_rem) + chr(0) * 2
        self._serial_connection.send_command(cmd)
        time.sleep(delay)
        self.stop_slew(axis)


    def get_azimuth(self) -> str:
        """response = self._serial_connection.communicate("z")
        az_string = response.split(",")[0]  # get the azimuth portion of controller response
        az_string = az_string[0:-2] #ignore last 2 chars as per datasheet
        az = float.fromhex(az_string)  # convert from hex string to decimal number
        az = round((az/16777216)*360, 2)  # convert to degrees"""

        response = self._serial_connection.communicate("Z")
        az_string = response.split(",")[0]  # get the azimuth portion of controller response
        az_string += "00"  # append 2 trailing zeros because 24 bit number

        return az_string

    def get_elevation(self) -> str:
        """response = self._serial_connection.communicate("z")
        el_string = response.split(",")[1]  # get the azimuth portion of controller response
        el_string = el_string[0:-3]  # ignore last 2 chars as per datasheet as well as '#'
        el = float.fromhex(el_string)  # convert from hex string to decimal number
        el = round((el / 16777216) * 360,2)  # convert to degrees
        return el"""
        response = self._serial_connection.communicate("Z")
        el_string = response.split(",")[1]  # get the azimuth portion of controller response
        el_string = el_string[0:-1]
        el_string += "00"  # append 2 trailing zeros because 24 bit number
        return el_string



if __name__ == "__main__":
    sc = SynscanSerialClient(SerialConnection())
    sc.slew_negative_fixed(1, 9)
    sleep(5)
    sc.stop_slew(1)
    response = sc.get_azimuth()
    print(response)