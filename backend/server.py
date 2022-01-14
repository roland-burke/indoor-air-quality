# general
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

def setup():
	controlsFile = open('controls.json', 'a+')
	controlsFile.seek(0)
	#controls = json.load(controlsFile)

	try:
		controls = json.load(controlsFile)
		alarmEnabled = controls['alarmEnabled']
		displayEnabled = controls['displayEnabled']
	except json.decoder.JSONDecodeError:
		alarmEnabled = False
		displayEnabled = True
		print('exception')
		controlsFile.write(json.dumps({"alarmEnabled": alarmEnabled, "displayEnabled": displayEnabled}, indent = 4))
	controlsFile.close()

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
    data = {
         'hostname' : socket.gethostname(),
         'temperature': getSensorData().get('temperature'),
         'humidity': getSensorData().get('humidity'),
         'pressure': -1,
         'co2': -1,
         'tvoc': -1,
         'uptime': getUptime()
    }
    return data

@app.route('/')
def welcome():
	return send_from_directory('static', 'index.html')

@app.route('/api/data')
def data():
	return getData()

@app.route('/api/controls/alarm/<value>')
def controlAlarm(value):
	if value.lower() == 'true':
		controlAlarm = True
	elif value.lower() == 'false':
		controlAlarm = False
	else:
		data = {
			'status' : 'Error',
    	}
		return data

	data = {
		'status' : 'success',
    }
	return data

@app.route('/api/controls/display/<value>')
def controlDisplay(value):
	if value.lower() == 'true':
		saveControls()
		controlDisplay = True
	elif value.lower() == 'false':
		saveControls()
		controlDisplay = False
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