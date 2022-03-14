# display
from PIL import Image, ImageDraw, ImageFont
from time import sleep
import adafruit_ssd1306
import busio
import board
import digitalio

WIDTH = 128
HEIGHT = 64

x_start = 0
x_space = 72
y_start = 14
y_space = 10

font = ImageFont.load_default()
image = Image.new('1',(128,64))
draw = ImageDraw.Draw(image)
oled = None

def initialize():
    global oled
    try:
        spi = busio.SPI(board.SCK, MOSI=board.MOSI)
        reset_pin = digitalio.DigitalInOut(board.D19)
        cs_pin = digitalio.DigitalInOut(board.D8)
        dc_pin = digitalio.DigitalInOut(board.D13)
        oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, dc_pin, reset_pin, cs_pin)

        displayCleared = False

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
    # cleanup display
	draw.rectangle((0, 0, WIDTH, HEIGHT), outline = 0, fill=0)
    
	# Device name
	draw.text((x_start, 0), " Hostname:", font=font, fill=255)
	draw.text((x_space,0), hostname, font=font, fill=255)
 
	# Temperature
	draw.text((x_start,y_start), " Temp:", font=font, fill=255)
	draw.text((x_space,y_start), "{:.1f} C".format(data['temperature']), fill=255)
 
	# Huimidty
	draw.text((x_start,y_start + 10), " Humidity:", font=font, fill=255)
	draw.text((x_space,y_start + 10), "{:.0f} %".format(data['humidity']), font=font, fill=255)
 
	# Pressure
	draw.text((x_start,y_start + 20), " Pressure:", font=font, fill=255)
	draw.text((x_space,y_start + 20), "{:.0f} hPa".format(data['pressure']), font=font, fill=255)
 
	#TVOC
	draw.text((x_start,y_start + 30), " TVOC:", font=font, fill=255)
	draw.text((x_space,y_start + 30), "{}".format(data['tvoc']), font=font, fill=255)
 
	#CO2
	draw.text((x_start,y_start + 40), " CO2:", font=font, fill=255)
	draw.text((x_space,y_start + 40), "{}".format(data['co2']), font=font, fill=255)
	
	oled.image(image)
	oled.show()