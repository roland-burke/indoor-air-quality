from re import X


class ControlsModel:
    alarmEnabled = False
    displayEnabled = True
    smartAlarmEnabled = False
    smartDisplayEnabled = False

    def __init__(self, alarmEnabled, displayEnabled, smartAlarmEnabled, smartDisplayEnabled):
        self.alarmEnabled = alarmEnabled
        self.displayEnabled = displayEnabled
        self.smartAlarmEnabled = smartAlarmEnabled
        self.smartDisplayEnabled = smartDisplayEnabled

    def toJson(self):
        return {
            'alarmEnabled': self.alarmEnabled,
            'displayEnabled': self.displayEnabled,
            'smartAlarmEnabled': self.smartAlarmEnabled,
            'smartDisplayEnabled': self.smartDisplayEnabled
        }

    @staticmethod
    def of(controls):
        try:
            return ControlsModel(controls['alarmEnabled'], controls['displayEnabled'], controls['smartAlarmEnabled'], controls['smartDisplayEnabled'])
        except Exception as e:
            print("Error parsing controls:", e)
            return ControlsModel(False, True, False, False)

    @staticmethod
    def initial():
        return ControlsModel(False, True, False, False)


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

    def __init__(self, host, room, uptime, sensors, controls):
        self.hostname = host
        self.room = room
        self.uptime = uptime

        self.sensors = sensors
        self.controls = controls

    def toJson(self):
        return {
         'meta': {
            'hostname': self.hostname,
            'uptime': self.uptime,
            'room': self.room,
            },
        'controls': self.controls.toJson(),
        'sensors': self.sensors.toJson()
        }