from PyQt5 import QtCore, QtWidgets
from configuration.Appconfig import Appconfig
from projManagement.Validation import Validation
from subcircuit.newSub import NewSub
from subcircuit.openSub import openSub
from subcircuit.convertSub import convertSub
from subcircuit.uploadSub import UploadSub


# This class creates Subcircuit GUI.
class Subcircuit(QtWidgets.QWidget):
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
        QtWidgets.QWidget.__init__(self)
        self.obj_appconfig = Appconfig()
        self.obj_validation = Validation()
        self.obj_dockarea = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.splitter = QtWidgets.QSplitter()
        self.splitter.setOrientation(QtCore.Qt.Vertical)

        self.newbtn = QtWidgets.QPushButton('New Subcircuit Schematic')
        self.newbtn.setToolTip('<b>To create new Subcircuit Schematic</b>')
        self.newbtn.setFixedSize(200, 40)
        self.newbtn.clicked.connect(self.newsch)
        self.editbtn = QtWidgets.QPushButton('Edit Subcircuit Schematic')
        self.editbtn.setToolTip('<b>To edit existing Subcircuit Schematic</b>')
        self.editbtn.setFixedSize(200, 40)
        self.editbtn.clicked.connect(self.editsch)
        self.convertbtn = QtWidgets.QPushButton('Convert Kicad to Ngspice')
        self.convertbtn.setToolTip(
            '<b>To convert Subcircuit Kicad Netlist to Ngspice Netlist</b>')
        self.convertbtn.setFixedSize(200, 40)
        self.convertbtn.clicked.connect(self.convertsch)
        self.uploadbtn = QtWidgets.QPushButton('Upload a Subcircuit')
        self.uploadbtn.setToolTip(
                '<b>To Upload a subcircuit</b>')
        self.uploadbtn.setFixedSize(180, 38)
        self.uploadbtn.clicked.connect(self.uploadSub)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.newbtn)
        self.hbox.addWidget(self.editbtn)
        self.hbox.addWidget(self.convertbtn)
        self.hbox.addWidget(self.uploadbtn)
        self.hbox.addStretch(1)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.vbox.addStretch(1)

        self.setLayout(self.vbox)
        self.show()

    def newsch(self):
        text, ok = QtWidgets.QInputDialog.getText(
            self, 'New Schematic', 'Enter Schematic Name:'
        )
        if ok:
            if not text:
                print("Schematic name cannot be empty")
                print("==================")
                msg = QtWidgets.QErrorMessage(self)
                msg.setModal(True)
                msg.setWindowTitle("Error Message")
                msg.showMessage('The schematic name cannot be empty')
                msg.exec_()
                return

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
