from serial.tools import list_ports
import pointList
import pydobot
import numpy as np
import pandas as pd
import os

PARALLAXX = 53
PARALLAXZ = -5

def myMovJ(device, posList):
    device.move_to(float(posList['x']), float(posList['y']), float(posList['z']), float(posList['r']), wait=True)

def myJump(device, posList):
    pos = device.pose()[0:4]
    posListTemp = {
        "x" : pos[0] ,
        "y" : pos[1],
        "z" : posList['z'],
        "r" : pos[3]
    }
    
    myMovJ(device, posListTemp)
    myMovJ(device, posList)
    


def moveToCamObject(device):
    pos = device.pose()[0:4]
    
    j4 = device.pose()[-1]
    
    posList = {
        "x" : pos[0] + PARALLAXX,
        "y" : pos[1],
        "z" : pos[2] + PARALLAXZ,
        "r" : -j4
    }
    myMovJ(device, posList)
    takeUpObject(device, posList)
    

def takeUpObject(device, posList):
    device.suck(True)
    posList['z'] = posList ['z'] - 2
    myMovJ(device, posList)
    
    
def pallet(device):
    print("Select P1")
    input()
    P1 = device.pose()
    
    P1List = {
        "x" : P1[0],
        "y" : P1[1],
        "z" : P1[2],
        "r" : P1[3]
    }
    
    print("Select P2")
    input()
    P2 = device.pose()
    
    P1List = {
        "x" : P2[0],
        "y" : P2[1],
        "z" : P2[2],
        "r" : P2[3]
    }
    
    row = int(input("Row:"))
    col = int(input("Col:"))
    
    y =(float((P2[0] - P1[0])) / float(row - 1))
    x = float((P2[1] - P1[1])) / float(col - 1)
    
    """for i in range(0, row):
        for j in range(0, col):
            dftemp = {
                'Point' : '(' + str(i) + ', ' + str(j) + ')',
                'x' : round((P1[0] + x * i), 2),
                'y' : round((P1[1] + y * j), 2),
                'z' : P1[2],
                'r' : P1[3]
            }
            #print(pd.json_normalize(dftemp))
            allPoint = pd.concat([allPoint, pd.json_normalize(dftemp)], ignore_index=True)
            
    for i in range(0, len(allPoint)):
        print(allPoint.iloc[i])"""
        
    allPoint = []
    
    for i in range(0, row):
        for j in range(0, col):
            allPoint.append(['(' + str(i) + ', ' + str(j) + ')', round((P1[0] + y * i), 2), round((P1[1] + x * j), 2),  P1[2], P1[3]])
    
    return(allPoint)
    
    
