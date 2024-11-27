from serial.tools import list_ports

import pydobot

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[0].device

device = pydobot.Dobot(port=port, verbose=True)

device.move_to(250, 0 ,70, 0, wait=True)


(x, y, z, r, j1, j2, j3, j4) = device.pose()
print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')



device.move_to(x + 50, y + 80, z - 40, r, wait=False)

device.suck(True)

device.suck(False)
device.move_to(x, y, z, r, wait=True)  # we wait until this movement is done before continuing
device.close()