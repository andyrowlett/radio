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

indicate("Hi, startup")


station = 0
def rotary_unit_callback(event):
    global station
    if event == RotaryEncoder.CLOCKWISE:
        if station < 10:
            station += 1
    elif event == RotaryEncoder.ANTICLOCKWISE:
        if station > 0:
            station -= 1
    indicate("station:%i" % station)
    #time.sleep(bb)

# Define GPIO inputs for rotary encoder
PIN_A = 18 	
PIN_B = 17	
rswitch = RotaryEncoder(PIN_A,PIN_B,False,rotary_unit_callback)

vol = 50
def volume_callback(event):
    global vol
    if event == RotaryEncoder.ANTICLOCKWISE:
        if vol < 100:
            vol += 10
    elif event == RotaryEncoder.CLOCKWISE:
        if vol > 0:
            vol -= 10
    indicate("vol:%i" % vol)
    #time.sleep(bb)

GPIO.setup(20, GPIO.OUT)
GPIO.output(20, GPIO.LOW)
# Define GPIO inputs for volume
PIN_VA = 19	
PIN_VB = 21
volEncode = RotaryEncoder(PIN_VA,PIN_VB,False,volume_callback)

def button_yellow():
    print("Hi")


# Yellow button
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(16, GPIO.BOTH, callback=button_yellow, bouncetime=200)

while True:
    time.sleep(1)