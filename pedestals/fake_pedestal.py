from interfaces.pedestal_remote_interface import IPedestalRemote

class FakePedestal(IPedestalRemote): #TODO add IPedestalRemote inheritance

    def calibrate(self):
        """ Set current azimuth and elevation to be the 0,0 point"""
        print("Calibrating")

    def slew_to_location(self, target_lat, target_long, target_altitude):
        """ Method to slew to a target location entered in latitude and longitude"""
        print("Slewing to lcoation")

    def slew_positive_specific(self, axis: int, rate: float):
        print("Slew positive specific")

    def slew_positive_preset(self, axis):  #axis == 1: azimuth, 2: elevation
        print("Slew positive preset")

    def slew_negative_preset(self, axis: int):
        print("Slew negative preset")

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
    def set_moving(self):
        print("moving")

    """Setter methods: """

    def set_location(self) :
        print("location")

    def set_altitude(self) :
        print("altitude")

    def set_az_limits(self) -> None:
        print("Set az limits")

    def set_el_limits(self) -> None:
        print("Set el limits")


    def set_slew_rate_limit(self) -> None:
        print("slew rate limit")

    """Getter methods:"""

    def slew_negative_specific(self, axis, rate):
        print("slew negative specific")

    def set_slew_rate(self):
        print("Set slew rate")

    def set_slew_preset(self):
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
