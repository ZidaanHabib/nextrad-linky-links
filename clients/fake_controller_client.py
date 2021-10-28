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

    def slew_positive_fixed(self, axis, preset):  #axis == 1: azimuth, 2: elevation
        print("slew positive fixed command")

    def slew_negative_fixed(self, axis: int, preset: int):
        print("slew negative fixed command")

    def slew_positive_specific(self, axis: chr, slew_rate: float, azimuth_diff, elevation_diff ):  # rate is in arcseconds per sec
        print("slew positive specific")


    def slew_negative_specific(self, axis: chr, slew_rate: float,  azimuth_diff, elevation_diff ):  # rate is in arcseconds per sec
        print("stop negative specific")

    def stop_slew(self, axis):
        print("stop slew command")


    def get_azimuth(self) -> str:
        print("get azimuth")

    def get_elevation(self) -> str:
        print("get elevation")