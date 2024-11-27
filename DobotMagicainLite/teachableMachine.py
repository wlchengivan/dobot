import tensorflow as tf
import cv2
import numpy as np
import json
import takePhoto

#PATH = "3PeopleModel"


def makeString(PATH):
    modelNameString = PATH + "/keras_model.h5"
    classNameString = PATH + "/labels.txt"
    class_names = open(classNameString, "r").readlines()
    
    return modelNameString, class_names



def getObjectClassRealTime(PATH):
    modelNameString, class_names = makeString(PATH)
    model = tf.keras.models.load_model(modelNameString, compile=False)   # 載入 model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)           # 設定資料陣列

    cap = cv2.VideoCapture(0)         # 設定攝影機鏡頭
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, frame = cap.read()       # 讀取攝影機影像
        if not ret:
            print("Cannot receive frame")
            break
        img = cv2.resize(frame , (398, 224))   # 改變尺寸
        img = img[0:224, 80:304]               # 裁切為正方形，符合 model 大小
        BGRimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 

        
        image_array = np.asarray(BGRimg)          # 去除換行符號和結尾空白，產生文字陣列
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1  # 轉換成預測陣列
        data[0] = normalized_image_array
        prediction = model.predict(data)       # 預測結果
        
        
        for i in range(0, len(prediction[0])):
            if prediction[0][i] > 0.9:
                print(class_names[i][2:] + str(round(prediction[0][i] * 100, 2)) + "%")
                cv2.putText(img, class_names[i][2:].strip() + " " + str(round(prediction[0][i] * 100, 2)) + "%", (0, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                        (255, 0, 0), 2)     
                
        
        cv2.imshow('Webcam, press q to stop', img)
        if cv2.waitKey(500) == ord('q'):
            break     # 按下 q 鍵停止
    cap.release()
    cv2.destroyAllWindows()
    
    
def getObjectClassWithImage(PATH):
    modelNameString, class_names = makeString(PATH)
    takePhoto.takePhoto()
    
    model = tf.keras.models.load_model(modelNameString, compile=False)   # 載入 model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)           # 設定資料陣列
    
    image = cv2.imread('Webcam.jpg')
    image = cv2.resize(image, (224, 224))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 

    
    image_array = np.asarray(image)          # 去除換行符號和結尾空白，產生文字陣列
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1  # 轉換成預測陣列
    data[0] = normalized_image_array
    prediction = model.predict(data)       # 預測結果
    
    
    for i in range(0, len(prediction[0])):
        if prediction[0][i] > 0.9:
            
            objectJSON = {
                "className" : class_names[i][2:].strip(),
                "cv" : str(round(prediction[0][i] * 100, 2))
            }
            return objectJSON
            
            #return (class_names[i][2:] + str(round(prediction[0][i] * 100, 2)) + "%")

    objectJSON = {
        "className" : None,
        "cv" : None
    }
    
    return objectJSON
    

getObjectClassRealTime("legoColorModel")