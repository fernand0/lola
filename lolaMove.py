#!/usr/bin/python
# -*- coding: utf-8 -*-

# This code can be reused in any project and in any way you want. 
# It would be nice if you let me know or you cite this project.
# 
# Fernando Tricas García
# https://github.com/fernand0/lola
#

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

srvGPIO=[[0,1,2],
         [3,4,5],
         [6,7,8],
         [9,10,11],
         [12,13,14],
         [15,16,17]]

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

srvPOS=[[[2, 0, 90], [2, 2, 135], [2, 1, 90]],  # r-1
        [[4, 0, 90], [4, 2, 135], [4, 1, 90]],  # r-2
        [[3, 0, 90], [3, 2, 45],  [3, 1, 90]],  # r-3
        [[1, 0, 90], [1, 2, 45],  [1, 1, 90]],  # l-1
        [[5, 0, 90], [5, 2, 45],  [5, 1, 90]],  # l-2
        [[0, 0, 90], [0, 2, 135], [0, 1, 90]]]  # l-3
 
# Depending on the way the servo was mounted increments (or decrements) are not
# alwasy consistent across articulations. This matrix helps us to be able to
# manage the servos in a consitent way.

srvINC=[[-1,-1,+1], 
        [-1,+1,-1], 
        [+1,-1,+1],
        [+1,+1,-1],
        [+1,-1,+1],
        [-1,+1,-1]]

# Timing for movements and waits between movements

SPEED=100
WAIT=0.1
debug=0


def angleMap(angle):
    pos = int((round((1950.0/180.0),0)*angle)/10)*10+550
    pos = int((round((2000.0/180.0),0)*angle)/10)*10+500
    return pos

def movePos(art, pos):
    cadPos="#%d P%d T%d\r"%(art,angleMap(pos),SPEED)
    ser.write(cadPos)
    time.sleep(WAIT)

def legGPIO(i, serv):
    return srvGPIO[srvPOS[i][serv][0]][srvPOS[i][serv][1]]

def legPOS(i,serv, inc):
    return (srvPOS[i][serv][2] +
        srvINC[srvPOS[i][serv][0]][srvPOS[i][serv][1]]*inc)

while True:
    # This is a simple sequence of steps Three legs are up and moving forward,
    # the other three are down and moving backward

    WAIT=0.2
    if (debug !=0):
        print srvPOS

    mov1=""

    for i in [0,2,4]:
        legS=legGPIO(i+1,1)
        pos=angleMap(legPOS(i+1,1,0))
        mov1=mov1+"#%d P%s "%(legS,pos)
        legS=legGPIO(i+1,2)
        pos=angleMap(legPOS(i+1,2,0))
        mov1=mov1+"#%d P%s "%(legS,pos)

    mov1=mov1+ "T%d\r"%(SPEED)
    print "Bajar lado 2"
    if (debug > 1):
        print mov1
    ser.write(mov1)
    time.sleep(WAIT)

    mov1=""
    for i in [0,2,4]:
        legS=legGPIO(i,1)
        pos=angleMap(legPOS(i,1,90))
        mov1=mov1+"#%d P%s "%(legS,pos)

        legS=legGPIO(i,2)
        pos=angleMap(legPOS(i,2,65))
        mov1=mov1+"#%d P%s "%(legS,pos)
    mov1=mov1+ "T%d\r"%(SPEED)
    print "Levantar lado 1"
    if (debug > 1):
        print mov1
    ser.write(mov1)
    time.sleep(WAIT)


    mov1 = ""
    for i in [0,2,4]:
        if (i == 0):
            legS=legGPIO(i,0)
            pos=angleMap(legPOS(i,0,20))
            mov1=mov1+"#%d P%s "%(legS,pos)
        if (i == 2):
            legS=legGPIO(i,0)
            pos=angleMap(legPOS(i,0,10))
            mov1=mov1+"#%d P%s "%(legS,pos)
        if (i == 4):
            legS=legGPIO(i,0)
            pos=angleMap(legPOS(i,0,15))
            mov1=mov1+"#%d P%s "%(legS,pos)

    for i in [1,3,5]:
        if (i==5):
            legS=legGPIO(i,0)
            pos=angleMap(legPOS(i,0,-20))
            mov1=mov1+"#%d P%s "%(legS,pos)
        if (i==3):
            legS=legGPIO(i,0)
            pos=angleMap(legPOS(i,0,-10))
            mov1=mov1+"#%d P%s "%(legS,pos)
        if (i==1):
            legS=legGPIO(i,0)
            pos=angleMap(legPOS(i,0,-15))
            mov1=mov1+"#%d P%s "%(legS,pos)

    mov1=mov1+ "T%d\r"%(SPEED)

    print "Avance lado 2"
    if (debug > 1):
        print mov1
    ser.write(mov1)
    time.sleep(WAIT)


    mov1 = ""
    for i in [0,2,4]:
        legS=legGPIO(i,1)
        pos=angleMap(legPOS(i,1,0))
        mov1=mov1+"#%d P%s "%(legS,pos)

        legS=legGPIO(i,2)
        pos=angleMap(legPOS(i,2,0))
        mov1=mov1+"#%d P%s "%(legS,pos)

    mov1=mov1+ "T%d\r"%(SPEED)
    print "Bajar lado 1"
    if (debug > 1):
        print mov1
    ser.write(mov1)
    time.sleep(WAIT)

    mov1=""
    for i in [0,2,4]:
        legS=legGPIO(i+1,1)
        pos=angleMap(legPOS(i+1,1,90))
        mov1=mov1+"#%d P%s "%(legS,pos)

        legS=legGPIO(i+1,2)
        pos=angleMap(legPOS(i+1,2,65))
        mov1=mov1+"#%d P%s "%(legS,pos)

    mov1=mov1+ "T%d\r"%(SPEED)
    print "Levantar lado 2"
    if (debug > 1):
        print mov1
    ser.write(mov1)
    time.sleep(WAIT)

    mov1 = ""
    for i in [1,3,5]:
        if (i == 5):
            legS=legGPIO(i,0)
            pos=angleMap(legPOS(i,0,10))
            mov1=mov1+"#%d P%s "%(legS,pos)
        if (i == 3):
            legS=legGPIO(i,0)
            pos=angleMap(legPOS(i,0,20))
            mov1=mov1+"#%d P%s "%(legS,pos)
        if (i == 1):
            legS=legGPIO(i,0)
            pos=angleMap(legPOS(i,0,15))
            mov1=mov1+"#%d P%s "%(legS,pos)

    for i in [0,2,4]:
        if (i==0):
            legS=legGPIO(i,0)
            pos=angleMap(legPOS(i,0,-10))
        if (i==2):
            mov1=mov1+"#%d P%s "%(legS,pos)
            legS=legGPIO(i,0)
            pos=angleMap(legPOS(i,0,-20))
        if (i==4):
            mov1=mov1+"#%d P%s "%(legS,pos)
            legS=legGPIO(i,0)
            pos=angleMap(legPOS(i,0,-15))
            mov1=mov1+"#%d P%s "%(legS,pos)

    mov1=mov1+ "T%d\r"%(SPEED)

    print "Avance lado 1"
    if (debug > 1):
        print mov1
    ser.write(mov1)
    time.sleep(WAIT)

