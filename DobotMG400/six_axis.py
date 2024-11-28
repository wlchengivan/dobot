from dobot_api import DobotApiDashMove,  alarmAlarmJsonFile
import threading
from time import sleep
import numpy as np
import re
import sys


class six_axis():
    def __init__(self, ip):
        self.ip = ip
        self.dashboardPort = 29999
        self.feedPortFour = 30004
        self.dashboardmove = None
        self.feedInfo=[]
        self.__globalLockValue = threading.Lock()
        self.standard_z = -20
        self.x, self.y = 0, 0
        self.std_drop_height, self.std_drop_rotate = 0, 0
        self.rx, self.ry, self.rz = 0, 0, 90
        self.start_coor = np.array([90,0,-90,0,90,0], dtype=np.float32)
        self.xycoor = np.array([self.x, self.y, self.standard_z, self.rx, self.ry, self.rz], dtype=np.float32)
        self.dashboardmove = DobotApiDashMove(self.ip, self.dashboardPort,self.feedPortFour)
        enableState = self.parseResultId(self.dashboardmove.EnableRobot())
        if enableState[0] != 0:
            print("使能失败: 检查29999端口是否被占用)")
            return
        print("使能成功:)")

        feed_thread = threading.Thread(
            target=self.GetFeed)  # 机器状态反馈线程
        feed_thread.daemon = True
        feed_thread.start()
        #######################user#############################
        '''
        2: roulette
        4: pen
        5: sticks
        '''
        self.dashboardmove.User(4)
        ########################################################

    def GetFeed(self):
        while True:
            with self.__globalLockValue:
               self.feedInfo = self.dashboardmove.parseFeedData()
            sleep(0.01)

    def RunPoint(self, point_list: list, status):
        '''
        status 0 - coor mode
               1 - joint mode
        '''
        recvmovemess = self.dashboardmove.MovJ(
            point_list[0], point_list[1], point_list[2], point_list[3], point_list[4], point_list[5], status)
        print("Movj", recvmovemess)
        commandArrID = self.parseResultId(recvmovemess)  # 解析Movj指令的返回值
        return commandArrID

    def parseResultId(self, valueRecv):
        if valueRecv.find("Not Tcp") != -1:  # 通过返回值判断机器是否处于tcp模式
            print("Control Mode Is Not Tcp")
            return [1]
        recvData = re.findall(r'-?\d+', valueRecv)
        recvData = [int(num) for num in recvData]
        #  返回tcp指令返回值的所有数字数组
        if len(recvData) == 0:
            return [2]
        return recvData

    def ClearRobotError(self):
        dataController, dataServo = alarmAlarmJsonFile()    # 读取控制器和伺服告警码
        while True:
          with self.__globalLockValue:
            if self.feedInfo.robotErrorState:
                geterrorID = self.parseResultId(self.dashboardmove.GetErrorID())
                if geterrorID[0] == 0:
                    for i in range(1, len(geterrorID)):
                        alarmState = False
                        for item in dataController:
                            if geterrorID[i] == item["id"]:
                                print("机器告警 Controller GetErrorID",
                                      i, item["zh_CN"]["description"])
                                alarmState = True
                                break
                        if alarmState:
                            continue

                        for item in dataServo:
                            if geterrorID[i] == item["id"]:
                                print("机器告警 Servo GetErrorID", i,
                                      item["zh_CN"]["description"])
                                break

                    choose = input("输入1, 将清除错误, 机器继续运行: ")
                    if int(choose) == 1:
                        clearError = self.parseResultId(
                            self.dashboardmove.ClearError())
                        if clearError[0] == 0:
                            print("--机器清错成功--")
                            break
            else:
                if self.feedInfo.robotMode==11:
                    print("机器发生碰撞")
                    choose = input("输入1, 将清除碰撞, 机器继续运行: ")
                    self.dashboardmove.ClearError()
          sleep(5)

    def __del__(self):
        del self.dashboardmove
    
    def robotic_arm_calibration(self, letter):
        '''
        my a is [116.1684, -114.4681, 78.3973, 0, 0, 90]
        my b is [116.1684, 85.9641, 75.2439, 0, 0, 90]
        my c is [-4.9, 84.2436, 72.3738, 0, 0, 90]
        my d is [-7.999, -114.4681, 78.3973, 0, 0, 90]

        a is for 5,0
        b is for 0,0    d is for 0,8
        '''
        file_name = "calibration_coord_arm.txt"
        match letter:
            case "a":
                num_point = 1
                # current_coor = [-4.9, 84.2436, 72.3738, 0, 0, 90]
                current_coor = self.pose()
                self.camera.storing_calibration_data(current_coor[0], current_coor[1], num_point, file_name)

            case "b":
                num_point = 0
                # current_coor = [116.1684, 85.9641, 75.2439, 0, 0, 90]
                current_coor = self.pose()
                self.camera.storing_calibration_data(current_coor[0], current_coor[1], num_point, file_name)

            case "d":
                num_point = 2
                # current_coor = [116.1684, -114.4681, 78.3973, 0, 0, 90]
                current_coor = self.pose()
                self.camera.storing_calibration_data(current_coor[0], current_coor[1], num_point, file_name)
    
    def new_robotic_arm_calibration(self, letter):
        '''
        a is for 5,0
        b is for 0,0    d is for 0,8
        '''
        file_name = "calibration_coord_arm.txt"

        match letter:
            case "a":
                num_point = 1
                a_current_coor = self.pose()
                self.camera.storing_calibration_data(a_current_coor[0], a_current_coor[1], num_point, file_name)

                num_point = 0
                b_current_coor = [a_current_coor[0] + 121, a_current_coor[1]]
                self.camera.storing_calibration_data(b_current_coor[0], b_current_coor[1], num_point, file_name)

                num_point = 2
                d_current_coor = [b_current_coor[0], b_current_coor[1]-194]
                self.camera.storing_calibration_data(d_current_coor[0], d_current_coor[1], num_point, file_name)

    def RBG_box_coordinate(self, letter):
        '''
        1 for red 2 for blue 3 for green
        '''
        file_name = "box_coordinate_RBG_new.txt"
        match letter:
            case "R":
                num_point = 0
                current_coor = self.pose()
                self.camera.storing_calibration_data(current_coor[0], current_coor[1], num_point, file_name)

            case "G": 
                num_point = 1
                current_coor = self.pose()
                self.camera.storing_calibration_data(current_coor[0], current_coor[1], num_point, file_name)

            case "B":
                num_point = 2
                current_coor = self.pose()
                self.camera.storing_calibration_data(current_coor[0], current_coor[1], num_point, file_name)
    
    def pose(self):
        string = self.dashboardmove.GetPose()
        start_index = string.find("{") + 1
        end_index = string.find("}")
        values_str = string[start_index:end_index]
        values = values_str.split(",")
        coor = np.array([float(value.strip()) for value in values], dtype=np.float32)
        print(coor)
        return coor

    def ClearError(self):
        self.dashboardmove.ClearError()
        print('Error Cleared')

    def grip(self, status):
        '''
        1 open
        0 close
        '''
        match status:
            case 1:
                self.dashboardmove.ToolDO(2,1)
            case 0:
                self.dashboardmove.ToolDO(2,0)

    def default_pos(self):
        '''
        self.start_coor = [0,0,-90,0,90,0] joint mode
        '''
        p2Id = self.RunPoint(self.start_coor, 1)
        if p2Id[0] == 0:  # 运动指令返回值正确
            self.dashboardmove.WaitArrive(p2Id[1])  # 传入运动指令commandID ,进入等待指令完成
        sleep(0.5)

    def grip_and_drop_block(self, tar_x, tar_y, box_color, tar_r):
        self.grip(1)
        point_a = self.xycoor
        point_a[0], point_a[1], point_a[-1] = tar_x, tar_y, tar_r
        self.RunPoint(point_a, 0)
        sleep(1.5)
        point_a[2] = 82 # z
        self.RunPoint(point_a, 0)
        sleep(1.5)
        self.grip(0)
        sleep(1.5)
        point_a[2] = self.standard_z
        self.RunPoint(point_a, 0)
        sleep(1.5)
        self.camera.read_calibration_from_file("box_coordinate_RBG_new.txt", "box")
        match box_color:    
            case "red":
                point_a = self.xycoor
                point_a[0], point_a[1], point_a[2] = self.camera.dst_points_box[0][0], self.camera.dst_points_box[0][1], self.std_drop_height,
                point_a[-1] = self.std_drop_rotate
                self.RunPoint(point_a, 0)
                sleep(0.5)
                self.grip(1)
                sleep(0.5)

            case "blue":
                point_a = self.xycoor
                point_a[0], point_a[1], point_a[2] = self.camera.dst_points_box[1][0], self.camera.dst_points_box[1][1], self.std_drop_height,
                point_a[-1] = self.std_drop_rotate
                self.RunPoint(point_a, 0)
                sleep(0.5)
                self.grip(1)
                sleep(0.5)
            case "green":
                point_a = self.xycoor
                point_a[0], point_a[1], point_a[2] = self.camera.dst_points_box[2][0], self.camera.dst_points_box[2][1], self.std_drop_height,
                point_a[-1] = self.std_drop_rotate
                self.RunPoint(point_a, 0)
                sleep(0.5)
                self.grip(1)
                sleep(0.5)


    def chasing(self, tar_x, tar_y, tar_r):
        point_a = self.xycoor
        point_a[0], point_a[1], point_a[-1] = tar_x, tar_y, tar_r
        self.RunPoint(point_a, 0)
