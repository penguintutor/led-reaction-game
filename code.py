"""
NeoPixel reaction game with LCD display
"""
import board
import busio
import neopixel
import time
from digitalio import DigitalInOut, Direction, Pull
import adafruit_pixelbuf
from lcd.lcd import LCD, CursorMode
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

# delay when starting
time.sleep(1)

# NeoPixels
neopixel_pin = board.GP22

# Buttons
start_btn_pin = board.GP2
react_btn_pin = board.GP3

start_led_pin = board.GP18
react_led_pin = board.GP19

# Pin definitions
# I2C used for LCD Display
i2c_scl = scl = board.GP17
i2c_sda = board.GP16
i2c_address = 0x27 # 39 decimal

# NeoPixel info
num_pixels = 44
brightness = 0.5

# LCD display info
cols = 16
rows = 2

# Setup LCD display
i2c = busio.I2C(scl=i2c_scl, sda=i2c_sda)
interface = I2CPCF8574Interface(i2c, i2c_address)
lcd = LCD(interface, num_rows=rows, num_cols=cols)
lcd.set_cursor_mode(CursorMode.HIDE)

# Setup Buttons
start_btn = DigitalInOut(start_btn_pin)
start_btn.direction = Direction.INPUT
start_btn.pull = Pull.UP

react_btn = DigitalInOut(react_btn_pin)
react_btn.direction = Direction.INPUT
react_btn.pull = Pull.UP

# Setup button LEDs
start_led = DigitalInOut(start_led_pin)
start_led.direction = Direction.OUTPUT

react_led = DigitalInOut(react_led_pin)
react_led.direction = Direction.OUTPUT

# Setup neopixels
pixels = neopixel.NeoPixel(neopixel_pin, num_pixels, pixel_order = "GRB", auto_write = False, brightness = 0.5)
# Where the pixel is when scanning
pixel_position = 0
# Is pixel going left to right or right to left
# (Actual depends upon direction of strip) - forward is starting from pixel 0
pixel_forward = True
pixel_delay = 0.5




def main ():
    global pixel_delay, pixel_position

    score = 0

    #print ("starting")
    lcd.print ("Starting...")
    flash_lights()


    lcd.clear()
    start_led.value = True
    lcd.print ("Press start to\nstart game")

    # Wait until button pressed
    while start_btn.value:
        continue
    flash_lights(color=(0,0,255), delay=0.4)
    lcd.clear()
    start_led.value = False
    react_led.value = True
    lcd.print ("Play")

    while True:

        # while button not pressed
        while (react_btn.value):
            pixel_move()

        lcd.clear()
        react_led.value = False

        # Whatever pixel is selected is what user reacted to
        if pixel_position == int(num_pixels / 2-1):
            score += 1
            lcd.print ("On target! \nScore: "+str(score))
            pixel_delay -= 0.1
            if (pixel_delay < 0):
                pixel_delay = 0
            pixel_position = 0
            flash_lights ((0,255,0))
        else:
            lcd.print ("Game Over!\n Score "+str(score))
            pixel_delay = 0.5
            pixel_position = 0
            flash_lights ((255,0,0))
            while start_btn.value:
                continue
            score = 0
            flash_lights(color=(0,0,255), delay=0.4)
            lcd.clear()
            lcd.print ("Play")

def flash_lights (color=(255,255,255), delay=1, num_flashes=3):
    for i in range (num_flashes):
        pixels.fill(color)
        pixels.show()
        time.sleep(delay)
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(delay)

# move 1 pixel in the selected direction
def pixel_move (color=(255,255,255)):
    global pixel_position, pixel_forward
    if pixel_forward:
        pixel_position += 1
        if (pixel_position >= num_pixels):
            pixel_position = num_pixels -1
            pixel_forward = not pixel_forward
    else:
        pixel_position -= 1
        if (pixel_position <= 0):
            pixel_position = 0
            pixel_forward = not pixel_forward
    # Light up this pixel
    pixels.fill((0,0,0))
    pixels[pixel_position] = color
    pixels.show()
    if (pixel_delay > 0):
        time.sleep(pixel_delay)


if __name__ == '__main__':
    main()