from remotes.azeq6_remote import AZEQ6PedestalRemote
from time import sleep
from pedestals.azeq6_pedestal import AZEQ6Pedestal
from clients.fake_controller_client import FakeControllerClient
from clients.fake_gps_client import FakeGPSClient

def main():
    pc = AZEQ6PedestalRemote.get_fake_pedestal_device()  # instantiate fake AZEQ6 # pedestal using Fake gps client and fake controller client
    print(pc.get_location())
    print(pc.get_altitude())
    pc.slew_to_location(1,1,1)

if __name__ == "__main__":
    main()
