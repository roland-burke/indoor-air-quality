
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
    temperature = 0.0
    humidity = 0.0
    pressure = 0.0
    co2 = 0.0
    tvoc = 0.0

    def __init__(self, temp, hum, pressure, co2, tvoc):
        self.temperature = temp
        self.humidity = hum
        self.pressure = pressure
        self.co2 = co2
        self.tvoc = tvoc

    def toJson(self):
        return {
            'temperature': round(self.temperature, 2),
            'humidity': round(self.humidity, 2),
            'pressure': round(self.pressure, 2),
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

    def __init__(self, host, room, uptime, sensors, controls, ipAddr, macAddr):
        self.hostname = host
        self.room = room
        self.uptime = uptime
        self.ipAddr = ipAddr
        self.macAddr = macAddr

        self.sensors = sensors
        self.controls = controls

    def toJson(self):
        return {
         'meta': {
            'hostname': self.hostname,
            'uptime': self.uptime,
            'room': self.room,
            'ipAddr': self.ipAddr,
            'macAddr': self.macAddr
            },
        'controls': self.controls.toJson(),
        'sensors': self.sensors.toJson()
        }