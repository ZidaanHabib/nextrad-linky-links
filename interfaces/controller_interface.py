import serial


class ControllerInterface:

    def __init__(self):
        self._serial_connection = serial.Serial(port='/dev/ttyUSB0',
                                                    baudrate=9600,
                                                    parity=serial.PARITY_NONE,
                                                    stopbits=serial.STOPBITS_ONE)

    def send_command(self, cmd: str):
        self._serial_connection.write(cmd.encode())

    def receive_response(self):
        response = self._serial_connection.read_until(expected='#')  # controller response has # ending char
        return response.decodde('UTF-8')

    def communicate(self, cmd: str):
        self.send_command(cmd)
        response = self.receive_response()
        return response

    def get_azimuth(self):
        pass

    def get_elevation(self):
        pass