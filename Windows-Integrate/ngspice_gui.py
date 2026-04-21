import sys
import os
import shutil
import py7zr
import json
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import QCoreApplication
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread, pyqtSignal
# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "Download")
EXTRACT_BASE_DIR = os.path.join(DOWNLOAD_DIR, "nghdl-simulator")  # Extracted folder path
INSTALL_DIR = r"C:\FOSSEE\nghdl-simulator"
MSYS_DIR = r"C:\FOSSEE\MSYS\mingw64"
LIB_FILE = os.path.join(MSYS_DIR, "x86_64-w64-mingw32", "lib", "libws2_32.a")
DEST_DIR = r"C:\FOSSEE\eSim\nghdl\src\ghdlserver"
INFO_JSON = os.path.join(BASE_DIR, "information.json")

# Available Ngspice versions
VERSIONS = ["43", "42", "41"]
LATEST_VERSION = VERSIONS[0]  # Use the first version as the latest
PACKAGE_NAMES = {v: f"nghdl-simulator-{v}.7z" for v in VERSIONS}


def get_installed_version():
    """Retrieve the installed Ngspice version from information.json."""
    if os.path.exists(INFO_JSON):
        with open(INFO_JSON, "r") as f:
            data = json.load(f)
            for package in data.get("important_packages", []):
                if package["package_name"] == "ngspice":
                    return package.get("version", "Unknown")
    return "Unknown"


