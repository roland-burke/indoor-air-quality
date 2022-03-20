# sensors
#from adafruit_bme280 import basic as adafruit_bme280
#import adafruit_ccs811
#import busio

#import board
from models import SensorDataModel

bme280 = None
ccs811 = None

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

def getData():
    try:
        temperature = bme280.temperature
        humidity = bme280.humidity
        pressure = bme280.pressure
    except:
        temperature = 0
        humidity = 0
        pressure = 0

    try:
        tvoc = ccs811.tvoc
        co2 = ccs811.eco2
    except:
        tvoc = 0
        co2 = 0

    return SensorDataModel(temperature, humidity, pressure, co2, tvoc)