# display
from hashlib import new
from time import sleep

try:
	import adafruit_ssd1306
	import board
	import busio
	import digitalio
except:
	print("Display: Imporintg adafruit_ssd1306, board, busio, digitalio failed")

from PIL import Image, ImageDraw, ImageFont

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64

X_START = 0
Y_START = 14

X_SPACE = 72
Y_SPACE = 10

font = ImageFont.load_default()
image = Image.new('1',(128,64))
draw = ImageDraw.Draw(image)
oled = None

# 0 = Show everything: hostname, temp, hum, pressure, tvoc, c02
# 1 = Show 2 values and swithc: temp hum - tvoc co2 - pressure calculated height
displayMode = 0

# indicates which data is shown
# 0 = temp hum
# 1 = tvoc co2
# 2 = pressure height
pairCycle = 0

displayCleared = False

def initialize():
    global oled
    try:
        spi = busio.SPI(board.SCK, MOSI=board.MOSI)
        reset_pin = digitalio.DigitalInOut(board.D19)
        cs_pin = digitalio.DigitalInOut(board.D8)
        dc_pin = digitalio.DigitalInOut(board.D13)
        oled = adafruit_ssd1306.SSD1306_SPI(DISPLAY_WIDTH, DISPLAY_HEIGHT, spi, dc_pin, reset_pin, cs_pin)

        # show initial loading message
        initializeFont = ImageFont.truetype("Gidole-Regular.ttf", 20)
        draw.text((10, 20), "INITIALIZING", font=initializeFont, fill=255)
        oled.image(image)
        oled.show()
        sleep(1)
        return True
    except Exception as e:
        print("Failed to initialize display:", e)
        return False

def setMode(newMode):
    global displayMode
    if newMode <= 1 and newMode >= 0:
        displayMode = newMode

def updateEverything(hostname, data):
    global displayCleared
    # cleanup display
    draw.rectangle((0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT), outline = 0, fill=0)

    # Device name
    draw.text((X_START,0), " Hostname:", font=font, fill=255)
    draw.text((X_SPACE,0), hostname, font=font, fill=255)

    # Temperature
    draw.text((X_START,Y_START), " Temp:", font=font, fill=255)
    draw.text((X_SPACE,Y_START), "{:.1f} C".format(data.temperature), fill=255)

    # Huimidty
    draw.text((X_START,Y_START + 10), " Humidity:", font=font, fill=255)
    draw.text((X_SPACE,Y_START + 10), "{:.0f} %".format(data.humidity), font=font, fill=255)

    # Pressure
    draw.text((X_START,Y_START + 20), " Pressure:", font=font, fill=255)
    draw.text((X_SPACE,Y_START + 20), "{:.0f} hPa".format(data.pressure), font=font, fill=255)

    #TVOC
    draw.text((X_START,Y_START + 30), " TVOC:", font=font, fill=255)
    draw.text((X_SPACE,Y_START + 30), "{}".format(data.tvoc), font=font, fill=255)

    #CO2
    draw.text((X_START,Y_START + 40), " CO2:", font=font, fill=255)
    draw.text((X_SPACE,Y_START + 40), "{}".format(data.co2), font=font, fill=255)

    oled.image(image)
    oled.show()
    displayCleared = False

def drawTwo(dataString1, dataString2):
    pairFont = ImageFont.truetype("Gidole-Regular.ttf", 33)
    draw.text((X_START + 10, 0), dataString1, font=pairFont, fill=255)
    draw.text((X_START + 10, 32), dataString2, font=pairFont, fill=255)

def updatePairs(data):
    global displayCleared
    global pairCycle
    
    # cleanup display
    draw.rectangle((0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT), outline = 0, fill=0)

    if pairCycle == 0:
        drawTwo("{:.1f} °C".format(data.temperature), "{:.0f} %".format(data.humidity))
    elif pairCycle == 1:
        drawTwo("{} ppb".format(data.tvoc), "{} ppm".format(data.co2))
    else:
        drawTwo("{:.0f} hPa".format(data.pressure), "0 m")

    pairCycle = pairCycle + 1
    if pairCycle > 2:
        pairCycle = 0

    oled.image(image)
    oled.show()
    displayCleared = False

def update(hostname, data):
    global displayMode

    if displayMode == 0:
        updateEverything(hostname, data)
    else:
        updatePairs(data)

def clear():
    global displayCleared
    if not displayCleared:
        draw.rectangle((0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT), outline = 0, fill=0) # Dark
        oled.image(image)
        oled.show()
        displayCleared = True
