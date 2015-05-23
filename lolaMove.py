#!/usr/bin/python

# This code can be reused in any project and in any way you want. 
# It would be nice if you let me know or you cite this project.
# 
# Fernando Tricas García
# https://github.com/fernand0/lola

from serial import Serial
import time
import sys

ser = Serial('/dev/ttyACM1', 115200)
srvGPIO=[[0,1,2], 
         [3,4,5], 
         [6,7,8],
         [9,10,11],
         [12,13,14],
         [15,16,17]]

srvPOS=[[[2, 0, 90], [2, 2, 135], [2, 1, 90]],  # d-1
        [[4, 0, 90], [4, 2, 135], [4, 1, 90]],  # d-2
        [[3, 0, 90], [3, 2, 45],  [3, 1, 90]],  # d-3
        [[1, 0, 90], [1, 2, 45],  [1, 1, 90]],  # i-1
        [[5, 0, 90], [5, 2, 45],  [5, 1, 90]],  # i-2
        [[0, 0, 90], [0, 2, 135], [0, 1, 90]]]  # i-3
 
srvINC=[[-1,-1,+1], 
        [-1,+1,-1], 
        [+1,-1,+1],
        [+1,+1,-1],
        [+1,-1,+1],
        [-1,+1,-1]]
VEL=100
WAI=0.1

def loadInitialState():
    # Unused now
    j=1
    component=[]

    print "Leg Articulation Position" 
    move = raw_input()
    i=1
    cadPos=""
    leg = []
    for token in move.split():
        if (i==1):
            legS=token
            leg.append(int(legS))
        if (i==2):
            art=token
            leg.append(int(art))
        if (i==3):
            pos=token
            leg.append(int(pos))
            cadPos=cadPos + "#%d P%s "%(srvGPIO[int(legS)][int(art)], angleMap(int(pos)))
            i=0 
        i = i + 1
    component.append(leg)
    j = j + 1    
    if (j==4):
        j=1 
        srvPOS.append(component)
        component=[]

        
    cadPos=cadPos+ "T%d\r"%(VEL)
    print cadPos
    ser.write(cadPos)
    time.sleep(WAI)



def angleMap(angle):
    pos = int((round((1950.0/180.0),0)*angle)/10)*10+550
    pos = int((round((2000.0/180.0),0)*angle)/10)*10+500
    return pos

def movePos(art, pos):
    cadPos="#%d P%d T%d\r"%(art,angleMap(pos),VEL)
    ser.write(cadPos)
    time.sleep(WAI)

