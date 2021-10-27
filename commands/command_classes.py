from interfaces.command_interface import ICommand
from interfaces.pedestal_remote_interface import IPedestalRemote


class Calibrate(ICommand):

    def __init__(self, pedestal_device: IPedestalRemote):
        self.pedestal_device = pedestal_device

    def execute(self):
        self.pedestal_device.calibrate()


class SweepOn(ICommand):

    def __init__(self, pedestal_device: IPedestalRemote):
        self.pedestal_device = pedestal_device

    def execute(self):
        self.pedestal_device.sweep_on()


class SweepOff(ICommand):

    def __init__(self, pedestal_device: IPedestalRemote):
        self.pedestal_device = pedestal_device

    def execute(self):
        self.pedestal_device.sweep_off()


class StopSlew(ICommand):

    def __init__(self, pedestal_device: IPedestalRemote):
        self.pedestal_device = pedestal_device

    def execute(self):
        self.pedestal_device.stop_slew(1)
        self.pedestal_device.stop_slew(2)

class StartSlewPreset(ICommand):

    def __init__(self, pedestal_device: IPedestalRemote, axis):
        self.pedestal_device = pedestal_device
        self.axis = axis

    def execute(self):
        self.pedestal_device.stop_slew(self.axis)


class GoToLocation(ICommand):

    def __init__(self, pedestal_device: IPedestalRemote, lat, long):
        self.pedestal_device = pedestal_device
        self.lat = lat
        self.long = long

    def execute(self):
        self.pedestal_device.slew_to_location(self.lat, self.long)


class GoToAzEl(ICommand):

    def __init__(self, pedestal_device: IPedestalRemote, az, el):
        self.pedestal_device = pedestal_device
        self.az = az
        self.el = el

    def execute(self):
        self.pedestal_device.slew_to_az_el(self.az, self.el)


class GetOrientation(ICommand):

    def __init__(self, pedestal_device: IPedestalRemote):
        self.pedestal_device = pedestal_device

    def execute(self):
        az = self.pedestal_device.get_azimuth()
        el = self.pedestal_device.get_elevation()
        return az, el


