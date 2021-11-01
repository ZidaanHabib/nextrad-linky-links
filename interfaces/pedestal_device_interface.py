from abc import ABC, abstractmethod


class IPedestalDevice(ABC):

    @abstractmethod
    def calibrate(self):
        pass

    """Slewing methods:"""
    @abstractmethod
    def slew_to_location(self, lat, long, altitude):
        pass

    @abstractmethod
    def slew_to_az_el(self, azimuth, elevation):
        pass

    @abstractmethod
    def slew_preset(self, axis, dir):
        pass

    @abstractmethod
    def stop_slew(self, axis):
        pass

    @abstractmethod
    def sweep_on(self):
        pass

    @abstractmethod
    def sweep_off(self):
        pass

    @abstractmethod
    def slew(self, axis, dir):
        pass

    @abstractmethod
    def is_moving(self) -> bool:
        pass

    """Setter methods"""

    @abstractmethod
    def set_slew_rate(self, rate):
        pass

    @abstractmethod
    def set_slew_preset(self, preset):
        pass

    @abstractmethod
    def set_moving(self, status: bool):
        pass

    @abstractmethod
    def set_location(self, latitude: float, longitude: float, altitude) -> None:
        pass

    @abstractmethod
    def set_altitude(self, altitude: float) -> None:
        pass

    @abstractmethod
    def set_az_limits(self, az_limit: [float]) -> None:
        pass

    @abstractmethod
    def set_el_limits(self, el_limits: [float]) -> None:
        pass

    @abstractmethod
    def set_slew_rate_limit(self, limit: float) -> None:
        pass


    """Getter methods:"""

    @abstractmethod
    def get_azimuth(self):
        pass

    @abstractmethod
    def get_elevation(self):
        pass

    @abstractmethod
    def get_location_str(self):
        pass

    @abstractmethod
    def get_location(self):
        pass

    @abstractmethod
    def get_altitude(self):
        pass

    @abstractmethod
    def get_azimuth_limits(self):
        pass

    @abstractmethod
    def get_slew_preset(self):
        pass

    @abstractmethod
    def get_tn_offset(self):
        pass

    @abstractmethod
    def get_horizontal_offset(self):
        pass

    @abstractmethod
    def toggle_debug_mode(self):
        pass