from flask import Flask, render_template
import psutil
import time
import socket
import adafruit_dht
import board
import time
import curses

# init sensor
dht_device = adafruit_dht.DHT11(board.D4)

app = Flask(__name__)

def getUptime():
    uptime = time.time() - psutil.boot_time()
    return time.strftime('%H:%M:%S', time.gmtime(uptime))

def getSensorData():
	temperature = dht_device.temperature
	humidity = dht_device.humidity
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
         'uptime': getUptime()
    }
    return data

@app.route('/')
def welcome():
	return render_template('index.html', **getData())

@app.route('/api/data')
def data():
	return getData()
    
    
if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')