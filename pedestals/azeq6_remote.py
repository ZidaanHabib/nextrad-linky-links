from interfaces.pedestal_remote_interface import IPedestalRemote
from interfaces.controller_interface import ControllerInterface
from clients.pedestal_controller import PedestalController
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



    def slew_cw(self):
        pass

    def slew_ccw(self):
        pass


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
        print(cmd)


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
        return el

    def is_slew_az_el(self) -> bool:
        response = self._serial_client.communicate("L")
        moving: bool = int(response[0:-1])
        return moving

    def sweep_thread(self, stop_sweep):
        """ Method to continously sweep pedestal between the 2 azimuth limits"""
        elevation = self._pedestal_controller.get_elevation()
        #  Stop pedestal if already moving:
        """self.stop_slew(1)
        self.stop_slew(2)
        #  make this a threaded function:
        sweep_thread = Thread(target=self.sweep_on)
        Thread.daemon = True
        Thread.start()
        while not stop_sweep:
            while self.is_slew_az_el():
                pass   # block if already moving
            self.slew_to_az_el(self._pedestal_controller.get_azimuth_limits()[0], elevation)  # when stopped slewing, go to min azimuth
            while self.is_slew_az_el():
                pass  # block if already moving
            self.slew_to_az_el(self._pedestal_controller.get_azimuth_limits()[1],elevation )  # when stopped slewing, go to min azimuth"""

        while True:
            print("hello\n")
            if stop_sweep:
                break

    def sweep_off(self):
        global stop_sweep
        stop_sweep = True  # stop sweep thread
        #self.stop_slew(1)
        #self.stop_slew(2)

    def sweep_on(self):
        global stop_sweep
        stop_sweep = False
        sweep_thread = Thread(target=self.sweep_thread, args=[stop_sweep])
        sweep_thread.daemon = True
        sweep_thread.start()


if __name__ == "__main__":

    os.chdir("../")
    sc = FakeControllerClient()
    pc = PedestalController(sc, FakeGPSClient())
    az = AZEQ6Remote(pc, sc)

    #print("Azimuth: " + str(az.get_azimuth()))
    #print("Elevation: " + str(az.get_elevation()))
    #az.slew_to_az_el(10,10)
    #print(az.is_moving())
    #az.slew_positive_fixed(1)
    #print(az.is_slew_az_el())
    #time.sleep(1)
    #az.stop_slew(1)
    #print(az.is_moving())
    #print(sc.get_azimuth())
    #time.sleep(5)
    #az._serial_client.send_command("B12AB,12AB")
    '''sweep_thread = Thread(target=az.sweep_on)
    sweep_thread.daemon = True
    sweep_thread.start()'''
    az.sweep_on()
    time.sleep(2)
    az.sweep_off()