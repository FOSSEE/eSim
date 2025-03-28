import os
import subprocess
import json
from PyQt5 import QtWidgets, QtGui, QtCore
from ngspice_package_manager import update_installation_status_ngspice
from kicad_package_manager import update_installation_status_kicad
from ghdl_package_manager import update_installation_status_ghdl
from llvm_package_manager import update_installation_status_llvm
from chocolatey import check_chocolatey_directory

# Path to JSON file
JSON_FILE_PATH = os.path.join(os.getcwd(), "install_details.json")

# Path to the external program
NGSPICE_INSTALL_PROGRAM = os.path.join(os.getcwd(), "ngspice_package_manager.py")
KICAD_INSTALL_PROGRAM = os.path.join(os.getcwd(), "kicad_package_manager.py")
LLVM_INSTALL_PROGRAM = os.path.join(os.getcwd(), "llvm_package_manager.py")
GHDL_INSTALL_PROGRAM = os.path.join(os.getcwd(), "ghdl_package_manager.py")
PYTHON_PACKAGES_INSTALL_PROGRAM = os.path.join(os.getcwd(), "python_package_manager.py")
CHOCOLATEY_INSTALL_PROGRAM = os.path.join(os.getcwd(), "chocolatey.py")

update_installation_status_ngspice()
update_installation_status_kicad()
update_installation_status_ghdl()
update_installation_status_llvm()
check_chocolatey_directory(JSON_FILE_PATH)

class DependenciesInstallerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("Tool Manager")
        self.resize(400, 500)
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        # Layout setup
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(20)  # Reduce spacing between widgets
        self.layout.setContentsMargins(20, 20, 20, 20)  # Compact layout margins

        # Heading
        self.heading = QtWidgets.QLabel("Tool Manager for eSim", self)
        self.heading.setFont(QtGui.QFont("Arial", 12))
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setFixedHeight(40)  # Set fixed height for compactness
        self.layout.addWidget(self.heading)


        # Status label
        self.status_label = QtWidgets.QLabel("", self)
        self.status_label.setFont(QtGui.QFont("Arial", 12))
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setFixedHeight(40)  # Set fixed height for compactness
        self.layout.addWidget(self.status_label)

        # Chocolatey status label
        self.chocolatey_status_label = QtWidgets.QLabel("Chocolatey Status: Checking...", self)
        self.chocolatey_status_label.setFont(QtGui.QFont("Arial", 12))
        self.chocolatey_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.chocolatey_status_label.setFixedHeight(40)  # Set fixed height for compactness
        self.layout.addWidget(self.chocolatey_status_label)

        # Button styles with hover effect
        button_style = """
            QPushButton {
                font-size: 14px;
                padding: 10px;
                border-radius: 10px;  /* Rounded corners */
                border: 1px solid gray;  /* Default border */
                background-color: lightgray;  /* Default background */
                color: black;  /* Default text color */
            }
            QPushButton:hover {
                background-color: #87CEFA;  /* Light blue background on hover */
                border: 1px solid #4682B4;  /* Steel blue border on hover */
                color: black;  /* White text on hover */
            }
        """

        # Chocolatey button
        self.chocolatey_button = QtWidgets.QPushButton("Install Chocolatey", self)
        self.chocolatey_button.setStyleSheet(button_style)
        self.chocolatey_button.clicked.connect(self.install_chocolatey)
        self.layout.addWidget(self.chocolatey_button)

        # Ngspice button
        self.ngspice_button = QtWidgets.QPushButton("Install Ngspice", self)
        self.ngspice_button.setStyleSheet(button_style)
        self.ngspice_button.clicked.connect(self.install_ngspice)
        self.layout.addWidget(self.ngspice_button)

        # Kicad button
        self.kicad_button = QtWidgets.QPushButton("Install Kicad", self)
        self.kicad_button.setStyleSheet(button_style)
        self.kicad_button.clicked.connect(self.install_kicad)
        self.layout.addWidget(self.kicad_button)

        # LLVM button
        self.llvm_button = QtWidgets.QPushButton("Install LLVM", self)
        self.llvm_button.setStyleSheet(button_style)
        self.llvm_button.clicked.connect(self.install_llvm)
        self.layout.addWidget(self.llvm_button)

        # GHDL button
        self.ghdl_button = QtWidgets.QPushButton("Install GHDL", self)
        self.ghdl_button.setStyleSheet(button_style)
        self.ghdl_button.clicked.connect(self.install_ghdl)
        self.layout.addWidget(self.ghdl_button)

        # Python packages button
        self.python_packages_button = QtWidgets.QPushButton("Install Python Packages", self)
        self.python_packages_button.setStyleSheet(button_style)
        self.python_packages_button.clicked.connect(self.install_python_packages)
        self.layout.addWidget(self.python_packages_button)

        self.setLayout(self.layout)

        # Update the status label
        self.update_status_label()

    def check_dependencies(self):
        try:
            with open(JSON_FILE_PATH, "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            # Default values if the file is not found
            data = {
                "important_packages": [
                    {
                        "package_name": "ngspice",
                        "installed": "No"
                    },
                    {
                        "package_name": "kicad",
                        "installed": "No"
                    },
                    {
                        "package_name": "llvm",
                        "installed": "No"
                    },
                    {
                        "package_name": "ghdl",
                        "installed": "No"
                    },
                    {
                        "package_name": "chocolatey",
                        "installed": "No"
                    }
                ]
            }

        # Initialize statuses
        ngspice_status = "No"
        kicad_status = "No"
        llvm_status = "No"
        ghdl_status = "No"
        chocolatey_status = "No"

        # Iterate over important packages to find statuses
        for package in data.get("important_packages", []):
            if package.get("package_name") == "ngspice":
                ngspice_status = package.get("installed", "No")
            elif package.get("package_name") == "kicad":
                kicad_status = package.get("installed", "No")
            elif package.get("package_name") == "llvm":
                llvm_status = package.get("installed", "No")
            elif package.get("package_name") == "ghdl":
                ghdl_status = package.get("installed", "No")
            elif package.get("package_name") == "chocolatey":
                chocolatey_status = package.get("installed", "No")

        return ngspice_status, kicad_status, llvm_status, ghdl_status, chocolatey_status

    def update_status_label(self):
        ngspice_status, kicad_status, llvm_status, ghdl_status, chocolatey_status = self.check_dependencies()

        if ngspice_status == "Yes" and kicad_status == "Yes" and llvm_status == "Yes" and ghdl_status == "Yes":
            self.status_label.setText("All necessary dependencies are installed.")
            self.status_label.setStyleSheet("color: green;")
        else:
            missing = []
            installed = []
            if ngspice_status == "No":
                missing.append("Ngspice")
            else:
                installed.append("Ngspice")
            if kicad_status == "No":
                missing.append("Kicad")
            else:
                installed.append("Kicad")
            if llvm_status == "No":
                missing.append("LLVM")
            else:
                installed.append("LLVM")
            if ghdl_status == "No":
                missing.append("GHDL")
            else:
                installed.append("GHDL")

            self.status_label.setText(f"Missing: {', '.join(missing)}\nInstalled: {', '.join(installed)}")
            self.status_label.setStyleSheet("color: red;")

        # Update Chocolatey status label
        if chocolatey_status == "Yes":
            self.chocolatey_status_label.setText("Chocolatey Status: Installed")
            self.chocolatey_status_label.setStyleSheet("color: green;")
        else:
            self.chocolatey_status_label.setText("Chocolatey Status: Not Installed")
            self.chocolatey_status_label.setStyleSheet("color: red;")

    def install_ngspice(self):
        try:
            subprocess.run(["python", NGSPICE_INSTALL_PROGRAM], check=True)
            QtWidgets.QMessageBox.information(self, "Success", "Ngspice installation started successfully!")
            self.update_status_label()  # Update status after installation attempt
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to run Ngspice installer: {e}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def install_kicad(self):
        try:
            subprocess.run(["python", KICAD_INSTALL_PROGRAM], check=True)
            QtWidgets.QMessageBox.information(self, "Success", "Kicad installation started successfully!")
            self.update_status_label()  # Update status after installation attempt
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to run Kicad installer: {e}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def install_llvm(self):
        try:
            subprocess.run(["python", LLVM_INSTALL_PROGRAM], check=True)
            QtWidgets.QMessageBox.information(self, "Success", "LLVM installation started successfully!")
            self.update_status_label()  # Update status after installation attempt
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to run LLVM installer: {e}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def install_ghdl(self):
        try:
            subprocess.run(["python", GHDL_INSTALL_PROGRAM], check=True)
            QtWidgets.QMessageBox.information(self, "Success", "GHDL installation started successfully!")
            self.update_status_label()  # Update status after installation attempt
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to run GHDL installer: {e}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def install_python_packages(self):
        try:
            subprocess.run(["python", PYTHON_PACKAGES_INSTALL_PROGRAM], check=True)
            QtWidgets.QMessageBox.information(self, "Success", "Python packages installation started successfully!")
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to run the Python Packages GUI: {e}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def install_chocolatey(self):
        try:
            subprocess.run(["python", CHOCOLATEY_INSTALL_PROGRAM], check=True)
            QtWidgets.QMessageBox.information(self, "Success", "Chocolatey installation started successfully!")
            self.update_status_label()  # Update status after installation attempt
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to run Chocolatey installer: {e}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

# Main function
def main():
    app = QtWidgets.QApplication([])
    window = DependenciesInstallerApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
