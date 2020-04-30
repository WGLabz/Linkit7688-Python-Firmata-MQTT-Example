import paho.mqtt.client as mqtt
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("home/test/in")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.username_pw_set("********", password="**")
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.7", 1883, 60)

client.loop_start()

while 1:
    client.publish("home/test/out", "Test Data")
    time.sleep(5)