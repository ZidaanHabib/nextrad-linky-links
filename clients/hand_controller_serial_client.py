import serial
from interfaces.controller_interface import ControllerInterface
from time import sleep


class SynscanSerialClient(ControllerInterface):

    def __init__(self):
        super(SynscanSerialClient, self).__init__()

    def slew_positive_fixed(self, axis, slew_rate_preset):  #axis == 1: azimuth, 2: elevation
        axis_char = ""
        if axis == 1:
            axis_char = chr(16)
        else: # axis = 2
            axis_char = chr(17)
        msg: str = "P" + chr(2) + axis_char + chr(36) + chr(slew_rate_preset) + chr(0)*3
        self.send_command(msg)

    def slew_negative_fixed(self, axis: int, slew_rate_preset: int):
        axis_char = ""
        if axis == 1:
            axis_char = chr(16)
        else:  # axis = 2
            axis_char = chr(17)
        msg: str = "P" + chr(2) + axis_char + chr(37) + chr(slew_rate_preset) + chr(0) * 3
        self.send_command(msg)

    def slew_positive_variable(self, axis: chr, rate: float ):  # rate is in arcseconds per sec
        """Slew in positive direction at a specific rate in arcseconds per sec"""
        track_rate_high: int = int((rate * 4) // 256)  # according to data sheet
        track_rate_low: int = int((rate * 4) % 256)   # according to data sheet

        axis_char = ""
        if axis == 1:  # azimuth axis
            axis_char = chr(16)
        else:  # axis = 2  elevation axis
            axis_char = chr(17)
        msg: str = "P" + chr(3) + axis_char + chr(6) + chr(track_rate_high) + chr(track_rate_low) + chr(0) * 2
        self.send_command(msg)

    def slew_negative_variable(self, axis: chr, rate: float ):  # rate is in arcseconds per sec
        """Slew in negative direction at a specific rate in arcseconds per sec"""
        track_rate_high: int = int((rate * 4) // 256)  # according to data sheet
        track_rate_low: int = int((rate * 4) % 256)   # according to data sheet

        axis_char = ""
        if axis == 1:  # azimuth axis
            axis_char = chr(16)
        else:  # axis = 2  elevation axis
            axis_char = chr(17)
        msg: str = "P" + chr(3) + axis_char + chr(7) + chr(track_rate_high) + chr(track_rate_low) + chr(0) * 2
        self.send_command(msg)

    def stop_slew(self, axis):
        axis_char = ""
        if axis == 1:
            axis_char = chr(16)
        else:  # axis = 2
            axis_char = chr(17)
        msg = "P" + chr(2) + axis_char + chr(36) + chr(0) + chr(0) * 3
        self.send_command(msg)

    def set_tracking(self, mode):
        msg = "T" + str(mode)
        self.send_command(msg)

    def send_command(self, cmd: str):
        self._serial_connection.write(cmd.encode())

    def receive_response(self):
        response = self._serial_connection.read_until(expected=b'#')  # controller response has # ending char
        return response.decode('UTF-8')

    def communicate(self, cmd: str):
        self.send_command(cmd)
        response = self.receive_response()
        return response

    def get_azimuth(self) -> float:
        response = self.communicate("z")
        az_string = response.split(",")[0]  # get the azimuth portion of controller response
        az_string = az_string[0:-2] #ignore last 2 chars as per datasheet
        az = float.fromhex(az_string)  # convert from hex string to decimal number
        az = round((az/16777216)*360, 2)  # convert to degrees

        return az

    def get_elevation(self):
        response = self.communicate("z")
        el_string = response.split(",")[1]  # get the azimuth portion of controller response
        el_string = el_string[0:-3]  # ignore last 2 chars as per datasheet as well as '#'
        el = float.fromhex(el_string)  # convert from hex string to decimal number
        el = round((el / 16777216) * 360,2)  # convert to degrees
        return el

if __name__ == "__main__":
    sc = SynscanSerialClient()
    sc.slew_negative_fixed(1, 9)
    sleep(5)
    sc.stop_slew(1)
    response = sc.get_azimuth()
    print(response)