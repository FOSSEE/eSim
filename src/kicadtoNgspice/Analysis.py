
from PyQt4 import QtGui,QtCore
#from numpy import partition
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
        self.flag=0
        if self.checkAC.isChecked():
            self.acbox.setDisabled(False)
            self.dcbox.setDisabled(True)
            self.trbox.setDisabled(True)
            self.flag=1
            
        elif self.checkDC.isChecked():
            self.dcbox.setDisabled(False)
            self.acbox.setDisabled(True)
            self.trbox.setDisabled(True)
            self.flag=2
            
        elif self.checkTRAN.isChecked():
            self.trbox.setDisabled(False)
            self.acbox.setDisabled(True)
            self.dcbox.setDisabled(True)
            self.flag=3 
        
        return self.flag
        
                
    def createACgroup(self):
        self.acbox = QtGui.QGroupBox()
        self.acbox.setTitle("AC Analysis")
        #self.acgrid2 =QtGui.QGridLayout()
        self.acgrid = QtGui.QGridLayout()
        self.acbox.setDisabled(True)
        self.acbox.setLayout(self.acgrid)
        #self.acbox.setLayout(self.acgrid2)
        
        self.Lin = QtGui.QRadioButton("Lin")
        self.Dec = QtGui.QRadioButton("Dec")
        self.Oct = QtGui.QRadioButton("Oct")
        self.acgrid.addWidget(self.Lin,1,1)
        self.acgrid.addWidget(self.Dec,1,2)
        self.acgrid.addWidget(self.Oct,1,3)
        
        
        self.Lin.setMaximumWidth(150)
        self.Dec.setMaximumWidth(150)
        self.Oct.setMaximumWidth(150)
                       
             
        self.scale_label = QtGui.QLabel("Scale")
        self.start_fre_lable = QtGui.QLabel("Start Frequency")
        self.stop_fre_lable = QtGui.QLabel("Stop Frequency")
        self.no_of_points = QtGui.QLabel("No.of Points")
        
        self.scale_label.setMaximumWidth(150)
        self.start_fre_lable.setMaximumWidth(150)
        self.stop_fre_lable.setMaximumWidth(150)
        self.no_of_points.setMaximumWidth(150)
        
        self.acgrid.addWidget(self.scale_label,1,0)
        self.acgrid.addWidget(self.start_fre_lable,2,0)
        self.acgrid.addWidget(self.stop_fre_lable,3,0)
        self.acgrid.addWidget(self.no_of_points,4,0)
        
        self.start_fre_in = QtGui.QLineEdit()
        self.stop_fre_in = QtGui.QLineEdit()
        self.points_in = QtGui.QLineEdit()
        self.acgrid.addWidget(self.start_fre_in,2,1)
        self.acgrid.addWidget(self.stop_fre_in,3,1)
        self.acgrid.addWidget(self.points_in,4,1)
        
        self.start_fre_in.setMaximumWidth(150)
        self.stop_fre_in.setMaximumWidth(150)
        self.points_in.setMaximumWidth(150)
                
        self.start_fre_combo = QtGui.QComboBox()
        self.start_fre_combo.addItem("Hz",)
        self.start_fre_combo.addItem("KHz")
        self.start_fre_combo.addItem("MHz")
        self.start_fre_combo.addItem("GHz")
        self.start_fre_combo.addItem("THz")
        self.start_fre_combo.setMaximumWidth(150)
        self.acgrid.addWidget(self.start_fre_combo,2,2)
        self.stop_fre_combo = QtGui.QComboBox()
        self.stop_fre_combo.addItem("Hz")
        self.stop_fre_combo.addItem("KHz")
        self.stop_fre_combo.addItem("MHz")
        self.stop_fre_combo.addItem("GHz")
        self.stop_fre_combo.addItem("THz")
        self.stop_fre_combo.setMaximumWidth(150)
        self.acgrid.addWidget(self.stop_fre_combo,3,2)
        
        self.start_fre_val = str(self.start_fre_in.text())
        self.stop_fre_val = str(self.stop_fre_in.text())
        self.no_points_val = str(self.points_in.text())
        
        if (self.Lin.isCheckable()):
            self.checked = 1
        elif (self.Dec.isCheckable()):
            self.checked = 2 
        else:
            self.checked = 3
            
        self.start_unit = str(self.start_fre_combo.currentText())
        self.stop_unit = str(self.stop_fre_combo.currentText())
        
        self.ac_output_list=['ac.',self.checked,self.start_fre_val, self.stop_fre_val, self.no_points_val,self.start_unit, self.stop_unit, self.no_points_val]
        
        print self.ac_output_list
        
        #return(self.output_list)
        #CSS   
        self.acbox.setStyleSheet(" \
        QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
        ")
        #return self.ac_output_list 
        return self.acbox
    
    def createDCgroup(self):
        self.dcbox = QtGui.QGroupBox()
        self.dcbox.setTitle("DC Analysis")
        self.dcgrid = QtGui.QGridLayout()

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
        
        self.start_spin= QtGui.QLineEdit()
        self.increment_spin= QtGui.QLineEdit()
        self.stop_spin= QtGui.QLineEdit()
        self.start_spin.setMaximumWidth(150)
        self.increment_spin.setMaximumWidth(150)
        self.stop_spin.setMaximumWidth(150)
        
        self.inputbox=QtGui.QLineEdit(self)
        self.inputbox.setMaximumWidth(150)
        self.check=QtGui.QCheckBox('Operating Point Analysis',self)
        
        if(self.check.isChecked()):
            self.flagcheck = 1
            
        else:
            self.flagcheck= 2
            
        self.start_val= str(self.start_spin.text())
        self.stop_val = str(self.stop_spin.text())
        self.increment_val= str(self.increment_spin.text())        
                
        self.start_combo=QtGui.QComboBox(self)
        self.start_combo.setMaximumWidth(150)
        self.start_combo.addItem('volts or Amperes')
        self.start_combo.addItem('mV or mA')
        self.start_combo.addItem('uV or uA')
        self.start_combo.addItem("nV or nA")
        self.start_combo.addItem("pV or pA")
        
        self.start_combo_val= str(self.start_combo.currentText())
        self.start_power = self.getpower(self.start_combo_val)
        
        self.increment_combo=QtGui.QComboBox(self)
        self.increment_combo.setMaximumWidth(150)
        self.increment_combo.addItem("volts or Amperes")
        self.increment_combo.addItem("mV or mA")
        self.increment_combo.addItem("uV or uA")
        self.increment_combo.addItem("nV or nA")
        self.increment_combo.addItem("pV or pA")
        
        self.increment_power= self.getpower(str(self.increment_combo.currentText()))
        
        self.stop_combo=QtGui.QComboBox(self)
        self.stop_combo.setMaximumWidth(150)
        self.stop_combo.addItem("volts or Amperes")
        self.stop_combo.addItem("mV or mA")
        self.stop_combo.addItem("uV or uA")
        self.stop_combo.addItem("nV or nA")
        self.stop_combo.addItem("pV or pA")  
        
        self.stop_power= self.getpower(str(self.stop_combo.currentText()))
        
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
        self.dc_output_list = ['.dc',self.start_val,self.start_power,self.increment_val, self.increment_power, self.stop_val, self.stop_power]
        
        print self.dc_output_list
        
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
        
        self.trbox.setDisabled(True)
        self.trbox.setLayout(self.trgrid)
        
        self.start = QtGui.QLabel("Start Time")
        self.step = QtGui.QLabel("Step Time")
        self.stop = QtGui.QLabel("Stop Time")
        self.trgrid.addWidget(self.start,1,0)
        self.trgrid.addWidget(self.step,2,0)
        self.trgrid.addWidget(self.stop,3,0)
        self.start.setMaximumWidth(150)
        self.step.setMaximumWidth(150)
        self.stop.setMaximumWidth(150)
        
        self.start_time = QtGui.QLineEdit()
        self.step_time = QtGui.QLineEdit()
        self.stop_time = QtGui.QLineEdit()
        self.trgrid.addWidget(self.start_time,1,1)
        self.trgrid.addWidget(self.step_time,2,1)
        self.trgrid.addWidget(self.stop_time,3,1)
        
        self.start_time.setMaximumWidth(150)
        self.step_time.setMaximumWidth(150)
        self.stop_time.setMaximumWidth(150)        
        
        self.start_time_val= str(self.start_time.text())
        self.step_time_val= str(self.step_time.text())
        self.stop_time_val= str(self.stop_time.text())
        
        self.start_combobox = QtGui.QComboBox()
        self.start_combobox.addItem("Sec")
        self.start_combobox.addItem("ms")
        self.start_combobox.addItem("us")
        self.start_combobox.addItem("ns")
        self.start_combobox.addItem("ps")
        self.trgrid.addWidget(self.start_combobox,1,2)
        self.start_combobox.setMaximumWidth(150)
                
        self.step_combobox = QtGui.QComboBox()
        self.step_combobox.addItem("Sec")
        self.step_combobox.addItem("ms")
        self.step_combobox.addItem("us")
        self.step_combobox.addItem("ns")
        self.step_combobox.addItem("ps")
        self.trgrid.addWidget(self.step_combobox,2,2)
        self.step_combobox.setMaximumWidth(150)
                
        self.stop_combobox = QtGui.QComboBox()
        self.stop_combobox.addItem("Sec")
        self.stop_combobox.addItem("ms")
        self.stop_combobox.addItem("us")
        self.stop_combobox.addItem("ns")
        self.stop_combobox.addItem("ps")
        self.trgrid.addWidget(self.stop_combobox,3,2)
        self.stop_combobox.setMaximumWidth(150)
                
        self.start_tpower=self.getpower(str(self.start_combobox.currentText()))
        self.step_tpower=self.getpower(str(self.step_combobox.currentText()))
        self.stop_tpower=self.getpower(str(self.stop_combobox.currentText()))
        
        self.trans_output_list =['.tran', self.start_time_val, self.start_tpower, self.step_time_val, self.step_tpower, self.stop_time_val, self.stop_tpower]
        print self.trans_output_list
           
        #CSS
        self.trbox.setStyleSheet(" \
        QGroupBox { border: 1px solid gray; border-radius: 9px; margin-top: 0.5em; } \
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; } \
        ")
              
        
        return self.trbox
    
    
    def getpower(self, unit):
        if unit[0] == 'p':
            return "e-12"
        elif unit[0] == 'n':
            return "e-09"
        elif unit[0] == 'u':
            return "e-06"
        elif unit[0] == 'm':
            return "e-03"
        else:
            return "e-00"
