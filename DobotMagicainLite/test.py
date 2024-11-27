from serial.tools import list_ports
import pointList
import pydobot
import myDobotAPI
import detectColorWithImage
import alignment

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[0].device

device = pydobot.Dobot(port=port, verbose=True)

device.move_to(250, 0 ,70, 0, wait=True)


plallet = myDobotAPI.pallet(device)

print(plallet)

for point in plallet:
    posListTemp = {
        "x" : point[1],
        "y" : point[2],
        "z" : point[3],
        "r" : point[4]
    }
    print(posListTemp)
    device.move_to(250, 0 ,70, 0, wait=True)

    myDobotAPI.myMovJ(device, posListTemp)
    device.suck(True)
    myDobotAPI.myJump(device, pointList.greenPoint)
    device.suck(False)

