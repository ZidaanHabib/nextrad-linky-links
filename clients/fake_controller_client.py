from interfaces.controller_interface import ControllerInterface
from time import sleep
import random


class FakeControllerClient(ControllerInterface):
    """Fake controller used for development and testing purposes"""

    def __init__(self):
        pass

    def slew_positive_fixed(self, axis, slew_rate_preset):  #axis == 1: azimuth, 2: elevation
        print("< Slew positive fixed> ")

    def slew_negative_fixed(self, axis: int, slew_rate_preset: int):
        print("< Slew negative fixed> ")

    #def slew_positive_variable(self, rate: float ):


    def stop_slew(self, axis):
        print("<Stopped slewing>")

    def set_tracking(self, mode):
        print("<Set tracking mode to >" + mode)


    def get_azimuth(self) -> float:
        az = random.uniform(180, 360)
        return az

    def get_elevation(self):
        el = random.uniform(180, 360)
        return el

    def communicate(self, cmd: str):
        pass

    def receive_response(self):
        pass

    def send_command(self, cmd: str):
        pass
