from paho.mqtt import client as mqtt
from configparser import ConfigParser
from clients.pedestal_controller import PedestalController
from clients.fake_controller_client import FakeControllerClient
from clients.gps_client import GPSClient
from clients.fake_gps_client import FakeGPSClient


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection OK.")
    else:
        print("Connection failed with response code " + str(rc))
    client.subscribe("test")


def on_log(client, userdata, level, buf):
    print("log:" + buf)


def on_subscribe(client, userdata, mid, granted_qos):
    print("<<Subscription  successful.>>")


def on_message(client, userdata, msg_enc) -> str:
    msg = msg_enc.payload.decode("UTF-8")
    print("Message received: " + msg)
    return msg


#def mqtt_monitor_thread():



def main():
    cf = ConfigParser()
    cf.read("config.ini")

    broker = cf["MQTT"]["Broker"]
    client = mqtt.Client("Pi-1", protocol=mqtt.MQTTv31)

    # bind callbacks:
    client.on_connect = on_connect
    client.on_log = on_log
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    # Instantiate pedestal controller object:
    pc = PedestalController(FakeControllerClient(), FakeGPSClient())
    try:
        client.connect(host="localhost", port=1883)
    except Exception as e:
        print(e)
    #client.connect(host="mqtt.eclipseprojects.io", port=1883, keepalive=60, keepalive=60)
    #client.connect(host="raspberrypizero.local", port=1883, keepalive=60)

    client.loop_start() # start mqtt client loop
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Quitting...")
        SystemExit()


if __name__ == "__main__":
    main()





