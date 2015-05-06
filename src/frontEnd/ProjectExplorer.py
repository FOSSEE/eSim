from PyQt4 import QtCore, QtGui
from configuration.Appconfig import Appconfig
import os
import json

class Node(object):
    
    def __init__(self, name, parent=None):
        
        self._name = name
        self._children = []
        self._parent = parent
        
        if parent is not None:
            parent.addChild(self)

    def typeInfo(self):
        return self._typeInfo
    
    def settypeInfo(self,typeInfo):
        self._typeInfo = typeInfo

    def addChild(self, child):
        self._children.append(child)

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self, row):
        return self._children[row]
    
    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent
    
    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)
    

class SceneGraphModel(QtCore.QAbstractItemModel):
    
    """INPUTS: Node, QObject"""
    def __init__(self, root, parent=None):
        super(SceneGraphModel, self).__init__(parent)
        self._rootNode = root

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def columnCount(self, parent):
        return 1
    
    """INPUTS: QModelIndex, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def data(self, index, role):
        
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.name()
            else:
                return node.typeInfo()
            
          

    """INPUTS: QModelIndex, QVariant, int (flag)"""
    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if index.isValid():
            
            if role == QtCore.Qt.EditRole:
                
                node = index.internalPointer()
                node.setName(value)
                
                return True
        return False

    
    """INPUTS: int, Qt::Orientation, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Project Explorer"
            else:
                return "FilePath"
    
    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable 

    """INPUTS: QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return the parent of the node with the given QModelIndex"""
    def parent(self, index):
        
        node = self.getNode(index)
        parentNode = node.parent()
        
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        
        return self.createIndex(parentNode.row(), 0, parentNode)
        
    """INPUTS: int, int, QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return a QModelIndex that corresponds to the given row, column and parent node"""
    def index(self, row, column, parent):
        
        parentNode = self.getNode(parent)

        childItem = parentNode.child(row)


        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()


    """CUSTOM"""
    """INPUTS: QModelIndex"""
    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
            
        return self._rootNode

    

class ProjectExplorer(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self)
        
        returnwidget = self.maketree()
        returnwidget.setStyleSheet("""
        .QWidget {
            border: 3px solid gray;
            border-radius: 40px;
            background-color:white;
            }
        """)
        
    def maketree(self):
        self.obj_appconfig = Appconfig()
        self.root = Node("Projects")
        currentpath= self.obj_appconfig.current_project["ProjectName"]
        if currentpath == None:
            pass
        else:
            self.children =[]
            for dirct, subdir, files in os.walk(currentpath):
                dirlist = dirct.split(os.sep)
                self.parentof = dirlist[-1]
                self.obj_appconfig.project_explorer[dirct]= files
                json.dump(self.obj_appconfig.project_explorer, open(self.obj_appconfig.dictPath,'w'))
        
        for item, value  in self.obj_appconfig.project_explorer.items():
            os.path.join(item)
            pathlist= item.split(os.sep)
            parentnode = Node(pathlist[-1], self.root)
            parentnode.settypeInfo(item)
            for projFiles in value:
                childnode = Node(projFiles, parentnode)
                childnode.settypeInfo (item+ '/' + projFiles)
        
        self.model = SceneGraphModel(self.root)
        
        self.treeView = QtGui.QTreeView()
        self.treeView.doubleClicked.connect(self.openProject)
        
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)
        self.treeView.show()
        
        self.treeView.setModel(self.model)
        self.treeView.setStyleSheet("""
        .QWidget {
            border: 3px solid gray;
            border-radius: 40px;
            background-color:white;
            }
        """)
        return self.treeView
                  
    def openMenu(self, position):
    
        indexes = self.treeView.selectedIndexes()
        if len(indexes) > 0:
        
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        
        menu = QtGui.QMenu()
        if level == 0:
            deleteproject = menu.addAction(self.tr("Remove Project"))
            deleteproject.triggered.connect(self.removeProject)
        elif level == 1:
            openfile = menu.addAction(self.tr("Open"))
            openfile.triggered.connect(self.openProject)
        
        menu.exec_(self.treeView.viewport().mapToGlobal(position))  
                  
    def openProject(self):
        self.indexItem =self.treeView.currentIndex()
        filename= self.indexItem.data().toString()
        self.filePath= self.indexItem.sibling(self.indexItem.row(), 1).data().toString()
        
        self.textwindow = QtGui.QWidget()
        self.textwindow.setMinimumSize(600, 500)
        self.text = QtGui.QTextEdit()
        #self.text.setMaximumSize(580, 450)
        self.save = QtGui.QPushButton('Save and Exit')
        self.save.setDisabled(True)
        self.windowgrid = QtGui.QGridLayout()
        if (os.path.isfile(str(self.filePath)))== True:
            self.fopen = open(str(self.filePath), 'r')
            lines = self.fopen.readlines()
            for line in lines:
                self.text.append(line)
    
            QtCore.QObject.connect(self.text,QtCore.SIGNAL("textChanged()"), self.enable_save)        
            
            vbox_main = QtGui.QVBoxLayout(self.textwindow)
            vbox_main.addWidget(self.text)
            vbox_main.addWidget(self.save)
            self.save.clicked.connect(self.save_data)
            #self.connect(exit,QtCore.SIGNAL('close()'), self.onQuit)
            
            self.textwindow.show()
        else:
            pass
             
    def enable_save(self):
        self.save.setEnabled(True)
        
    def save_data(self):
        self.fopen=open(self.filePath, 'w')
        self.fopen.write(self.text.toPlainText())
        self.fopen.close()
        self.textwindow.close()
        
    def removeProject(self):
        self.indexItem =self.treeView.currentIndex()
        filename= self.indexItem.data().toString()
        self.filePath= self.indexItem.sibling(self.indexItem.row(), 1).data().toString()
        del self.obj_appconfig.project_explorer[str(self.filePath)]
        json.dump(self.obj_appconfig.project_explorer, open(self.obj_appconfig.dictPath,'w'))
