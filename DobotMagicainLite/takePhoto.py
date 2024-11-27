from serial.tools import list_ports
import cv2
import pydobot
from matplotlib import pyplot as plt
import base64

X = 720
Y = 640


def takePhoto():
  cap = cv2.VideoCapture(0)
  while(cap.isOpened()):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (720, 640))
    frame = cv2.rectangle(frame, (360, 310),  
                                       (360, 330),  
                                       (0, 0, 255), 2) 
    
    frame = cv2.rectangle(frame, (350, 320),  
                                       (370, 320),  
                                       (0, 0, 255), 2) 
    
    cv2.imshow("Webcam", frame)
    
    
    
    #cv2.imwrite("Webcam.jpg", frame)
    if(cv2.waitKey(1) == ord("s")):
       cv2.imwrite("Webcam.jpg", frame)
       cap.release()
       break
    
  return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

