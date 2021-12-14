# Final Project
by Nicholas Burka (nab262)

and Jeongmin Huh (jh2229)

## Big Idea

We have a batch of old cell phones one of our team members purchased from a cell phone repair store that was going out of business (to convert to a music studio). We’d like to “revive” these, by using them as augmented displays and touchscreens for regular computer use. We hope to answer the questions: What typical HCI experiences would be enhanced by an additional, smaller screen? How can using the phone’s touch display augment the user experience?

We’ve thought of several potential use cases, scaling in anticipated complexity. However, at the basic level of what a screen display is, they best communicate images or video. Then we thought about how expansive the human visual experience becomes through the medium of a phone display, yet so limited by its small framed screen. So we came up with an idea that attempts to expand our attention to detail by bringing to the forefront the missed details of our perspective through the screens.


## Parts Needed
Batch of old phones to test / multiple screens

Raspberry Pi 4 + External Camera

[Spacedesk](https://www.spacedesk.net/) (software) installed on the phone and computer


## Ideation phase
Initially, our idea was to use the phone for productivity purposes, by delegating minimal but useful information from the big screen to the smaller phone screens. This is how we first strived to develop "Digital Sticky Notes". Instead of using paper sticky notes around the deskspace, room, house, one would place these old phones and from the connected computer, compose messages, tasks, figures, or motivation quotes and send them to each phone. The reader of the messages on the phone screens would also be able to interact with these screens to communicate back through these screens with a few simple touches of the screen. However, we found this idea not interactive enough for our liking.

<img width="588" alt="image" src="https://user-images.githubusercontent.com/89954387/145902591-ab3ff7d7-b0c3-4d43-b33e-af3d0ad3fc43.png">
<img width="588" alt="image" src="https://github.com/nicholasburka/IDD-final/blob/main/spacedesk-1.png">

Our new idea is more suited for interactive purposes, by delegating segments of one image stream to however many screen devices connected to the host. This was done using MQTT Explorer. This opens up many possibilities for potential uses. The confusion caused by the breaking of the mechanism of how human process what s/he sees allows for interactive challenges that can explored in games, performance arts, or even film effects.

<img width="586" alt="image" src="https://user-images.githubusercontent.com/89954387/145922215-2d62b05f-8e9c-4558-b608-f7e0b9bc52aa.png">


## Storyboard

<img width="1025" alt="image" src="https://user-images.githubusercontent.com/89954387/145920015-ae853088-5a6b-41d3-84f4-04076a52273b.png">

This storyboard is inspired by the famous parable from India of the blind men and the elephant.
The illustration suggests that many visual effects could be accomplished for something as simple as puzzles for children, or grandiose for large-scale concerts, or in films, not unlike that achieved in the iconic Bruce Lee scene in the 1974 film "Enter the Dragon", which evokes a unique set of emotions (confusion, suspense, curiosity etc.) in the viewer.
![image](https://user-images.githubusercontent.com/89954387/145920336-aa8841d0-0d09-4108-a22c-48abde012543.png)


## Setup

The architecture of our system depends on running an MQTT broker (probably on a Raspberry Pi), an MQTT video streaming client (we also had this on the Raspberry Pi), and a live webpage on each client/screen container (we used this repo and hosted our static files on GitHub Pages). The webpage is oldcellmqtt.html, and the python code for the server is mqtt-slice-work-joy.py. The config file for the broker is m.conf.

BROKER
To get the server running, install mosquitto using sudo apt-get install mosquitto

To communicate with the web browser, the server has to be configured to use web sockets.
To configure the MQTT server (called a broker) to use websockets, the server must be configured
in a config file in /etc/mosquitto/conf.d/a_conf_file.conf. Our conf file is called m.conf, in this repo.

For more info, check out:
http://www.steves-internet-guide.com/mqtt-websockets/

Pretty much all you have to do is designate a listener port and say websockets.
Then you can get the broker up and running by running mosquitto -c /etc/mosquitto/conf.d/conf_file.conf
If it works, there won't be any errors in the terminal. Sometimes we fixed errors by switching around the
port number randomly, which might indicate that the problem comes from old mosquitto instances still running.

VIDEO SERVER
To get the video server running, configure the MQTT topic name and MQTT connection IP address and port. 
The first will need to match the topic to be run in the webpage, and the 2nd and 3rd will need to match the broker. 

Then run the video server by call python video_server_filename.py

The video server won't begin streaming until at least 2 screens/screen containers have connected. This includes
if one screen runs the same webpage in two windows - the video server will consider this 2 screens and begin
streaming to them.

WEBPAGE
Match the MQTT topic to the video server. Match the IP address and port to the Broker's device IP address (the Pi's, if the
broker is running on the Pi) and the websocket port number from the broker config file.

Then upload the webpage or try opening it locally. If there are issues about an insecure connection, either allow the
insecure connection to that specific URL by going into the browser's settings (tested on Chrome) or provide a 
certificate. We at one point attempted to generate an SSL certificate according to [this guide](http://www.steves-internet-guide.com/mosquitto-tls/), but couldn't get it working - be warned that the steps require careful attention, including to the author's
sidenotes.

If the webpage and video server connect, then the video server will split the video feed onto the connected screens
once two screens have connected. If the web console is open, then a real-time feed of incoming MQTT messages will be displayed,
including the handshake message. When the webpage attempts to connect, it sends a random session ID, and once the webpage
receives an ACK (acknowledgement) of its ID, it subscribes to the channel of its ID, waiting for images from the video stream
to display on the HTML5 canvas.

## Demo
[Jeongmin and Nicholas pretending to become one body, using the completed 'ManyFrom1' Prototype](https://www.youtube.com/watch?v=doB3IrJ9eHw)
