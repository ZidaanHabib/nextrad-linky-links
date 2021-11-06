from remotes.azeq6_remote import AZEQ6PedestalRemote
from time import sleep
from pedestals.azeq6_pedestal import AZEQ6Pedestal
from clients.fake_controller_client import FakeControllerClient
from clients.fake_gps_client import FakeGPSClient

def main():
    pc = AZEQ6PedestalRemote.get_fake_pedestal_device()  # instantiate fake AZEQ6 # pedestal using Fake gps client and fake controller client
    pc.toggle_debug_mode()
    avg_time = 0
    for i in range(5):
        avg_time += pc.slew_to_location(1,1,1)
    avg_time = (avg_time / 5)*1000  # milliseconds
    print("Slew_to_location() avg run time: {}".format(avg_time))

    pc.slew(1,1)
    avg_time = 0
    for i in range(5):
        avg_time += pc.slew(1,1)
    avg_time = (avg_time / 5)*1000  # milliseconds
    print("Slew() avg run time: {}".format(avg_time))

    pc.stop_slew(1)
    avg_time = 0
    for i in range(5):
        avg_time += pc.stop_slew(1)
    avg_time = (avg_time / 5) * 1000  # milliseconds
    print("stop_slew() avg run time: {}".format(avg_time))

    pc.slew_to_az_el(1,1)
    avg_time = 0
    for i in range(5):
        avg_time += pc.slew_to_az_el(1, 1)
    avg_time = (avg_time / 5) * 1000  # milliseconds
    print("slew_to_az_el() avg run time: {}".format(avg_time))

if __name__ == "__main__":
    main()
