import pynmea2 as nmea
import serial
from time import sleep
from types.gps_location import GPSLocation


class GPSClient:

    def __init__(self, baud_rate=9600, timeout=5):
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = serial.Serial("/dev/ttyS0", self.baud_rate, self.timeout)

    def get_gga_msg(self):
        """ Read a GPGGA NMEA message """
        nmea_msg = ''
        while nmea_msg[0:6] != '$GNGGA':
            nmea_msg = self.ser.readline().decode()
            nmea_msg = nmea_msg[0:len(nmea_msg) - 2]  # exclude <CR><LF> when parsing
        nmea_obj = nmea.parse(nmea_msg)
        return nmea_obj

    def get_gll_msg(self):
        """ Read a GPGLL NMEA message """
        nmea_msg = ''
        while nmea_msg[0:6] != '$GNGLL':
            nmea_msg = self.ser.readline().decode()
            nmea_msg = nmea_msg[0:len(nmea_msg) - 2]  # exclude <CR><LF> when parsing
        nmea_obj = nmea.parse(nmea_msg)
        return nmea_obj

    def get_altitude(self):
        """ Determine current altitude """
        nmea_obj = self.get_gga_msg()
        alt = nmea_obj.altitude
        return alt

    @staticmethod
    def get_location(nmea_obj: nmea.nmea.NMEASentenceType):
        """ Return the current longitude and latitude coordinates as a string
                    arguments:
                    nmea_obj -- pynmea2 NMEA object for a GNGLL or GNGGA message
                    """
        lat = nmea_obj.latitude
        lat_direction = nmea_obj.lat_dir
        long = nmea_obj.longitude
        long_direction = nmea_obj.lon_dir
        return GPSLocation(lat, lat_direction, long, long_direction)

    def continuous_read(self):
        """ Continously print raw NMEA messages to terminal """
        while True:
            try:
                print(self.ser.readline().decode())
                sleep(0.1)
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    gps = GPSClient(9600 , 5)
    print(gps.get_altitude())
