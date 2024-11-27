# Python code for Multiple Color Detection 
  
  
import numpy as np 
import cv2 
  
  
# Capturing video through webcam 
cap = cv2.VideoCapture(0) 
  
# Start a while loop 
while(1): 
      
    # Reading the video from the 
    # webcam in image frames 
    _, imageFrame = cap.read() 
  
    # Convert the imageFrame in  
    # BGR(RGB color space) to  
    # HSV(hue-saturation-value) 
    # color space 
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 
  
      
    # Morphological Transform, Dilation 
    # for each color and bitwise_and operator 
    # between imageFrame and mask determines 
    # to detect only that particular color 
    kernel = np.ones((5, 5), "uint8") 


    # Importing Models and set mean values
    face1 = "openCV/opencv_face_detector.pbtxt"
    face2 = "openCV/opencv_face_detector_uint8.pb"
    age1 = "openCV/age_deploy.prototxt"
    age2 = "openCV/age_net.caffemodel"
    gen1 = "openCV/gender_deploy.prototxt"
    gen2 = "openCV/gender_net.caffemodel"

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

    # Using models
    # Face
    face = cv2.dnn.readNet(face2, face1)

    # age
    age = cv2.dnn.readNet(age2, age1)

    # gender
    gen = cv2.dnn.readNet(gen2, gen1)

    la = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
        '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    lg = ['Male', 'Female']


    # Face detection
    fr_h = imageFrame.shape[0]
    fr_w = imageFrame.shape[1]
    blob = cv2.dnn.blobFromImage(imageFrame, 1.0, (300, 300),
                                [104, 117, 123], True, False)

    face.setInput(blob)
    detections = face.forward()

    # Face bounding box creation
    faceBoxes = []
    for i in range(detections.shape[2]):
    
    #Bounding box creation if confidence > 0.7
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            
            x1 = int(detections[0, 0, i, 3]*fr_w)
            y1 = int(detections[0, 0, i, 4]*fr_h)
            x2 = int(detections[0, 0, i, 5]*fr_w)
            y2 = int(detections[0, 0, i, 6]*fr_h)
            
            faceBoxes.append([x1, y1, x2, y2])
            
            cv2.rectangle(imageFrame, (x1, y1), (x2, y2),
                        (0, 255, 0), int(round(fr_h/150)), 8)
            
    faceBoxes
      
    for faceBox in faceBoxes:
            #Extracting face as per the faceBox
            face = imageFrame[max(0, faceBox[1]-15):
                        min(faceBox[3]+15, imageFrame.shape[0]-1),
                        max(0, faceBox[0]-15):min(faceBox[2]+15,
                                          imageFrame.shape[1]-1)]
            
            #Extracting the main blob part
            blob = cv2.dnn.blobFromImage(
                  face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

            #Prediction of gender
            gen.setInput(blob)
            genderPreds = gen.forward()
            gender = lg[genderPreds[0].argmax()]



            #Putting text of age and gender 
            #At the top of box
            cv2.putText(imageFrame,
                        f'{gender}',
                        (faceBox[0]-150, faceBox[1]+10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.3,
                        (217, 0, 0),
                        4,
                        cv2.LINE_AA)

        
              
    # Program Termination 
    cv2.imshow("Multiple Face Detection in Real-TIme", imageFrame) 
    if cv2.waitKey(10) & 0xFF == ord('q'): 
        cap.release() 
        cv2.destroyAllWindows() 
        break