# general
from cProfile import run
from concurrent.futures import thread
from curses.ascii import NUL
from math import fabs
from ntpath import join
from signal import alarm
import psutil # for uptime
import time
from time import sleep
import json
import socket
from threading import Thread
import data_read
import display
import database

# webserver
from flask import Flask, send_from_directory
from flask_cors import CORS

# hardware
#import board
#import busio
#import digitalio
#import RPi.GPIO as GPIO


# initialize LDR = Light Dependendent Resistor
def initializeLDR():
    GPIO.setmode(GPIO.BCM)
    LDR_PIN=4 # input 1 means Bright
    GPIO.setup(LDR_PIN,GPIO.IN)

def display_thread():
    while True:
        if GPIO.input(LDR_PIN) == 1:
            updateDisplay(socket.gethostname(), getSensorData()) # Bright
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

def setup():
    try:
        display.initialize
    except Exception as e:
        print("Failed to initialize display:", e)

    try:
        initializeLDR()
    except Exception as e:
        print("Failed to initialize LDR:", e)

    data_read.initializeSensors()

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