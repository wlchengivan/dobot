from serial.tools import list_ports
import cv2
import pydobot
from matplotlib import pyplot as plt
import base64



def takePhoto():
  cap = cv2.VideoCapture(1)
  while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow("Webcam", frame)
    #cv2.imwrite("Webcam.jpg", frame)
    if(cv2.waitKey(1) == ord("s")):
       cv2.imwrite("Webcam.jpg", frame)
       cap.release()
       break
    
  return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
