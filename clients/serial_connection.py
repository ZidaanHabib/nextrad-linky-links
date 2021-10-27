from interfaces.connection_interface import ConnectionInterface
import serial
from threading import Lock

class SerialConnection(ConnectionInterface):

    def __init__(self):
        self._serial_connection = serial.Serial(port='/dev/ttyUSB0',
                                                    baudrate=9600,
                                                    parity=serial.PARITY_NONE,
                                                    stopbits=serial.STOPBITS_ONE)
        self.lock = Lock()

    def send_command(self, cmd: str):
        self.lock.acquire()
        self._serial_connection.write(cmd.encode())
        self.lock.release()

    def receive_response(self):
        response = self._serial_connection.read_until(expected=b'#')  # controller response has # ending char
        return response.decode('UTF-8')

    def communicate(self, cmd: str):
        self.send_command(cmd)
        response = self.receive_response()
        return response
