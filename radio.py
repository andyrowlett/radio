import sys
import time
import os, subprocess
import math
import tm1637

from rotary_class import RotaryEncoder

## globals
playing = 0
station = 0 # station this was really a sort of pseudo frequency...
button_state = 0 # button state
volume = 75 # volume
v_step = 5 # vol step

playlist = ""

## functions
def get_max():
	global playlist
	pls = os.popen("mpc playlist").read()
	playlist = pls.splitlines()
	max = len(playlist)
	return max

# display
def display(p, v):
	n = '{0:0{width}}'.format(v, width=2)
	global tm1,tm2
	if p == 1:
		tm1 = v
	elif p == 2:
		tm2 = v
	tm.show("%s %s" % (p,str(n)))

def set_volume(cmd, val):
	global v
	if cmd == 'set':
		v = val
	elif cmd == '+':
		if v + val < 100:
			v = v + val
		else:
			v = 100
	elif cmd == '-':
		if v - val > 0:
			v = v - val
		else:
			v = 0
	os.system("mpc volume %i" % v)
	display('v',v)

# This is the event callback routine to handle events
def rotary_unit_callback(event):
	global station, button_state
	if event == RotaryEncoder.CLOCKWISE:
		if button_state == 0:
			if station < max:
				station += 1
		elif button_state == 1:
			set_volume('+',v_step )
		time.sleep(bb)

	elif event == RotaryEncoder.ANTICLOCKWISE:
		if button_state == 0:
			if station > min:
				station -= 1
		elif button_state == 1:
			set_volume('-',v_step )
		time.sleep(bb)
	elif event == RotaryEncoder.BUTTONDOWN:
		if button_state == 0:
			button_state = 1
			display('v',v)
		else:
			button_state = 0
			display('s',playing)
		print("b:%i" % button_state)
		return
	elif event == RotaryEncoder.BUTTONUP:
		return

	## this handles changing the station...
	if station < 1:
		play_station(0)
	elif v >= 1:
		play_station(station)
	return

def play_station(play):
	#print("play_station %i" % p)
	global playing, station
	if play != playing:
		#tm.numbers(00,p)
		display('s', play)
		playing = play
		if play != 0 and play < 99:
			os.system("bash /home/station/radio/shell_pc.sh %i & >/dev/null 2>/dev/null" % play)
		else:
			os.system("mpc stop")

# Vars
# bounce
bb = 0.1
# time sleep
ts = 0.2

# Define GPIO inputs
PIN_A = 18 	# Pin 8 
PIN_B = 17	# Pin 10
BUTTON = 21	# Pin 7

# Define display
tm = tm1637.TM1637(clk=5, dio=6)
tm1 = 00
tm2 = 00

min = 0
max = get_max()

# clear and reload stations
os.system("mpc stop")
os.system("mpc clear")
os.system("mpc load playlist")
os.system("mpc repeat off")
os.system("mpc crossfade 3")

set_volume('set',v)
display('h', 00)

# Define the switch
rswitch = RotaryEncoder(PIN_A,PIN_B,BUTTON,rotary_unit_callback)

# Listen
while True:
	try:
		time.sleep(ts)
	except KeyboardInterrupt:
		print("Keyboard interrupt")
		os.system("mpc stop")
		exit()
	
