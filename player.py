import i2c_dev as drivers
from time import sleep
from datetime import datetime
from rotary_class import RotaryEncoder
import RPi.GPIO as GPIO
import time, os, cls_mpc, cls_blt
from multiprocessing import Process


# Define vars to track what is happening
vol = 30
v_step = 5
play = 0
pause = 0
# switch mode hold the track or playlist selection
switch_mode = 0
current_file = 0
current_list = 1
current_list_name = "Moana"
GPIO.setmode(GPIO.BCM) 

Blue = cls_blt.Blue()
Blue.connect(Blue.square)

os.system("mpc volume %i" % vol)
os.system("mpc clear")
os.system("mpc load %s" % current_list_name)

### SLEEP MODE ###

awake = 1
sleepint = 0

def wakeUp():
    global awake, sleepint
    awake = 1
    sleepint += 1
    display.lcd_backlight(1)
    try:
        p = Process(target=goSleep, args=(sleepint,))
        p.start()
    except:
        print('n')

def goSleep(s):
    global awake, sleepint
    if not awake or s != sleepint:
        return
    time.sleep(20)
    awake = 0
    display.lcd_backlight(0)


### END SLEEP MODE ###


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
        if length < 16:
            for i in range(length, 16):
                text += " "
        else:
            text = text[:16]
        display.lcd_display_string(text, line)
        #asyncio.sleep(20)
        #display.lcd_backlight(0)
    else:
        print(text)

def rotary_unit_callback(event):
    global current_file, Playlist
    if event == RotaryEncoder.ANTICLOCKWISE:
        if current_file < Playlist.playlist_length:
            current_file += 1
    elif event == RotaryEncoder.CLOCKWISE:
        if current_file > 1:
            current_file -= 1
    show_track()

def rotary_unit_callback_p(event):
    global current_list, Playlist, current_list_name
    if event == RotaryEncoder.ANTICLOCKWISE:
        if current_list < Playlist.playlists_length:
            current_list += 1
    elif event == RotaryEncoder.CLOCKWISE:
        if current_list > 1:
            current_list -= 1    
    show_playlist()

def show_track():
    global current_file, Playlist
    Playlist.reinit()
    file_name = Playlist.get_track(current_file)
    indicate("%i:%s" % (current_file, file_name), 1)

def show_playlist():
    global current_list, Playlist, current_list_name
    Playlist.reinit()
    current_list_name = Playlist.get_playlist(current_list)
    indicate("%i:%s" % (current_list, current_list_name), 1)


def volume_callback(event):
    wakeUp()
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
    wakeUp()
    global play, pause, switch_mode, current_file, current_list
    if switch_mode:
        # in playlist mode, so load that playlist, and return to track mode
        os.system("mpc clear")
        os.system("mpc load %s" % current_list_name)
        indicate("Loaded %s" % current_list_name, 2)
        Playlist.reinit()
        current_file = 1
        show_track()
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
    
red_mode = 1

def button_red(self):
    wakeUp()
    global play, pause, red_mode

    Blue = cls_blt.Blue()
    Blue.connect(Blue.square)

    play = 0
    pause = 0
    os.system("mpc stop")
    indicate("Stop", 2)
    print("red")
    red_mode = 2
    time.sleep(1)
    red_mode = 1

def button_green(self):
    wakeUp()
    global rswitch, switch_mode
    GPIO.remove_event_detect(PIN_A)
    GPIO.remove_event_detect(PIN_B)
    if switch_mode == 0:
        indicate("Select story", 2)
        rswitch = RotaryEncoder(PIN_A,PIN_B,False,rotary_unit_callback_p)   
        switch_mode = 1
        Playlist.reinit()
        show_playlist()
    else:  
        indicate("Select track", 2)
        rswitch = RotaryEncoder(PIN_A,PIN_B,False,rotary_unit_callback)   
        switch_mode = 0
        Playlist.reinit()
        show_track()

# Yellow button
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(23, GPIO.RISING, callback=button_yellow, bouncetime=500)
# red button
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(24, GPIO.RISING, callback=button_red, bouncetime=100)
# green button
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(25, GPIO.RISING, callback=button_green, bouncetime=500)

# Setup additional grounds for rotary encoder
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.LOW)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.LOW)
# additional out for player 2, which does not have nive 3v outs
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, GPIO.HIGH)

# Define GPIO inputs for rotary encoder
PIN_A = 27	
PIN_B = 17	
rswitch = RotaryEncoder(PIN_A,PIN_B,False,rotary_unit_callback)

# Define GPIO inputs for volume
PIN_VA = 6
PIN_VB = 12
volEncode = RotaryEncoder(PIN_VA,PIN_VB,False,volume_callback)

indicate("Player 1")
indicate("4 Beth & Sophie", 2)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Keyboard stop, exit...")
    GPIO.cleanup()
except:
    GPIO.cleanup()
