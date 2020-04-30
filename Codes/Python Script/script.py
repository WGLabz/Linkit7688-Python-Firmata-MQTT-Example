#!/usr/bin/python
import time
import sys
import signal
import paho.mqtt.client as mqtt
from PyMata.pymata import PyMata

DEBUG = True
BOARD_LED = 13
board = PyMata("/dev/ttyS0", verbose=False)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
  
def signal_handler(sig, frame):
    print('You pressed Ctrl+C')
    if board is not None:
        board.reset()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

board.set_pin_mode(BOARD_LED, board.OUTPUT, board.DIGITAL)
board.i2c_config(0, board.DIGITAL, 3, 2)

# Setup MQTT Client
client = mqtt.Client()
client.username_pw_set("********", password="**")
client.on_connect = on_connect

client.connect("192.168.0.7", 1883, 60)
client.loop_start()

sensor_data = {"HUM":0,"TEMP":0}
while 1:
    board.i2c_read(0x5c, 0, 5, board.I2C_READ)
    time.sleep(3)

    data = board.i2c_get_read_data(0x5c)
    calculated_sum = data[1] + data[2] + data[3] + data[4]

    if data[5] == calculated_sum: # Check for Checksum
        humidity = data[1] + float(data[2])/ 10
        scaleValue = data[4] & 0xEF
        signValue = data[4] & 0x80
        
        temperature = data[3] +float(scaleValue )/ 10

        if signValue:
            temperature = -temperature
        sensor_data["HUM"] = humidity
        sensor_data["TEMP"] = temperature
    else:
        print("Communication/Checksum Error")

    if DEBUG:
        print("Temperature: "+str(temperature))
        print("Humidity: "+str(humidity))
    
    client.publish("home/linkit/dht12", sensor_data)
    
    board.digital_write(BOARD_LED, 1)
    time.sleep(.5)
    board.digital_write(BOARD_LED, 0)
    time.sleep(10)
board.close()
