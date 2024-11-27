from serial.tools import list_ports
import pointList
import pydobot
import myDobotAPI
import detectColorWithImage

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[0].device

device = pydobot.Dobot(port=port, verbose=True)
device.move_to(250, 0 ,70, 0, wait=True)



while True:
    myDobotAPI.myMovJ(device, pointList.homePoint)


    color = detectColorWithImage.getColorPos()[0]
    
    if(color == "0"):
        print("Turn off")
        break
    myDobotAPI.moveToCamObject(device)

    if(color == "red"):
        myDobotAPI.myJump(device, pointList.redPoint)
        device.suck(False)
    if(color == "blue"):
        myDobotAPI.myJump(device, pointList.bluePoint)
        device.suck(False)
    if(color == "green"):
        myDobotAPI.myJump(device, pointList.greenPoint)
        device.suck(False)
    

    


device.close()