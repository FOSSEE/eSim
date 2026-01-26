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

        # Create buttons with proper sizing and styling
        self.newbtn = QtWidgets.QPushButton('New Subcircuit Schematic')
        self.newbtn.setToolTip('<b>To create new Subcircuit Schematic</b>')
        self.newbtn.setMinimumWidth(250)  # Increased width
        self.newbtn.setMinimumHeight(45)  # Increased height
        self.newbtn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #40c4ff, stop:1 #1976d2);
                color: #181b24;
                border: 1px solid #40c4ff;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background: #1976d2;
                color: #fff;
                border: 1.5px solid #1976d2;
            }
            QPushButton:pressed {
                background: #23273a;
                color: #40c4ff;
                border: 1.5px solid #40c4ff;
            }
        """)
        self.newbtn.clicked.connect(self.newsch)

        self.editbtn = QtWidgets.QPushButton('Edit Subcircuit Schematic')
        self.editbtn.setToolTip('<b>To edit existing Subcircuit Schematic</b>')
        self.editbtn.setMinimumWidth(250)  # Increased width
        self.editbtn.setMinimumHeight(45)  # Increased height
        self.editbtn.setStyleSheet(self.newbtn.styleSheet())
        self.editbtn.clicked.connect(self.editsch)

        self.convertbtn = QtWidgets.QPushButton('Convert Kicad to Ngspice')
        self.convertbtn.setToolTip('<b>To convert Subcircuit Kicad Netlist to Ngspice Netlist</b>')
        self.convertbtn.setMinimumWidth(250)  # Increased width
        self.convertbtn.setMinimumHeight(45)  # Increased height
        self.convertbtn.setStyleSheet(self.newbtn.styleSheet())
        self.convertbtn.clicked.connect(self.convertsch)

        self.uploadbtn = QtWidgets.QPushButton('Upload a Subcircuit')
        self.uploadbtn.setToolTip('<b>To Upload a subcircuit</b>')
        self.uploadbtn.setMinimumWidth(250)  # Increased width
        self.uploadbtn.setMinimumHeight(45)  # Increased height
        self.uploadbtn.setStyleSheet(self.newbtn.styleSheet())
        self.uploadbtn.clicked.connect(self.uploadSub)

        # Create layout with proper spacing
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.setSpacing(15)  # Add spacing between buttons
        self.hbox.setContentsMargins(15, 15, 15, 15)  # Add margins around buttons
        self.hbox.addWidget(self.newbtn)
        self.hbox.addWidget(self.editbtn)
        self.hbox.addWidget(self.convertbtn)
        self.hbox.addWidget(self.uploadbtn)
        self.hbox.addStretch(1)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setSpacing(15)  # Add vertical spacing
        self.vbox.setContentsMargins(15, 15, 15, 15)  # Add margins
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
