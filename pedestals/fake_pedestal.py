from interfaces.pedestal_device_interface import IPedestalDevice

class FakePedestal(IPedestalDevice):

    def __init__(self):
        print("Fake pedestal created!")

    def calibrate(self):
        """ Fake calibration command"""
        print("Calibrating")

    def slew_to_location(self, target_lat, target_long, target_altitude):
        """ Fake goto command"""
        print("Slewing to location from FakePedestal ")

    def slew(self, axis: chr, dir: chr):
        """ Fake slew command"""
        print("Slew from FakePedestal ")

    def slew_preset(self, axis, dir):  #axis == 1: azimuth, 2: elevation
        """ Fake slew preset command"""
        print("Slew positive preset")

    def stop_slew(self, axis: int):
        """ Fake stop command"""
        print("Stop slew cmd from FakePedestal")

    def slew_to_az_el(self, azimuth: float, elevation: float):
        """ Fake goto command"""
        print("Slew to azimuth and elevation FakePedestal")

    def get_azimuth(self):
        """ Fake get azimuth command"""
        print("Get azimuth from FakePedestal")

    def get_elevation(self):
        """ Fake get elevation command"""
        print("Get elev from FakePedestal")

    def is_slew_az_el(self):
        """ Fake is slewing command"""
        print("is slewing FakePedestal")


    def sweep_off(self):
        print("sweep off ")

    def sweep_on(self):
        """ Fake sweep on command"""
        print("sweep on from FakePedestal")

    """Setter methods"""
    def set_moving(self, status):
        """ Fake set moving command"""
        print("Set moving from FakePedestal")

    def set_location(self, lat, long, alt):
        """ Fake set location command"""
        print("location from FakePedestal")

    def set_altitude(self, alt):
        """ Fake set altitude command"""
        print("Get altitude from FakePedestal")

    def set_az_limits(self, limits: [int]) -> None:
        """ Fake set az limits command """
        print("Set az limits")

    def set_el_limits(self, limits: [int]) -> None:
        """ Fake set el limits command"""
        print("Set el limits from FakePedestal")


    def set_slew_rate_limit(self, slew_rate) -> None:
        """ Fake set slew rate command"""
        print("slew rate limit from FakePedestal")

    def set_slew_rate(self, slew_rate):
        """ Fake get slew rate command"""
        print("Set slew rate from FakePedestal")

    def set_slew_preset(self, preset):
        """ Fake set slew rate command"""
        print("Set slew preset from FakePedestal")

    """Getter methods:"""

    def get_location_str(self):
        """ fake get location string command"""
        print("get location from FakePedestal")

    def get_location(self):
        """ Fake get location string"""
        """Return instance location object """

    def get_altitude(self):
        """ Fake get altitude command"""
        print(" Get altitude from FakePedestal")

    def get_azimuth_limits(self):
        """ Fake get az limits command"""
        print("Get azimuth limits from FakePedestal")

    def is_moving(self) :
        """ Fake is moving command"""
        print("Check if moving from FakePedestal")


    def get_slew_preset(self):
        """ Fake get slew preset command"""
        print("Get slew preset from FakePedestal")

    def get_tn_offset(self):
        """ Fake get true north offset command"""
        print("Get tn offset from FakePedestal")

    def get_horizontal_offset(self):
        """ fake get horizontal offset command"""
        print("Get h offset from FakePedestal")

    def toggle_debug_mode(self):
        """ Fake debug command """
        print("Toggle debug mode from FakePedestal")