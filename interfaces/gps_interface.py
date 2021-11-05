from abc import ABC, abstractmethod

class IGPSInterface(ABC):

    @abstractmethod
    def get_location(self):
        pass

    @abstractmethod
    def get_altitude(self):
        pass