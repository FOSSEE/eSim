import sys
import subprocess
import json
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QProgressBar, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal

INSTALL_DETAILS_PATH = "install_details.json"

def update_install_details(version):
    """Update the install_details.json file with the installed Verilator version."""
    if not os.path.exists(INSTALL_DETAILS_PATH):
        print("install_details.json not found.")
        return

    with open(INSTALL_DETAILS_PATH, "r") as file:
        data = json.load(file)

    # Update Verilator entry
    for package in data["important_packages"]:
        if package["package_name"].lower() == "verilator":
            package["version"] = version
            package["installed"] = "Yes"
            package["installed_date"] = subprocess.run(["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True).stdout.strip()
            package["install_directory"] = "/usr/local/bin/verilator"

    with open(INSTALL_DETAILS_PATH, "w") as file:
        json.dump(data, file, indent=4)

    print("install_details.json updated successfully.")

class InstallThread(QThread):
    finished = pyqtSignal(str)
    
    def __init__(self, version):
        super().__init__()
        self.version = version
    
    def run(self):
        try:
            install_verilator_version(self.version)
            self.finished.emit(f"Verilator {self.version} installed successfully!")
        except Exception as e:
            self.finished.emit(f"Installation failed: {str(e)}")

class VerilatorInstallerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Verilator Installer")
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()
        
        title_label = QLabel("Verilator Installer")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        self.version_dropdown = QComboBox()
        self.version_dropdown.addItems(["4.028", "5.002"])
        layout.addWidget(QLabel("Select Verilator Version:"))
        layout.addWidget(self.version_dropdown)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        install_button = QPushButton("Install Verilator")
        install_button.clicked.connect(self.install_verilator_action)
        layout.addWidget(install_button)
        
        self.setLayout(layout)
    
    def install_verilator_action(self):
        selected_version = self.version_dropdown.currentText()
        self.progress_bar.show()
        self.thread = InstallThread(selected_version)
        self.thread.finished.connect(self.show_message)
        self.thread.start()
    
    def show_message(self, result):
        QMessageBox.information(self, "Installation Status", result)
        self.progress_bar.hide()

def install_verilator_version(version):
    try:
        print(f"Installing Verilator version {version}...")
        
        # Update system
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "upgrade", "-y"], check=True)

        # Install required dependencies
        print("Installing required dependencies...")
        dependencies = [
            "git", "make", "autoconf", "g++", "flex", "bison",
            "libfl-dev", "zlib1g-dev"
        ]
        subprocess.run(["sudo", "apt", "install", "-y"] + dependencies, check=True)

        # Clone Verilator repository
        print("Cloning Verilator repository...")
        subprocess.run(["git", "clone", "https://github.com/verilator/verilator.git"], check=True)

        # Checkout the specified version
        print(f"Checking out version {version}...")
        subprocess.run(["git", "checkout", f"v{version}"], cwd="verilator", check=True)

        # Build and install Verilator
        print("Building Verilator...")
        subprocess.run(["autoconf"], cwd="verilator", check=True)
        subprocess.run(["./configure"], cwd="verilator", check=True)
        subprocess.run(["make", "-j$(nproc)"], cwd="verilator", shell=True, check=True)
        subprocess.run(["sudo", "make", "install"], cwd="verilator", check=True)

        # Verify installation
        print("Verifying installation...")
        result = subprocess.run(["verilator", "--version"], check=True, capture_output=True, text=True)
        print(f"Verilator {version} installed successfully!")
        print(result.stdout)

        # Update installation details
        update_install_details(version)

        # Clean up
        print("Cleaning up...")
        subprocess.run(["rm", "-rf", "verilator"], check=True)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred during installation of Verilator {version}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VerilatorInstallerApp()
    window.show()
    sys.exit(app.exec_())
