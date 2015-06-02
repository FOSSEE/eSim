from PyQt4 import QtGui,QtCore
from ngspiceSimulation.pythonPlotting import plotWindow
from ngspiceSimulation.NgspiceWidget import NgspiceWidget
from configuration.Appconfig import Appconfig
from modelEditor.ModelEditor import ModelEditorclass
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
            dock[dockName].setWidget(QtGui.QTextEdit())
            #CSS
            dock[dockName].setStyleSheet(" \
            QWidget { border-radius: 15px; border: 1px solid gray; padding: 5px; width: 200px; height: 150px;  } \
            ")            
            self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock[dockName])  
                    
        #self.tabifyDockWidget(dock['Notes'],dock['Blank'])
        self.show()
    
             
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
        QWidget { border-radius: 15px; border: 1px solid gray; padding: 5px; width: 200px; height: 150px;  } \
        ")
        """
        
        dock['Tips-'+str(count)].setVisible(True)
        dock['Tips-'+str(count)].setFocus()
        dock['Tips-'+str(count)].raise_()
        
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
        QWidget { border-radius: 15px; border: 1px solid gray; padding: 5px; width: 200px; height: 150px;  } \
        ")
        """
        dock['Plotting-'+str(count)].setVisible(True)
        dock['Plotting-'+str(count)].setFocus()
        dock['Plotting-'+str(count)].raise_()
        
        count = count + 1
        
    def ngspiceEditor(self,projDir):
        """
        This function creates widget for NgSpice window
        """
        
        
        self.projDir = projDir
        self.projName = os.path.basename(self.projDir)
        self.ngspiceNetlist = os.path.join(self.projDir,self.projName+".cir.out")
        
               
        
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
        
        """
        #CSS
        dock['NgSpice-'+str(count)].setStyleSheet(" \
        QWidget { border-radius: 15px; border: 1px solid gray; padding: 0px; width: 200px; height: 150px;  } \
        ")
        """
        dock['NgSpice-'+str(count)].setVisible(True)
        dock['NgSpice-'+str(count)].setFocus()
        dock['NgSpice-'+str(count)].raise_()
        
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
            
            dock['Model Editor-'+str(count)].setVisible(True)
            dock['Model Editor-'+str(count)].setFocus()
            dock['Model Editor-'+str(count)].raise_()
        
            count = count + 1
        
        
        
                
        
                     
        