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

import json

# Set Parameters
hostname = 'localhost'
username =  'demo:demo@rtloc.com' # Locally not needed.
password = '12345'                # Locally not needed.
port = 1883


# Define event callbacks
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print(">> Connected")
    else:
        print(" >> Connection failed (rc= " + str(rc) + ")")

def on_message(client, obj, msg):
    #msg.topic, msg.qos, msg.payload
    print('Received ' + msg.topic + ' message')
    parsed_json = (json.loads(msg.payload))
    print(parsed_json)

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
mqttc.subscribe('data/#', 0)

# Loop (exit when an error occurs)
rc = 0
while rc == 0:
    rc = mqttc.loop()

print(" >> error - rc: " + str(rc))