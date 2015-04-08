#===============================================================================
#
#          FILE: kicadtoNgspice.py
# 
#         USAGE: --- 
# 
#   DESCRIPTION: This define all configuration used in Application. 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 04 March 2015 
#      REVISION:  ---
#===============================================================================
import sys
import os
from PyQt4 import QtGui,QtCore
from Processing import PrcocessNetlist
import Analysis
import Source
import Convert
import TrackWidget


class MainWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        #Create object of track widget
        self.obj_track = TrackWidget.TrackWidget()
              
        print "Init Kicad to Ngspice"             
            
        #Creating GUI for kicadtoNgspice window
        self.grid = QtGui.QGridLayout(self)
        self.convertbtn = QtGui.QPushButton("Convert")
        self.convertbtn.clicked.connect(self.callConvert)
        self.cancelbtn = QtGui.QPushButton("Cancel")
        self.cancelbtn.clicked.connect(self.close)
        self.grid.addWidget(self.createcreateConvertWidget(),0,0)
        self.grid.addWidget(self.convertbtn,1,1)
        self.grid.addWidget(self.cancelbtn,1,2)
        #self.setGeometry(800, 800, 1000, 1000)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setLayout(self.grid)
        self.show()
             
    
    def createcreateConvertWidget(self):
        
        self.convertWindow = QtGui.QWidget()
                      
        self.analysisTab = QtGui.QScrollArea()
        self.analysisTab.setWidget(Analysis.Analysis())
        self.analysisTabLayout = QtGui.QVBoxLayout(self.analysisTab.widget())
        self.analysisTab.setWidgetResizable(True)
        
        self.sourceTab = QtGui.QScrollArea()
        self.sourceTab.setWidget(Source.Source(sourcelist,sourcelisttrack))
        self.sourceTabLayout = QtGui.QVBoxLayout(self.sourceTab.widget())
        self.sourceTab.setWidgetResizable(True)
        
        self.modelTab = QtGui.QScrollArea()
        self.modelTab.setWidget(QtGui.QWidget())
        self.modelTabLayout = QtGui.QVBoxLayout(self.modelTab.widget())
        self.modelTab.setWidgetResizable(True)

        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.addTab(self.analysisTab,"Analysis Tab")
        self.tabWidget.addTab(self.sourceTab,"Source Tab")
        self.tabWidget.addTab(self.modelTab,"Model Tab")
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addWidget(self.tabWidget)
        #self.mainLayout.addStretch(1)
        self.convertWindow.setLayout(self.mainLayout)
        self.convertWindow.show()
    
        
        return self.convertWindow 
    
    def callConvert(self):
        """
        Calling Convert Class Constructor
        """
        global schematicInfo
        global analysisoutput
        self.obj_convert = Convert.Convert(self.obj_track.sourcelisttrack["ITEMS"],
                                           self.obj_track.entry_var["ITEMS"],
                                           schematicInfo)
        #Adding Source Value to Schematic Info
        schematicInfo = self.obj_convert.addSourceParameter()
        analysisoutput = self.obj_convert.analysisInsertor(self.obj_track.AC_entry_var["ITEMS"],
                                           self.obj_track.DC_entry_var["ITEMS"],
                                           self.obj_track.TRAN_entry_var["ITEMS"],
                                           self.obj_track.set_CheckBox["ITEMS"],
                                           self.obj_track.AC_Parameter["ITEMS"],
                                           self.obj_track.DC_Parameter["ITEMS"],
                                           self.obj_track.TRAN_Parameter["ITEMS"],
                                           self.obj_track.AC_type["ITEMS"])
        
        
def main(args):
    print "=================================="
    print "Kicad to Ngspice netlist converter "
    print "=================================="
    global kicadFile,kicadNetlist,schematicInfo
    kicadFile = "/home/fossee/workspace/FreeEDA/Examples/BJT_amplifier/BJT_amplifier.cir"
    #kicadFile = sys.argv[1]
    
    #Object of Processing
    obj_proc = PrcocessNetlist()
    
    # Read the netlist
    kicadNetlist = obj_proc.readNetlist(kicadFile)
    
    # Construct parameter information
    param=obj_proc.readParamInfo(kicadNetlist)
    
    # Replace parameter with values
    netlist,infoline=obj_proc.preprocessNetlist(kicadNetlist,param)
    
    print "NETLIST ",netlist
    print "INFOLINE",infoline
    
    # Separate option and schematic information
    optionInfo, schematicInfo=obj_proc.separateNetlistInfo(netlist)
    
    print "OPTIONINFO",optionInfo
    print "SCHEMATICINFO",schematicInfo
    
    #Getting model and subckt list
    modelList=[]
    subcktList=[]
    modelList,subcktList = obj_proc.getModelSubcktList(schematicInfo,modelList,subcktList)
    
    print "MODEL LIST ",modelList
    print "SUBCKT ",subcktList
        
    #List for storing source and its value
    global sourcelist, sourcelisttrack
    sourcelist=[]
    sourcelisttrack=[]
    schematicInfo,sourcelist=obj_proc.insertSpecialSourceParam(schematicInfo,sourcelist)
    
    print "SOURCELIST",sourcelist
    print "SCHEMATICINFO",schematicInfo
      
    
      
    app = QtGui.QApplication(args)
    #app.setApplicationName("KicadToNgspice")
    #app.setQuitOnLastWindowClosed(True)
    kingWindow = MainWindow()
    kingWindow.show()
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main(sys.argv)
    
    
  
    
    
        
        