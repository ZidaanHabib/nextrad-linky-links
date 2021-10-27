import serial
from abc import ABC, abstractmethod

class ConnectionInterface(ABC):


    @abstractmethod
    def send_command(self, cmd: str):
        pass

    @abstractmethod
    def receive_response(self):
        pass


    @abstractmethod
    def communicate(self, cmd: str):
        pass


