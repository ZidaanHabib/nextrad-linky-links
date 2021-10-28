from remotes.azeq6_remote import AZEQ6PedestalRemote
from time import sleep
from pedestals.azeq6_pedestal import AZEQ6Pedestal
from clients.fake_controller_client import FakeControllerClient
from clients.fake_gps_client import FakeGPSClient

def main():
    pc = AZEQ6PedestalRemote.get_fake_pedestal_device()

    pc.sweep_on()
    sleep(2)
    pc.sweep_off()

if __name__ == "__main__":
    main()