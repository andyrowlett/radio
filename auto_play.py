from time import sleep
from datetime import datetime
from rotary_class import RotaryEncoder
import RPi.GPIO as GPIO
import time, os, cls_mpc, cls_blt

time.sleep(5)

Blue = cls_blt.Blue()
Blue.connect(Blue.square)

time.sleep(5)

os.system("mpc clear")
os.system("mpc load SleepyTime")
os.system("mpc volume 20")
os.system("mpc play 1")