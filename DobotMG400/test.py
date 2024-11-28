import threading
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType,alarmAlarmJsonFile
from time import sleep
import numpy as np
import re
import pydobot
from serial.tools import list_ports

# 全局变量(当前坐标)
current_actual = None
algorithm_queue = None
enableStatus_robot = None
robotErrorState = False
globalLockValue = threading.Lock()


try:
    ip = "192.168.1.6"
    dashboardPort = 29999
    movePort = 30003
    feedPort = 30004
    print("連接中")
    dashboard = DobotApiDashboard(ip, dashboardPort)
    move = DobotApiMove(ip, movePort)
    feed = DobotApi(ip, feedPort)
    print("連接成功")
    


    dashboard.EnableRobot()
    print("開機")

    
    dashboard.DisableRobot()
    print("關機")
    

    
except Exception as e:
    print("連接失敗")
    raise e

