from remotes.azeq6_remote import AZEQ6PedestalRemote
from time import sleep
from pedestals.azeq6_pedestal import AZEQ6Pedestal
from clients.fake_controller_client import FakeControllerClient
from clients.fake_gps_client import FakeGPSClient

def main():
    pc = AZEQ6PedestalRemote.get_fake_pedestal_device()
    #pc = AZEQ6PedestalRemote.get_pedestal_device_wo_gps()

    """pc.sweep_on()
    sleep(2)
    pc.sweep_off()"""
    #pc.calibrate()
    #pc.slew_to_location(-33.95898249833889, 18.470658926566475, 15)
    #pc.slew_to_az_el(-90,0)
    #print(pc.get_azimuth())
    #print(pc.get_elevation())
    #pc.slew_to_az_el(0,39)
    #print(pc.get_location().get_longitude())
    #pc.slew_positive_specific(1)
    #print(pc.get_azimuth_limits())
    pc.slew(1,1)
    sleep(2)
    pc.stop_slew(1)

if __name__ == "__main__":
    main()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting")