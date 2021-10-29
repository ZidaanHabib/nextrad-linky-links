from pedestals.azeq6_pedestal import AZEQ6Pedestal
from interfaces.pedestal_device_interface import IPedestalDevice
from clients.hand_controller_serial_client import SynscanSerialClient
from clients.gps_client import GPSClient
from clients.serial_connection import SerialConnection
#  fake clients for testing purposes
from clients.fake_gps_client import FakeGPSClient
from clients.fake_controller_client import FakeControllerClient


class AZEQ6PedestalRemote:

    @staticmethod
    def get_pedestal_device() -> IPedestalDevice:
        return AZEQ6Pedestal(SynscanSerialClient(SerialConnection()), GPSClient())

    @staticmethod
    def get_fake_pedestal_device() -> IPedestalDevice:
        return AZEQ6Pedestal(FakeControllerClient(), FakeGPSClient())

    @staticmethod
    def get_pedestal_device_wo_gps() -> IPedestalDevice:
        return AZEQ6Pedestal(SynscanSerialClient(SerialConnection()), FakeGPSClient())
