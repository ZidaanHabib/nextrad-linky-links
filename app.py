from paho.mqtt import client as mqtt
from configparser import ConfigParser
from clients.pedestal_controller import PedestalController
from clients.fake_controller_client import FakeControllerClient
from clients.gps_client import GPSClient


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection OK.")
    else:
        print("Connection failed with response code " + rc)


def on_log(client, userdata, level, buf):
    print("log:" + buf)


def on_subscribe(client, userdata, mid, granted_qos):
    print("<<Subscription from " + client + " successful.>>")


def on_message(client, userdata, msg_enc) -> str:
    msg = msg_enc.payload.decode("UTF-8")
    return msg


def main():
    cf = ConfigParser()
    cf.read("config.ini")

    broker = cf["MQTT"]["Broker"]
    client = mqtt.Client("Pi-1")

    # bind callbacks:
    client.on_connect = on_connect
    client.on_log = on_log
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    # Instantiate pedestal controller object:
    pc = PedestalController(FakeControllerClient(), )




