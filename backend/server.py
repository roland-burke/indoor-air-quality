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
import threading

# webserver
from flask import Flask, send_from_directory
from flask_cors import CORS

# hardware
import board
import busio
import digitalio
import RPi.GPIO as GPIO

# display
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# sensor
from adafruit_bme280 import basic as adafruit_bme280

WIDTH = 128
HEIGHT = 64

x_start = 0
x_space = 72
y_start = 14
y_space = 10

# initialize Display
spi = busio.SPI(board.SCK, MOSI=board.MOSI)
reset_pin = digitalio.DigitalInOut(board.D19)
cs_pin = digitalio.DigitalInOut(board.D8)
dc_pin = digitalio.DigitalInOut(board.D13)

oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, dc_pin, reset_pin, cs_pin)

# setup Display
font = ImageFont.load_default()
image = Image.new('1',(128,64))
draw = ImageDraw.Draw(image)

displayCleared = False

draw.text((22, 30), "INITIALIZING", font=font, fill=255)
oled.image(image)
oled.show()
sleep(0.5)

# initialize LDR = Light Dependendent Resistor
GPIO.setmode(GPIO.BCM)
LDR_PIN=4 # input 1 means Bright
GPIO.setup(LDR_PIN,GPIO.IN)


def updateDisplay():
    # cleanup display
	draw.rectangle((0, 0, WIDTH, HEIGHT), outline = 0, fill=0)
    
	# Device name
	draw.text((x_start, 0), " Hostname:", font=font, fill=255)
	draw.text((x_space,0), socket.gethostname(), font=font, fill=255)
 
	# Temperature
	draw.text((x_start,y_start), " Temp:", font=font, fill=255)
	draw.text((x_space,y_start), "{:.1f} C".format(getSensorData()['temperature']), fill=255)
 
	# Huimidty
	draw.text((x_start,y_start + 10), " Humidity:", font=font, fill=255)
	draw.text((x_space,y_start + 10), "{:.0f} %".format(getSensorData()['humidity']), font=font, fill=255)
 
	# Pressure
	draw.text((x_start,y_start + 20), " Pressure:", font=font, fill=255)
	draw.text((x_space,y_start + 20), "{:.0f} hPa".format(getSensorData()['pressure']), font=font, fill=255)
 
	#TVOC
	draw.text((x_start,y_start + 30), " TVOC:", font=font, fill=255)
	draw.text((x_space,y_start + 30), "{}".format(100), font=font, fill=255)
 
	#CO2
	draw.text((x_start,y_start + 40), " CO2:", font=font, fill=255)
	draw.text((x_space,y_start + 40), "{}".format(800), font=font, fill=255)
	
	oled.image(image)
	oled.show()


def display_thread():
	while True:
		if GPIO.input(LDR_PIN) == 1:
			updateDisplay() # Bright
			displayCleared = False
		else:
			if not displayCleared:
				draw.rectangle((0, 0, WIDTH, HEIGHT), outline = 0, fill=0) # Dark
				oled.image(image)
				oled.show()
				displayCleared = True

		sleep(1)

displayThread = Thread(target = display_thread)

# initialize BME280
# Remember to enable I2C
i2c = board.I2C()
try:
	bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
except:
	bme280 = None

# initialize LDR = Light Dependendent Resistor
GPIO.setmode(GPIO.BCM)
LDR_PIN=4
GPIO.setup(LDR_PIN,GPIO.IN)


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
		temperature = bme280.temperature
		humidity = bme280.humidity
		pressure = bme280.pressure
	except:
		temperature = -1
		humidity = -1
		pressure = -1
     
	data = {
		'temperature' : float("{:.2f}".format(temperature)),
		'humidity': float("{:.2f}".format(humidity)),
		'pressure': float("{:.2f}".format(pressure))
	}
	return data

def getData():
    global alarmEnabled
    global displayEnabled
    data = {
         'hostname' : socket.gethostname(),
         'temperature': getSensorData().get('temperature'),
         'humidity': getSensorData().get('humidity'),
         'pressure': getSensorData().get('pressure'),
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
    displayThread.start()
    app.run(debug=False, port=5000, host='0.0.0.0')
