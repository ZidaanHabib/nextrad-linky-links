import pynmea2 as nmea
import serial


class GPSClient:

    def __init__(self, baud_rate=9600, timeout=5):
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = serial.Serial("/dev/ttyS0", self.baud_rate, self.timeout)

    def get_gga_msg(self):
        """ Read a GPGGA NMEA message """
        nmea_msg = ''
        while nmea_msg[0:6] != '$GPGGA':
            nmea_msg = self.ser.readline().decode()
            nmea_msg = nmea_msg[0:len(nmea_msg) - 2]  # exclude <CR><LF> when parsing
        nmea_obj = nmea.parse(nmea_msg)
        return nmea_obj

    def get_altitude(self):
        """ Determine current altitude """
        nmea_obj = self.get_gga_msg()
        alt = nmea_obj.altitude
        return alt


if __name__ == "__main__":
    gps = GPSClient(9600,5)
    print(gps.get_altitude())
