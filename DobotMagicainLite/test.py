# version: Python3
from DobotEDU import *
import os
import myDobotEDUAPI

res = dobotEdu.m_lite.search_dobot()  # 调用search_dobot接口，搜索机械臂接口，返回接口列表
print("搜索到的接口结果：", res)
port_name = res[0]["portName"]  # 选择可用机械臂接口，默认选择第一个，出现问题用户需要确认是否连接的是机械臂接口
dobotEdu.m_lite.connect_dobot(port_name, True)
dobot = dobot_edu.m_lite

print(port_name)
dobot.set_ptpcmd(port_name, 0, 230, 50, 0, 20, True, True)  # 调用set_ptpcmd接口，机械臂PTP运动


myDobotEDUAPI.takeUpObject(dobot, port_name)



dobot.set_endeffector_suctioncup(port_name, False, True, True)
dobot.disconnect_dobot(port_name)