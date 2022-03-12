class DataModel:
    # meta data
    hostname = ""
    room = ""
    uptime = None

    # sensor data
    temperature = 0
    humidity = 0
    pressure = 0
    co2 = 0
    tvoc = 0

    # controls
    alarmEnabled = False
    displayEnabled = False

    def of(self, host, room, uptime, temp, hum, pressure, co2, tvoc, alarmEnabled, displayEnabled):
        self.hostname = host
        self.room = room
        self.uptime = uptime

        self.temperature = temp
        self.humidity = hum
        self.pressure = pressure
        self.co2 = co2
        self.tvoc = tvoc

        self.alarmEnabled = alarmEnabled
        self.displayEnabled = displayEnabled
        return self

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
        'sensors': {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'co2': self.co2,
            'tvoc': self.tvoc,
            }
        }