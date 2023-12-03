#! /usr/bin/env python

# Simple clock program. Writes the exact time.
# Demo program for the I2C 16x2 Display from Ryanteck.uk
# Created by Matthew Timmons-Brown for The Raspberry Pi Guy YouTube channel

# Import necessary libraries for communication and display use
import i2c_dev as drivers
from time import sleep
from datetime import datetime
from rotary_class import RotaryEncoder
import RPi.GPIO as GPIO
import time

bb = 0.1

# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd()
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
station = 0

max = 10
min = 0

def rotary_unit_callback(event):
    global station
    if event == RotaryEncoder.CLOCKWISE:
        if station < max:
            station += 1
    elif event == RotaryEncoder.ANTICLOCKWISE:
        if station > min:
            station -= 1
    indicate(station)
    print(station)
    time.sleep(bb)
    

# Define GPIO inputs for rotary encoder
PIN_A = 23 	
PIN_B = 17	
BUTTON = 20
rswitch = RotaryEncoder(PIN_A,PIN_B,BUTTON,rotary_unit_callback)

def indicate(station):
    pad = ""
    rpad = " "
    for i in range(0,station):
        pad += ' '
    for i in range(station+1, 16):
        rpad += ' '
    display.lcd_display_extended_string(pad + "{0x00}" + rpad, 1)

#display.lcd_display_extended_string(" {0x00}", 1)
#display.lcd_backlight(1)