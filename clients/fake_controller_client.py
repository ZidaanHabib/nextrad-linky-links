from interfaces.controller_interface import IControllerInterface
from time import sleep
import random


class FakeControllerClient(IControllerInterface):
    """Fake controller used for development and testing purposes"""

    def __init__(self):
        pass
    def calibrate_command(self):
        print("calibrating")  # manufacturer command to set current elevation as 0

    def goto_az_el(self, azimuth: float, elevation: float):
        print("goto command")

    def is_goto(self):
        print("is goto in action ")

    def slew_fixed(self, axis, preset, dir):  #axis == 1: azimuth, 2: elevation
        print("slew positive fixed command")


    def slew(self, axis: chr, slew_rate: float, dir: chr):  # rate is in arcseconds per sec
        print("slewing positive specific")

    def stop_slew(self, axis):
        print("Stop slew")

    def slew_step(self, axis, direction, slew_rate):
        print("Slewing 1 degree")


    def get_azimuth(self) :
        print("get azimuth")
        return "000000"


    def get_elevation(self) :
        print("get elevation")
        return "000000"
