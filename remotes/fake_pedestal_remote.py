
from pedestals.fake_pedestal import FakePedestal
from interfaces.pedestal_device_interface import IPedestalDevice


class FakePedestalRemote:

    @staticmethod
    def get_pedestal_device() -> IPedestalDevice:
        """ Return an instance of a FakePedestalDevice"""
        return FakePedestal()
