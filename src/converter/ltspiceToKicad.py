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
        
        # Get the base name of the file without the extension
        filename = os.path.splitext(os.path.basename(file_path))[0]
        conPath = os.path.dirname(file_path)
        
        # Check if the file is not empty
        if os.path.getsize(file_path) > 0:
            print("con lt")
            # Get the absolute path of the current script's directory
            script_dir = os.path.dirname(os.path.abspath(__file__))

            # Define the relative path to parser.py from the current script's directory
            relative_parser_path = "LTSpiceToKiCadConverter/src/Ubuntu"

            # Construct the full path to parser.py
            parser_path = os.path.join(script_dir, relative_parser_path)
            print(f"{file_path} {conPath} {filename}")
            #command = f"cd {parser_path} && python3 sch_LTspice2Kicad.py {file_path} {conPath}/{filename}"
            try:
                subprocess.run(command, shell=True, check=True)
                # Message box with the conversion success message
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("Conversion Successful")
                msg_box.setText("The file has been converted successfully. Do you want to include it under the project explorer?")
                msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg_box.setDefaultButton(QMessageBox.Yes)
                result = msg_box.exec_()
                print("Conversion of LTspice to eSim schematic Successful")
            
            except subprocess.CalledProcessError as e:
                print("Error:", e)
        else:
            print("File is empty. Cannot perform conversion.")
            # A message box indicating that the file is empty
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Empty File")
            msg_box.setText("The selected file is empty. Conversion cannot be performed.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

    def upload_file_LTspice(self, file_path):
        if file_path:
            # Check if the file path contains spaces
            if ' ' in file_path:
                # Show a message box indicating that spaces are not allowed
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("Invalid File Path")
                msg_box.setText("Spaces are not allowed in the file path.")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                return
            print(file_path)
            (self.convert(file_path))
            
        else:
            print("No file selected.")

            # Message box indicating that no file is selected
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("No File Selected")
            msg_box.setText("Please select a file before uploading.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()