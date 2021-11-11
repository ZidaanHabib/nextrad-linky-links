# NeXtRAD Client Controller 

---
Author: Zidaan Habib


The NextRAD client controller is software package to communicate with the NeXtRAD command application, and to interact with the Skywatcher AZEQ6 pedestal device.
The following devies are required:
* Pi 4
* Waveshare L70 or (Quectel L70 - L80 series)

When started, the application starts an MQTT client and continously runs. When certain MQTT messages of a predefined type are received, the application interacts with the pedestal device, such as by causing it to slew in a given direction.



### Licensing

---

GNU General Public v3

## Installation:
1. Clone the repository
2. pip3 install -r requirements.txt

Alternatively, *pip3 install nextrad_client*

## Setup:
* Replace ip address or host name of intended MQTT broker in config file in the root of the package
* Replace name of client in the config file - this will be the topic that the Pi's MQTT client will subscribe to

## Running application:
* python3 app.py : this starts the client application and mqtt client and will continue indefinitely
* alternatively, if being run on  Pi 4, you can run it in the provided Docker container
* in project root, run *docker build -t <your_name> .*
* After the image is built - *docker run -p 1883:1883 <your_name>* 


### Credits
The pynmea2 python library was used for GPS parsing of NMEA 0183 messages.