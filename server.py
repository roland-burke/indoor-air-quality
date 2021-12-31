from flask import Flask, render_template
import psutil
import time
import socket

app = Flask(__name__)

def getUptime():
    uptime = time.time() - psutil.boot_time()
    return time.strftime('%H:%M:%S', time.gmtime(uptime))

def getSensorData():
	data = {
         'temperature' : 23,
         'humidity': 45
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