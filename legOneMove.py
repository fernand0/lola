#!/usr/bin/python

# This code can be reused in any project and in any way you want. 
# It would be nice if you let me know or you cite this project.
# 
# Fernando Tricas García
# https://github.com/fernand0/lola
#
# This code can be used to test individual movements. It is useful when you
# need to test some configuration, positions of the legs and so on.



#from RPIO import PWM
from serial import Serial
import time
import sys

ser = Serial('/dev/ttyACM1', 115200)
servoGPIO=[[0,1,2], 
           [3,4,5], 
           [6,7,8],
           [9,10,11],
           [12,13,14],
           [15,16,17]]
servoINC=[['-','-','+'], 
           ['-','+','-'], 
           ['+','-','+'],
           ['+','+','-'],
           ['+','-','+'],
           ['-','+','-']]
VEL=200
WAI=0.1


def angleMap(angle):
    pos = int((round((1950.0/180.0),0)*angle)/10)*10+550
    pos = int((round((2000.0/180.0),0)*angle)/10)*10+500
    return pos

def movePos(art, pos):
    cadPos="#%d P%d T%d\r"%(art,angleMap(pos),VEL)
    ser.write(cadPos)
    time.sleep(WAI)


if (len(sys.argv)>1):
	#movePos(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
	i=1
	cadPos=""
	sys.argv[1:]
	for token in sys.argv[1:]:
		if (i==1):
			leg=token
		if (i==2):
			art=token
		if (i==3):
			pos=token
			cadPos=cadPos + "#%d P%s "%(servoGPIO[int(leg)][int(art)], angleMap(int(pos)))
		i = i + 1
	cadPos=cadPos+ "T%d\r"%(VEL)
	print cadPos
	ser.write(cadPos)
	time.sleep(WAI)
else:
	while True:
		print "pata articulacion posicion" 
		move = raw_input()
		i=1
		cadPos=""
		for token in move.split():
			if (i==1):
				leg=token
			if (i==2):
				art=token
			if (i==3):
				pos=token
				cadPos=cadPos + "#%d P%s "%(servoGPIO[int(leg)][int(art)], angleMap(int(pos)))
				i=0 
			i = i + 1
		cadPos=cadPos+ "T%d\r"%(VEL)
		print cadPos
		ser.write(cadPos)
		time.sleep(WAI)
	


