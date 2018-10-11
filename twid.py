import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import os
import spidev
import sys
import subprocess as sp

GPIO.setmode(GPIO.BCM)

#pin Definition

SPICLK = 11
SPIMISO = 9 
SPIMOSI = 10
SPICS = 8

# pin numbers switch

start = 19
locked = 26
unlocked = 21
#SET ADC Pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

#Button pin setups
GPIO.setup(start,   GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(locked,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(unlocked,GPIO.IN, pull_up_down=GPIO.PUD_UP)

mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK,   cs=SPICS,   mosi=SPIMOSI,  miso=SPIMISO)

#Global Variables
dur = [0]*16;
code =[1,1,0];
dir = [0]*16;
values = [0]*8
count = 0;
duration = 0;
change  = 0.0;
pre_pot = 0.0;
place = 3
stop =0
#direction =[0]
# 0 is a left movement 
# 1 is a right movement
def potconvert(Vals,dec):
	volts = (Vals*3.3/float(1023))
	volts = round(volts,dec)
	return volts
def getpot():
	global values
	global change
	global pot
	global pre_pot
	pre_pot = pot; 
	values[0] = mcp.read_adc(0);
	pot = potconvert(values[0],2);
	change = pot-pre_pot;
	print (" this is change",change)
	return change
def direction (change):
	global place
	global count
	global dir
	if (change > 0.01):
		if (len(master)-1)==0:
			master.append(place)
			place =count+1
		print("right")
		#dir.popleft()
		master.append(1)
		count = 0
	elif (change <-0.01):
		if (len(master)-1)==1:
			master.append(place)
			place =place+1
		print("left")
		#dir.popleft()
		master.append(0)
		count = 0
	elif (change<0.05 or change >-0.05 ):
		print("no change")
		count = count+1
def directionR (change):
	duration = 0
	global dir
	global dur
	while (change > 0.01):
		time.sleep(1)
		print("right")
		duration  = duration + 10
		getpot()
	if (duration > 0):
		dir = dir[1:]
		dir.append(1)
		dur = dur[1:]
		dur.append(duration)

def directionL(change):
	duration = 0
	global dir
	global dur
	while (change <-0.01):
		time.sleep(1)
		print("left")
		duration = duration +10
		getpot()
	if (duration > 0):
		dir = dir[1:]
		dir.append(0)
		dur = dur[1:]
		dur.append(duration)
		
def s(channel):
	os.system('Apple Pay Success Sound Effect.wav')

GPIO.add_event_detect(start, GPIO.FALLING, callback=s, bouncetime=200)

try:
  pot = 0.0
  while (stop ==0):
     # values[0] = mcp.read_adc(0)
      #pre_pot = pot
      #pot = potconvert(values[0],2)
      #change = pot - pre_pot;
      #print(pot);
      #print(pre_pot);
      getpot()
      #directionL(change)
      #directionR(change)

      if (count == 2):
	stop = 1
	if (dir[(len(dir)-1)] == code[2] and  dir[(len(dir)-2)] == code[1] and dir[(len(dir)-3)] == code[0]):
		print('yay')
		dir = [0]*16;
	else :
		print ('Failed')
		dir = [0]*16;
      print(master)
      if(stop ==1)
	for i in range (2,place):
		start = master.index(i)
		finish = master.index(i+1)
		duration = (finish -start)*100
		dur=dur[1:]
		dur.append(duration)
		val = master[(finsh -1)]
		dir = dir[1:]
		dir.append(val)
      time.sleep(0.01);
	
finally:
    GPIO.cleanup()
