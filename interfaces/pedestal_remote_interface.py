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
    def slew_posiive_fixed(self, axis):
        pass

    @abstractmethod
    def slew_negative_fixed(self, axis):
        pass

    @abstractmethod
    def stop_slew(self, axis):
        pass

    @abstractmethod
    def set_slew_speed(self):
        pass

    @abstractmethod
    def set_slew_preset(self):
        pass
