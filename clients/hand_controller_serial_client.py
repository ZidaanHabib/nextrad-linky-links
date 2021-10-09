import serial
from interfaces.serial_client import SerialInterface

class SynscanSerialClient(SerialInterface):

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

    def slew_positive_variable(self, ):


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
        response = self._serial_connection.read_until(expected='#')  # controller response has # ending char
        return response.decodde('UTF-8')

    def communicate(self, cmd: str):
        self.send_command(cmd)
        response = self.receive_response()
        return response


if __name__ == "__main__":

