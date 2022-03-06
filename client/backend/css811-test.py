import time
import board
import busio
import adafruit_ccs811

i2c_bus = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c_bus)

while not ccs811.data_ready:
    pass

while True:
    print("CO2: %f PPM" % ccs811.eco2)
    print("TVOC: %f PPM" % ccs811.tvoc)
    time.sleep(1)

    