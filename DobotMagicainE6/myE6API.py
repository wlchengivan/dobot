from dobot_api import DobotApiFeedBack,DobotApiDashboard
import threading
from time import sleep
import re
import sys
import time
import pointList

class E6:
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
        
        print(self.dashboard.RobotMode())
        while True:  #完成判断循环

            self.feedData.robotMode = self.dashboard.RobotMode()[3]
            print(self.dashboard.RobotMode()[3])
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
        self.wait(0)
        return self.toList(self.dashboard.GetPose())
    
    def getAngle(self):
        self.wait(0)
        return self.toList(self.dashboard.GetAngle())
    
    def poseToJoint(self, poseList):
        self.wait(0)
        return self.toList(self.dashboard.InverseKin(float(poseList[0]), float(poseList[1]), float(poseList[2]), float(poseList[3]), float(poseList[4]), float(poseList[5])))
    
    def jointToPose(self, poseList):
        self.wait(0)
        return self.toList(self.dashboard.PositiveKin(float(poseList[0]), float(poseList[1]), float(poseList[2]), float(poseList[3]), float(poseList[4]), float(poseList[5])))

    def toList(self, str):
        self.wait(0)
        return str.split("{")[1].split("}")[0].split(",")
    
    def myMovJJoint(self, joint):
        self.wait(0)
        self.dashboard.MovJ(float(joint[0]), float(joint[1]),  float(joint[2]), float(joint[3]), float(joint[4]), float(joint[5]), 1)
        
    def myMovJPose(self, pose):
        self.wait(0)
        self.dashboard.MovJ(float(pose[0]), float(pose[1]),  float(pose[2]), 180, 0, 0, 0)
        

    def myMovJPtoJ(self, pose):
        self.wait(0)
        pose = [float(x) for x in pose]
        
        joint = self.poseToJoint(pose)
        self.myMovJJoint(joint)
        
        
    def myMovLJoint(self, joint):
        self.wait(0)
        self.dashboard.MovL(float(joint[0]), float(joint[1]),  float(joint[2]), float(joint[3]), float(joint[4]), float(joint[5]), 1)
        
    def myMovLPose(self, pose):
        self.wait(0)
        self.dashboard.MovL(float(pose[0]), float(pose[1]),  float(pose[2]), float(pose[3]), float(pose[4]), float(pose[5]), 0)
        

    def myMovLPtoJ(self, pose):
        self.wait(0)
        pose = [float(x) for x in pose]
        
        joint = self.poseToJoint(pose)
        self.myMovLJoint(joint)
        
        

    def getTrayPoint(self, P1, P2, count, i):
        x = P1[0] + ((P2[0] - P1[0]) / (count - 1) * i)
        y = P1[1] + ((P2[1] - P1[1]) / (count - 1) * i)
        z = P1[2] + ((P2[2] - P1[2]) / (count - 1) * i)
        rx = P1[3] + ((P2[3] - P1[3]) / (count - 1) * i)
        ry = P1[4] + ((P2[4] - P1[4]) / (count - 1) * i)
        rz = P1[5] + ((P2[5] - P1[5]) / (count - 1) * i)
        
        pointTemp = [x, y, z, rx, ry, rz]
        return pointTemp

    def Create1DTray(self, P1, P2, count):
        count = int(count)
        
        P1 = [float(x) for x in P1]
        P2 = [float(x) for x in P2]
        
        if(count < 2):
            print("count最少為2")
            return
        else:
            pointList = []
            
            for i in range (0, count):
                pointList.append(self.getTrayPoint(P1, P2, count, i))
                
            return pointList
        
    def Create2DTray(self, P1, P2, P3, P4, row, col):
        row = int(row)
        col = int(col)
        
        P1 = [float(x) for x in P1]
        P2 = [float(x) for x in P2]
        P3 = [float(x) for x in P3]
        P4 = [float(x) for x in P4]
        
        if(row < 2 or col < 2):
            print("row and col 最少為2")
            return
        else:
            pointList = []
            
            for i in range(0, col):
                point1Temp = self.getTrayPoint(P1, P3, col, i)
                point2Temp = self.getTrayPoint(P2, P4, col, i)
                
                pointListTemp = self.Create1DTray(point1Temp, point2Temp, row)
                                
                pointList.append(pointListTemp)
            
            
            return pointList
        
    def Create3DTray(self, P1, P2, P3, P4, P5, P6, P7, P8, row, col, layer):
        row = int(row)
        col = int(col)
        layer = int(layer)
        
        P1 = [float(x) for x in P1]
        P2 = [float(x) for x in P2]
        P3 = [float(x) for x in P3]
        P4 = [float(x) for x in P4]
        P5 = [float(x) for x in P5]
        P6 = [float(x) for x in P6]
        P7 = [float(x) for x in P7]
        P8 = [float(x) for x in P8]
        
        if(row < 2 or col < 2):
            print("row and col and layer 最少為2")
            return
        else:
            pointList = []
            
            for i in range(0, layer):
                point1Temp = self.getTrayPoint(P1, P5, layer, i)
                point2Temp = self.getTrayPoint(P2, P6, layer, i)
                point3Temp = self.getTrayPoint(P3, P7, layer, i)
                point4Temp = self.getTrayPoint(P4, P8, layer, i)
                
                pointListTemp = self.Create2DTray(point1Temp, point2Temp, point3Temp, point4Temp, row, col)
                
                pointList.append(pointListTemp)
                
                
            return pointList
        
    def wait(self, s):
        while self.dashboard.RobotMode()[3] != '5':
            time.sleep(s)
            
    def home(self):
        self.wait(0)
        self.myMovJJoint(pointList.HomeJ)
        
    def myToolDO(self, mode):
        if(mode == 1):
            self.wait(1)

            pose = self.getPose()
            pose = [float(x) for x in pose]
            
            pose[2] = pose[2] - 3
            
            self.myMovJPtoJ(pose)
            
            self.dashboard.ToolDO(1, mode)
            self.wait(1)
            
        if(mode == 0):
            self.wait(1)
            self.dashboard.ToolDO(1, mode)
            self.wait(1)
            
            
    def dance(self): 
        self.wait(0)
        for danceJ in pointList.dacneList:
            self.myMovJJoint(danceJ)
            
    def move(self): 
        self.wait(0)
        for danceJ in pointList.moveList:
            self.myMovJJoint(danceJ)
            
            
    def checkRobotModeInBG(self):
        
        while True:
            robotMode = self.dashboard.RobotMode().split("{")[1].split("}")[0]
            
            print(robotMode)
            
            if(robotMode == "9" or robotMode == "10" or robotMode == "11"):
                self.dashboard.ClearError()
                self.dashboard.Stop()
                self.start()
            else:
                time.sleep(5)
                
