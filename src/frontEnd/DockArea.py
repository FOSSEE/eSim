from PyQt4 import QtGui,QtCore
from ngspiceSimulation.pythonPlotting import plotWindow
from ngspiceSimulation.NgspiceWidget import NgspiceWidget
from configuration.Appconfig import Appconfig
from modelEditor.ModelEditor import ModelEditorclass
from subcircuit.Subcircuit import Subcircuit
from kicadtoNgspice.KicadtoNgspice import MainWindow
from browser.Welcome import Welcome
from browser.UserManual import UserManual
from ngspicetoModelica.ModelicaUI import OpenModelicaEditor
import os

dockList = ['Welcome']
count = 1 
dock = {}

class DockArea(QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.obj_appconfig = Appconfig()
         
        for dockName in dockList:
            dock[dockName] = QtGui.QDockWidget(dockName)
            self.welcomeWidget = QtGui.QWidget()
            self.welcomeLayout = QtGui.QVBoxLayout()
            self.welcomeLayout.addWidget(Welcome())  ##Call browser
            
            #Adding to main Layout
            self.welcomeWidget.setLayout(self.welcomeLayout)
            dock[dockName].setWidget(self.welcomeWidget)
            #CSS
            dock[dockName].setStyleSheet(" \
            QWidget { border-radius: 15px; border: 1px solid gray; padding: 5px; width: 200px; height: 150px;  } \
            ")            
            self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock[dockName])  
                    
        #self.tabifyDockWidget(dock['Notes'],dock['Blank'])
        self.show()
    
    '''
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.obj_appconfig = Appconfig()
                
        for dockName in dockList:
            dock[dockName] = QtGui.QDockWidget(dockName)
            self.welcome = QtGui.QTextEdit()
            self.welcome.setReadOnly(True)
            dock[dockName].setWidget(self.welcome)
            #CSS
            dock[dockName].setStyleSheet(" \
            QWidget { border-radius: 15px; border: 1px solid gray; padding: 5px; width: 200px; height: 150px;  } \
            ")            
            self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock[dockName])  
                    
        #self.tabifyDockWidget(dock['Notes'],dock['Blank'])
        self.show()
    '''
             
    def createTestEditor(self):
        """
        This function create widget for Library Editor
        """
        global count
                
        self.testWidget = QtGui.QWidget()
        self.testArea = QtGui.QTextEdit()
        self.testLayout = QtGui.QVBoxLayout()
        self.testLayout.addWidget(self.testArea)
        
        #Adding to main Layout
        self.testWidget.setLayout(self.testLayout)
        dock['Tips-'+str(count)] = QtGui.QDockWidget('Tips-'+str(count))
        dock['Tips-'+str(count)].setWidget(self.testWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock['Tips-'+str(count)])  
        self.tabifyDockWidget(dock['Welcome'],dock['Tips-'+str(count)])
        
        """
        #CSS
        dock['Tips-'+str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray; padding: 5px; width: 200px; height: 150px;  } \
        ")
        """
        
        dock['Tips-'+str(count)].setVisible(True)
        dock['Tips-'+str(count)].setFocus()
        """
        dock['Tips-'+str(count)].setStyleSheet(" \
        :hover { background-color: yellow;  } \
        ")
        """
        dock['Tips-'+str(count)].raise_()

        self.obj_appconfig.dock_dict[self.obj_appconfig.current_project['ProjectName']].append(dock['Tips-'+str(count)])
        count = count + 1
        
    def plottingEditor(self):
        """
        This function create widget for interactive PythonPlotting
        """
        self.projDir = self.obj_appconfig.current_project["ProjectName"]
        self.projName = os.path.basename(self.projDir)
        #self.project = os.path.join(self.projDir,self.projName)
        
        
        global count
        self.plottingWidget = QtGui.QWidget()
                
        self.plottingLayout = QtGui.QVBoxLayout()
        self.plottingLayout.addWidget(plotWindow(self.projDir,self.projName))
        
        #Adding to main Layout
        self.plottingWidget.setLayout(self.plottingLayout)
        dock['Plotting-'+str(count)] = QtGui.QDockWidget('Plotting-'+str(count))
        dock['Plotting-'+str(count)].setWidget(self.plottingWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock['Plotting-'+str(count)])  
        self.tabifyDockWidget(dock['Welcome'],dock['Plotting-'+str(count)])
        
        """
        #CSS
        dock['Plotting-'+str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray; padding: 5px; width: 200px; height: 150px;  } \
        ")
        """
        dock['Plotting-'+str(count)].setVisible(True)
        dock['Plotting-'+str(count)].setFocus()
        dock['Plotting-'+str(count)].raise_()

        self.obj_appconfig.dock_dict[self.obj_appconfig.current_project['ProjectName']].append(dock['Plotting-'+str(count)])
        count = count + 1
        
    def ngspiceEditor(self,projDir):
        """
        This function creates widget for NgSpice window
        """
        
        
        self.projDir = projDir
        self.projName = os.path.basename(self.projDir)
        self.ngspiceNetlist = os.path.join(self.projName+".cir.out")
        
               
        
        global count
        self.ngspiceWidget = QtGui.QWidget()
                
        self.ngspiceLayout = QtGui.QVBoxLayout()
        self.ngspiceLayout.addWidget(NgspiceWidget(self.ngspiceNetlist,self.projDir))
        
        #Adding to main Layout
        self.ngspiceWidget.setLayout(self.ngspiceLayout)
        dock['NgSpice-'+str(count)] = QtGui.QDockWidget('NgSpice-'+str(count))
        dock['NgSpice-'+str(count)].setWidget(self.ngspiceWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock['NgSpice-'+str(count)])  
        self.tabifyDockWidget(dock['Welcome'],dock['NgSpice-'+str(count)])

        #CSS
        dock['NgSpice-'+str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray; padding: 0px; width: 200px; height: 150px;  } \
        ")
        
        dock['NgSpice-'+str(count)].setVisible(True)
        dock['NgSpice-'+str(count)].setFocus()
        dock['NgSpice-'+str(count)].raise_()
        self.obj_appconfig.dock_dict[self.obj_appconfig.current_project['ProjectName']].append(dock['NgSpice-'+str(count)])
        count = count + 1

    def modelEditor(self):    
            print"in model editor"
            global count
            self.modelwidget = QtGui.QWidget() 
            
            self.modellayout = QtGui.QVBoxLayout()
            self.modellayout.addWidget(ModelEditorclass())
            
            #Adding to main Layout
            self.modelwidget.setLayout(self.modellayout)
            
            dock['Model Editor-'+str(count)] = QtGui.QDockWidget('Model Editor-'+str(count))
            dock['Model Editor-'+str(count)].setWidget(self.modelwidget)
            self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock['Model Editor-'+str(count)])  
            self.tabifyDockWidget(dock['Welcome'],dock['Model Editor-'+str(count)])
            
            #CSS
            dock['Model Editor-'+str(count)].setStyleSheet(" \
            .QWidget { border-radius: 15px; border: 1px solid gray; padding: 5px; width: 200px; height: 150px;  } \
            ")
            
            dock['Model Editor-'+str(count)].setVisible(True)
            dock['Model Editor-'+str(count)].setFocus()
            dock['Model Editor-'+str(count)].raise_()

            self.obj_appconfig.dock_dict[self.obj_appconfig.current_project['ProjectName']].append(dock['Model Editor-'+str(count)])
            count = count + 1
    
    def kicadToNgspiceEditor(self,clarg1,clarg2=None):
        global count
        self.kicadToNgspiceWidget=QtGui.QWidget()
        self.kicadToNgspiceLayout=QtGui.QVBoxLayout()
        self.kicadToNgspiceLayout.addWidget(MainWindow(clarg1,clarg2))
        
        self.kicadToNgspiceWidget.setLayout(self.kicadToNgspiceLayout)
        dock['kicadToNgspice-'+str(count)] = QtGui.QDockWidget('kicadToNgspice-'+str(count))
        dock['kicadToNgspice-'+str(count)].setWidget(self.kicadToNgspiceWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock['kicadToNgspice-'+str(count)])  
        self.tabifyDockWidget(dock['Welcome'],dock['kicadToNgspice-'+str(count)])
        
        #CSS
        dock['kicadToNgspice-'+str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray; padding: 5px; width: 200px; height: 150px;  } \
        ")
        
        dock['kicadToNgspice-'+str(count)].setVisible(True)
        dock['kicadToNgspice-'+str(count)].setFocus()
        dock['kicadToNgspice-'+str(count)].raise_()

        self.obj_appconfig.dock_dict[self.obj_appconfig.current_project['ProjectName']].append(dock['kicadToNgspice-'+str(count)])
        count = count + 1
        
        
    def subcircuiteditor(self):
        """
        This function creates a widget for different subcircuit options
        """
        
        global count
        self.subcktWidget=QtGui.QWidget()
        self.subcktLayout=QtGui.QVBoxLayout()
        self.subcktLayout.addWidget(Subcircuit(self))
        
        self.subcktWidget.setLayout(self.subcktLayout)
        dock['Subcircuit-'+str(count)] = QtGui.QDockWidget('Subcircuit-'+str(count))
        dock['Subcircuit-'+str(count)].setWidget(self.subcktWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock['Subcircuit-'+str(count)])  
        self.tabifyDockWidget(dock['Welcome'],dock['Subcircuit-'+str(count)])
        
        #CSS
        dock['Subcircuit-'+str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray; padding: 5px; width: 200px; height: 150px;  } \
        ")
        
        dock['Subcircuit-'+str(count)].setVisible(True)
        dock['Subcircuit-'+str(count)].setFocus()
        dock['Subcircuit-'+str(count)].raise_()

        self.obj_appconfig.dock_dict[self.obj_appconfig.current_project['ProjectName']].append(dock['Subcircuit-'+str(count)])
        count = count + 1
    
    def usermanual(self):
        """
        This function creates a widget for different subcircuit options
        """
        
        global count
        self.usermanualWidget=QtGui.QWidget()
        self.usermanualLayout=QtGui.QVBoxLayout()
        self.usermanualLayout.addWidget(UserManual())
        
        self.usermanualWidget.setLayout(self.usermanualLayout)
        dock['User Manual-'+str(count)] = QtGui.QDockWidget('User Manual-'+str(count))
        dock['User Manual-'+str(count)].setWidget(self.usermanualWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock['User Manual-'+str(count)])  
        self.tabifyDockWidget(dock['Welcome'],dock['User Manual-'+str(count)])
        
        #CSS
        dock['User Manual-'+str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray; padding: 5px; width: 200px; height: 150px;  } \
        ")
        
        dock['User Manual-'+str(count)].setVisible(True)
        dock['User Manual-'+str(count)].setFocus()
        dock['User Manual-'+str(count)].raise_()
        
        count = count + 1

    def modelicaEditor(self, projDir):
        """
        This function sets up the UI for ngspice to modelica conversion
        """

        global count
        self.modelicaWidget = QtGui.QWidget()
        self.modelicaLayout = QtGui.QVBoxLayout()
        self.modelicaLayout.addWidget(OpenModelicaEditor(projDir))

        self.modelicaWidget.setLayout(self.modelicaLayout)
        dock['Modelica-'+str(count)] = QtGui.QDockWidget('Modelica-'+str(count))
        dock['Modelica-'+str(count)].setWidget(self.modelicaWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock['Modelica-'+str(count)])
        self.tabifyDockWidget(dock['Welcome'],dock['Modelica-'+str(count)])

        dock['Modelica-'+str(count)].setVisible(True)
        dock['Modelica-'+str(count)].setFocus()
        dock['Modelica-'+str(count)].raise_()

        #CSS
        dock['Modelica-'+str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray; padding: 5px; width: 200px; height: 150px;  } \
        ")

        self.obj_appconfig.dock_dict[self.obj_appconfig.current_project['ProjectName']].append(dock['Modelica-'+str(count)])

        count = count + 1

    def closeDock   (self):
        for dockwidget in self.obj_appconfig.dock_dict[self.obj_appconfig.current_project['ProjectName']]:
            dockwidget.close()
