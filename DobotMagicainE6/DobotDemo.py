from dobot_api import DobotApiFeedBack,DobotApiDashboard
import threading
from time import sleep
import re
import sys
import takePhoto
import detectFaceWithImage
import detectColorWithImage

camXmid = 360
camYmid = 320

class DobotDemo:
    def __init__(self, ip):
        self.ip = ip
        self.dashboardPort = 29999
        self.feedPortFour = 30004
        self.dashboard = None
        self.feedInfo = []

        class item:
            def __init__(self):
                self.robotMode = 1     #

                for i in range(1,6):
                    self.robotMode = i     #

                self.robotCurrentCommandID = 0
                # 自定义添加所需反馈数据

        self.feedData = item()  # 定义结构对象

    def start(self):
        # 启动机器人并使能
        self.dashboard = DobotApiDashboard(self.ip, self.dashboardPort)
        self.feedFour = DobotApiFeedBack(self.ip, self.feedPortFour)
        if self.parseResultId(self.dashboard.EnableRobot())[0] != 0:
            print(self.dashboard.EnableRobot())
            print("使能失败: 检查29999端口是否被占用")
            return
        print("使能成功")

        # 启动状态反馈线程
        threading.Thread(target=self.GetFeed, daemon=True).start()

        

    def GetFeed(self):
        # 获取机器人状态
        while True:
            self.feedFour = DobotApiFeedBack(self.ip, self.feedPortFour)
            feedInfo = self.feedFour.feedBackData()
            if feedInfo != None:   
                if hex((feedInfo['test_value'][0])) == '0x123456789abcdef':
                    print("456")

                    self.feedData.robotMode = feedInfo['robot_mode'][0]
                    #print(self.feedData.robotMode)
                    self.feedData.robotCurrentCommandID = feedInfo['currentcommandid'][0]
                    # 自主添加所需机械臂反馈的数据
                    '''
                    self.feedData.robotErrorState = feedInfo['error_status'][0]
                    self.feedData.robotEnableStatus = feedInfo['enable_status'][0]
                    self.feedData.robotCurrentCommandID = feedInfo['currentcommandid'][0]
                    '''

    def RunPoint(self, point_list):
        # 走点指令
        print(point_list)
        recvmovemess = self.dashboard.MovJ(*point_list, 1)
        print("MovJ:", recvmovemess)
        print(self.parseResultId(recvmovemess))
        currentCommandID = self.parseResultId(recvmovemess)[1]
        print("指令 ID:", currentCommandID)
        
        #sleep(0.02)
        
        print(dobot.dashboard.RobotMode())
        while True:  #完成判断循环

            self.feedData.robotMode = dobot.dashboard.RobotMode()[3]
            print(dobot.dashboard.RobotMode()[3])
            if self.feedData.robotMode == '5':
                print("运动结束")
                break
            sleep(1)

    def parseResultId(self, valueRecv):
        # 解析返回值，确保机器人在 TCP 控制模式
        if "Not Tcp" in valueRecv:
            print("Control Mode Is Not Tcp")
            return [1]
        return [int(num) for num in re.findall(r'-?\d+', valueRecv)] or [2]

    def __del__(self):
        del self.dashboard
        del self.feedFour


    def off(self):
        self.dashboard.DisableRobot()
    
    def getPose(self):
        return self.toList(self.dashboard.GetPose())
    
    def poseToJoint(self, poseList):
        return self.toList(self.dashboard.InverseKin(float(poseList[0]), float(poseList[1]), float(poseList[2]), float(poseList[3]), float(poseList[4]), float(poseList[5])))

    def toList(self, str):
        return str.split("{")[1].split("}")[0].split(",")
    
    def myMovJJoint(self, joint):
        dobot.dashboard.MovJ(float(joint[0]), float(joint[1]),  float(joint[2]), float(joint[3]), float(joint[4]), float(joint[5]), 1)
        
    def myMovJPose(self, pose):
        dobot.dashboard.MovJ(float(pose[0]), float(pose[1]),  float(pose[2]), float(pose[3]), float(pose[4]), float(pose[5]), 0)

    
dobot = DobotDemo("192.168.5.1")

    
def checkColor(self):
    #dobot.myMovJJoint([-9.1099, 101.9493, -55.8517, 44.6622, -91.1378, -131.9925])
    dobot.myMovJPose([-400, -15, 150, 180, 1, -150])
    pose = dobot.getPose()
    legoPos = detectColorWithImage.getColorPos()

    print(dobot.poseToJoint(pose))

    color = legoPos[0]

    if color == "red":
        print("red")
        
        print(legoPos)
        xMid = (legoPos[1]*2+legoPos[3])/2
        yMid = (legoPos[2]*2+legoPos[4])/2
        
        xMove = (xMid-camXmid)/5
        yMove = (yMid-camYmid)/5
        print("xmove"+str(xMove))
        print("ymove"+str(yMove))
        
        joint = dobot.poseToJoint(pose)
        print(pose)
        
        
        """pose[0] = pose[0] + 20
        pose[1] = pose[1] + 20 """
        
        pose[0] = (float(pose[0])) + yMove
        pose[1] = (float(pose[1])) + xMove
        pose[2] = 40
        
        
        joint = dobot.poseToJoint(pose)
        print(pose)
        #dobot.myMovJJoint(joint)
        dobot.myMovJPose(pose)
        
        
    elif color == "blue":
        print("blue")
            
            
    elif color == "green":
        print("green")
            
            
    elif color == "0":
        print("no color")


dobot.start()
#print(dobot.dashboard.RobotMode()[3])
#dobot.dashboard.MovJ(10,10,20,0,0,0, 1)  
#dobot.dashboard.MovJ(10,10,40,0,0,0, 1)   
dobot.dashboard.ClearError()

sex = detectFaceWithImage.checkSex()

if sex == "Male":
    print("Male")
    dobot.dashboard.MovJ(10,10,20,0,0,0, 1)  
elif sex == "Female":
    print("Female")
    dobot.dashboard.MovJ(10,10,40,0,0,0, 1)  
elif sex == 0:
    print("No person")
    dobot.dashboard.MovJ(0,0,0,0,0,0, 1)  
elif sex == 1:
    print("Many people")
    dobot.dashboard.MovJ(0,0,0,0,0,0, 1) 

#print(dobot.dashboard.InverseKin(float(pose[0]), float(pose[1]), float(pose[2]), float(pose[3]), float(pose[4]), float(pose[5])))
#print(dobot.dashboard.InverseKin(-318, 128, 203, 178, 0.22, 54))
#dobot.off()