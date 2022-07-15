# general
import fcntl
import json
import os
import random
import socket
import struct
import time
from concurrent.futures import thread
from threading import Thread
from time import sleep
from typing import final

import psutil  # for uptime

# hardware
try:
	import RPi.GPIO as GPIO
except:
	print("Server: Imporintg RPi.GPIO failed")

# webserver
from flask import Flask, Response
from flask import request as req
from flask import send_from_directory
from flask_cors import CORS

import display
import sensors
from models import ControlsModel, DataModel, SensorDataModel

# Constants
BUZZER_DURATION = 1 # seconds
BUZZER_PAUSE = 0.5 # seconds
HIGH = 1 # bright
LOW = 0

# input 1 means Bright
LDR_PIN = 4 # GPIO 4, pin num: 7
BUZZER_PIN = 5 # GPIO 5, pin num: 29

# meta information
ROOM_IDENTIFIER = "rolands-zimmer"
xDistance = 0 # distance to next vertical wall
yDistance = 0 # height, distance from ground
hostname = socket.gethostname()

updateRate = 2 # seconds

alarmOn = False

displayWorking = False

controls = None

app = Flask(__name__, static_url_path='', static_folder='static')

# LDR = Light Dependendent Resistor
def initializeLDR():
	try:
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(LDR_PIN,GPIO.IN)
	except Exception as e:
		print("Failed to initialize LDR:", e)

def isBright():
	return GPIO.input(LDR_PIN) == HIGH

def display_thread():
	while True:
		if controls.smartDisplayEnabled:
			if isBright():
				display.update(socket.gethostname(), sensors.getData())
		elif controls.displayEnabled:
			display.update(socket.gethostname(), sensors.getData())
		else:
			display.clear()
		sleep(updateRate)

def saveControls(controls):
	try:
		controlsFile = open('controls.json', 'w+')
		controlsFile.seek(0, 0)
		controlsFile.write(json.dumps(controls.toJson(), indent = 4))
	except Exception as e:
		print("Failed to save controls:", e)
	finally:
		controlsFile.close()

 
def loadControls():
	global controls

	try:
		controlsFile = open('controls.json', 'r+')
		controlsFile.seek(0, 0)
		loaded = json.load(controlsFile)
		controls = ControlsModel.of(loaded)
	except Exception as e:
		controls = ControlsModel.initial()
		print("Failed to load controls:", e)
	finally:
		controlsFile.close()

def getUptime():
	uptime = time.time() - psutil.boot_time()
	return time.strftime('%H:%M:%S', time.gmtime(uptime))

def getHwAddr(ifname):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
	except:
		info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes("wlp0s20f3", 'utf-8')[:15]))
	return ':'.join('%02x' % b for b in info[18:24])

def getData():
	mode = os.environ['MODE']

	if mode == "dev":
		return getMockData()

	return DataModel(host=hostname, room=ROOM_IDENTIFIER, uptime=getUptime(), displayWorking=displayWorking, ipAddr=socket.gethostbyname(socket.gethostname()), macAddr=getHwAddr("wlan0"), sensors=sensors.getData(), controls=controls)

def getMockData():
	temperature = random.uniform(21.0, 21.5)
	humidity = random.uniform(40.0, 42.0)
	pressure = random.uniform(972, 974)
	co2 = random.randint(800,820)
	tvoc = random.randint(120,130)
	indexLevel = random.randint(0, 6)

	sensorData = SensorDataModel(temperature, humidity, pressure, co2, tvoc, indexLevel, sensors.BME280Working, sensors.CCS811Working)
	return DataModel(host=hostname, room=ROOM_IDENTIFIER, uptime=getUptime(), displayWorking=displayWorking, ipAddr=socket.gethostbyname(socket.gethostname()), macAddr=getHwAddr("wlan0"), sensors=sensorData, controls=controls)

def alarm():
	global alarmOn
	# abort if another alarm is still going on or alarm is disabled
	if alarmOn or not controls.alarmEnabled:
		return

	# abort if smart alarm is enabled and its dark outside
	if controls.smartAlarmEnabled and not isBright():
		return

	alarmOn = True

	GPIO.setup(BUZZER_PIN,GPIO.OUT)
	for i in range(2):
		GPIO.output(BUZZER_PIN, HIGH)
		time.sleep(BUZZER_DURATION)
		GPIO.output(BUZZER_PIN, LOW)
		time.sleep(BUZZER_PAUSE)
	GPIO.output(BUZZER_PIN, LOW)

	alarmOn = False


def setup():
	global displayWorking
	loadControls()

	displayWorking = display.initialize()
	initializeLDR()

# data must be a string
def getResponse(data, statusCode):
	return Response(data, status=statusCode, mimetype='application/json')

@app.route('/', methods = ['GET'])
def welcome():
	return send_from_directory('static', 'index.html')

@app.route('/api/data', methods = ['GET'])
def data():
	return getResponse(json.dumps(getData().toJson()), 200)

@app.route('/api/alarm/test', methods = ['POST'])
def testAlarm():
	if(not alarmOn):
		alarm()
		return getResponse(json.dumps({'status': 'success'}), 200)
	else:
		return getResponse(json.dumps({'status': 'alarm still in progress'}), 423)

@app.route('/api/controls', methods = ['POST'])
def setControls():
	global controls
	print(req.json)
	try:
		controls = ControlsModel.of(req.json)
		saveControls(controls)
		display.setMode(controls.displayMode)

	except:
		return getResponse(json.dumps({'status' : 'error'}), 500)
	return getResponse(json.dumps({'status' : 'success'}), 200)

if __name__ == '__main__':
	setup()

	if displayWorking:
		displayThread = Thread(target = display_thread)
		myThread = displayThread.start()
		thread.daemon=True
	else:
		print("Server: Failed to initialize display")
	
	cors = CORS(app)
	app.config['CORS_HEADERS'] = 'Content-Type'
	app.run(debug=False, port=5000, host='0.0.0.0')
