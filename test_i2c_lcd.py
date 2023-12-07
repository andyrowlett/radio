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

GPIO.setmode(GPIO.BCM)

bb = 0.1

GPIO.setup(17, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, GPIO.PUD_DOWN)

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


display.lcd_display_extended_string("Hello, zero", 1)
display.lcd_backlight(1)