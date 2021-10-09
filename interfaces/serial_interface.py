import serial


class SerialInterface:

    def __init__(self):
        self.rate = 9
        self.serial = serial.Serial(port='/dev/ttyUSB0',
                            baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE)

    def move_positive(self):
        msg: str = "P" + chr(2) + chr(16) + chr(36) + chr(self.rate) + chr(0)*3
        self.serial.write(msg.encode())

    def move_negative(self):
        msg: str = "P" + chr(2) + chr(16) + chr(37) + chr(self.rate) + chr(0) * 3
        self.serial.write(msg.encode())

    def stop_slew(self):
        msg = "P" + chr(2) + chr(16) + chr(36) + chr(0) + chr(0) * 3
        self.serial.write(msg.encode())

    def set_tracking(self, mode):
        msg = "T" + str(mode)
        self.serial.write(msg.encode())


if __name__ == "__main__":
    sc = SerialInterface()
    sc.move_positive()
    response = sc.serial.read(1)
    print(response.decode('utf-8'))

