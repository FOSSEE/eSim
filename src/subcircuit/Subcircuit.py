from PyQt4 import QtCore, QtGui
from configuration.Appconfig import Appconfig
from projManagement.Validation import Validation
from subcircuit.newSub import NewSub
from subcircuit.openSub import openSub
from subcircuit.convertSub import convertSub
from subcircuit.uploadSub import UploadSub


# This class creates Subcircuit GUI.
class Subcircuit(QtGui.QWidget):
    """
    Creates buttons for New project, Edit existing project and
    Kicad Netlist to Ngspice Netlist converter and link them with the
    methods defined for it in other files.

        - New Project(NewSub method of newSub).
        - Open Project(openSub method of openSub).
        - Kicad to Ngspice convertor(convertSub of convertSub).
    """

    def __init__(self, parent=None):
        super(Subcircuit, self).__init__()
        QtGui.QWidget.__init__(self)
        self.obj_appconfig = Appconfig()
        self.obj_validation = Validation()
        self.obj_dockarea = parent
        self.layout = QtGui.QVBoxLayout()
        self.splitter = QtGui.QSplitter()
        self.splitter.setOrientation(QtCore.Qt.Vertical)

        self.newbtn = QtGui.QPushButton('New Subcircuit Schematic')
        self.newbtn.setToolTip('<b>To create new Subcircuit Schematic</b>')
        self.newbtn.setFixedSize(200, 40)
        self.newbtn.clicked.connect(self.newsch)
        self.editbtn = QtGui.QPushButton('Edit Subcircuit Schematic')
        self.editbtn.setToolTip('<b>To edit existing Subcircuit Schematic</b>')
        self.editbtn.setFixedSize(200, 40)
        self.editbtn.clicked.connect(self.editsch)
        self.convertbtn = QtGui.QPushButton('Convert Kicad to Ngspice')
        self.convertbtn.setToolTip(
            '<b>To convert Subcircuit Kicad Netlist to Ngspice Netlist</b>')
        self.convertbtn.setFixedSize(200, 40)
        self.convertbtn.clicked.connect(self.convertsch)
        self.uploadbtn = QtGui.QPushButton('Upload a Subcircuit')
        self.uploadbtn.setToolTip(
            '<b>To Upload a subcircuit</b>')
        self.uploadbtn.setFixedSize(180, 38)
        self.uploadbtn.clicked.connect(self.uploadSub)

        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addWidget(self.newbtn)
        self.hbox.addWidget(self.editbtn)
        self.hbox.addWidget(self.convertbtn)
        self.hbox.addWidget(self.uploadbtn)
        self.hbox.addStretch(1)

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.vbox.addStretch(1)

        self.setLayout(self.vbox)
        self.show()

    def newsch(self):
        text, ok = QtGui.QInputDialog.getText(
            self, 'New Schematic', 'Enter Schematic Name:')
        if ok:
            self.schematic_name = (str(text))
            self.subcircuit = NewSub()
            self.subcircuit.createSubcircuit(self.schematic_name)

        else:
            print("Sub circuit creation cancelled")

    def editsch(self):
        self.obj_opensubcircuit = openSub()
        self.obj_opensubcircuit.body()

    def convertsch(self):
        self.obj_convertsubcircuit = convertSub(self.obj_dockarea)
        self.obj_convertsubcircuit.createSub()

    def uploadSub(self):
        self.obj_uploadsubcircuit = UploadSub()
        self.obj_uploadsubcircuit.upload()
