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
import DeviceModel
import Convert
import TrackWidget

from xml.etree import ElementTree as ET



class MainWindow(QtGui.QWidget):
    """
    This class create KicadtoNgspice window. 
    And Call Convert function if convert button is pressed.
    The convert function takes all the value entered by user and create a final netlist "*.cir.out".
    This final netlist is compatible with NgSpice.  
    """
    def __init__(self):
        QtGui.QWidget.__init__(self)
        #Create object of track widget
        self.obj_track = TrackWidget.TrackWidget()
        """
        Checking if any unknown model is used in schematic which is not recognized by NgSpice.
        Also if the two model of same name is present under modelParamXML directory
        """           
        if unknownModelList:
            print "Unknown Model List is : ",unknownModelList
            self.msg = QtGui.QErrorMessage()
            self.content = "Your schematic contain unknown model "+', '.join(unknownModelList)
            self.msg.showMessage(self.content)
            self.msg.setWindowTitle("Unknown Models")
            
        elif multipleModelList:
            print "Multiple Model List is : ",multipleModelList
            self.msg = QtGui.QErrorMessage()
            self.mcontent = "Look like you have duplicate model in modelParamXML directory "+', '.join(multipleModelList[0])
            self.msg.showMessage(self.mcontent)
            self.msg.setWindowTitle("Multiple Models")
                
        else:
            self.createMainWindow()
           
             
    def createMainWindow(self):
        """
        This function create main window of Kicad to Ngspice converter
        """
        
        self.grid = QtGui.QGridLayout(self)
        self.convertbtn = QtGui.QPushButton("Convert")
        self.convertbtn.clicked.connect(self.callConvert)
        self.cancelbtn = QtGui.QPushButton("Cancel")
        self.cancelbtn.clicked.connect(self.close)
        self.grid.addWidget(self.createcreateConvertWidget(),0,0)
        self.grid.addWidget(self.convertbtn,1,1)
        self.grid.addWidget(self.cancelbtn,1,2)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setLayout(self.grid)
        self.setWindowTitle("Kicad To NgSpice Converter")
        self.show()
          
    
    def createcreateConvertWidget(self):
        global obj_analysis
        self.convertWindow = QtGui.QWidget()
        self.analysisTab = QtGui.QScrollArea()
        obj_analysis=Analysis.Analysis()
        self.analysisTab.setWidget(obj_analysis)
        #self.analysisTabLayout = QtGui.QVBoxLayout(self.analysisTab.widget())
        self.analysisTab.setWidgetResizable(True)
        global obj_source
        self.sourceTab = QtGui.QScrollArea()
        obj_source=Source.Source(sourcelist,sourcelisttrack)
        self.sourceTab.setWidget(obj_source)
        #self.sourceTabLayout = QtGui.QVBoxLayout(self.sourceTab.widget())
        self.sourceTab.setWidgetResizable(True)
        global obj_model
        self.modelTab = QtGui.QScrollArea()
        obj_model=Model.Model(schematicInfo,modelList)
        self.modelTab.setWidget(obj_model)
        #self.modelTabLayout = QtGui.QVBoxLayout(self.modelTab.widget())
        self.modelTab.setWidgetResizable(True)
        global obj_devicemodel
        self.deviceModelTab = QtGui.QScrollArea()
        obj_devicemodel=DeviceModel.DeviceModel(schematicInfo)
        self.deviceModelTab.setWidget(obj_devicemodel)
        self.deviceModelTab.setWidgetResizable(True)
        
        

        self.tabWidget = QtGui.QTabWidget()
        #self.tabWidget.TabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.addTab(self.analysisTab,"Analysis")
        self.tabWidget.addTab(self.sourceTab,"Source Details")
        self.tabWidget.addTab(self.modelTab,"NgSpice Model")
        self.tabWidget.addTab(self.deviceModelTab,"Device Modeling")
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
        kicadFile = sys.argv[1]
        (projpath,filename)=os.path.split(kicadFile)
        project_name=projpath.split("/")
        project_name=project_name[len(project_name)-1]
        print "PROJ PATH---",projpath
        
        
        check=1
        try:
            fr=open(os.path.join(projpath,project_name+"_Previous_Values.xml"),'r')
            temp_tree=ET.parse(fr)
            temp_root=temp_tree.getroot()
        except:
            check=0
            
        
        
        fw=open(os.path.join(projpath,project_name+"_Previous_Values.xml"),'w')
        if check==0:
            attr_parent=ET.Element("KicadtoNgspice")
        if check==1:
            attr_parent=temp_root  
        
        for child in attr_parent:
            if child.tag=="analysis":
                attr_parent.remove(child)
        
        attr_analysis=ET.SubElement(attr_parent,"analysis")
        attr_ac=ET.SubElement(attr_analysis,"ac")
        if obj_analysis.Lin.isChecked():
            ET.SubElement(attr_ac,"field1",name="Lin").text="true"
            ET.SubElement(attr_ac,"field2",name="Dec").text="false"
            ET.SubElement(attr_ac,"field3",name="Oct").text="false"
        elif obj_analysis.Dec.isChecked():
            ET.SubElement(attr_ac,"field1",name="Lin").text="false"
            ET.SubElement(attr_ac,"field2",name="Dec").text="true"
            ET.SubElement(attr_ac,"field3",name="Oct").text="false"
        if obj_analysis.Oct.isChecked():
            ET.SubElement(attr_ac,"field1",name="Lin").text="false"
            ET.SubElement(attr_ac,"field2",name="Dec").text="false"
            ET.SubElement(attr_ac,"field3",name="Oct").text="true"
        else:
            pass
        ET.SubElement(attr_ac,"field4",name="Start Frequency").text= str(obj_analysis.ac_entry_var[0].text())
        ET.SubElement(attr_ac,"field5",name="Stop Frequency").text= str(obj_analysis.ac_entry_var[1].text())
        ET.SubElement(attr_ac,"field6",name="No. of points").text= str(obj_analysis.ac_entry_var[2].text())
        ET.SubElement(attr_ac,"field7",name="Start Fre Combo").text= obj_analysis.ac_parameter[0]
        ET.SubElement(attr_ac,"field8",name="Stop Fre Combo").text= obj_analysis.ac_parameter[1]
        attr_dc=ET.SubElement(attr_analysis,"dc")
        ET.SubElement(attr_dc,"field1",name="Source Name").text= str(obj_analysis.dc_entry_var[0].text())
        ET.SubElement(attr_dc,"field2",name="Start").text= str(obj_analysis.dc_entry_var[1].text())
        ET.SubElement(attr_dc,"field3",name="Increment").text= str(obj_analysis.dc_entry_var[2].text())
        ET.SubElement(attr_dc,"field4",name="Stop").text= str(obj_analysis.dc_entry_var[3].text())
        ET.SubElement(attr_dc,"field5",name="Operating Point").text=str(obj_analysis.check.isChecked()) 		
        print "OBJ_ANALYSIS.CHECK -----",obj_analysis.check.isChecked()
        ET.SubElement(attr_dc,"field6",name="Start Combo").text= obj_analysis.dc_parameter[0]
        ET.SubElement(attr_dc,"field7",name="Increment Combo").text=obj_analysis.dc_parameter[1]
        ET.SubElement(attr_dc,"field8",name="Stop Combo").text= obj_analysis.dc_parameter[2]
        attr_tran=ET.SubElement(attr_analysis,"tran")
        ET.SubElement(attr_tran,"field1",name="Start Time").text= str(obj_analysis.tran_entry_var[0].text())
        ET.SubElement(attr_tran,"field2",name="Step Time").text= str(obj_analysis.tran_entry_var[1].text())
        ET.SubElement(attr_tran,"field3",name="Stop Time").text= str(obj_analysis.tran_entry_var[2].text())
        ET.SubElement(attr_tran,"field4",name="Start Combo").text= obj_analysis.tran_parameter[0]
        ET.SubElement(attr_tran,"field5",name="Step Combo").text= obj_analysis.tran_parameter[1]
        ET.SubElement(attr_tran,"field6",name="Stop Combo").text= obj_analysis.tran_parameter[2]
        print "TRAN PARAMETER 2-----",obj_analysis.tran_parameter[2]
        
        #tree=ET.ElementTree(attr_analysis)
        #tree.write(f)
        
        
        if check==0:
            attr_source=ET.SubElement(attr_parent,"source")
        if check==1:
            for child in attr_parent:
                if child.tag=="source":
                    attr_source=child  
        count=1
        grand_child_count=1
        #global tmp_check
        #tmp_check=0
        for i in schematicInfo:
            tmp_check=0
            words=i.split(' ')
            wordv=words[0]
            for child in attr_source:
                if child.tag==wordv and child.text==words[len(words)-1]:
                    tmp_check=1
                    for grand_child in child:
                        grand_child.text=str(obj_source.entry_var[grand_child_count].text())
                        grand_child_count=grand_child_count+1
                    grand_child_count=grand_child_count+1
            if tmp_check==0:        
                words=i.split(' ')
                wordv=words[0]
                if wordv[0]=="v":
                    attr_var=ET.SubElement(attr_source,words[0],name="Source type")
                    attr_var.text=words[len(words)-1]
                    #ET.SubElement(attr_ac,"field1",name="Lin").text="true"    
                if words[len(words)-1]=="ac":
                    #attr_ac=ET.SubElement(attr_var,"ac")
                    ET.SubElement(attr_var,"field1",name="Amplitude").text=str(obj_source.entry_var[count].text())
                    count=count+2
                elif words[len(words)-1]=="dc":
                    #attr_dc=ET.SubElement(attr_var,"dc")
                    ET.SubElement(attr_var,"field1",name="Value").text=str(obj_source.entry_var[count].text())
                    count=count+2
                elif words[len(words)-1]=="sine":
                    #attr_sine=ET.SubElement(attr_var,"sine")
                    ET.SubElement(attr_var,"field1",name="Offset Value").text=str(obj_source.entry_var[count].text())
                    count=count+1
                    ET.SubElement(attr_var,"field2",name="Amplitude").text=str(obj_source.entry_var[count].text())
                    count=count+1
                    ET.SubElement(attr_var,"field3",name="Frequency").text=str(obj_source.entry_var[count].text())
                    count=count+1
                    ET.SubElement(attr_var,"field4",name="Delay Time").text=str(obj_source.entry_var[count].text())    
                    count=count+1
                    ET.SubElement(attr_var,"field5",name="Damping Factor").text=str(obj_source.entry_var[count].text())
                    count=count+2
                elif words[len(words)-1]=="pulse":
                    #attr_pulse=ET.SubElement(attr_var,"pulse")
                    ET.SubElement(attr_var,"field1",name="Initial Value").text=str(obj_source.entry_var[count].text())
                    count=count+1
                    ET.SubElement(attr_var,"field2",name="Pulse Value").text=str(obj_source.entry_var[count].text())
                    count=count+1
                    ET.SubElement(attr_var,"field3",name="Delay Time").text=str(obj_source.entry_var[count].text())
                    count=count+1
                    ET.SubElement(attr_var,"field4",name="Rise Time").text=str(obj_source.entry_var[count].text())    
                    count=count+1
                    ET.SubElement(attr_var,"field5",name="Fall Time").text=str(obj_source.entry_var[count].text())
                    count=count+1
                    ET.SubElement(attr_var,"field5",name="Pulse width").text=str(obj_source.entry_var[count].text())
                    count=count+1
                    ET.SubElement(attr_var,"field5",name="Period").text=str(obj_source.entry_var[count].text())
                    count=count+2
                elif words[len(words)-1]=="pwl":
                    #attr_pwl=ET.SubElement(attr_var,"pwl")
                    ET.SubElement(attr_var,"field1",name="Enter in pwl format").text=str(obj_source.entry_var[count].text())
                    count=count+2
                elif words[len(words)-1]=="exp":
                    #attr_exp=ET.SubElement(attr_var,"exp")
                    ET.SubElement(attr_var,"field1",name="Initial Value").text=str(obj_source.entry_var[count].text())
                    count=count+1
                    ET.SubElement(attr_var,"field2",name="Pulsed Value").text=str(obj_source.entry_var[count].text())
                    count=count+1
                    ET.SubElement(attr_var,"field3",name="Rise Delay Time").text=str(obj_source.entry_var[count].text())
                    count=count+1
                    ET.SubElement(attr_var,"field4",name="Rise Time Constant").text=str(obj_source.entry_var[count].text())
                    count=count+1
                    ET.SubElement(attr_var,"field5",name="Fall TIme").text=str(obj_source.entry_var[count].text())
                    count=count+1
                    ET.SubElement(attr_var,"field6",name="Fall Time Constant").text=str(obj_source.entry_var[count].text())
                    count=count+2
                else:
                    pass
                
        #tree=ET.ElementTree(attr_source)
        #tree.write(f1)
        
        
        
        if check==0:
            attr_model=ET.SubElement(attr_parent,"model")
        if check==1:
            for child in attr_parent:
                if child.tag=="model":
                    attr_model=child
        i=0    
        #tmp_check is a variable to check for duplicates in the xml file
        tmp_check=0
        #tmp_i is the iterator in case duplicates are there; then in that case we need to replace only the child node and not create a new parent node
        
        for line in modelList:
            print "i for each line in model List------",i
            tmp_check=0
            for rand_itr in obj_model.obj_trac.modelTrack:
                if rand_itr[2]==line[2] and rand_itr[3]==line[3]:
                    start=rand_itr[7]
                    end=rand_itr[8]
            i=start
            for child in attr_model:
                if child.text==line[2] and child.tag==line[3]:
                    for grand_child in child:
                        if i<=end:
                            grand_child.text=str(obj_model.obj_trac.model_entry_var[i].text())
                            print "STR OF MODEL----",str(obj_model.obj_trac.model_entry_var[i].text())
                            i=i+1
                            print "i incremented to ",i
                        else:
                            pass
                    tmp_check=1    
                        
            if tmp_check==0:
                attr_ui=ET.SubElement(attr_model,line[3],name="type")
                attr_ui.text=line[2]    
                for key,value in line[7].iteritems():
                    if hasattr(value, '__iter__') and i<=end:
                        for item in value:
                            ET.SubElement(attr_ui,"field"+str(i+1),name=item).text=str(obj_model.obj_trac.model_entry_var[i].text())
                            print "STR OF MODEL----",str(obj_model.obj_trac.model_entry_var[i].text())
                            i=i+1
                            print "i incremented to ",i
                    else:
                        ET.SubElement(attr_ui,"field"+str(i+1),name=value).text=str(obj_model.obj_trac.model_entry_var[i].text())
                        print "STR OF MODEL----",str(obj_model.obj_trac.model_entry_var[i].text())
                        i=i+1
                        print "i incremented to ",i
        #################################################################################################################
        if check==0:
            attr_devicemodel=ET.SubElement(attr_parent,"devicemodel")
        if check==1:
            for child in attr_parent:
                if child.tag=="devicemodel":
                    attr_devicemodel=child
        print "Device model dict",obj_devicemodel.devicemodel_dict_beg
        print "Device model dict end",obj_devicemodel.devicemodel_dict_end
        ##########################              
        for i in obj_devicemodel.devicemodel_dict_beg:
            attr_var=ET.SubElement(attr_devicemodel,i)
            it=obj_devicemodel.devicemodel_dict_beg[i]
            end=obj_devicemodel.devicemodel_dict_end[i]
            while it<=end:
                ET.SubElement(attr_var,"field").text=str(obj_devicemodel.entry_var[it].text())
                it=it+1
        #####################################    
             
        """keys=obj_devicemodel.devicemodel_dict.keys()
        n=len(keys)
        for i in range(n):
            thisKey=keys[i]
            nextKey=keys[(i+1)%n]
            nextValue=obj_devicemodel.devicemodel_dict[nextKey]
            attr_var=ET.SubElement(attr_devicemodel,thisKey)
            it=obj_devicemodel.devicemodel_dict[thisKey]
            while it<=nextValue:
                ET.SubElement(attr_var,"field").text=obj_devicemodel.entry_var[it]"""
                
        ###################################################################################################################   
        
        
        tree=ET.ElementTree(attr_parent)
        tree.write(fw)
        
                    
        self.obj_convert = Convert.Convert(self.obj_track.sourcelisttrack["ITEMS"],
                                           self.obj_track.source_entry_var["ITEMS"],
                                           schematicInfo)
        
        try:
            #Adding Source Value to Schematic Info
            schematicInfo = self.obj_convert.addSourceParameter()
            
            #Adding Model Value to schematicInfo
            schematicInfo = self.obj_convert.addModelParameter(schematicInfo)
            
            #Adding Device Library to SchematicInfo
            schematicInfo = self.obj_convert.addDeviceLibrary(schematicInfo,kicadFile)
            
              
            analysisoutput = self.obj_convert.analysisInsertor(self.obj_track.AC_entry_var["ITEMS"],
                                                               self.obj_track.DC_entry_var["ITEMS"],
                                                               self.obj_track.TRAN_entry_var["ITEMS"],
                                                               self.obj_track.set_CheckBox["ITEMS"],
                                                               self.obj_track.AC_Parameter["ITEMS"],
                                                               self.obj_track.DC_Parameter["ITEMS"],
                                                               self.obj_track.TRAN_Parameter["ITEMS"],
                                                               self.obj_track.AC_type["ITEMS"])
            #print "SchematicInfo after adding Model Details",schematicInfo
            
            #Calling netlist file generation function
            self.createNetlistFile(schematicInfo)
            
            self.msg = "The Kicad to Ngspice Conversion completed successfully!!!!!!"
            QtGui.QMessageBox.information(self, "Information", self.msg, QtGui.QMessageBox.Ok)
            self.close()         
        except Exception as e:
            print "Exception Message: ",e
            print "There was error while converting kicad to ngspice"
            self.close()
            
    
      
    
    def createNetlistFile(self,schematicInfo):
        print "Creating Final netlist"
        #print "INFOLINE",infoline
        #print "OPTIONINFO",optionInfo
        #print "Device MODEL LIST ",devicemodelList
        #print "SUBCKT ",subcktList
        #print "OUTPUTOPTION",outputOption
        #print "KicadfIle",kicadFile
        
        #checking if analysis files is present
        (projpath,filename) = os.path.split(kicadFile)
        analysisFileLoc = os.path.join(projpath,"analysis")
        #print "Analysis File Location",analysisFileLoc
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
                
        #print "Option Info",optionInfo
        analysisOption = []
        initialCondOption=[]
        simulatorOption =[]
        #includeOption=[]  #Don't know why to use it
        #model = []      #Don't know why to use it
        
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
            #elif (option=='.include' or option=='.lib'):
            #    includeOption.append(eachline+'\n')
            #elif (option=='.model'):
            #    model.append(eachline+'\n')
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
        
   
                   
            
#Main Function
        
def main(args):
    print "=================================="
    print "Kicad to Ngspice netlist converter "
    print "=================================="
    global kicadFile,kicadNetlist,schematicInfo
    global infoline,optionInfo
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
    
           
    #List for storing source and its value
    global sourcelist, sourcelisttrack
    sourcelist=[]
    sourcelisttrack=[]
    schematicInfo,sourcelist = obj_proc.insertSpecialSourceParam(schematicInfo,sourcelist)
    
    print "SOURCELIST",sourcelist
    print "SCHEMATICINFO",schematicInfo
    
    #List storing model detail
    global modelList,outputOption,unknownModelList,multipleModelList
      
    modelList = [] 
    outputOption = []
    schematicInfo,outputOption,modelList,unknownModelList,multipleModelList = obj_proc.convertICintoBasicBlocks(schematicInfo,outputOption,modelList)
    print "Unknown Model List",unknownModelList  
    print "Multiple Model List",multipleModelList
    print "Model List",modelList
    
   
    app = QtGui.QApplication(args)
    kingWindow = MainWindow()
    #kingWindow.show()  #No need to call show as we are doing it in createMainWindow
    sys.exit(app.exec_())
     

   
if __name__ == '__main__':
    main(sys.argv)
    
    
  
    
    
        
        