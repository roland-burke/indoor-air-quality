class SensorDataModel:
    # sensor data
    temperature = 0
    humidity = 0
    pressure = 0
    co2 = 0
    tvoc = 0

    def __init__(self, temp, hum, pressure, co2, tvoc):
        self.temperature = temp
        self.humidity = hum
        self.pressure = pressure
        self.co2 = co2
        self.tvoc = tvoc

    def toJson(self):
        return {
            'temperature': float("{:.2f}".format(self.temperature)),
            'humidity': float("{:.2f}".format(self.humidity)),
            'pressure': float("{:.2f}".format(self.pressure)),
            'co2': self.co2,
            'tvoc': self.tvoc,
        }

class DataModel:
    # meta data
    hostname = ""
    room = ""
    uptime = None

    # sensor data
    sensors = SensorDataModel(0, 0, 0, 0, 0)

    # controls
    alarmEnabled = False
    displayEnabled = False

    def __init__(self, host, room, uptime, sensors, alarmEnabled, displayEnabled):
        self.hostname = host
        self.room = room
        self.uptime = uptime

        self.sensors = sensors

        self.alarmEnabled = alarmEnabled
        self.displayEnabled = displayEnabled

    def toJson(self):
        return {
         'meta': {
            'hostname': self.hostname,
            'uptime': self.uptime,
            'room': self.room,
            },
        'controls': {
            'alarmEnabled': self.alarmEnabled,
            'displayEnabled': self.displayEnabled
            },
        'sensors': self.sensors.toJson()
        }