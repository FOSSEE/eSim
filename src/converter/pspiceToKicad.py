import os
import subprocess
import shutil
from PyQt5.QtWidgets import QFileDialog, QMessageBox ,QWidget
from PyQt5 import QtWidgets
from frontEnd.Application import Application

class PspiceConverter:
    def __init__(self, parent):
        self.parent = parent

    def convert(self, file_path,convert_button):
        
        # Get the base name of the file without the extension
        filename = os.path.splitext(os.path.basename(file_path))[0]
        conPath = os.path.dirname(file_path)
        
        # Check if the file is not empty
        if os.path.getsize(file_path) > 0:
            command = f"cd /home/ubuntus/eSim/schematic_converters/lib/PythonLib && python3 parser.py {file_path} {conPath}/{filename}"
            
            try:
                subprocess.run(command, shell=True, check=True)
                convert_button.setEnabled(False)
                # Message box with the conversion success message
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("Conversion Successful")
                msg_box.setText("The file has been converted successfully. Do you want to include it under the project explorer?")
                msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg_box.setDefaultButton(QMessageBox.Yes)
                result = msg_box.exec_()
                print("Conversion of Pspice to eSim schematic Successful")

                if result == QMessageBox.Yes:
                    # Add the converted file under the project explorer
                    newFile = str(conPath + "/" + filename)
                    print(newFile)
                    
                    self.app = Application(None)
                    self.app.obj_Mainview.obj_projectExplorer.addTreeNode(newFile, [newFile])
                    #shutil.copytree(newFile, f"/home/ubuntus/eSim-Workspace/{filename}") 
                    shutil.rmtree(f"/home/ubuntus/eSim-Workspace/{filename}", ignore_errors=True)
                    shutil.copytree(newFile, f"/home/ubuntus/eSim-Workspace/{filename}")

                    print("File added under the project explorer.")
                    # Message box with the Added Successfully message
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Information)
                    msg_box.setWindowTitle("Added Successfully")
                    msg_box.setText("File added under the project explorer successfully.")
                    result = msg_box.exec_()
                    #QtWidgets.QMainWindow.close(QWidget)

                else:
                    # User chose not to add the file
                    print("File not added under the project explorer.")
            except subprocess.CalledProcessError as e:
                # Handle any errors that occurred during command execution
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
        return

    def upload_file_Pspice(self, file_path,convert_button):
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
            convert_button.setEnabled(True)
            convert_button.clicked.connect(lambda: self.convert(file_path,convert_button))
            
        else:
            print("No file selected.")
            convert_button.setEnabled(False)

            # Message box indicating that no file is selected
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("No File Selected")
            msg_box.setText("Please select a file before uploading.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()