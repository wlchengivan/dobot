from ultralytics import YOLO as yolo
import cv2

model = yolo("yolo11n.pt")


results = model(cv2.imread('Webcam.jpg'))

#results = model("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/V6B1_at_Jordan%2C_West_Kowloon_Station_%2820190322100306%29.jpg/1200px-V6B1_at_Jordan%2C_West_Kowloon_Station_%2820190322100306%29.jpg")

names = model.names

#print(round(float(results[0].boxes.conf[0]),2)*100)

for i in range(len(results[0])):
    conf = round(float(results[0].boxes.conf[i])*100, 2)
    print(names[int(results[0].boxes.cls[i])] + "  " + str(conf) + "%")



results[0].show()


"""for i in range(0,len(results[0])):
    results[0][i].show()"""