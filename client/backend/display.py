# display
from PIL import Image, ImageDraw, ImageFont
from time import sleep
import adafruit_ssd1306
import busio
import board
import digitalio

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
        draw.text((22, 30), "INITIALIZING", font=font, fill=255)
        oled.image(image)
        oled.show()
        sleep(0.5)
        return True
    except Exception as e:
        print("Failed to initialize display:", e)
        return False

def update(hostname, data):
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

def clear():
    global displayCleared
    if not displayCleared:
        draw.rectangle((0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT), outline = 0, fill=0) # Dark
        oled.image(image)
        oled.show()
        displayCleared = True