def update_information_json(version):
    """Update the information.json file with the installed Ngspice version and date."""
    if os.path.exists(INFO_JSON):
        with open(INFO_JSON, "r") as f:
            data = json.load(f)
    else:
        data = {"important_packages": []}

    package_exists = False
    for package in data["important_packages"]:
        if package["package_name"] == "ngspice":
            package["version"] = version
            package["installed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            package_exists = True
            break

    if not package_exists:
        data["important_packages"].append({
            "package_name": "ngspice",
            "version": version,
            "installed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    with open(INFO_JSON, "w") as f:
        json.dump(data, f, indent=4)
class InstallWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, version, package_path, extracted_version_folder):
        super().__init__()
        self.version = version
        self.package_path = package_path
        self.extracted_version_folder = extracted_version_folder

    def run(self):
        try:
            # Step 1: Extraction (0–40)
            for i in range(0, 40, 5):
                self.progress.emit(i)
                self.msleep(100)

            with py7zr.SevenZipFile(self.package_path, mode='r') as archive:
                archive.extractall(EXTRACT_BASE_DIR)

            # Step 2: Copy files (40–80)
            extracted_path = os.path.join(EXTRACT_BASE_DIR, self.extracted_version_folder)

            if not os.path.exists(INSTALL_DIR):
                os.makedirs(INSTALL_DIR)

            items = os.listdir(extracted_path)
            total = len(items)

            for i, item in enumerate(items):
                src_path = os.path.join(extracted_path, item)
                dest_path = os.path.join(INSTALL_DIR, item)

                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_path, dest_path)

                progress_val = 40 + int((i / total) * 40)
                self.progress.emit(progress_val)

            # Step 3: Copy lib (80–100)
            shutil.copy(LIB_FILE, DEST_DIR)

            for i in range(80, 101, 5):
                self.progress.emit(i)
                self.msleep(50)

            self.finished.emit(True, self.version)

        except Exception as e:
            self.finished.emit(False, str(e))

class NgspiceUpdater(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ngspice Updater")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        self.title_label = QLabel("Ngspice Updater", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; padding: 10px 0;")
        layout.addWidget(self.title_label)

        # Show Installed Version
        self.installed_version = get_installed_version()
        self.version_label = QLabel(f"Installed Version: {self.installed_version}")
        self.version_label.setStyleSheet("font-size: 14px; padding: 10px 0;")
        layout.addWidget(self.version_label)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.update_status_label(self.installed_version)  # Initial status update
        layout.addWidget(self.status_label)

        self.dropdown_label = QLabel("Select Ngspice version to install:")
        self.dropdown_label.setStyleSheet("font-size: 14px; padding: 10px 0;")
        layout.addWidget(self.dropdown_label)

        self.version_dropdown = QComboBox()
        self.version_dropdown.addItems(VERSIONS)
        self.version_dropdown.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.version_dropdown)

        self.update_button = QPushButton("Update Ngspice")
        self.update_button.clicked.connect(self.install_ngspice)
        self.update_button.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.update_button)
        # Progress Bar (same like KiCad)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 20px;
            }
        """)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def update_status_label(self, version):
        """Update the status label based on the installed version."""
        if version == "Unknown":
            self.status_label.setText("GHDL is not installed.")
            self.status_label.setStyleSheet("color: red; font-size: 14px; padding: 10px 0;")
        elif version == LATEST_VERSION:
            self.status_label.setText("You are using the latest version.")
            self.status_label.setStyleSheet("color: green; font-size: 14px; padding: 10px 0;")
        else:
            self.status_label.setText("Please Update. Your Package is out of date.")
            self.status_label.setStyleSheet("color: red; font-size: 14px; padding: 10px 0;")
    
    def extract_package(self, package_path):
        """Extract the selected Ngspice package."""
        if not os.path.exists(package_path):
            QMessageBox.critical(self, "Error", f"Package {package_path} not found!")
            return False

        try:
            with py7zr.SevenZipFile(package_path, mode='r') as archive:
                archive.extractall(EXTRACT_BASE_DIR)
            print("Extraction successful.")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Extraction failed: {e}")
            return False

    def copy_all_files(self, extracted_version_folder):
        """Copy extracted files directly into the installation directory."""
        extracted_path = os.path.join(EXTRACT_BASE_DIR, extracted_version_folder)

        if not os.path.exists(extracted_path):
            QMessageBox.critical(self, "Error", f"Extracted folder {extracted_path} not found!")
            return False

        try:
            # Ensure INSTALL_DIR exists
            if not os.path.exists(INSTALL_DIR):
                os.makedirs(INSTALL_DIR)

            # Copy each item inside `nghdl-simulator-43`, NOT the folder itself
            for item in os.listdir(extracted_path):
                src_path = os.path.join(extracted_path, item)
                dest_path = os.path.join(INSTALL_DIR, item)

                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_path, dest_path)

            print(f"Copied all files from {extracted_path} to {INSTALL_DIR}")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error copying files: {e}")
            return False

    def copy_lib_file(self):
        """Copy libws2_32.a file to the destination."""
        try:
            if not os.path.exists(LIB_FILE):
                QMessageBox.critical(self, "Error", f"Source file {LIB_FILE} not found!")
                return False

            if not os.path.exists(DEST_DIR):
                os.makedirs(DEST_DIR)

            shutil.copy(LIB_FILE, DEST_DIR)
            print(f"Copied {LIB_FILE} to {DEST_DIR}")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error copying .a file: {e}")
            return False

    def install_ngspice(self):
        """Run installation using thread (REAL progress)."""

        self.progress_bar.setValue(0)
        self.update_button.setEnabled(False)

        version = self.version_dropdown.currentText()
        package_name = PACKAGE_NAMES[version]
        package_path = os.path.join(DOWNLOAD_DIR, package_name)
        extracted_version_folder = f"nghdl-simulator-{version}"

    # Start worker thread
        self.worker = InstallWorker(version, package_path, extracted_version_folder)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.install_finished)

        self.worker.start()

    def install_finished(self, success, message):
        self.update_button.setEnabled(True)

        if success:
            update_information_json(message)
            self.installed_version = message
            self.version_label.setText(f"Installed Version: {message}")
            self.update_status_label(message)

            self.progress_bar.setValue(100)  # show completion

            QMessageBox.information(self, "Success", f"Ngspice updated to {message}")

        # 🔥 RESET TO 0 AFTER COMPLETION
            self.progress_bar.setValue(0)

        else:
            self.progress_bar.setValue(0)
            QMessageBox.critical(self, "Error", message)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NgspiceUpdater()
    window.show()
    sys.exit(app.exec_())
