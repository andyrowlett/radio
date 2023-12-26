import i2c_dev as drivers
from time import sleep
from datetime import datetime
from rotary_class import RotaryEncoder
import RPi.GPIO as GPIO
import time, os

vol = 30
v_step = 5
os.system("mpc volume %i" % vol)
os.system("mpc clear")
os.system("mpc load playlist")

def get_max():
	global playlist
	pls = os.popen("mpc playlist").read()
	playlist = pls.splitlines()
	max = len(playlist)
	return max

st_max = get_max()

display = drivers.Lcd()
display.lcd_backlight(1)

def indicate(text, line=1):
    length = len(text)
    for i in range(length, 16):
        text += " "
    display.lcd_display_string(text, line)

indicate("Player 1")


cur_file = 0
def rotary_unit_callback(event):
    global cur_file, playlist, trck_name
    if event == RotaryEncoder.ANTICLOCKWISE:
        if cur_file < st_max:
            cur_file += 1
    elif event == RotaryEncoder.CLOCKWISE:
        if cur_file > 1:
            cur_file -= 1
    file_name = playlist[cur_file - 1]
    auth_name = file_name.split('-')[0]
    trck_name = file_name.split('-')[1].strip()
    indicate("%i:%s" % (cur_file, trck_name), 1)
    #indicate(trck_name, 2)
    #time.sleep(bb)

# Define GPIO inputs for rotary encoder
PIN_A = 27	
PIN_B = 17	
rswitch = RotaryEncoder(PIN_A,PIN_B,False,rotary_unit_callback)


def volume_callback(event):
    global vol
    if event == RotaryEncoder.ANTICLOCKWISE:
        if vol < 100:
            vol += v_step
    elif event == RotaryEncoder.CLOCKWISE:
        if vol > 0:
            vol -= v_step
    os.system("mpc volume %i" % vol)
    indicate("vol:%i" % vol)
    time.sleep(1)
    indicate("%i - %s" % (cur_file, trck_name), 1)
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
        play = 0
        os.system("mpc pause")
        indicate("Pause", 2)
    else:
        play = 1
        os.system("mpc play %i" % cur_file)
        indicate("Playing...", 2)
    print("Yellow button")
    
def button_red(self):
    os.system("mpc stop")
    indicate("Stop", 2)
    print("red")

def button_green(self):
    print("green")

# Yellow button
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(23, GPIO.RISING, callback=button_yellow, bouncetime=200)
# Yellow button
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(24, GPIO.RISING, callback=button_red, bouncetime=200)
# green button
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(25, GPIO.RISING, callback=button_green, bouncetime=200)

while True:
    time.sleep(1)