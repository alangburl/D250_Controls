#Error calculation from PID controller
class Controller(object):
    def __init__(self,desired_speed):
        '''Initialize the controller'''
        self.desired_speed=desired_speed
        
    
    def calculate(self,actual,DT,ui_past=0,error_past=0):
        '''calculate pid controller''' 
        ki=10
        kd=7
        kp=5                   
        uimax=10
        error= actual-self.desire
        up=error*kp
        ui=ki*error*DT+ui_past
        ui_past=ui
        
        if ui>uimax:
            ui=uimax
        elif ui<-uimax:
            ui=uimax
            
        ud=kd*(error-error_past)/DT
        error_past=error
        ut=up+ui+ud
        self.ut=ut        