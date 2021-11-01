from interfaces.pedestal_device_interface import IPedestalDevice

class FakePedestal(IPedestalDevice): #TODO add IPedestalDevice inheritance

    def calibrate(self):
        """ Set current azimuth and elevation to be the 0,0 point"""
        print("Calibrating")

    def slew_to_location(self, target_lat, target_long, target_altitude):
        """ Method to slew to a target location entered in latitude and longitude"""
        print("Slewing to lcoation")

    def slew(self, axis: chr, dir: chr):
        print("Slew positive specific")

    def slew_preset(self, axis, dir):  #axis == 1: azimuth, 2: elevation
        print("Slew positive preset")

    def stop_slew(self, axis: int):
        print("Stopping slew")

    def slew_to_az_el(self, azimuth: float, elevation: float):
        print("Slew to azimuth and elevation")

    def get_azimuth(self):
        print("Get azimuth")

    def get_elevation(self):
        print("Get elev")

    def is_slew_az_el(self):
        print("is slewing")


    def sweep_off(self):
        print("sweep off")

    def sweep_on(self):
        print("sweep on")

    """Setter methods"""
    def set_moving(self, status):
        print("moving")

    """Setter methods: """

    def set_location(self, lat, long, alt) :
        print("location")

    def set_altitude(self, alt) :
        print("altitude")

    def set_az_limits(self, limits: [int]) -> None:
        print("Set az limits")

    def set_el_limits(self, limits: [int]) -> None:
        print("Set el limits")


    def set_slew_rate_limit(self, slew_rate) -> None:
        print("slew rate limit")

    """Getter methods:"""


    def set_slew_rate(self, slew_rate):
        print("Set slew rate")

    def set_slew_preset(self, preset):
        print("Set slew preset")

    def get_location_str(self):
        print("location")

    def get_location(self):
        """Return instance location object """

    def get_altitude(self):
        print("altitude")

    def get_azimuth_limits(self):
        print("azimuth limits")

    def is_moving(self) :
        print("is moving")


    def get_slew_preset(self):
        print("slew preset")

    def get_tn_offset(self):
        print("get tn offset")

    def get_horizontal_offset(self):
        print("Get h offset")

    def toggle_debug_mode(self):
        print("debug")