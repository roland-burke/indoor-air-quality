# sensors
import adafruit_ccs811
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280

from models import SensorDataModel

bme280 = None
ccs811 = None

BME280Working = False
CCS811Working = False

# Remember to enable I2C
def initializeBME280():
	global bme280
	try:
		i2c_bme280 = board.I2C()
		bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c_bme280, address=0x76)
		return True
	except Exception as e:
		print("Failed to initialize bme280 sensor:", e)
		bme280 = None
		return False

def initializeCCS811():
	global ccs811
	try:
		i2c_ccs811 = busio.I2C(board.SCL, board.SDA)
		ccs811 = adafruit_ccs811.CCS811(i2c_ccs811)
		return True
	except Exception as e:
		print("Failed to initialize ccs811 sensor:", e)
		ccs811 = None
		return False

def getTempHumIndex(temp, hum):
	temp = round(temp)

	if temp == 16:
		if hum <= 85 and hum >= 45:
			return 5
	elif temp == 17:
		if hum >= 85:
			return 5
		elif hum >= 55:
			return 4
		elif hum >= 15:
			return 5
	elif temp == 18:
		if hum >= 85:
			return 4
		elif hum >= 75:
			return 2
		elif hum >= 55:
			return 3
		elif hum >= 45:
			return 4
		elif hum >= 15:
			return 5
	elif temp == 19:
		if hum >= 85:
			return 3
		elif hum >= 55:
			return 2
		elif hum >= 45:
			return 3
		elif hum >= 25:
			return 4
		elif hum >= 15:
			return 5

	# todo temp 20 bis 27

	elif temp == 27:
		if hum <= 85 and hum >= 15:
			return 5
	
	# this is just an approximation
	if temp >= 20 and temp <= 26:
		if hum >= 30 and hum <= 75:
			return 2

	return 6

def getIndexLevel(temp, hum, co2, tvoc):
	co2Index = 0
	tvocIndex = 0
	tempHumIndex = getTempHumIndex(temp, hum)

	if co2 <= 400:
		co2Index = 1
	elif co2 <= 1000:
		co2Index = 2
	elif co2 <= 1500:
		co2Index = 3
	elif co2 <= 2000:
		co2Index = 4
	elif co2 <= 5000:
		co2Index = 5
	else:
		co2Index = 6

	if tvoc <= 50:
		tvocIndex = 1
	elif tvoc <= 100:
		tvocIndex = 2
	elif tvoc <= 150:
		tvocIndex = 3
	elif tvoc <= 200:
		tvocIndex = 4
	elif tvoc <= 300:
		tvocIndex = 5
	else:
		tvocIndex = 6

	if BME280Working and CCS811Working:
		return round((co2Index + tvocIndex + tempHumIndex) / 3, 0)

	if BME280Working and not CCS811Working:
		return tempHumIndex
		
	if not BME280Working and CCS811Working:
		return round((co2Index + tvocIndex) / 2, 0)
	return 0

def getData():
	global BME280Working
	global CCS811Working

	if not BME280Working:
		BME280Working = initializeBME280()
	try:	
		temperature = bme280.temperature
		humidity = bme280.humidity
		pressure = bme280.pressure
	except:
		BME280Working = False
		temperature = 0
		humidity = 0
		pressure = 0

	if not CCS811Working:
		CCS811Working = initializeCCS811()
	try:
		tvoc = ccs811.tvoc
		co2 = ccs811.eco2
	except:
		CCS811Working = False
		tvoc = 0
		co2 = 0

	return SensorDataModel(temperature, humidity, pressure, co2, tvoc, getIndexLevel(temperature, humidity, co2, tvoc), bme280Status=BME280Working, ccs811Status=CCS811Working)
