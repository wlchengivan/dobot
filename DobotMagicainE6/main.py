#import teachableMachine
import dobot_api
import myE6API
import pointList

if __name__ == '__main__':
    E6 = myE6API.E6("192.168.5.1")
    E6.start()

    E6.dashboard.ToolDO(1, 1)
    E6.dashboard.ToolDO(1, 0)
    
"""    P1 = ['0.0000', '00.0000', '0.0000', '0.0000', '0.0000', '0.0000']
    P2 = ['0.0000', '100.0000', '0.0000', '0.0000', '0.0000', '0.0000']
    P3 = ['100.0000', '0.0000', '0.0000', '0.0000', '0.0000', '0.0000']
    P4 = ['100.0000', '100.0000', '0.0000', '0.0000', '0.0000', '0.0000']
    P5 = ['0.0000', '0.0000', '100.0000', '0.0000', '0.0000', '0.0000']
    P6 = ['0.0000', '100.0000', '100.0000', '0.0000', '0.0000', '0.0000']
    P7 = ['100.0000', '0.0000', '100.0000', '0.0000', '0.0000', '0.0000']
    P8 = ['100.0000', '100.0000', '100.0000', '0.0000', '0.0000', '0.0000']
    

    #pointList = E6.Create1DTray(P2, P4, 3)
    
    #pointList = E6.Create2DTray(P1, P2, P3, P4, 3, 3)
    
    pointList = E6.Create3DTray(P1, P2, P3, P4, P5, P6, P7, P8, 3, 3, 3)

    
    
    #print(pointList)
    
    for point2d in pointList:
        for point1d in point2d:
            print(point1d)
        print("\n\n")"""
        
        
        
    
    
    #E6.off()