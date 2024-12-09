#import teachableMachine
import dobot_api
import myE6API
import pointList
from pynput.keyboard import Key, Listener
import time
import os

moveDis = 10

def on_press(key):
    try:        
        if(key.char == 'w'):
            pose = E6.getPose()
            pose[0] = float(pose[0]) + moveDis
            joint =E6.poseToJoint(pose)
            E6.myMovJJoint(joint)
        if(key.char == 's'):
            pose = E6.getPose()
            pose[0] = float(pose[0]) - moveDis
            joint =E6.poseToJoint(pose)
            E6.myMovJJoint(joint)
        if(key.char == 'a'):
            pose = E6.getPose()
            pose[1] = float(pose[1]) + moveDis
            joint =E6.poseToJoint(pose)
            E6.myMovJJoint(joint)
        if(key.char == 'd'):
            pose = E6.getPose()
            pose[1] = float(pose[1]) - moveDis
            joint =E6.poseToJoint(pose)
            E6.myMovJJoint(joint)
        if(key.char == 'q'):
            pose = E6.getPose()
            pose[2] = float(pose[2]) + moveDis
            joint =E6.poseToJoint(pose)
            E6.myMovJJoint(joint)
        if(key.char == 'e'):
            pose = E6.getPose()
            pose[2] = float(pose[2]) - moveDis
            joint =E6.poseToJoint(pose)
            E6.myMovJJoint(joint)
            
        if(key.char == '5'):
            E6.dashboard.ToolDO(1, 1)
        if(key.char == '6'):
            E6.dashboard.ToolDO(1, 0)
            
        if(key == key.esc):
            return False
        
        time.sleep(0.3)
    
    except AttributeError:
        print("use wsad")
        
def on_release(key):
    if key == Key.esc:
        # 停止监听
        return False

if __name__ == '__main__':
    E6 = myE6API.E6("192.168.5.1")
    E6.start()

    E6.dashboard.Stop()
    E6.dashboard.ClearError()
    E6.dashboard.SpeedFactor(100)
    E6.dashboard.SetBackDistance(50)
    
    startJ, targetJ, startJ2, targetJ2 = pointList.turnLR(0)
    
    list= pointList.turnLR(0)
    
    #E6.myMovJJoint(targetJ)
    
    for p in list:
        E6.myMovJJoint(p)
        os.system("pause")