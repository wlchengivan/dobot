import cv2
import takePhoto
import dobot_api
import myE6API
import pointList
import time
import os

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


if __name__ == '__main__':
    E6 = myE6API.E6("192.168.5.1")
    E6.start()
    E6.dashboard.ClearError()
    E6.dashboard.SpeedFactor(100)



    while True:
        for i in range(0,2):
            E6.myMovJPose(pointList.Home)


            
            tempPoint = pointList.startPoint2
            
            tempPoint = [float(x) for x in tempPoint]

            
            tempPoint[2] = tempPoint[2] - (pointList.ankerSize * i)
            E6.myMovJPose(tempPoint)

            E6.wait()
            E6.dashboard.ToolDO(1, 1)

            E6.myMovJPose(pointList.Home)
            
            tempPoint2 = pointList.targetPoint2
            tempPoint2 = [float(x) for x in tempPoint2]


            tempPoint2[2] = tempPoint2[2] + (pointList.ankerSize * i)

            E6.myMovJPose(tempPoint2)

            
            E6.dashboard.ToolDO(1, 0)
            E6.wait()
            E6.myMovJPose(pointList.Home)
            
        
        for i in range(0,2):
            E6.myMovJPose(pointList.Home)



            
            tempPoint2[2] = tempPoint2[2] - (pointList.ankerSize * i)
            E6.myMovJPose(tempPoint2)

            E6.wait()
            E6.dashboard.ToolDO(1, 1)

            E6.myMovJPose(pointList.Home)

            tempPoint[2] = tempPoint[2] + (pointList.ankerSize * i)
            E6.myMovJPose(tempPoint)

            
            E6.dashboard.ToolDO(1, 0)
            E6.wait()
            E6.myMovJPose(pointList.Home)
            
            