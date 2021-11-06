from clients.gps_client import GPSClient
from dtypes.gps_location import GPSLocation

if __name__ == "__main__":
    gp = GPSClient()

    location = gp.get_gga_msg()
    print(location)
