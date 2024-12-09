import cv2
import takePhoto
import dobot_api
import myE6API
import pointList
import time
import os
import threading
from multiprocessing import Pool



# Capturing video through webcam 
#takePhoto.takePhoto()  
    
# Reading the video from the 
# webcam in image frames 
"""imageFrame = cv2.imread('Webcam.jpg')
imageFrame = cv2.resize(imageFrame, (720, 640))


gray = cv2.cvtColor(imageFrame, cv2.COLOR_RGB2GRAY)
img = cv2.medianBlur(gray, 7)                 # 模糊化，去除雜訊
output = cv2.Canny(img, 50, 50)        # 偵測邊緣

cv2.imshow("GRAY", output)
cv2.waitKey(0)                               
cv2.destroyAllWindows()"""

#import teachableMachine


def bigLego():
    E6 = myE6API.E6("192.168.5.1")
    E6.start()
    E6.dashboard.Stop()
    E6.dashboard.ClearError()
    E6.dashboard.SpeedFactor(100)
    E6.dashboard.SetBackDistance(50)

    


    
    while True:
        total = 3
        E6.home()

        
        for i in range(0, total):
                
            #E6.home()


            
            tempPoint = E6.jointToPose(pointList.startJ)
            tempPoint = [float(x) for x in tempPoint]

            tempPoint[2] = tempPoint[2] - (pointList.bigLegoSize * i) + i

            print(tempPoint)
            
            
            E6.myMovJJoint(pointList.startJ2)
            E6.myMovLJoint(E6.poseToJoint(tempPoint))
            
            E6.myToolDO(1)
            E6.myMovLJoint(pointList.startJ2)
            
            #E6.home()
            
            tempPoint2 = E6.jointToPose(pointList.targetJ)
            tempPoint2 = [float(x) for x in tempPoint2]

            tempPoint2[2] = tempPoint2[2] + (pointList.bigLegoSize * i)

            E6.myMovJJoint(pointList.targetJ2)
            #E6.move()
            #E6.myMovJPose(E6.jointToPose(pointList.targetJ2))
            
            E6.myMovLPose(tempPoint2)
            
            E6.myToolDO(0)
            E6.myMovLJoint(pointList.targetJ2)



        E6.home()
            
        
        
        for i in range(0, total):
                
            #E6.home()

            tempPoint = E6.jointToPose(pointList.targetJ)
            tempPoint = [float(x) for x in tempPoint]

            tempPoint[2] = tempPoint[2]  + (pointList.bigLegoSize * (total - i - 1))
            


            print(tempPoint)
            E6.myMovJJoint(pointList.targetJ2)
            E6.myMovLJoint(E6.poseToJoint(tempPoint))
        
            E6.myToolDO(1)
            E6.myMovLJoint(pointList.targetJ2)
            
            #E6.home()
            
            
            
            tempPoint2 = E6.jointToPose(pointList.startJ)
            tempPoint2 = [float(x) for x in tempPoint2]

            tempPoint2[2] = tempPoint2[2] - (pointList.bigLegoSize * (total - i - 1))

            E6.myMovJJoint(pointList.startJ2)
            E6.myMovLPose(tempPoint2)
        
            E6.myToolDO(0)
            E6.myMovLJoint(pointList.startJ2)
            
                    
        E6.home()

        E6.dance()
        
if __name__ == '__main__':
    bigLego()