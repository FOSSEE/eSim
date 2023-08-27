import os
import subprocess
import shutil
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5 import QtWidgets
from frontEnd.Application import Application

class LTspiceConverter:
    def __init__(self, parent):
        self.parent = parent

    def convert(self, file_path):
        self.convert_button.clicked.disconnect()
        # Get the base name of the file without the extension
        filename = os.path.splitext(os.path.basename(file_path))[0]
        conPath = os.path.dirname(file_path)
        
        # Check if the file is not empty
        if os.path.getsize(file_path) > 0:
            print("con lt")
            self.convert_button.setEnabled(False)
        else:
            print("File is empty. Cannot perform conversion.")
            # A message box indicating that the file is empty
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Empty File")
            msg_box.setText("The selected file is empty. Conversion cannot be performed.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()