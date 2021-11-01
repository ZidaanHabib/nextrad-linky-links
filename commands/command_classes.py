from interfaces.command_interface import ICommand
from interfaces.pedestal_device_interface import IPedestalDevice


class Test(ICommand):

    def __init__(self, pedestal_device: IPedestalDevice):
        self.pedestal_device = pedestal_device

    def execute(self):
        print("Command pattern test successful!!!!!")


class Calibrate(ICommand):

    def __init__(self, pedestal_device: IPedestalDevice):
        self.pedestal_device = pedestal_device

    def execute(self):
        self.pedestal_device.calibrate()


class SweepOn(ICommand):

    def __init__(self, pedestal_device: IPedestalDevice):
        self.pedestal_device = pedestal_device

    def execute(self):
        self.pedestal_device.sweep_on()


class SweepOff(ICommand):

    def __init__(self, pedestal_device: IPedestalDevice):
        self.pedestal_device = pedestal_device

    def execute(self):
        self.pedestal_device.sweep_off()


class StopSlew(ICommand):

    def __init__(self, pedestal_device: IPedestalDevice):
        self.pedestal_device = pedestal_device

    def execute(self):
        self.pedestal_device.stop_slew(1)
        self.pedestal_device.stop_slew(2)

class StartSlewPreset(ICommand):

    def __init__(self, pedestal_device: IPedestalDevice, axis):
        self.pedestal_device = pedestal_device
        self.axis = axis

    def execute(self):
        self.pedestal_device.stop_slew(self.axis)

class StartSlew(ICommand):

    def __init__(self, pedestal_device: IPedestalDevice):
        self.pedestal_device = pedestal_device


    def execute(self, axis, direction):
        self.pedestal_device.slew(axis, direction)


class GoToLocation(ICommand):

    def __init__(self, pedestal_device: IPedestalDevice):
        self.pedestal_device = pedestal_device

    def execute(self, lat, long, alt):
        self.pedestal_device.slew_to_location(lat, long, alt)


class GoToAzEl(ICommand):

    def __init__(self, pedestal_device: IPedestalDevice):
        self.pedestal_device = pedestal_device

    def execute(self, az, el):
        self.pedestal_device.slew_to_az_el(az, el)


class GetOrientation(ICommand):

    def __init__(self, pedestal_device: IPedestalDevice):
        self.pedestal_device = pedestal_device

    def execute(self):
        az = self.pedestal_device.get_azimuth()
        el = self.pedestal_device.get_elevation()
        return az, el


class ToggleDebug(ICommand):

    def __init__(self, pedestal_device: IPedestalDevice):
        self.pedestal_device = pedestal_device

    def execute(self):
        self.pedestal_device.toggle_debug_mode()

