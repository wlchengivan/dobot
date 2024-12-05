#import teachableMachine
import dobot_api
import myE6API
import pointList
from pynput.keyboard import Key, Listener
import time

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

    while True:
        print("1:移動 \n2:更改點動距離 \n3:取得位置 \n4:取得關節角度 \n0:退出")
        
        a = input()
        match a:
            case '1':
                with Listener(on_press=on_press, on_release=on_release) as listener:
                    listener.join()
                    
            case '2':
                print("請輸入點動距離:")
                moveDis = int(input())
                
            case '3':
                print(E6.getPose())
                
            case '4':
                print(E6.getAngle())
                
            case '5':
                E6.start()
                E6.dashboard.Stop()
                E6.dashboard.ClearError()
                
            case '6':
                E6.dance()
                    
            case '0':
                #E6.off()
                break
