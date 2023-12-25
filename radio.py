import sys
import time
import os, subprocess
import math
import tm1637
import re


from rotary_class import RotaryEncoder

## globals
playing = 0
station = 0 # station this was really a sort of pseudo frequency...
button_state = 0 # button state
volume = 75 # volume
v_step = 5 # vol step

# Vars
# bounce
bb = 0.2
# time sleep
ts = 0.2

# Define GPIO inputs for rotary encoder
PIN_A = 23 	
PIN_B = 17	
BUTTON = 20

def get_max():
	global playlist
	pls = os.popen("mpc playlist").read()
	playlist = pls.splitlines()
	max = len(playlist)
	return max

# Define display
tm = tm1637.TM1637(clk=5, dio=6)
tm1 = 00
tm2 = 00
min = 0
max = get_max()

playlist = ""

## functions


def get_station_normal_level():
	try:
		global playlist, playing
		station_name = playlist[playing - 1]
		print(">> playing %s" % station_name)
		levels = re.search(r"(\()([\d*\.?\d+$]+)(\))", station_name)
		if levels != type(None):
			level = levels.group(2)
			return float(level)
		else:
			return 1
	except:
		return 1

# display
def display(p, v, b=5):
	tm.brightness(b)
	n = '{0:0{width}}'.format(v, width=2)
	global tm1,tm2
	if p == 1:
		tm1 = v
	elif p == 2:
		tm2 = v
	tm.show("%s %s" % (p,str(n)))

def disp(text, bright=5):
	tm.brightness(bright)
	tm.show(text)

def set_volume(cmd, val, ignore=0):
	global volume
	if cmd == 'set':
		volume = val
	elif cmd == '+':
		if volume + val < 100:
			volume = volume + val
		else:
			volume = 100
	elif cmd == '-':
		if volume - val > 0:
			volume = volume - val
		else:
			volume = 0
	# get the normalisation level
	x = get_station_normal_level()
	total_volume = volume * x
	print(">> Station %i level: %f Volume: %i Total: %f" % (playing, x, volume, total_volume))
	#os.system("mpc volume %i" % total_volume)
	os.system("bash /home/station/radio/shell_vc.sh %i & >/dev/null 2>/dev/null" % total_volume)
	if not ignore:
		display('v',volume)

is_active = True

# This is the event callback routine to handle events
def rotary_unit_callback(event):
	global station, button_state, volume, is_active
	if not is_active:
		return False
	is_active = False
	if event == RotaryEncoder.CLOCKWISE:
		if button_state == 0:
			if station < max:
				station += 1
		elif button_state == 1:
			set_volume('+',v_step )

	elif event == RotaryEncoder.ANTICLOCKWISE:
		if button_state == 0:
			if station > min:
				station -= 1
		elif button_state == 1:
			set_volume('-',v_step )


	elif event == RotaryEncoder.BUTTONDOWN:
		if button_state == 0:
			button_state = 1
			display('v',volume)
		else:
			button_state = 0
			display('s',playing)
		print("b:%i" % button_state)
		is_active = True
		return
	elif event == RotaryEncoder.BUTTONUP:
		is_active = True
		return

	## this handles changing the station...
	if station < 1:
		play_station(0)
	elif station >= 1:
		play_station(station)
	
	time.sleep(bb)
	is_active = True
	return

def play_station(play):
	#print("play_station %i" % p)
	global playing, station, volume
	if play != playing:
		#tm.numbers(00,p)
		display('s', play)
		playing = play
		if play != 0 and play < 99:
			
			os.system("bash /home/station/radio/shell_pc.sh %i & >/dev/null 2>/dev/null" % play)
			set_volume('set', volume, 1)

		else:
			disp('Off ', 0)
			os.system("mpc stop")

# clear and reload stations
os.system("mpc stop")
os.system("mpc clear")
os.system("mpc load playlist")
os.system("mpc repeat off")
os.system("mpc crossfade 3")

set_volume('set',75)
display('OF', 0, 2)

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
	
