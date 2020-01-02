'''
 * Copyright (c) 2018 - 2019 - RTLOC
 * 
 * This file is part of RTLOC API tools.
 *
 * RTLOC API tools is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 * RTLOC API tools is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  To get a copy of the GNU General Public License see <https://www.gnu.org/licenses/>.
'''

import paho.mqtt.client as mqtt
import time
from mqtt_decoder import Decoder

print("test")

# Set Parameters
hostname = 'mqtt.cloud.rtloc.com'
topic = 'rtls/kart/posxyz'        # Replace with own topic
username =  'demo:demo@rtloc.com' # Replace with own username
password = '12345'                # Replace with own password
port = 1883

decoder = Decoder()

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print(">> Connected")
    else:
        print(" >> Connection failed (rc= " + str(rc) + ")")

def on_message(client, obj, msg):
    #msg.topic, msg.qos, msg.payload
    decoder.decode(msg)

def on_subscribe(client, obj, mid, granted_qos):
    print(" >> Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

mqttc = mqtt.Client()

# Assign callbacks (note: no need for on_publish)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Uncomment to enable log/debug
# mqttc.on_log = on_log

# Connect
mqttc.username_pw_set(username, password)
mqttc.connect(hostname, port)

# Subscribe (QoS level = 0)
mqttc.subscribe(topic, 0)

# Loop (exit when an error occurs)
rc = 0
while rc == 0:
    rc = mqttc.loop()

print(" >> error - rc: " + str(rc))