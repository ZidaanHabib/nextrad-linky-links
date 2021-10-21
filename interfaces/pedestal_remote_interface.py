from abc import ABC, abstractmethod


class IPedestalRemote(ABC):

    @abstractmethod
    def slew_to_loc(self):
        pass

    @abstractmethod
    def slew_to_az_el(self):
        pass

    @abstractmethod
    def sweep_mode_on(self):
        pass

    @abstractmethod
    def sweep_mode_off(self):
        pass

    @abstractmethod
    def slew_cw(self):
        pass

    @abstractmethod
    def slew_ccw(self):
        pass

    @abstractmethod
    def stop_slew(self):
        pass

    @abstractmethod
    def set_slew_speed(self):
        pass

    @abstractmethod
    def set_slew_preset(self):
        pass