def legGPIO(i, serv):
	return srvGPIO[srvPOS[i][serv][0]][srvPOS[i][serv][1]

while True:
    WAI=0.2
    print srvPOS

    mov1=""

    for i in [0,2,4]:
        legS=srvGPIO[srvPOS[i+1][1][0]][srvPOS[i+1][1][1]]
        pos=angleMap(srvPOS[i+1][1][2])
        mov1=mov1+"#%d P%s "%(legS,pos)
        legS=srvGPIO[srvPOS[i+1][2][0]][srvPOS[i+1][2][1]]
        pos=angleMap(srvPOS[i+1][2][2])
        mov1=mov1+"#%d P%s "%(legS,pos)

    mov1=mov1+ "T%d\r"%(VEL)
    print "Bajar lado 2", mov1
    ser.write(mov1)
    time.sleep(WAI)

    mov1=""
    for i in [0,2,4]:
        legS=srvGPIO[srvPOS[i][1][0]][srvPOS[i][1][1]]
        pos=angleMap(srvPOS[i][1][2] +
            srvINC[srvPOS[i][1][0]][srvPOS[i][1][1]]*90)
        mov1=mov1+"#%d P%s "%(legS,pos)

        legS=srvGPIO[srvPOS[i][2][0]][srvPOS[i][2][1]]
        pos=angleMap(srvPOS[i][2][2] +
            srvINC[srvPOS[i][2][0]][srvPOS[i][2][1]]*65)
        mov1=mov1+"#%d P%s "%(legS,pos)
    mov1=mov1+ "T%d\r"%(VEL)
    print "Levantar lado 1", mov1
    ser.write(mov1)
    time.sleep(WAI)


    mov1 = ""
    for i in [0,2,4]:
        if (i == 0):
            legS=srvGPIO[srvPOS[i][0][0]][srvPOS[i][0][1]]
            pos=angleMap(srvPOS[i][0][2] +
                srvINC[srvPOS[i][0][0]][srvPOS[i][0][1]]*20)
            mov1=mov1+"#%d P%s "%(legS,pos)
        if (i == 2):
            legS=srvGPIO[srvPOS[i][0][0]][srvPOS[i][0][1]]
            pos=angleMap(srvPOS[i][0][2] +
                srvINC[srvPOS[i][0][0]][srvPOS[i][0][1]]*10)
            mov1=mov1+"#%d P%s "%(legS,pos)
        if (i == 4):
            legS=srvGPIO[srvPOS[i][0][0]][srvPOS[i][0][1]]
            pos=angleMap(srvPOS[i][0][2] +
                srvINC[srvPOS[i][0][0]][srvPOS[i][0][1]]*15)
            mov1=mov1+"#%d P%s "%(legS,pos)

    for i in [1,3,5]:
        if (i==5):
            legS=srvGPIO[srvPOS[i][0][0]][srvPOS[i][0][1]]
            pos=angleMap(srvPOS[i][0][2] +
                srvINC[srvPOS[i][0][0]][srvPOS[i][0][1]]*-20)
            mov1=mov1+"#%d P%s "%(legS,pos)
        if (i==3):
            legS=srvGPIO[srvPOS[i][0][0]][srvPOS[i][0][1]]
            pos=angleMap(srvPOS[i][0][2] +
                srvINC[srvPOS[i][0][0]][srvPOS[i][0][1]]*-10)
            mov1=mov1+"#%d P%s "%(legS,pos)
        if (i==1):
            legS=srvGPIO[srvPOS[i][0][0]][srvPOS[i][0][1]]
            pos=angleMap(srvPOS[i][0][2] +
            srvINC[srvPOS[i][0][0]][srvPOS[i][0][1]]*-15)
            mov1=mov1+"#%d P%s "%(legS,pos)

    mov1=mov1+ "T%d\r"%(VEL)

    print "2", mov1
    ser.write(mov1)
    time.sleep(WAI)


    mov1 = ""
    for i in [0,2,4]:
        legS=srvGPIO[srvPOS[i][1][0]][srvPOS[i][1][1]]
        pos=angleMap(srvPOS[i][1][2])
        mov1=mov1+"#%d P%s "%(legS,pos)

        legS=srvGPIO[srvPOS[i][2][0]][srvPOS[i][2][1]]
        pos=angleMap(srvPOS[i][2][2])
        mov1=mov1+"#%d P%s "%(legS,pos)

    mov1=mov1+ "T%d\r"%(VEL)
    print "Bajar lado 1", mov1
    ser.write(mov1)
    time.sleep(WAI)

    mov1=""
    for i in [0,2,4]:
        legS=srvGPIO[srvPOS[i+1][1][0]][srvPOS[i+1][1][1]]
        pos=angleMap(srvPOS[i+1][1][2] +
            srvINC[srvPOS[i+1][1][0]][srvPOS[i+1][1][1]]*90)
        mov1=mov1+"#%d P%s "%(legS,pos)

        legS=srvGPIO[srvPOS[i+1][2][0]][srvPOS[i+1][2][1]]
        pos=angleMap(srvPOS[i+1][2][2] +
                srvINC[srvPOS[i+1][2][0]][srvPOS[i+1][2][1]]*65)
        mov1=mov1+"#%d P%s "%(legS,pos)

    mov1=mov1+ "T%d\r"%(VEL)
    print "Levantar lado 2", mov1
    ser.write(mov1)
    time.sleep(WAI)

    mov1 = ""
    for i in [1,3,5]:
        if (i == 5):
            legS=srvGPIO[srvPOS[i][0][0]][srvPOS[i][0][1]]
            pos=angleMap(srvPOS[i][0][2] +
                srvINC[srvPOS[i][0][0]][srvPOS[i][0][1]]*10)
            mov1=mov1+"#%d P%s "%(legS,pos)
        if (i == 3):
            legS=srvGPIO[srvPOS[i][0][0]][srvPOS[i][0][1]]
            pos=angleMap(srvPOS[i][0][2] +
                srvINC[srvPOS[i][0][0]][srvPOS[i][0][1]]*20)
            mov1=mov1+"#%d P%s "%(legS,pos)
        if (i == 1):
            legS=srvGPIO[srvPOS[i][0][0]][srvPOS[i][0][1]]
            pos=angleMap(srvPOS[i][0][2] +
                srvINC[srvPOS[i][0][0]][srvPOS[i][0][1]]*15)
            mov1=mov1+"#%d P%s "%(legS,pos)

    for i in [0,2,4]:
        if (i==0):
            legS=srvGPIO[srvPOS[i][0][0]][srvPOS[i][0][1]]
            pos=angleMap(srvPOS[i][0][2] +
            srvINC[srvPOS[i][0][0]][srvPOS[i][0][1]]*-10)
        if (i==2):
            mov1=mov1+"#%d P%s "%(legS,pos)
            legS=srvGPIO[srvPOS[i][0][0]][srvPOS[i][0][1]]
            pos=angleMap(srvPOS[i][0][2] +
                srvINC[srvPOS[i][0][0]][srvPOS[i][0][1]]*-20)
        if (i==4):
            mov1=mov1+"#%d P%s "%(legS,pos)
            legS=srvGPIO[srvPOS[i][0][0]][srvPOS[i][0][1]]
            pos=angleMap(srvPOS[i][0][2] +
                srvINC[srvPOS[i][0][0]][srvPOS[i][0][1]]*-15)
            mov1=mov1+"#%d P%s "%(legS,pos)

    mov1=mov1+ "T%d\r"%(VEL)

    print "2", mov1
    ser.write(mov1)
    time.sleep(WAI)

