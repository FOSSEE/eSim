import os
import subprocess
from PyQt5.QtWidgets import QMessageBox

class PspiceLibConverter:
    def __init__(self, parent):
        self.parent = parent

    def convert(self, file_path):
        
        # Get the base name of the file without the extension
        filename = os.path.splitext(os.path.basename(file_path))[0]
        conPath = os.path.dirname(file_path)
        
        # Checks if the file is not empty
        if os.path.getsize(file_path) > 0:
            # Get the absolute path of the current script's directory
            script_dir = os.path.dirname(os.path.abspath(__file__))

            # Define the relative path to parser.py from the current script's directory
            relative_parser_path = "schematic_converters/lib/PythonLib"

            # Construct the full path to libParser.py
            parser_path = os.path.join(script_dir, relative_parser_path)
            print(parser_path)
            command = f"cd {parser_path} && python3 libParser.py {file_path}"
            print(f"cd {parser_path} && python3 libParser.py {file_path}")
            try:
                subprocess.run(command, shell=True, check=True)
                # Message box with the conversion success message
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("Conversion Successful")
                msg_box.setText("The file has been converted successfully.")
                msg_box.exec()
                print("Conversion of Pspice library is Successful")

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

    def upload_file_Pspice(self, file_path):
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
            
            if ".slb" in file_path:
                print(file_path)
                self.convert(file_path)
            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("Invalid File Path")
                msg_box.setText("Only .slb file can be converted.")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                return
            
        else:
            print("No file selected.")

            # Message box indicating that no file is selected
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("No File Selected")
            msg_box.setText("Please select a file before uploading.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()