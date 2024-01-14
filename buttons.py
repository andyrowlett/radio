import i2c_dev as drivers
from time import sleep
from datetime import datetime
from rotary_class import RotaryEncoder
import RPi.GPIO as GPIO
import time, os, cls_mpc, cls_blt

# Define vars to track what is happening
vol = 30
v_step = 5
play = 0
pause = 0
# switch mode hold the track or playlist selection
switch_mode = 0
current_file = 0
current_list = 1
current_list_name = "play-sleep"
GPIO.setmode(GPIO.BCM) 

def button_red():
    print("red")

def button_green():
    print("green")

def button_yellow():
    print("yellow")

# Yellow button
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(23, GPIO.RISING, callback=button_yellow, bouncetime=500)
# red button
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(24, GPIO.RISING, callback=button_red, bouncetime=500)
# green button
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(25, GPIO.RISING, callback=button_green, bouncetime=500)