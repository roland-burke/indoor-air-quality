# general
import psutil
import time

# webserver
from flask import Flask, render_template
import socket

# sensors
#import adafruit_dht
#import board


# init sensor
#dht_device = adafruit_dht.DHT11(board.D4)

app = Flask(__name__)

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
         'deviceName' : socket.gethostname(),
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
	return render_template('index.html')

@app.route('/api/data')
def data():
	return getData()
    
    
if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')