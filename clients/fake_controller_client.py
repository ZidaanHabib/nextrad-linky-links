from interfaces.controller_interface import IControllerInterface
from time import sleep
import random


class FakeControllerClient(IControllerInterface):
    """Fake controller used for development and testing purposes"""

    def __init__(self):
        pass

    def calibrate_command(self):
        """ Fake calibration command """

        print(" Fake calibrating command from FakeControllerClient")  # manufacturer command to set current elevation as 0

    def goto_az_el(self, azimuth: float, elevation: float):
        """ Fake goto command"""
        print("going to Az:{} , El:{} from FakeControllerClient".format(azimuth, elevation))

    def is_goto(self):
        """ Fake is_goto command """

        print("Fake is_goto command from FakeControllerClient ")

    def slew_fixed(self, axis, preset, dir):  #axis == 1: azimuth, 2: elevation
        print("slew positive fixed command")

    def slew(self, axis: chr, slew_rate: float, dir: chr):  # rate is in arcseconds per sec
        """ Fake slew command """

        print("Fake slew command from FakeControllerClient")

    def stop_slew(self, axis):
        """ Fake stop command """
        print("Fake stop slew command from FakeControllerClient")

    def slew_step(self, axis, direction, slew_rate):
        """ """
        print("Slewing 1 degree")


    def get_azimuth(self) :
        """ Fake get_azimuth command """

        print("fake get azimuth command from FakeControllerClient")
        return "000000"  # return dummy value


    def get_elevation(self) :
        """ Fake get_elevation command"""

        print("Fake get elevation command from FakeControllerClient")
        return "000000"
