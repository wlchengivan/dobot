from serial.tools import list_ports
import pointList
import pydobot
import myDobotAPI
import detectColorWithImage
import takePhoto
import cv2
import pandas as pd
import math

"""available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[0].device

device = pydobot.Dobot(port=port, verbose=True)
device.move_to(250, 0 ,70, 0, wait=True)
myDobotAPI.myMovJ(device, pointList.homePoint)



while True:
    myDobotAPI.myMovJ(device, pointList.homePoint)


    color = detectColorWithImage.getColorPos()[0]
    
    

    


device.close()"""


def getAngle():
    img = cv2.imread('Webcam.jpg')
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, binImg = cv2.threshold(grayImg, 100, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(binImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_to_plot = -1
    plotting_color = (0, 255, 0)
    thickness = -1

    #with_contours = cv2.drawContours(img,  contours, contours_to_plot, plotting_color, thickness)


    df = pd.DataFrame(contours[1][0], columns = ["x", "y"])


    for i in range(1, len(contours[1])):
        df2 = pd.DataFrame(contours[1][i], columns = ["x", "y"])
        df = pd.concat([df, df2], ignore_index = True)

    df = df.sort_values(by=['x'])
    df = df.reset_index(drop = True)

    topPoint = df.iloc[0]

    df = df.sort_values(by=['y'])
    df = df.reset_index(drop = True)

    rightPoint = df.iloc[-1]

    print(topPoint)
    print(rightPoint)

    k = float(rightPoint.loc['y']-topPoint.loc['y'])/float(rightPoint.loc['x']-topPoint.loc['x'])

    h = math.atan(k)

    a = math.degrees(h)

    print(a)

    return a


def alignmentObject(device):
    myDobotAPI.myMovJ(device, pointList.homePoint)
    takePhoto.takePhoto()
    
    myDobotAPI.moveToCamObject(device)
    
    pos = device.pose()[0:4]
    posListTemp = {
        "x" : pos[0],
        "y" : pos[1],
        "z" : pos[2] + 100,
        "r" : pos[3]
    }
    
    myDobotAPI.myMovJ(device,posListTemp)
    posListTemp = {
        "x" : pos[0],
        "y" : pos[1],
        "z" : pos[2] + 100,
        "r" : pos[3] + getAngle()
    }
    
    myDobotAPI.myMovJ(device, posListTemp)
    
    posListTemp = {
        "x" : pos[0],
        "y" : pos[1],
        "z" : pos[2],
        "r" : pos[3] + getAngle()
    }
    
    myDobotAPI.myMovJ(device, posListTemp)
    device.suck(False)

    
    myDobotAPI.myMovJ(device, pointList.homePoint)

    
    
    
