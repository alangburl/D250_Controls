import numpy as np
#import the model used to interface with the ADC converter
#import piplates.DAQC2plate as DAQC2
class Gauges():
    def __init__(self):
        '''Class used for gauge cluster information gathering'''
        
    def find_speed(self):
        ''''Determine the speed from the GPIO input pins
        ***this is a simulated result for the purposes of this project***''' 
        read_value=np.random.randint(20,90) #DAQC2.getFrequency()
        #convert frequency to MPH
        scalar=1 #from sensor~ 1MPH/22Hz
        output_value=int(scalar*read_value)
        return output_value,1
    
    def find_oil_pressure(self):
        '''Find the oil pressure from the GPIO pins
        ***this is a simulated result for the purposes of this project***'''
        read_value=np.random.rand() #DAQC2.getADC(0,1)
        scalar=np.random.randint(30,40)
        output_value=int(read_value*scalar)
        return output_value
    
    def find_fuel_level(self):
        '''Find the fuel level from the GPIO pins
        ***this is a simulated result for the purposes of this project***'''
        read_value=np.random.rand() #DAQC2.getADC(0,2)
        scalar=np.random.randint(0,100)
        output_value=int(read_value*scalar)
        return output_value
    
    def find_temp(self):
        '''Find the temperature from the GPIO pins
        ***this is a simulated result for the purposes of this project***'''
        read_value=np.random.rand() #DAQC2.getADC(0,3)
        scalar=np.random.randint(100,220)
        output_value=int(read_value*scalar)
        if output_value>200:
            return 'OVERHEAT'
        else:
            return output_value   
 
    def find_voltage(self):
        '''Find the voltage from the GPIO pins
        ***this is a simulated result for the purposes of this project***'''
        read_value=np.random.rand() #DAQC2.getADC(0,4)
        scalar=np.random.randint(11,16)
        output_value=int(read_value*scalar)
        if output_value>200:
            return 'OVERCHARGE'
        else:
            return output_value 
    
    def find_boost(self):
        '''Find the boost from the GPIO pins
        ***this is a simulated result for the purposes of this project***'''
        read_value=np.random.rand() #DAQC2.getADC(0,5)
        scalar=np.random.randint(0,35)
        output_value=int(read_value*scalar)
        if output_value>25:
            return 'OVERBOOST'
        else:
            return output_value 