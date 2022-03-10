# general
from cProfile import run
from concurrent.futures import thread
from curses.ascii import NUL
from math import fabs
from ntpath import join
from signal import alarm
from time import sleep
import json
from threading import Thread
import socket
import time
import psutil # for uptime
import random

import sensors
import display

# webserver
from flask import Flask, send_from_directory
from flask_cors import CORS

# hardware
#import board
#import busio
#import digitalio
#import RPi.GPIO as GPIO

hostname = socket.gethostname()
room = "rolands-zimmer"
xDistance = 0 # distance to next vertical wall
yDistance = 0 # height, distance from ground

# initialize LDR = Light Dependendent Resistor
def initializeLDR():
    GPIO.setmode(GPIO.BCM)
    LDR_PIN=4 # input 1 means Bright
    GPIO.setup(LDR_PIN,GPIO.IN)

def display_thread():
    while True:
        if GPIO.input(LDR_PIN) == 1:
            updateDisplay(socket.gethostname(), sensors.getData()) # Bright
            displayCleared = False
        else:
           if not displayCleared:
                draw.rectangle((0, 0, WIDTH, HEIGHT), outline = 0, fill=0) # Dark
                oled.image(image)
                oled.show()
                displayCleared = True
        sleep(1)


displayThread = Thread(target = display_thread)

# initialize webserver

app = Flask(__name__, static_url_path='', static_folder='static')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

alarmEnabled = False
displayEnabled = True

def saveControls():
	controlsFile = open('controls.json', 'w+')
	controlsFile.seek(0, 0)
	controlsFile.write(json.dumps({"alarmEnabled": alarmEnabled, "displayEnabled": displayEnabled}, indent = 4))
	controlsFile.close()
 
def loadControls():
	global alarmEnabled
	global displayEnabled
	controlsFile = open('controls.json', 'r+')
	controlsFile.seek(0, 0)
	try:
		controls = json.load(controlsFile)
		alarmEnabled = controls['alarmEnabled']
		displayEnabled = controls['displayEnabled']
	except json.decoder.JSONDecodeError:
		alarmEnabled = False
		displayEnabled = True
	controlsFile.close()

def getUptime():
    uptime = time.time() - psutil.boot_time()
    return time.strftime('%H:%M:%S', time.gmtime(uptime))

def getData():
    global alarmEnabled
    global displayEnabled
    data = {
         'hostname' : hostname,
         'temperature': sensors.getData().get('temperature'),
         'humidity': sensors.getData().get('humidity'),
         'pressure': sensors.getData().get('pressure'),
         'co2': -1,
         'tvoc': -1,
         'uptime': getUptime(),
         'room': room,
         'alarmEnabled': alarmEnabled,
         'displayEnabled': displayEnabled
    }
    return getMockData()

def getMockData():
    return {
         'hostname' : hostname,
         'temperature': float("{:.2f}".format(random.uniform(21.0, 21.5))),
         'humidity': float("{:.2f}".format(random.uniform(40.0, 42.0))),
         'pressure': float("{:.2f}".format(random.uniform(972, 974))),
         'co2': random.randint(800,820),
         'tvoc': random.randint(120,130),
         'uptime': getUptime(),
         'room': room,
         'alarmEnabled': alarmEnabled,
         'displayEnabled': displayEnabled
    }

def setup():
    try:
        display.initialize
    except Exception as e:
        print("Failed to initialize display:", e)

    try:
        initializeLDR()
    except Exception as e:
        print("Failed to initialize LDR:", e)

    sensors.initialize()

    loadControls()
    saveControls()
    print("Alarm:", alarmEnabled)
    print("Display:", displayEnabled)

@app.route('/', methods = ['GET'])
def welcome():
	return send_from_directory('static', 'index.html')

@app.route('/api/data', methods = ['GET'])
def data():
	return getData()

@app.route('/api/controls/alarm/<value>', methods = ['POST'])
def controlAlarm(value):
	global alarmEnabled
	if value.lower() == 'true':
		alarmEnabled = True
		saveControls()
	elif value.lower() == 'false':
		alarmEnabled = False
		saveControls()
	else:
		data = {
			'status' : 'Error',
    	}
		return data

	data = {
		'status' : 'success',
    }
	return data

@app.route('/api/controls/display/<value>', methods = ['POST'])
def controlDisplay(value):
	global displayEnabled
	if value.lower() == 'true':
		displayEnabled = True
		saveControls()
	elif value.lower() == 'false':
		displayEnabled = False
		saveControls()
	else:
		data = {
			'status' : 'Error',
    	}
		return data

	data = {
		'status' : 'success',
    }
	return data


if __name__ == '__main__':
    setup()
    myThread = displayThread.start()
    thread.daemon=True

    app.run(debug=False, port=5000, host='0.0.0.0')