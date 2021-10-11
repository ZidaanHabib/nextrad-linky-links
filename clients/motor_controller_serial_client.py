import serial


class ControllerSerialClient:

    def __init__(self):
        self._serial_connection = serial.Serial(port='/dev/ttyUSB0',
                                                    baudrate=9600,
                                                    parity=serial.PARITY_NONE,
                                                    stopbits=serial.STOPBITS_ONE)

    def send_command(self, axis: int, cmd_char: str, cmd_data: str ) -> None:
        """ Method to send serial cmmand to motor controller"""

        cmd_list: [str] = [":"]  # all commands start with ':'
        cmd_list.append(cmd_char)
        cmd_list.append(str(axis))  # 1: azimuth axis, 2: elevation axis
        cmd_list.append(cmd_data)  #  depending on command, additional bytes may need to be sent
        cmd_list.append("\r")  # carriage return stop byte

        cmd = "".join(cmd_list)
        self._serial_connection.write(cmd.encode())

    def receive_response(self) ->str:
        response = self._serial_connection.read_until(expected='\r')  # controller response has carriage return ending character
        return response.decodde('UTF-8')
