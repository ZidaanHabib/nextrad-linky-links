
from pedestals.fake_pedestal import FakePedestal
from interfaces.pedestal_device_interface import IPedestalDevice


class FakePedestalRemote:

    @staticmethod
    def get_pedestal_device() -> IPedestalDevice:
        return FakePedestal()
