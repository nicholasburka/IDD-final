import paho.mqtt.client as mqtt
import uuid
import base64

import cv2
import sys
import time
import os
import numpy as np
import math

import qwiic_joystick

myJoystick = qwiic_joystick.QwiicJoystick()

if myJoystick.connected == False:
	print("The Qwiic Joystick device isn't connected to the system. Please check your connection", \
		file=sys.stderr)

myJoystick.begin()

# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()), transport='websockets')
# configure network encryption etc
#client.tls_set()
# this is the username and pw we have setup for the class
#client.username_pw_set('idd', '')
handshake_addr = 'oldphone/handshake7'


#connect to the broker
client.connect(
    '127.0.1.1',
    port=8000)

def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(handshake_addr)
    # you can subsribe to as many topics as you'd like
    # client.subscribe('some/other/topic')
devices = []
angles = []
just_sent = ''
# this is the callback that gets called each time a message is received
def on_message(client, userdata, msg):
	global devices
	decoded = msg.payload.decode('UTF-8')
	print(f"topic: {msg.topic} msg: {decoded}")
	if (not(decoded[:3] == "ACK")):
		client.publish(handshake_addr, 'ACK'+decoded)
		try:
			indexof = devices.index(decoded)
		except:
			devices.append(decoded)
			angles.append(0)
			print("added device, num devices == " + str(len(devices)))

client.on_connect = on_connect
client.on_message = on_message

with open("random.jpg", "rb") as image:
    img = image.read()
    message =img
base64_bytes = base64.b64encode(message)

base64_message = base64_bytes.decode('ascii')

topic = handshake_addr

#Initialize the camera
cap = cv2.VideoCapture(0)

height= 480
width = 640

number = len(devices) # # of screens

imgCropped=[]
selected = 0
count=1
while True:
    client.loop(timeout=1.0, max_packets=1)
    number = len(devices)
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    #client.publish(topic, 'capturing')
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
    #client.publish(topic, base64_message)
    #print('image sent')
    if count== 5 and (number >= 4):
        print('image sending')
        print('num devices : ' + str(len(devices)))
        cv2.imwrite('sample_out.jpg', frame)
        with open("sample_out.jpg", "rb") as image:
            img = image.read()
            img_f= cv2.imread("sample_out.jpg")
            
            #480, 640
            #imgResize = cv2.resize(img_f,(120, 160))
            if number%2 == 0:
                num_cols = int(number/2)
                num_rows = 2
                row_height = int(math.floor(height / num_rows))
                col_width = int(math.floor(width / num_cols))
                for i in range(number):
                    slot_num = i + 1
                    col = i%num_cols
                    if (i >= num_cols):
                        row = 1
                    else: 
                        row = 0
                    imgCropped.append(img_f[row*row_height:(row + 1)*row_height, col*col_width: (col+1)*col_width])
            else:
                num_cols = int(math.floor(number/2)) + number%2
                num_rows = 2
                row_height = int(math.floor(height / num_rows))
                col_width = int(math.floor(width / num_cols))
                for i in range(number):
                    if (i >= num_cols):
                        row = 1
                    else: 
                        row = 0
                    col = i%(num_cols - 1)
                    if (i == (number - 1)):
                        col = num_cols - 1
                        imgCropped.append(img_f[:(row+1)*row_height, col*col_width: (col+1)*col_width])
                    else:
                        #print("row: " + str(row) + "col: " + str(col))
                        imgCropped.append(img_f[row*row_height:(row+1)*row_height, col*col_width: (col+1)*col_width])
            
            for i in range(len(imgCropped)):
                cv2.imshow("%s"%i, imgCropped[i])
                        #cv2.imwrite('%s.jpg'%i, frame)
                        #with open("sample_out.jpg", "rb") as image:
                        #    img = image.read()
                        
                _, im_arr = cv2.imencode('.jpg', imgCropped[i])
                im_bytes = im_arr.tobytes()
                #message = imgCropped[i]
                base64_bytes = base64.b64encode(im_bytes)
                base64_message = base64_bytes.decode('ascii')
                client.publish(devices[i], base64_message)
                #client.publish(topic, base64_message)
            client.publish(devices[selected], "SLC" + str(myJoystick.horizontal))
        count=0
        
        #client.publish(topic, base64_message)
        imgCropped=[]
    if (number >= 4):
        count+=1
cap.release()
cv2.destroyAllWindows()

