from abc import ABC, abstractmethod

class IControllerInterface(ABC):

    @abstractmethod
    def calibrate_command(self):
        pass
    @abstractmethod
    def goto_az_el(self, azimuth: float, elevation: float):
        pass

    @abstractmethod
    def is_goto(self):
        pass

    @abstractmethod
    def slew_fixed(self, axis: chr, preset: int, dir: chr):  #axis == 1: azimuth, 2: elevation
        pass

    @abstractmethod
    def slew(self, axis: chr, slew_rate: float, dir: chr):  # rate is in arcseconds per sec
        pass

    @abstractmethod
    def stop_slew(self, axis):
        pass

    @abstractmethod
    def slew_step(self, axis, direction, slew_rate):
        pass

    @abstractmethod
    def get_azimuth(self) :
        pass

    @abstractmethod
    def get_elevation(self) :
        pass