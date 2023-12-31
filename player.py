import i2c_dev as drivers
from time import sleep
from datetime import datetime
from rotary_class import RotaryEncoder
import RPi.GPIO as GPIO
import time, os, cls_mpc

# Define vars to track what is happening
vol = 30
v_step = 5
play = 0
pause = 0
sleepl = 1
current_file = 0
GPIO.setmode(GPIO.BOARD) 

os.system("mpc volume %i" % vol)
os.system("mpc clear")
os.system("mpc load play-sleep")

Playlist = cls_mpc.Playlist()

display = drivers.Lcd()
display.lcd_backlight(1)

def indicate(text, line=1):
    length = len(text)
    for i in range(length, 16):
        text += " "
    display.lcd_display_string(text, line)

def rotary_unit_callback(event):
    global current_file, Playlist, trck_name
    if event == RotaryEncoder.ANTICLOCKWISE:
        if current_file < Playlist.playlist_length:
            current_file += 1
    elif event == RotaryEncoder.CLOCKWISE:
        if current_file > 1:
            current_file -= 1
    file_name = Playlist.playlist[current_file - 1]
    auth_name = file_name.split('-')[0]
    trck_name = file_name.split('-')[1].strip()
    indicate("%i:%s" % (current_file, trck_name), 1)


def volume_callback(event):
    global vol
    if event == RotaryEncoder.ANTICLOCKWISE:
        if vol < 100:
            vol += v_step
    elif event == RotaryEncoder.CLOCKWISE:
        if vol > 0:
            vol -= v_step
    os.system("mpc volume %i" % vol)
    indicate("vol:%i" % vol, 2)


def button_yellow(self):
    global play, pause
    if play:
        play = 0
        pause = 1
        os.system("mpc pause")
        indicate("Pause", 2)
    else:
        if pause == 1:
            os.system("mpc play")
        else:
            os.system("mpc play %i" % current_file)
        indicate("Playing...", 2)
        play = 1
        pause = 0
    print("Yellow button")
    
def button_red(self):
    global play, pause
    play = 0
    pause = 0
    os.system("mpc stop")
    indicate("Stop", 2)
    print("red")

def button_green(self):
    global sleepl, st_max
    if sleepl == 1:
        sleepl = 0
        os.system("mpc clear")
        os.system("mpc load play-stories")
        Playlist.reinit()
        indicate("Loaded stories", 2)
    else:
        sleepl = 1
        os.system("mpc clear")
        os.system("mpc load play-sleep")
        Playlist.reinit()
        indicate("Loaded sleep", 2)       

# Yellow button
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(23, GPIO.RISING, callback=button_yellow, bouncetime=400)
# Yellow button
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(24, GPIO.RISING, callback=button_red, bouncetime=400)
# green button
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(25, GPIO.RISING, callback=button_green, bouncetime=400)

# Setup additional grounds for rotary encoder
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.LOW)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.LOW)

# Define GPIO inputs for rotary encoder
PIN_A = 27	
PIN_B = 17	
rswitch = RotaryEncoder(PIN_A,PIN_B,False,rotary_unit_callback)

# Define GPIO inputs for volume
PIN_VA = 6
PIN_VB = 12
volEncode = RotaryEncoder(PIN_VA,PIN_VB,False,volume_callback)

indicate("Player 1")

while True:
    time.sleep(1)