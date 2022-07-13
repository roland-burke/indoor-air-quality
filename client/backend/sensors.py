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
	except Exception as e:
		print("Failed to initialize bme280 sensor:", e)
		bme280 = None

def initializeCCS811():
	global ccs811
	try:
		i2c_ccs811 = busio.I2C(board.SCL, board.SDA)
		ccs811 = adafruit_ccs811.CCS811(i2c_ccs811)
	except Exception as e:
		print("Failed to initialize ccs811 sensor:", e)
		ccs811 = None

def getData():
	global BME280Working
	global CCS811Working

	if not BME280Working:
		initializeBME280()
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
		initializeCCS811()
	try:
		tvoc = ccs811.tvoc
		co2 = ccs811.eco2
	except:
		CCS811Working = False
		tvoc = 0
		co2 = 0

	return SensorDataModel(temperature, humidity, pressure, co2, tvoc, bme280Status=BME280Working, ccs811Status=CCS811Working)
