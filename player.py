import i2c_dev as drivers
from time import sleep
from datetime import datetime
from rotary_class import RotaryEncoder
import RPi.GPIO as GPIO
import time, os

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

def indicate(text, line=1):
    length = len(text)
    for i in range(length, 16):
        text += " "
    display.lcd_display_string(text, 1)

indicate("Hi, startup")


station = 0
def rotary_unit_callback(event):
    global station
    if event == RotaryEncoder.ANTICLOCKWISE:
        if station < 10:
            station += 1
    elif event == RotaryEncoder.CLOCKWISE:
        if station > 0:
            station -= 1
    indicate("station:%i" % station)
    #time.sleep(bb)

# Define GPIO inputs for rotary encoder
PIN_A = 27	
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
    os.system("mpc volume %i" % vol)
    indicate("vol:%i" % vol)
    #time.sleep(bb)

GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.LOW)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.LOW)
# Define GPIO inputs for volume
PIN_VA = 6
PIN_VB = 12
volEncode = RotaryEncoder(PIN_VA,PIN_VB,False,volume_callback)

play = 0

def button_yellow(self):
    global play
    if play:
        os.system("mpc pause")
    else:
        os.system("mpc play %i" % station)
    #print("Yellow button")
    


# Yellow button
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(23, GPIO.BOTH, callback=button_yellow, bouncetime=200)

while True:
    time.sleep(1)