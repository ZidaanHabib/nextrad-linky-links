from abc import ABC, abstractclassmethod


class IPedestalRemote(ABC):

    @abstractclassmethod
    def slew_to_loc():
        pass

    @abstractclassmethod
    def slew_to_az_el():
        pass

    @abstractclassmethod
    def sweep_mode_on():
        pass

    @abstractclassmethod
    def sweep_mode_off():
        pass

    @abstractclassmethod
    def slew_cw():
        pass

    @abstractclassmethod
    def slew_ccw():
        pass

    @abstractclassmethod
    def stop_slew():
        pass

    @abstractclassmethod
    def set_slew_speed():
        pass

    @abstractclassmethod
    def set_slew_preset():
        pass
