#MTZK#
from PyQt5 import QtWidgets, QtCore,QtGui
from debuggingTool.extractInfo import InfoExtractor
from debuggingTool.error_detection import DetectAndSuggest
from debuggingTool.log_debug import ErrorLogDebug
import os
if os.name == 'nt':
    from frontEnd import pathmagic  # noqa:F401
    init_path = ''
else:
    import pathmagic  # noqa:F401
    init_path = '../../'

# -------------------------------
# Debugging Tool Class
# -------------------------------
class Debugging_tool(QtWidgets.QWidget):
    def __init__(self, ngspice_window=None, parent=None):
        super().__init__(parent)
        self.setWindowFlag(QtCore.Qt.Tool)  # Always stays above the main window
        self.setWindowTitle("Debugging Tool")
        self.netlist=None
        self.type=None
        self.ngspice_window = ngspice_window  # Store the kicad->Ngspice window instance
        self.initUI()
        
    def initUI(self):
        self.setFixedSize(400, 250)
        layout = QtWidgets.QVBoxLayout(self)

        self.suggestion = QtWidgets.QTextEdit(self, readOnly=True)
        self.suggestion.setStyleSheet("background-color: #f5f5f5; font-size: 14px;")
        
        self.debug_button = QtWidgets.QPushButton(self, icon=QtGui.QIcon(init_path + 'images/debug.png'))
        self.debug_button.setIconSize(QtCore.QSize(18, 18))
        self.debug_button.setStyleSheet("font-size: 14px; padding: 5px;")

        self.clear_button = QtWidgets.QPushButton(self, icon=QtGui.QIcon(init_path + 'images/clear.png'))
        self.clear_button.setIconSize(QtCore.QSize(18, 18))
        self.clear_button.setStyleSheet("font-size: 14px; padding: 5px;")

        input_layout = QtWidgets.QHBoxLayout()
        input_layout.addWidget(self.debug_button)
        input_layout.addWidget(self.clear_button)

        layout.addWidget(self.suggestion)
        layout.addLayout(input_layout)
        self.clear_button.clicked.connect(self.clear_session)
    def clear_session(self):
        """Clear the chat display."""
        self.suggestion.clear()
       
    def setNgspiceWindow(self, window,netlist):
        """Set the kicad-to-Ngspice window instance."""
        self.ngspice_window = window
        self.netlist=netlist

    def suggest(self):   
        # If the ngspice_window instance is provided, extract text only from its child widgets.
        self.suggestion.clear()
        if self.type !=3:
            if self.ngspice_window is not None:
                widgets = self.ngspice_window.findChildren(QtWidgets.QWidget)
                formatted=InfoExtractor(widgets,self.type).format()
                if self.type==2:
                    suggestion=DetectAndSuggest(formatted,self.netlist).validate_ng()
                if self.type==1:
                    suggestion=formatted
                self.suggestion.append(suggestion)
        if self.type==3:
                try:
                    with open(self.netlist, 'r') as file:
                        log = file.read()  # Read entire content instead of using readlines()
                        
                except Exception as e:

                    print("Failed to read netlist file.")
                suggestion=ErrorLogDebug(log).suggest()
                self.suggestion.append(suggestion)
        self.type=None
        
                            

        
        