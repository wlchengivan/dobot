# Python code for Multiple Color Detection 
  
  
import numpy as np 
import cv2 
from matplotlib import pyplot as plt 
import takePhoto
  
  
def getColorPos():
    # Capturing video through webcam 
    takePhoto.takePhoto()  
        
    # Reading the video from the 
    # webcam in image frames 
    imageFrame = cv2.imread('Webcam.jpg')
    imageFrame = cv2.resize(imageFrame, (720, 640))
    #imageFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2RGB)

    # Convert the imageFrame in  
    # BGR(RGB color space) to  
    # HSV(hue-saturation-value) 
    # color space 
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

    # Set range for red color and  
    # define mask 
    red_lower = np.array([0, 200, 150], np.uint8) 
    red_upper = np.array([15, 255, 200], np.uint8) 
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

    # Set range for green color and  
    # define mask 
    green_lower = np.array([71, 156, 52], np.uint8) 
    green_upper = np.array([86, 242, 135], np.uint8) 
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 

    # Set range for blue color and 
    # define mask 
    blue_lower = np.array([90, 200, 100], np.uint8) 
    blue_upper = np.array([130, 255, 150], np.uint8) 
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper) 
        
    # Morphological Transform, Dilation 
    # for each color and bitwise_and operator 
    # between imageFrame and mask determines 
    # to detect only that particular color 
    kernel = np.ones((5, 5), "uint8") 
        
    # For red color 
    red_mask = cv2.dilate(red_mask, kernel) 
    res_red = cv2.bitwise_and(imageFrame, imageFrame,  
                                mask = red_mask) 
        
    # For green color 
    green_mask = cv2.dilate(green_mask, kernel) 
    res_green = cv2.bitwise_and(imageFrame, imageFrame, 
                                mask = green_mask) 
        
    # For blue color 
    blue_mask = cv2.dilate(blue_mask, kernel) 
    res_blue = cv2.bitwise_and(imageFrame, imageFrame, 
                                mask = blue_mask) 



    # Creating contour to track red color 
    contours, hierarchy = cv2.findContours(red_mask, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE) 
    
    """if(hierarchy is not None):
        area = cv2.contourArea(contours[0])
        print(cv2.contourArea(contours[0]) )

        if(area > 300): 
            x, y, w, h = cv2.boundingRect(contours[0]) 
        return("red", x, y, w, h)
    else:
        contours, hierarchy = cv2.findContours(green_mask, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE) 
        if(hierarchy is not None):
            area = cv2.contourArea(contours[0]) 
            print(contours) 

            print(cv2.contourArea(contours[0]) )
            if(area > 300): 
                x, y, w, h = cv2.boundingRect(contours[0]) 
            return("green", x, y, w, h)
        else:
            contours, hierarchy = cv2.findContours(blue_mask, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE) 
            if(hierarchy is not None):
                area = cv2.contourArea(contours[0]) 
                print(contours[0]) 

                if(area > 300): 
                    x, y, w, h = cv2.boundingRect(contours[0]) 
                return("blue", x, y, w, h)
            else:
                return(0)"""
                
    contours, hierarchy = cv2.findContours(red_mask, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE) 
                
    for pic, contour in enumerate(contours): 
        if(hierarchy is not None):
            area = cv2.contourArea(contour)
            #print(cv2.contourArea(contour) )

            if(area > 300): 
                x, y, w, h = cv2.boundingRect(contours[0]) 
                return("red", x, y, w, h)
    
    contours, hierarchy = cv2.findContours(green_mask, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE) 
    
    for pic, contour in enumerate(contours): 
        if(hierarchy is not None):
            area = cv2.contourArea(contour)
            #print(cv2.contourArea(contour) )

            if(area > 300): 
                x, y, w, h = cv2.boundingRect(contours[0]) 
                return("green", x, y, w, h)
            
    contours, hierarchy = cv2.findContours(blue_mask, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE) 
            
    for pic, contour in enumerate(contours): 
        if(hierarchy is not None):
            area = cv2.contourArea(contour)
            #print(cv2.contourArea(contour) )

            if(area > 300): 
                x, y, w, h = cv2.boundingRect(contours[0]) 
                return("blue", x, y, w, h)
            
    return "0", 0, 0, 0, 0

    
