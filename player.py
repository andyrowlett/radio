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
switch_mode = 0
current_file = 0
current_list = 0
current_list_name = "play-sleep"
GPIO.setmode(GPIO.BCM) 

os.system("mpc volume %i" % vol)
os.system("mpc clear")
os.system("mpc load %s" % current_list_name)

Playlist = cls_mpc.Playlist()

lcd_test = 0
try:
    display = drivers.Lcd()
    display.lcd_backlight(1)
except:
    lcd_test = 1

def indicate(text, line=1):
    if not lcd_test:
        length = len(text)
        for i in range(length, 16):
            text += " "
        display.lcd_display_string(text, line)
    else:
        print(text)

def rotary_unit_callback(event):
    global current_file, Playlist, trck_name
    if event == RotaryEncoder.ANTICLOCKWISE:
        if current_file < Playlist.playlist_length:
            current_file += 1
    elif event == RotaryEncoder.CLOCKWISE:
        if current_file > 1:
            current_file -= 1
    file_name = Playlist.playlist[current_file - 1]
    if "-" in file_name:
        auth_name = file_name.split('-')[0]
        trck_name = file_name.split('-')[1].strip()
    else:
        trck_name = file_name
    indicate("%i:%s" % (current_file, trck_name), 1)

def rotary_unit_callback_p(event):
    global current_list, Playlist, current_list_name
    if event == RotaryEncoder.ANTICLOCKWISE:
        if current_list < Playlist.playlists_length:
            current_list += 1
    elif event == RotaryEncoder.CLOCKWISE:
        if current_list > 1:
            current_list -= 1
    try:
        current_list_name = Playlist.playlists[current_list - 1].split('.')[0]
    except:
        current_list_name = Playlist.playlists[current_list - 1]
    indicate("%i:%s" % (current_list, current_list_name), 1)


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
    global play, pause, switch_mode, current_file
    if switch_mode:
        # in playlist mode, so load that playlist, and return to track mode
        os.system("mpc clear")
        os.system("mpc load %s" % current_list_name)
        indicate("Loaded %s" % current_list_name, 2)
        Playlist.reinit()
        current_file = 1
        # call green button to switch back
        button_green(False)

    else:
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
    global rswitch, switch_mode
    GPIO.remove_event_detect(PIN_A)
    GPIO.remove_event_detect(PIN_B)
    if switch_mode == 0:
        indicate("Select story", 2)
        rswitch = RotaryEncoder(PIN_A,PIN_B,False,rotary_unit_callback_p)   
        switch_mode = 1
    else:  
        indicate("Select track", 2)
        rswitch = RotaryEncoder(PIN_A,PIN_B,False,rotary_unit_callback)   
        switch_mode = 0

# Yellow button
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(23, GPIO.RISING, callback=button_yellow, bouncetime=500)
# Yellow button
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(24, GPIO.RISING, callback=button_red, bouncetime=500)
# green button
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(25, GPIO.RISING, callback=button_green, bouncetime=500)

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

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Keyboard stop, exit...")
    GPIO.cleanup()
except:
    GPIO.cleanup()