import serial
from abc import ABC, abstractmethod

class ControllerInterface(ABC):

    def __init__(self):
        self._serial_connection = serial.Serial(port='/dev/ttyUSB0',
                                                    baudrate=9600,
                                                    parity=serial.PARITY_NONE,
                                                    stopbits=serial.STOPBITS_ONE)
    @abstractmethod
    def send_command(self, cmd: str):
        pass

    @abstractmethod
    def receive_response(self):
        pass


    @abstractmethod
    def communicate(self, cmd: str):
        pass


