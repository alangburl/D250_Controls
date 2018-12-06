import sys,time
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, 
                             QLCDNumber, QVBoxLayout, QProgressBar,
                             QGridLayout,QLineEdit,
                             QSizePolicy)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont
import PyQt5.QtCore as q

import Speedometer as sp

class Display(QWidget):
    def __init__(self):
        super().__init__()
        self.showMaximized()
        self.setWindowTitle('D250 Speedometer v1.0')
        font=QFont()
        font.setPointSize(16)
        
        #displaying the throttle position from the stepper motor controller
        self.throttle_position=QProgressBar(self)
        self.throttle_position.setFont(font)
        self.throttle_position.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.throttle_position.setMaximumHeight(30)
        
        #use thread to display value
        self.speed=QLCDNumber(self)
        self.speed.setFont(font)
        self.speed.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        
        #Indication of various vehicle parameters
        self.cruise_indicator=QLineEdit(self)
        self.cruise_indicator.setReadOnly(True)
        self.cruise_indicator.setFont(font)
        self.cruise_indicator.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.cruise_indicator.setAlignment(q.Qt.AlignRight)
        self.cruise_indicator.setMaximumHeight(100)
        
        #values of vehicle parameters
        self.indicator=QLineEdit(self)
        self.indicator.setReadOnly(True)
        self.indicator.setFont(font)
        self.indicator.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.indicator.setAlignment(q.Qt.AlignRight)
        self.indicator.setMaximumHeight(100)
        
        #incorporation of cruise control feature to maintain and resume the vehicle speed
        self.set_cruise=QPushButton('Set',self)
        self.set_cruise.setCheckable(True)
        self.set_cruise.setFont(font)
        self.set_cruise.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.set_cruise.clicked.connect(self.sets)
        self.set_cruise.setDisabled(True)
        
        #resume vehicle speed
        self.resume=QPushButton('Resume',self)
        self.resume.setFont(font)
        self.resume.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.resume.clicked.connect(self.resumes)
        self.resume.setDisabled(True)
        
        #cancel cruise
        self.cancel=QPushButton('Cancel',self)
        self.cancel.setFont(font)
        self.cancel.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.cancel.clicked.connect(self.cancels)
        self.cancel.setDisabled(True)
        
        #turn cruise on and off
        self.cruise_state=QPushButton('On\Off',self)
        self.cruise_state.setCheckable(True)
        self.cruise_state.setFont(font)
        self.cruise_state.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.cruise_state.clicked.connect(self.on_off)
        
        'Add the layout to the widget'
        layout=QGridLayout()
        layout.addWidget(self.speed,0,1)
        layout.addWidget(self.cruise_indicator,1,1)
        layout.addWidget(self.indicator,2,1)
        layout.addWidget(self.resume,0,2)
        layout.addWidget(self.set_cruise,1,0,2,1)
        layout.addWidget(self.cancel,1,2,2,1)
        layout.addWidget(self.cruise_state,0,0)
        
        vlayout=QVBoxLayout()
        vlayout.addLayout(layout)
        vlayout.addWidget(self.throttle_position)
        self.setLayout(vlayout)
        self.initUI()
        
    def initUI(self):
        '''Setting up the GUI'''
        self.th=Mileage(self)
        self.th.changeprogressbar.connect(self.throttle_position.setValue)
        self.th.changelcd.connect(self.speed.display)
        self.th.change_odometer.connect(self.cruise_indicator.setText)
        self.th.start()
        
        self.gauges=Gauge_Readouts(self)
        self.gauges.values.connect(self.indicator.setText)
        self.gauges.start()
        
    def on_off(self):
        '''State of the Cruise Control'''
        if self.cruise_state.isChecked()==True:
            self.cruise_indicator.setText('On')
            self.set_cruise.setEnabled(True)
            
        elif self.cruise_state.isChecked()==False:
            self.cruise_indicator.setText('Off')
            self.cancel.setEnabled(False)
            self.resume.setEnabled(False)
            self.set_cruise.setEnabled(False)
            
    def resumes(self):
        '''Resumes the pickup to set speed'''
        self.indicator.setText('Resuming to {:.1f}:'.format(self.set_speed))
        
    def cancels(self):
        '''Cancels and keeps set speed'''
        self.indicator.setText('Cancels')
        self.resume.setEnabled(True)
        
    def sets(self):
        '''Sets the speed for the cruise control'''
        self.set_speed=sp.Gauges.find_speed(self)[0]
        self.indicator.setText('Set at {:.1f}'.format(self.set_speed))
        self.cancel.setEnabled(True)
        self.resume.setEnabled(False)
    
class Mileage(QThread):
    '''Creates the thread to update the progress bar'''
    changeprogressbar=pyqtSignal(int)
    changelcd=pyqtSignal(int)
    change_odometer=pyqtSignal(str)
    
    def __init__(self, parent=None):
        '''Setting up the thread'''
        QThread.__init__(self, parent=parent)
        self.isRunning=True
    
    def run(self):
        '''Starting the thread'''
        #this file is opened and left open to write the new values back to when
        #at a stop light/stop sign
        file=open('odometer.csv','r+')
        mile=float(file.readlines()[0])
        st=time.time()
        delta=0
        speed_run_time=0
        #inplace an infinite while loop, which would be used in reality, this times 
        #out after 40 seconds of run time
        while delta<60.0:
            speed_time=time.time()
            self.changelcd.emit(int(sp.Gauges.find_speed(self)[0]))
            #assumes a constant speed between the data points
            mile+=sp.Gauges.find_speed(self)[0]*(speed_run_time/3600)
            #emit a signal to be used for display purposes
            self.change_odometer.emit(str(round(mile,1)))
            #speed the vehicle is traveling at currently
            speed=sp.Gauges.find_speed(self)[0]
            #pause so its is readable
            time.sleep(.5)
            if speed<0.1:
                #finding the top line and writing the new mileage count to it
                file.seek(0,0)
                file.truncate(0)
                file.write(str(mile))
                file.close()
                #wait a second
                time.sleep(0.25)
                #reopen the file and get the new mileage
                file=open('odometer.csv','r+')
                mile=float(file.readlines()[0])
            delta=time.time()-st
            speed_run_time=time.time()-speed_time
            
        file.close()
            
class Gauge_Readouts(QThread):
    '''Update the values of the various parameters'''
    values=pyqtSignal(str)
    
    def __init__(self,parent=None):
        '''initialize the thread'''
        QThread.__init__(self, parent=parent)
        
    def run(self):
        '''Display the values'''
        st=time.time()
        delta=0
        #delay cycle for gauge cluster
        wait=2
        #inplace an infinite while loop, which would be used in reality, this times 
        #out after 40 seconds of run time
        while delta<60.0: 
            #emitting signals for all the various parameters and pausing so they are readable
            self.values.emit('Oil Pressure: {} psi'.format(sp.Gauges.find_oil_pressure(self)))
            time.sleep(wait)
            self.values.emit('Fuel Level: {}%'.format(sp.Gauges.find_fuel_level(self)))
            time.sleep(wait)
            self.values.emit('Engine Temperature: {}F'.format(sp.Gauges.find_temp(self)))
            time.sleep(wait)
            self.values.emit('Oil Temperature: {}F'.format(sp.Gauges.find_oil_pressure(self)))
            time.sleep(wait)
            self.values.emit('Voltage: {} V'.format(sp.Gauges.find_voltage(self)))
            time.sleep(wait)
            self.values.emit('Boost: {} psi'.format(sp.Gauges.find_boost(self)))
            delta=time.time()-st
                            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Display()
    window.show()
    sys.exit(app.exec_())