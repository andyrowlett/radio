import sys
import time
import os, subprocess
import math
import tm1637
from rotary_class import RotaryEncoder

# Define GPIO inputs
PIN_A = 18 	# Pin 8 
PIN_B = 17	# Pin 10
BUTTON = 4	# Pin 7

# Define display
#tm = tm1637.TM1637(clk=5, dio=6)
#tm1 = 00
#tm2 = 00


def tmdisp(p, v):
    return False
    global tm1,tm2
    if p == 1:
        tm1 = v
    elif p == 2:
        tm2 = v
    tm.numbers(tm1, tm2)
    

tmdisp(1, 00)


# clear and reload stations
os.system("mpc clear")
os.system("mpc load playlist")
os.system("mpc repeat off")
os.system("mpc crossfade 3")

tps = 3 # turns per stat
min = 0

def get_max():
    pls = os.popen("mpc playlist").read()
    pls_list = pls.splitlines()
    max = (len(pls_list) * tps) + (len(pls_list) - 1) + 2
    print("Stations: %i Max: %i" % (len(pls_list),max))
    return max


max = get_max()
v = 0


# This is the event callback routine to handle events
def switch_event(event):
    global v, s
    if event == RotaryEncoder.CLOCKWISE:
        if v < max:
            v += 1
        time.sleep(0.1)
    elif event == RotaryEncoder.ANTICLOCKWISE:
        if v > min:
            v -= 1
        time.sleep(0.1)
    elif event == RotaryEncoder.BUTTONDOWN:
        print("Button down")
    elif event == RotaryEncoder.BUTTONUP:
        print("Button up")
    print(v)
    tmdisp(1, v)
    if v < 1:
        setPlay(0)
    elif v > 1:
        r = 1 + math.floor(v / tps)
        setPlay(r)


    return

play = 0

def setPlay(p):
    print("setplay %i" % p)
    global play, s
    if p != play:
        #tm.numbers(00,p)
        tmdisp(2, p)
        play = p
        print('play %i' % p)
        if p != 0 and p < 99:
            s = 0
            os.system("mpc stop")
            os.system("mpc play %i" % p)
        else:
            os.system("mpc stop")

# Define the switch
rswitch = RotaryEncoder(PIN_A,PIN_B,BUTTON,switch_event)

print("Pin A "+ str(PIN_A))
print("Pin B "+ str(PIN_B))
print("BUTTON "+ str(BUTTON))

# Listen
while True:
    try:
        time.sleep(0.5)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        os.system("mpc stop")
        exit()
	