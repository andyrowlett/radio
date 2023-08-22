import sys
import time
import os, subprocess
import math
import tm1637

from rotary_class import RotaryEncoder

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


tps = 3 # turns per stat
min = 0
def get_max():
	pls = os.popen("mpc playlist").read()
	pls_list = pls.splitlines()
	max = (len(pls_list) * tps) + (len(pls_list) - 1) + 2
	print("Stations: %i Max: %i" % (len(pls_list),max))
	return max

# display
def tmdisp(p, v):
	n = '{0:0{width}}'.format(v, width=2)
	global tm1,tm2
	if p == 1:
		tm1 = v
	elif p == 2:
		tm2 = v
	tm.show(" %s%s" % (p,str(n)))
#    tm.show("  " + str(tmp2))

tmdisp(1, 00)


# clear and reload stations
os.system("mpc stop")
os.system("mpc clear")
os.system("mpc load playlist")
os.system("mpc repeat off")
os.system("mpc crossfade 3")


max = get_max()
s = 0 # station
b = 0 # button state
v = 75 # volume
v_step = 5 # vol step


def volume(cmd, val):
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
	tmdisp('v',v)

volume('set',v)

def button_event():
	global b
	if b==0:
		b = 1
		tmdisp('v',v)
	else:
		b = 0
		tmdisp('s',play)
	print("b:%i" % b)

# This is the event callback routine to handle events
def switch_event(event):
	global s,b
	if event == RotaryEncoder.CLOCKWISE:
		if b == 0:
			if s < max:
				s += 1
		elif b == 1:
			volume('+',v_step )
		time.sleep(bb)

	elif event == RotaryEncoder.ANTICLOCKWISE:
		if b == 0:
			if s > min:
				s -= 1
		elif b == 1:
			volume('-',v_step )
		time.sleep(bb)
	elif event == RotaryEncoder.BUTTONDOWN:
		print("Button down")
		button_event()
	elif event == RotaryEncoder.BUTTONUP:
		print("Button up")
		
	print(s)
	#tmdisp(1, v)
	if s < 1:
		setPlay(0)
	elif v >= 1:
		#r = 1 + math.floor(v / tps)
		setPlay(s)


	return

play = 0

def setPlay(p):
	print("setplay %i" % p)
	global play
	if p != play:
		#tm.numbers(00,p)
		tmdisp('s', p)
		play = p
		print('play %i' % p)
		if p != 0 and p < 99:
			s = 0
			#os.system("mpc stop")
			#os.system("mpc play %i" % p)
			os.system("bash /home/station/radio/shell_pc.sh %i & >/dev/null 2>/dev/null" % p)
		else:
			os.system("mpc stop")

# Define the switch
rswitch = RotaryEncoder(PIN_A,PIN_B,BUTTON,switch_event)

# Listen
while True:
	try:
		time.sleep(ts)
	except KeyboardInterrupt:
		print("Keyboard interrupt")
		os.system("mpc stop")
		exit()
	
