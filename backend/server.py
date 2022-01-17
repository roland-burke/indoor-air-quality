# general
from signal import alarm
import psutil
import time
import json

# webserver
from flask import Flask, send_from_directory
from flask_cors import CORS
import socket

# sensors
#import adafruit_dht
#import board


# init sensor
#dht_device = adafruit_dht.DHT11(board.D4)

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
	loadControls()
	saveControls()
	print(alarmEnabled)
	print(displayEnabled)


setup()

def getUptime():
    uptime = time.time() - psutil.boot_time()
    return time.strftime('%H:%M:%S', time.gmtime(uptime))

def getSensorData():
	try:
		temperature = dht_device.temperature
		humidity = dht_device.humidity
	except:
		temperature = -1
		humidity = -1
     
	data = {
		'temperature' : temperature,
		'humidity': humidity
	}
	return data

def getData():
    global alarmEnabled
    global displayEnabled
    data = {
         'hostname' : socket.gethostname(),
         'temperature': getSensorData().get('temperature'),
         'humidity': getSensorData().get('humidity'),
         'pressure': -1,
         'co2': -1,
         'tvoc': -1,
         'uptime': getUptime(),
         'alarmEnabled': alarmEnabled,
         'displayEnabled': displayEnabled
    }
    return data

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
    app.run(debug=False, port=5000, host='0.0.0.0')