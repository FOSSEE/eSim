import os
import subprocess
import shutil
from PyQt5.QtWidgets import QMessageBox
from frontEnd import ProjectExplorer

class PspiceConverter:
    def __init__(self, parent):
        self.parent = parent

    def get_workspace_directory(self):
        # Path to the hidden folder and the workspace file
        hidden_folder_path = os.path.join(os.path.expanduser('~'), '.esim')
        workspace_file_path = os.path.join(hidden_folder_path, 'workspace.txt')

        # Check if the hidden folder and the workspace file exist
        if os.path.exists(hidden_folder_path) and os.path.exists(workspace_file_path):
            # Read the workspace directory from the workspace.txt file
            with open(workspace_file_path, 'r') as file:
                workspace_directory = file.read().strip()  # Remove any leading/trailing whitespaces
            # Split the string by spaces and select the last element
            workspace_directory = workspace_directory.split()[-1]
            return workspace_directory

        return None  # Return None if the hidden folder or the workspace file is not found

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

            # Construct the full path to parser.py
            parser_path = os.path.join(script_dir, relative_parser_path)
            command = f"python3 {parser_path}/parser.py {file_path} {conPath}/{filename}"
            try:
                subprocess.run(command, shell=True, check=True)
                # Message box with the conversion success message
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("Conversion Successful")
                newFile = str(conPath + "/" + filename)
                workspace_directory = self.get_workspace_directory()
                    

                if workspace_directory:
                        print(f"Workspace directory found: {workspace_directory}")
                        merge_copytree(newFile, workspace_directory, filename)
                        msg_box.setText(f"The file has been converted successfully.  Saved in {workspace_directory}.  Open the Project manually.")
                        print("File added under the project explorer.")
                else:
                        print("Workspace directory not found.")
                result = msg_box.exec_()
                print("Conversion of Pspice to eSim schematic Successful")

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
            
            if ".sch" in file_path:
                print(file_path)
                self.convert(file_path)
            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("Invalid File Path")
                msg_box.setText("Only .sch file can be converted.")
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

def merge_copytree(src, dst, filename):
    if not os.path.exists(dst):
        os.makedirs(dst)

    folder_path = f"{dst}/{filename}" # Folder to be created in eSim-Workspace

    # Create the folder 
    try:
        os.makedirs(folder_path)
        print(f"Folder created at {folder_path}")
    except OSError as error:
        print(f"Folder creation failed: {error}")

    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dst_item = os.path.join(folder_path, item)

        if os.path.isdir(src_item):
            merge_copytree(src_item, dst_item, filename)
        else:
            if not os.path.exists(dst_item) or os.stat(src_item).st_mtime > os.stat(dst_item).st_mtime:
                shutil.copy2(src_item, dst_item)
