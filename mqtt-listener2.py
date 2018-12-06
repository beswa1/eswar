#!/usr/bin/python

import os
import time
import paho.mqtt.client as mqtt

broker = "127.0.0.1"
topic = "IoT-Gateway01/instruct"

# The callback for when the client receives a CONNACK response from  # the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
# Subscribing in on_connect() means that if we lose the      
# connection and reconnect then subscriptions will be renewed.
    client.subscribe(topic)
    client.publish("IoT-Gateway01/status", "I am alive", 1, True)
    client.publish("IoT-Gateway01/ble/status", ".", 1, True)
    client.publish("IoT-Gateway01/notification", ".", 1, True)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    words = str(msg.payload).split(" ")

    if (str(msg.payload) == "reboot"):
    	client.publish("IoT-Gateway01/status", "Goodbye", 1, True)
    	client.publish("IoT-Gateway01/ble/status", ".", 1, True)
    	client.publish("IoT-Gateway01/notification", ".", 1, True)
        time.sleep(2)
	os.system("reboot")
    if (words[0] == "connect"):
	print(str(msg.payload))
    	client.publish("IoT-Gateway01/ble/status", "Connecting", 1, False)
	os.system("/usr/bin/nohup /usr/bin/python /home/root/sensorTag/myscript5.py " + str(words[1]) + "&")  
	os.system("/home/root/oily/oily_lcddisplay monitoring")
    if (str(msg.payload) == "water"):
	print(str(msg.payload))
    	client.publish("IoT-Gateway01/notification", "watering", 1, True)
	os.system("/home/root/oily/oily_lcddisplay watering")
	time.sleep(2)	
	os.system("/home/root/oily/oily_lcddisplay watered")
    	client.publish("IoT-Gateway01/notification", "watered", 1, True)
	time.sleep(2)
	os.system("/home/root/oily/oily_lcddisplay OK!")
    	client.publish("IoT-Gateway01/notification", "OK!", 1, True)
	

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.will_set("IoT-Gateway01/status", "Goodbye", 1, True)
client.connect(broker, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks # and handles reconnecting.
client.loop_forever()

