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
from PyQt4 import QtGui,QtCore
from Processing import PrcocessNetlist
import Analysis
import Source
import Model
import Convert
import TrackWidget



class MainWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        #Create object of track widget
        self.obj_track = TrackWidget.TrackWidget()
         
        print "Init Kicad to Ngspice"             
        #print "Current Project",sys.argv[1]
        
            
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
        #self.analysisTabLayout = QtGui.QVBoxLayout(self.analysisTab.widget())
        self.analysisTab.setWidgetResizable(True)
        
        self.sourceTab = QtGui.QScrollArea()
        self.sourceTab.setWidget(Source.Source(sourcelist,sourcelisttrack))
        #self.sourceTabLayout = QtGui.QVBoxLayout(self.sourceTab.widget())
        self.sourceTab.setWidgetResizable(True)
        
        self.modelTab = QtGui.QScrollArea()
        self.modelTab.setWidget(Model.Model())
        #self.modelTabLayout = QtGui.QVBoxLayout(self.modelTab.widget())
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
        self.obj_convert = Convert.Convert(self.obj_track.sourcelisttrack["ITEMS"],
                                           self.obj_track.source_entry_var["ITEMS"],
                                           schematicInfo)
        
        #Adding Source Value to Schematic Info
        schematicInfo = self.obj_convert.addSourceParameter()
        #print "Schematic After adding source parameter",schematicInfo
        schematicInfo = self.obj_convert.addModelParameter(schematicInfo)
          
        
 
    
        
def main(args):
    print "=================================="
    print "Kicad to Ngspice netlist converter "
    print "=================================="
    global kicadFile,kicadNetlist,schematicInfo
    #kicadFile = "/home/fahim/eSim-Workspace/BJT_amplifier/BJT_amplifier.cir"
    kicadFile = sys.argv[1]
    
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
    devicemodelList=[]
    subcktList=[]
    devicemodelList,subcktList = obj_proc.getModelSubcktList(schematicInfo,devicemodelList,subcktList)
    
    print "MODEL LIST ",devicemodelList
    print "SUBCKT ",subcktList
        
    #List for storing source and its value
    global sourcelist, sourcelisttrack
    sourcelist=[]
    sourcelisttrack=[]
    schematicInfo,sourcelist = obj_proc.insertSpecialSourceParam(schematicInfo,sourcelist)
    
    print "SOURCELIST",sourcelist
    print "SCHEMATICINFO",schematicInfo
    
    #List storing model detail
    global modelList,outputOption
    modelList = [] 
    outputOption = []
    schematicInfo,outputOption,modelList,unknownModelList,multipleModelList = obj_proc.convertICintoBasicBlocks(schematicInfo,outputOption,modelList)
    print "Unknown Model List",unknownModelList  
    print "Multple Model List",multipleModelList
    

    
    #Checking for unknown Model List and Multiple Model List
    if unknownModelList:
        print "ErrorMessage : These Models are not available.Please check it",unknownModelList
        sys.exit(2)
    else:
        if multipleModelList:
            print "ErrorMessage: There are multiple model for same name. Please check it",multipleModelList
            sys.exit(2)
        else:
            pass
    
    app = QtGui.QApplication(args)
    #app.setApplicationName("KicadToNgspice")
    #app.setQuitOnLastWindowClosed(True)
    kingWindow = MainWindow()
    kingWindow.show()
    sys.exit(app.exec_())
      
    
    

   
if __name__ == '__main__':
    main(sys.argv)
    
    
  
    
    
        
        