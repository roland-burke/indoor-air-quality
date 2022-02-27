# sensors
#from adafruit_bme280 import basic as adafruit_bme280
#import adafruit_ccs811

#import board

def initializeSensors():
    # initialize BME280
    # Remember to enable I2C
    try:
        i2c_bme280 = board.I2C()
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c_bme280, address=0x76)
    except Exception as e:
        print("Failed to initialize bme280 sensor:", e)
        bme280 = None

    try:
        i2c_ccs811 = busio.I2C(board.SCL, board.SDA)
        ccs811 = adafruit_ccs811.CCS811(i2c_ccs811)
    except Exception as e:
        print("Failed to initialize ccs811 sensor:", e)
        ccs811 = None

def getUptime():
    uptime = time.time() - psutil.boot_time()
    return time.strftime('%H:%M:%S', time.gmtime(uptime))

def getSensorData():
    try:
        temperature = bme280.temperature
        humidity = bme280.humidity
        pressure = bme280.pressure
        tvoc = ccs811.tvoc
        co2 = ccs811.eco2
    except:
        temperature = -1
        humidity = -1
        pressure = -1
        tvoc = -1
        co2 = -1

    data = {
		'temperature' : float("{:.2f}".format(temperature)),
		'humidity': float("{:.2f}".format(humidity)),
		'pressure': float("{:.2f}".format(pressure)),
        'tvoc': tvoc,
        'co2': co2
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