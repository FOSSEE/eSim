
from PyQt4 import QtGui,QtCore
from numpy import partition
from PyQt4.Qt import QRect
#import GroupBox

class Analysis(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.createAnalysisWidget()
         
    def createAnalysisWidget(self):
        self.grid = QtGui.QGridLayout()
        self.grid.addWidget(self.createCheckBobx(),0,0)
        self.grid.addWidget(self.createACgroup(),1,0)
        self.grid.addWidget(self.createDCgroup(),2,0)
        self.grid.addWidget(self.createTRANgroup(),3,0)
            
        '''
        self.grid.addWidget(self.createTRANgroup(),3,0)
        self.grid.addWidget(self.createTRANgroup(),4,0)
        self.grid.addWidget(self.createTRANgroup(),5,0)
        self.grid.addWidget(self.createTRANgroup(),6,0)
        self.grid.addWidget(self.createTRANgroup(),7,0)
        self.grid.addWidget(self.createTRANgroup(),8,0)
        self.grid.addWidget(self.createTRANgroup(),9,0)
        self.grid.addWidget(self.createTRANgroup(),10,0)
        self.grid.addWidget(self.createTRANgroup(),11,0)
        self.grid.addWidget(self.createTRANgroup(),12,0)
        self.grid.addWidget(self.createTRANgroup(),13,0)
        self.grid.addWidget(self.createTRANgroup(),14,0)
        self.grid.addWidget(self.createTRANgroup(),15,0)
        self.grid.addWidget(self.createTRANgroup(),16,0)
        self.grid.addWidget(self.createTRANgroup(),17,0)
        self.grid.addWidget(self.createTRANgroup(),18,0)
        self.grid.addWidget(self.createTRANgroup(),19,0)
        self.grid.addWidget(self.createTRANgroup(),20,0)
        '''
        
        self.setLayout(self.grid)
        self.show()
        
    
    def createCheckBobx(self):
        self.checkbox = QtGui.QGroupBox()
        self.checkbox.setTitle("Select Analysis Type")
        self.checkgrid = QtGui.QGridLayout()
        
        self.checkgroupbtn = QtGui.QButtonGroup()
        self.checkAC = QtGui.QCheckBox("AC")
        self.checkDC = QtGui.QCheckBox("DC")
        self.checkTRAN = QtGui.QCheckBox("TRANSIENT")
        self.checkgroupbtn.addButton(self.checkAC)
        self.checkgroupbtn.addButton(self.checkDC)
        self.checkgroupbtn.addButton(self.checkTRAN)
        self.checkgroupbtn.setExclusive(True)
        self.checkgroupbtn.buttonClicked.connect(self.enableBox)
        
        self.checkgrid.addWidget(self.checkAC,0,0)
        self.checkgrid.addWidget(self.checkDC,0,1)
        self.checkgrid.addWidget(self.checkTRAN,0,2)
        self.checkbox.setLayout(self.checkgrid)
        
        
        #CSS
        '''
        self.checkbox.setStyleSheet(" \
        QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
        ")
        '''
              
        return self.checkbox
        #return self.checkgroupbtn
    
    def enableBox(self):
        if self.checkAC.isChecked():
            self.acbox.setDisabled(False)
            self.dcbox.setDisabled(True)
            self.trbox.setDisabled(True)
        elif self.checkDC.isChecked():
            self.dcbox.setDisabled(False)
            self.acbox.setDisabled(True)
            self.trbox.setDisabled(True)
            
        elif self.checkTRAN.isChecked():
            self.trbox.setDisabled(False)
            self.acbox.setDisabled(True)
            self.dcbox.setDisabled(True)
        
                
    def createACgroup(self):
        self.acbox = QtGui.QGroupBox()
        self.acbox.setTitle("AC Analysis")
        self.acgrid = QtGui.QGridLayout()
        
        self.Lin = QtGui.QRadioButton("Lin")
        self.Dec = QtGui.QRadioButton("Dec")
        self.Oct = QtGui.QRadioButton("Oct")
        self.acgrid.addWidget(self.Lin,1,1)
        self.acgrid.addWidget(self.Dec,1,2)
        self.acgrid.addWidget(self.Oct,1,3)
        self.acbox.setDisabled(True)
        self.acbox.setLayout(self.acgrid)
        
        self.Scale = QtGui.QLabel("Scale")
        self.Start_Frequency = QtGui.QLabel("Start Frequency")
        self.Stop_Frequency = QtGui.QLabel("Stop Frequency")
        self.No_of_Points = QtGui.QLabel("No.of Points")
        #self.Scale.setMaximumWidth(150)
        #self.Start_Frequency.setMaximumWidth(150)
        #self.Stop_Frequency.setMaximumWidth(150)
        #self.No_of_Points.setMaximumWidth(150)
        self.acgrid.addWidget(self.Scale,1,0)
        self.acgrid.addWidget(self.Start_Frequency,2,0)
        self.acgrid.addWidget(self.Stop_Frequency,3,0)
        self.acgrid.addWidget(self.No_of_Points,4,0)
        
        self.Start_Frequency = QtGui.QLineEdit(self)
        self.Stop_Frequency = QtGui.QLineEdit()
        self.No_of_Points = QtGui.QLineEdit()
        self.acgrid.addWidget(self.Start_Frequency,2,1)
        self.acgrid.addWidget(self.Stop_Frequency,3,1)
        self.acgrid.addWidget(self.No_of_Points,4,1)
        self.Start_Frequency.setMaximumWidth(150)
        self.Stop_Frequency.setMaximumWidth(150)
        self.No_of_Points.setMaximumWidth(150)
        
        #self.lineEdit1.setGeometry()
        
        self.Start_Frequency = QtGui.QComboBox()
        self.Start_Frequency.addItem("Hz",)
        self.Start_Frequency.addItem("KHz")
        self.Start_Frequency.addItem("MHz")
        self.Start_Frequency.addItem("GHz")
        self.Start_Frequency.addItem("THz")
        #self.Start_Frequency.setMaximumWidth(150)
        self.acgrid.addWidget(self.Start_Frequency,2,2)
        self.Stop_Frequency = QtGui.QComboBox()
        self.Stop_Frequency.addItem("Hz")
        self.Stop_Frequency.addItem("KHz")
        self.Stop_Frequency.addItem("MHz")
        self.Stop_Frequency.addItem("GHz")
        self.Stop_Frequency.addItem("THz")
        self.Stop_Frequency.setMaximumWidth(150)
        self.acgrid.addWidget(self.Stop_Frequency,3,2)
        
        
        

        
        
        #CSS   
        self.acbox.setStyleSheet(" \
        QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
        ")
             
        return self.acbox
    
    def createDCgroup(self):
        self.dcbox = QtGui.QGroupBox()
        self.dcbox.setTitle("DC Analysis")
        self.dcgrid = QtGui.QGridLayout()
        #self.dcgrid.setGeometry(self, QRect)
        #self.partition= QtGui.QHBoxLayout()
        #self.dcgrid.addWidget(partition,0,0)
        #self.dcgrid.setHorizontalSpacing(60)
                
        #self.btn3 = QtGui.QRadioButton("Radio button 3")
        #self.simulation_button = QtGui.QPushButton("Add Simulation Data")
        #self.dcgrid.addWidget(self.btn3,0,0)
        #self.dcgrid.addWidget(self.btn4,0,1)
        self.dcbox.setDisabled(True)
        self.dcbox.setLayout(self.dcgrid)
        
        self.source_name= QtGui.QLabel('Enter Source Name',self)
        self.source_name.setMaximumWidth(150)
        self.start= QtGui.QLabel('Start', self)
        self.start.setMaximumWidth(150)
        self.increment=QtGui.QLabel('Increment',self)
        self.increment.setMaximumWidth(150)
        self.stop=QtGui.QLabel('Stop',self)
        self.stop.setMaximumWidth(150)
        self.start_spin= QtGui.QSpinBox()
        self.increment_spin= QtGui.QSpinBox()
        self.stop_spin= QtGui.QSpinBox()
        self.inputbox=QtGui.QLineEdit(self)
        self.inputbox.setMaximumWidth(200)
        self.check=QtGui.QCheckBox('Operating Point Analysis',self)
        
        self.start_combo=QtGui.QComboBox(self)
        self.start_combo.setMaximumWidth(150)
        self.start_combo.addItem('volts or Amperes')
        self.start_combo.addItem('mV or mA')
        self.start_combo.addItem('uV or uA')
        self.start_combo.addItem("nV or nA")
        self.start_combo.addItem("pV or pA")
        
        self.increment_combo=QtGui.QComboBox(self)
        self.increment_combo.setMaximumWidth(150)
        self.increment_combo.addItem("volts or Amperes")
        self.increment_combo.addItem("mV or mA")
        self.increment_combo.addItem("uV or uA")
        self.increment_combo.addItem("nV or nA")
        self.increment_combo.addItem("pV or pA")
        
        self.stop_combo=QtGui.QComboBox(self)
        self.stop_combo.setMaximumWidth(150)
        self.stop_combo.addItem("volts or Amperes")
        self.stop_combo.addItem("mV or mA")
        self.stop_combo.addItem("uV or uA")
        self.stop_combo.addItem("nV or nA")
        self.stop_combo.addItem("pV or pA")  
        
        self.dcgrid.addWidget(self.source_name,1,0)
        self.dcgrid.addWidget(self.inputbox,1,1)
        
        self.dcgrid.addWidget(self.start,2,0)
        self.dcgrid.addWidget(self.start_spin,2,1)
        self.dcgrid.addWidget(self.start_combo,2,2)
        
        self.dcgrid.addWidget(self.increment,3,0)
        self.dcgrid.addWidget(self.increment_spin,3,1)
        self.dcgrid.addWidget(self.increment_combo,3,2)
        
        self.dcgrid.addWidget(self.stop,4,0)
        self.dcgrid.addWidget(self.stop_spin,4,1)
        self.dcgrid.addWidget(self.stop_combo,4,2)
        
        self.dcgrid.addWidget(self.check,5,1,5,2)
        #self.dcgrid.addWidget(self.simulation_button,6,1,6,2)'''
        
        
        
        
        #CSS
        self.dcbox.setStyleSheet(" \
        QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
        ")
              
        
        return self.dcbox
    
    def createTRANgroup(self):
        self.trbox = QtGui.QGroupBox()
        self.trbox.setTitle("Transient Analysis")
        self.trgrid = QtGui.QGridLayout()
        
        #self.btn5 = QtGui.QRadioButton("Radio button 5")
        #self.btn6 = QtGui.QRadioButton("Radio button 6")
        #self.trgrid.addWidget(self.btn5,0,0)
        #self.trgrid.addWidget(self.btn6,0,1)
        self.trbox.setDisabled(True)
        self.trbox.setLayout(self.trgrid)
        
        self.Start_Time = QtGui.QLabel("Start Time")
        self.Step_Time = QtGui.QLabel("Step Time")
        self.Stop_Time = QtGui.QLabel("Stop Time")
        self.trgrid.addWidget(self.Start_Time,1,0)
        self.trgrid.addWidget(self.Step_Time,2,0)
        self.trgrid.addWidget(self.Stop_Time,3,0)
        
        self.Start_Time = QtGui.QLineEdit()
        self.Step_Time = QtGui.QLineEdit()
        self.Stop_Time = QtGui.QLineEdit()
        self.trgrid.addWidget(self.Start_Time,1,1)
        self.trgrid.addWidget(self.Step_Time,2,1)
        self.trgrid.addWidget(self.Stop_Time,3,1)
        
        self.Start_Time = QtGui.QComboBox()
        self.Start_Time.addItem("Sec")
        self.Start_Time.addItem("ms")
        self.Start_Time.addItem("us")
        self.Start_Time.addItem("ns")
        self.Start_Time.addItem("ps")
        self.trgrid.addWidget(self.Start_Time,1,2)
        
        self.Step_Time = QtGui.QComboBox()
        self.Step_Time.addItem("Sec")
        self.Step_Time.addItem("ms")
        self.Step_Time.addItem("us")
        self.Step_Time.addItem("ns")
        self.Step_Time.addItem("ps")
        self.trgrid.addWidget(self.Step_Time,2,2)
        
        self.Stop_Time = QtGui.QComboBox()
        self.Stop_Time.addItem("Sec")
        self.Stop_Time.addItem("ms")
        self.Stop_Time.addItem("us")
        self.Stop_Time.addItem("ns")
        self.Stop_Time.addItem("ps")
        self.trgrid.addWidget(self.Stop_Time,3,2)
        
        
        
        
        #CSS
        self.trbox.setStyleSheet(" \
        QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
        ")
              
        
        return self.trbox