import i2c_dev as drivers
from time import sleep
from datetime import datetime
from rotary_class import RotaryEncoder
import RPi.GPIO as GPIO
import time

display = drivers.Lcd()
display.lcd_backlight(1)
cc = drivers.CustomCharacters(display)
cc.char_1_data = ["11111",
                "11111",
                "11111",
                "11111",
                "11111",
                "11111",
                "11111",
                "11111"]
cc.load_custom_characters_data()

def indicate(text):
    display.lcd_display_string(text, 1)

indicate("Hi")


station = 0
def rotary_unit_callback(event):
    global station
    if event == RotaryEncoder.CLOCKWISE:
        if station < 10:
            station += 1
    elif event == RotaryEncoder.ANTICLOCKWISE:
        if station > 0:
            station -= 1
    indicate(station)
    print("S=%s" % station)
    #time.sleep(bb)

# Define GPIO inputs for rotary encoder
PIN_A = 18 	
PIN_B = 17	
BUTTON = 0
rswitch = RotaryEncoder(PIN_A,PIN_B,BUTTON,rotary_unit_callback)

vol = 50
def volume_callback(event):
    global vol
    if event == RotaryEncoder.CLOCKWISE:
        if vol < 100:
            vol += 10
    elif event == RotaryEncoder.ANTICLOCKWISE:
        if vol > 0:
            vol -= 10
    indicate(station)
    print("S=%s" % station)
    #time.sleep(bb)

GPIO.setup(20, GPIO.OUT)
GPIO.output(20, GPIO.LOW)
# Define GPIO inputs for volume
PIN_VA = 19	
PIN_VB = 21
BUTTON = 0
vol = RotaryEncoder(PIN_VA,PIN_VB,BUTTON,volume_callback)

while True:
    time.sleep(1)