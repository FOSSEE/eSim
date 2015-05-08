from PyQt4 import QtGui,QtCore
#from configuration.Appconfig import Appconfig

dockList = ['Blank','Notes']
dock = {}

class DockArea(QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        for dockName in dockList:
            dock[dockName] = QtGui.QDockWidget(dockName)
            dock[dockName].setWidget(QtGui.QTextEdit())
                        
            self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock[dockName])  
                    
        self.tabifyDockWidget(dock['Notes'],dock['Blank'])
        self.show()
    
    def createDockArea(self):
        """
        This function creates Dock Area
        """
        self.mainWindow = QtGui.QMainWindow()
        
               
        for dockName in dockList:
            dock[dockName] = QtGui.QDockWidget(dockName)
            dock[dockName].setWidget(QtGui.QTextEdit())
                        
            self.mainWindow.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock[dockName])  
            
        
       
        self.mainWindow.tabifyDockWidget(dock['Notes'],dock['Blank'])
        self.mainWindow.tabifyDockWidget(dock['Blank'],dock['Tips'])
        
        """
        if len(dockList) > 1:
            for index in range(0, len(dockList) - 1):
                self.mainWindow.tabifiedDockWidgets(dockList[index]),dockList[index + 1])
        """
        
        
           
        self.mainWindow.show()
        
        
        return self.mainWindow
     
        
    def createTestEditor(self):
        """
        This function create widget for Library Editor
        """
        
        self.testWidget = QtGui.QWidget()
        self.testArea = QtGui.QTextEdit()
        self.testLayout = QtGui.QVBoxLayout()
        self.testLayout.addWidget(self.testArea)
         
        #Adding to main Layout
        self.testWidget.setLayout(self.testLayout)
        
        dock['Tips'] = QtGui.QDockWidget('Tips')
        dock['Tips'].setWidget(self.testWidget)
            

        self.tabifyDockWidget(dock['Blank'],dock['Tips'])
                
        
                     
        