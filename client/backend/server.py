# general
from cProfile import run
from concurrent.futures import thread
from time import sleep
import json
from threading import Thread
import socket
import time
import psutil # for uptime
import random

import sensors
import display
from models import DataModel, SensorDataModel

# webserver
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask import Response

# hardware
import RPi.GPIO as GPIO

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

displayWorking = False
BME280Working = False
CCS811Working = False

alarmEnabled = False
displayEnabled = True

app = Flask(__name__, static_url_path='', static_folder='static')

# LDR = Light Dependendent Resistor
def initializeLDR():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LDR_PIN,GPIO.IN)
    except Exception as e:
        print("Failed to initialize LDR:", e)

def display_thread():
    global displayEnabled
    while True:
        if GPIO.input(LDR_PIN) == HIGH and displayEnabled:
            display.update(socket.gethostname(), sensors.getData())
        else:
            display.clear()
        sleep(1)

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

    data = DataModel(host=hostname, room=ROOM_IDENTIFIER, uptime=getUptime(), sensors=sensors.getData(), alarmEnabled=alarmEnabled, displayEnabled=displayEnabled)
    return data

def getMockData():
    temperature = float("{:.2f}".format(random.uniform(21.0, 21.5))),
    humidity = float("{:.2f}".format(random.uniform(40.0, 42.0))),
    pressure = float("{:.2f}".format(random.uniform(972, 974))),
    co2 = random.randint(800,820),
    tvoc = random.randint(120,130),
    sensorData = SensorDataModel(temperature, humidity, pressure, co2, tvoc)
    data = DataModel(host=hostname, room=ROOM_IDENTIFIER, uptime=getUptime(), sensors=sensorData, alarmEnabled=alarmEnabled, displayEnabled=displayEnabled)
    return data

def alarm():
    GPIO.setup(BUZZER_PIN,GPIO.OUT)

    for i in range(3):
        GPIO.output(BUZZER_PIN, HIGH)
        time.sleep(BUZZER_DURATION)

        GPIO.output(BUZZER_PIN, LOW)
        time.sleep(BUZZER_PAUSE)

    GPIO.output(BUZZER_PIN, LOW)


def setup():
    global displayWorking
    global BME280Working
    global CCS811Working

    displayWorking = display.initialize()
    initializeLDR()

    BME280Working = sensors.initializeBME280()
    CCS811Working = sensors.initializeCCS811()

    loadControls()
    saveControls()

    alarm()


# data must be a string
def getResponse(data, statusCode):
    return Response(data, status=statusCode, mimetype='application/json')

@app.route('/', methods = ['GET'])
def welcome():
	return send_from_directory('static', 'index.html')

@app.route('/api/data', methods = ['GET'])
def data():
    return getResponse(json.dumps(getData().toJson()), 200)

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
		return getResponse(json.dumps({'status' : 'error'}), 400)
	return getResponse(json.dumps({'status' : 'success'}), 200)

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
		return getResponse(json.dumps({'status' : 'error'}), 400)
	return getResponse(json.dumps({'status' : 'success'}), 200)


if __name__ == '__main__':
    setup()

    displayThread = Thread(target = display_thread)
    myThread = displayThread.start()
    thread.daemon=True

    app.config['CORS_HEADERS'] = 'Content-Type'
    app.run(debug=False, port=5000, host='0.0.0.0')