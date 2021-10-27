from pedestals.azeq6_pedestal import AZEQ6Pedestal
from interfaces.pedestal_device_interface import IPedestalDevice
from clients.hand_controller_serial_client import SynscanSerialClient
from clients.gps_client import GPSClient
from clients.serial_connection import SerialConnection

class AZEQ6PedestalRemote:

    @staticmethod
    def get_pedestal_device() -> IPedestalDevice:
        return AZEQ6Pedestal(SynscanSerialClient(SerialConnection()), GPSClient())
