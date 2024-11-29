from DobotEDU import *

def takeUpObject(dobot, port_name):
    dobot.set_endeffector_suctioncup(port_name, True, True, True)    
    dobot.set_ptpcmd(port_name, 0, dobotEdu.m_lite.get_pose(port_name)['x'], dobotEdu.m_lite.get_pose(port_name)['y'], dobotEdu.m_lite.get_pose(port_name)['z'] - 2, dobotEdu.m_lite.get_pose(port_name)['r'], True, True)