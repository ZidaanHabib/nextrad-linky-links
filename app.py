from paho.mqtt import client as mqtt
from configparser import ConfigParser

from pedestals.fake_pedestal import FakePedestal
from commands import command_classes
from commands.button import Button

from remotes.azeq6_remote import AZEQ6PedestalRemote
from remotes.fake_pedestal_remote import FakePedestalRemote
#from commands.message_parser import MessageParser


""" MQTT call backs:"""
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


def on_message(client, userdata, msg_enc):
    msg = msg_enc.payload.decode("UTF-8")
    print("Message received: " + msg)
    select_button(msg)


#def mqtt_monitor_thread():


""" Creating commands:"""
def commands_init(pedestal_device):
    stop_command = command_classes.StopSlew(pedestal_device)
    global stop_pressed
    stop_pressed = Button(stop_command)

    sweep_on_command = command_classes.SweepOn(pedestal_device)
    global sweep_pressed
    sweep_pressed = Button(sweep_on_command)

    calibrate_command = command_classes.Calibrate(pedestal_device)
    global calibrate_pressed
    calibrate_pressed = Button(calibrate_command)


    slew_command = command_classes.StartSlew(pedestal_device)
    global slew_pressed
    slew_pressed = Button(slew_command)



    get_coords_command = command_classes.GetOrientation(pedestal_device)
    global get_coords_pressed
    get_coords_pressed = Button(get_coords_command)


    goto_az_el_command = command_classes.GoToAzEl(pedestal_device)
    global goto_az_el_pressed
    goto_az_el_pressed = Button(goto_az_el_command)

    goto_location_command = command_classes.GoToLocation(pedestal_device)
    global goto_location_pressed
    goto_location_pressed = Button(goto_location_command)

def select_button(msg):
    mqtt_cmds = {"calibrate": "CALIB", "stop": "STOP", "slew": "SLEW", "goto_location": "GOTO-LOC",
                 "goto_az_el": "GOTO-AZEL",  "sweep": "SWEEP", "get_pos": "GET-AZ-EL"
                 }
    msg_list = msg.split("/")
    if msg_list[0] == mqtt_cmds["calibrate"]:
        calibrate_pressed.press()
    elif msg_list[0] == mqtt_cmds["stop"]:
        stop_pressed.press()
    elif msg_list[0] == mqtt_cmds["slew"]:
        axis = 0
        dir = 0
        if msg_list[1] == "AZ":
            axis = 1
        else:
            axis = 2
        if msg_list[2] == "POS":
            dir = 1
        else:
            dir = 2
        slew_pressed.press(axis, dir)
    elif msg_list[0] == mqtt_cmds["goto_az_el"]:
        az = float(msg_list[1])
        el = float(msg_list[2])
        goto_az_el_pressed.press(az, el)
    elif msg_list[0] == mqtt_cmds["goto_location"]:
        lat = float(msg_list[1])
        long = float(msg_list[2])
        alt = float(msg_list[3])
        goto_location_pressed.press(lat, long)
    elif msg_list[0] == mqtt_cmds["sweep"]:
        sweep_pressed.press()



def main():

    # Instantiate pedestal controller object:
    #pc = FakePedestalRemote.get_pedestal_device()
    pc = AZEQ6PedestalRemote.get_fake_pedestal_device()
    commands_init(pc)
    """# bind commands to buttons as per command design pattern.
    command = command_classes.Test(pc)
    test_button = Button(command)
    test_button.press()"""
    #mp = MessageParser()

    cf = ConfigParser()
    cf.read("config.ini")

    broker = cf["MQTT"]["Broker"]
    #broker = "169.254.228.235"
    client = mqtt.Client("Pi-1", protocol=mqtt.MQTTv31)

    # bind callbacks:
    client.on_connect = on_connect
    client.on_log = on_log
    client.on_subscribe = on_subscribe
    client.on_message = on_message


    #pc = PedestalController(FakeControllerClient(), FakeGPSClient())
    try:
        #client.connect(host="localhost", port=1883)
        client.connect(host="169.254.228.235", port=1883)
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





