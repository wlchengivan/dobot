from serial.tools import list_ports
import pointList
import pydobot
import myDobotAPI
import detectColorWithImage
import alignment
import math

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[0].device

device = pydobot.Dobot(port=port, verbose=True)

device.move_to(250, 0 ,70, 0, wait=True)


plallet1 = myDobotAPI.pallet(device)
plallet2 = myDobotAPI.pallet(device)

print(plallet1)
print(plallet2)



for i in range(0, len(plallet1)):
    k = float(plallet2[i][2] - plallet1[i][2]) / float(plallet2[i][1] - plallet1[i][1])
    h = math.atan(k)
    a = math.degrees(h)
    
    
    pos1ListTemp = {
        "x" : plallet1[i][1],
        "y" : plallet1[i][2],
        "z" : plallet1[i][3],
        "r" : plallet1[i][4]
    }
    
    pos2ListTemp = {
        "x" : plallet2[i][1],
        "y" : plallet2[i][2],
        "z" : plallet2[i][3],
        "r" : plallet2[i][4] + a
    }
    
    
    
    device.move_to(250, 0 ,70, 0, wait=True)
    device.move_to(pos1ListTemp["x"], pos1ListTemp["y"], 70, pos1ListTemp["r"], wait=True)

    myDobotAPI.myJump(device, pos1ListTemp)
    device.suck(True)
    
    device.move_to(pos2ListTemp["x"], pos2ListTemp["y"], 70, pos2ListTemp["r"], wait=True)
    myDobotAPI.myJump(device, pos2ListTemp)
    device.suck(False)
    
device.close()