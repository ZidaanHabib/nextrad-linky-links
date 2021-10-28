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
    def slew_positive_fixed(self, axis, preset):  #axis == 1: azimuth, 2: elevation
        pass

    @abstractmethod
    def slew_negative_fixed(self, axis: int, preset: int):
        pass

    @abstractmethod
    def slew_positive_specific(self, axis: chr, slew_rate: float, azimuth_diff, elevation_diff ):  # rate is in arcseconds per sec
        pass

    @abstractmethod
    def slew_negative_specific(self, axis: chr, slew_rate: float,  azimuth_diff, elevation_diff ):  # rate is in arcseconds per sec
        pass

    @abstractmethod
    def stop_slew(self, axis):
        pass

    @abstractmethod
    def slew_step(self, axis, direction, slew_rate):
        pass

    @abstractmethod
    def get_azimuth(self) -> str:
        pass

    @abstractmethod
    def get_elevation(self) -> str:
        pass