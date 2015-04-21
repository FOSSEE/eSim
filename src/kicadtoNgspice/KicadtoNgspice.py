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
        self.modelTab.setWidget(Model.Model(schematicInfo,modelList))
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
        global analysisoutput
        self.obj_convert = Convert.Convert(self.obj_track.sourcelisttrack["ITEMS"],
                                           self.obj_track.source_entry_var["ITEMS"],
                                           schematicInfo)
        
        try:
            #Adding Source Value to Schematic Info
            schematicInfo = self.obj_convert.addSourceParameter()
            
            #Adding Model Value to schematic Info
            schematicInfo = self.obj_convert.addModelParameter(schematicInfo)
            
            analysisoutput = self.obj_convert.analysisInsertor(self.obj_track.AC_entry_var["ITEMS"],
                                                               self.obj_track.DC_entry_var["ITEMS"],
                                                               self.obj_track.TRAN_entry_var["ITEMS"],
                                                               self.obj_track.set_CheckBox["ITEMS"],
                                                               self.obj_track.AC_Parameter["ITEMS"],
                                                               self.obj_track.DC_Parameter["ITEMS"],
                                                               self.obj_track.TRAN_Parameter["ITEMS"],
                                                               self.obj_track.AC_type["ITEMS"])
            print "SchematicInfo after adding Model Details",schematicInfo
            #Calling netlist file generation function
            self.createNetlistFile()
            self.msg = "The Kicad to Ngspice Conversion completed successfully!!!!!!"
            QtGui.QMessageBox.information(self, "Information", self.msg, QtGui.QMessageBox.Ok)
            self.close()         
        except Exception as e:
            print "Exception Message: ",e
            print "SchematicInfo after adding Model Details",schematicInfo
            print "There was error while converting kicad to ngspice"
            self.close()
            
    
      
    
    def createNetlistFile(self):
        print "Creating Final netlist"
        print "INFOLINE",infoline
        print "OPTIONINFO",optionInfo
        print "Device MODEL LIST ",devicemodelList
        print "SUBCKT ",subcktList
        print "OUTPUTOPTION",outputOption
        print "KicadfIle",kicadFile
        
        #checking if analysis files is present
        (filepath,filename) = os.path.split(kicadFile)
        analysisFileLoc = os.path.join(filepath,"analysis")
        print "FilePath",filepath
        print "FileName",filename
        print "Analysis File Location",analysisFileLoc
        if os.path.exists(analysisFileLoc):
            try:
                f = open(analysisFileLoc)
                #Read data
                data = f.read()
                # Close the file
                f.close()

            except :
                print "Error While opening Project Analysis file. Please check it"
                sys.exit()
        else:
            print analysisFileLoc + " does not exist"
            sys.exit()
            
        #Adding analysis file info to optionInfo
        analysisData=data.splitlines()
        for eachline in analysisData:
            eachline=eachline.strip()
            if len(eachline)>1:
                if eachline[0]=='.':
                    optionInfo.append(eachline)
                else:
                    pass
                
        print "Option Info",optionInfo
        analysisOption = []
        initialCondOption=[]
        simulatorOption =[]
        includeOption=[]  #Don't know why to use it
        model = []      #Don't know why to use it
        
        for eachline in optionInfo:
            words=eachline.split()
            option=words[0]
            if (option=='.ac' or option=='.dc' or option=='.disto' or option=='.noise' or
                option=='.op' or option=='.pz' or option=='.sens' or option=='.tf' or
                option=='.tran'):
                analysisOption.append(eachline+'\n')
                
            elif (option=='.save' or option=='.print' or option=='.plot' or option=='.four'):
                eachline=eachline.strip('.')
                outputOption.append(eachline+'\n')
            elif (option=='.nodeset' or option=='.ic'):  
                initialCondOption.append(eachline+'\n')
            elif option=='.option':  
                simulatorOption.append(eachline+'\n')
            elif (option=='.include' or option=='.lib'):
                includeOption.append(eachline+'\n')
            elif (option=='.model'):
                model.append(eachline+'\n')
            elif option=='.end':
                continue;
            
            
        #Start creating final netlist cir.out file
        outfile = kicadFile+".out"
        out=open(outfile,"w")
        out.writelines(infoline)
        out.writelines('\n')
        sections=[simulatorOption, initialCondOption, schematicInfo, analysisOption]
        print "SECTIONS",sections
        for section in sections:
            if len(section) == 0:
                continue
            else:
                for line in section:
                    out.writelines('\n') 
                    out.writelines(line)
        
        out.writelines('\n* Control Statements \n')
        out.writelines('.control\n')
        out.writelines('run\n')
        #out.writelines(outputOption)
        out.writelines('print allv > plot_data_v.txt\n')
        out.writelines('print alli > plot_data_i.txt\n')
        out.writelines('.endc\n')
        out.writelines('.end\n')
        
        out.close()
        
   
        
                
            
    
        
def main(args):
    print "=================================="
    print "Kicad to Ngspice netlist converter "
    print "=================================="
    global kicadFile,kicadNetlist,schematicInfo
    global infoline,optionInfo
    #kicadFile = "/home/fahim/eSim-Workspace/BJT_amplifier/BJT_amplifier.cir"
    kicadFile = sys.argv[1]
    
    #Object of Processing
    obj_proc = PrcocessNetlist()
    
    # Read the netlist
    kicadNetlist = obj_proc.readNetlist(kicadFile)
    
    # Construct parameter information
    param = obj_proc.readParamInfo(kicadNetlist)
    
    # Replace parameter with values
    netlist,infoline = obj_proc.preprocessNetlist(kicadNetlist,param)
    
    print "NETLIST ",netlist
    print "INFOLINE",infoline
    
    # Separate option and schematic information
    optionInfo, schematicInfo = obj_proc.separateNetlistInfo(netlist)
    
    print "OPTIONINFO",optionInfo
    print "SCHEMATICINFO",schematicInfo
    
    #Getting model and subckt list
    global devicemodelList,subcktList
    devicemodelList = []
    subcktList = []
    devicemodelList,subcktList = obj_proc.getModelSubcktList(schematicInfo,devicemodelList,subcktList)
    
    print "Device MODEL LIST ",devicemodelList
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
    print "Multiple Model List",multipleModelList
    print "Model List",modelList
    

    
    #Checking for unknown Model List and Multiple Model List
    if unknownModelList:
        print "ErrorMessage : These Models are not available.Please check it",unknownModelList
        sys.exit(2)
    else:
        if multipleModelList:
            print "ErrorMessage: There are multiple model of same name. Please check it",multipleModelList
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
    
    
  
    
    
        
        