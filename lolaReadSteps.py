#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# This code can be reused in any project and in any way you want. 
# It would be nice if you let me know or you cite this project.
# 
# Fernando Tricas García
# https://github.com/fernand0/lola
#

from yaml import load, dump
from serial import Serial
import time
import sys

# http://www.dfrobot.com/wiki/index.php/Veyron_Servo_Driver_%2824-Channel%29_%28SKU:DRI0029%29
# We need to send the instructions to the servo controller using the serial
# port. In this case I'm using it via USB.

ser = Serial('/dev/ttyACM1', 115200)

# Here we are grouping the servos forming legs
# Each component is a leg:
# 	. First component is for movement on the plane
#	. Second and third components are used for moving the leg
#	  up and down

file =  open('srvGPIO.yml','r')
srvGPIO=load(file)

# Here we establish the initial position for each leg. In this position 
# the hexapod is standing in its 'central' position and it can start moving
# Notice that the order is a bit 'extrange' because of the way the code
# has been evolving from the beginning.
# In any case this way of configuring the thing should allow us to easily
# reconfigure things. 
# The first three components are the legs of the right part of the robot
# (looking from behind) and the other three components correspond to the 
# legs of the left part of the robot. 
# The numbers correspond to the position in each part, from 1 to 3 (front,
# middle, rear).
#
# r-1
# r-2
# r-3
# l-1
# l-2
# l-3
 
file =  open('srvPOS.yml','r')
srvPOS=load(file)

# Depending on the way the servo was mounted increments (or decrements) are not
# alwasy consistent across articulations. This matrix helps us to be able to
# manage the servos in a consitent way.

file =  open('srvINC.yml','r')
srvINC=load(file)

# Timing for movements and waits between movements

SPEED=100
WAIT=0.2
debug=0

def angleMap(angle):
    pos = int((round((1950.0/180.0),0)*angle)/10)*10+550
    pos = int((round((2000.0/180.0),0)*angle)/10)*10+500
    return pos

def movePos(art, pos):
    cadPos="#%d P%d T%d\r"%(art,angleMap(pos),SPEED)
    ser.write(cadPos)
    time.sleep(WAIT)

def legGPIO(i, j): 
    leg = int(i)
    serv = int(j)
    return srvGPIO[srvPOS[leg][serv][0]][srvPOS[leg][serv][1]]

def legPOS(i,j, incr):
    leg = int(i)
    serv = int(j)
    inc = int(incr)
    return (srvPOS[leg][serv][2] +
        srvINC[srvPOS[leg][serv][0]][srvPOS[leg][serv][1]]*inc)

def legINI():
    mov1=""
    for i in range(5):
	for j in range(3):
		legS=legGPIO(i,j)
		pos=angleMap(legPOS(i,j,0))
        	mov1=mov1+"#%d P%s "%(legS,pos)
    mov1=mov1+ "T%d\r"%(SPEED)
    ser.write(mov1)
    time.sleep(WAIT)

while True:
    try:
        move = raw_input()
        print move
	moves = move.split()

        mov1=""
        for i in range(len(moves)/3):
            leg=legGPIO(moves[i*3], moves[i*3+1])
            pos=angleMap(legPOS(moves[i*3], moves[i*3+1], moves[i*3+2]))
            mov1=mov1+"#%d P%s "%(leg,pos)
        mov1=mov1+ "T%d\r"%(SPEED)
    
        print mov1
        ser.write(mov1)
        time.sleep(WAIT)
    except:
        #legINI()
        sys.exit()

