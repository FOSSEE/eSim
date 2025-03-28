import sys
import os
import shutil
import py7zr
import subprocess
import json
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QMessageBox
from PyQt5.QtCore import Qt

# Define paths
BASE_DIR = r"C:\FOSSEE\Tool-Manager"
DOWNLOAD_DIR = os.path.join(BASE_DIR, "Download")
MINGW64_PATH = r"C:\FOSSEE\MSYS\mingw64"
INFO_JSON = os.path.join(BASE_DIR, "information.json")
VERILATOR_VERSIONS = ["5.032", "5.026", "5.018", "5.006"]
LATEST_VERSION = VERILATOR_VERSIONS[0]
VERILATOR_PACKAGES = {v: f"verilator-{v}.7z" for v in VERILATOR_VERSIONS}


def get_installed_version():
    """Get the installed Verilator version."""
    try:
        result = subprocess.run([os.path.join(MINGW64_PATH, "bin", "verilator_bin.exe"), "--version"], capture_output=True, text=True, check=True)
        version_line = result.stdout.split()[1]
        return version_line
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        return "Unknown"


def update_information_json(version):
    """Update the information.json file with the installed version and date."""
    if os.path.exists(INFO_JSON):
        with open(INFO_JSON, "r") as f:
            data = json.load(f)
    else:
        data = {"important_packages": []}
    
    for package in data["important_packages"]:
        if package["package_name"] == "verilator":
            package["version"] = version
            package["installed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    
    with open(INFO_JSON, "w") as f:
        json.dump(data, f, indent=4)


class VerilatorUpdater(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Verilator Updater")
        self.setGeometry(200, 200, 400, 200)
        layout = QVBoxLayout()

        self.title_label = QLabel("Verilator Updater", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; padding: 10px 0;")
        layout.addWidget(self.title_label)

        self.installed_version = get_installed_version()
        self.version_label = QLabel(f"Installed Version: {self.installed_version}")
        self.version_label.setStyleSheet("font-size: 14px; padding: 10px 0;")
        layout.addWidget(self.version_label)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.update_status_label(self.installed_version)
        layout.addWidget(self.status_label)

        self.dropdown_label = QLabel("Select Verilator version to update:")
        self.dropdown_label.setStyleSheet("font-size: 14px; padding: 10px 0;")
        layout.addWidget(self.dropdown_label)

        self.version_dropdown = QComboBox()
        self.version_dropdown.addItems(VERILATOR_VERSIONS)
        self.version_dropdown.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.version_dropdown)

        self.update_button = QPushButton("Update Verilator")
        self.update_button.clicked.connect(self.install_verilator)
        self.update_button.setStyleSheet("font-size: 14px; padding: 10px 0;")
        layout.addWidget(self.update_button)

        self.setLayout(layout)

    def update_status_label(self, version):
        if version == "Unknown":
            self.status_label.setText("Verilator is not installed.")
            self.status_label.setStyleSheet("color: red; font-size: 14px; padding: 10px 0;")
        elif version == LATEST_VERSION:
            self.status_label.setText("You have the latest version.")
            self.status_label.setStyleSheet("color: green; font-size: 14px; padding: 10px 0;")
        else:
            self.status_label.setText("Please update. Your package is out of date.")
            self.status_label.setStyleSheet("color: red; font-size: 14px; padding: 10px 0;")

    def extract_verilator(self, archive_path, extract_path):
        os.makedirs(extract_path, exist_ok=True)
        print(f"Extracting {os.path.basename(archive_path)}...")
        with py7zr.SevenZipFile(archive_path, mode='r') as archive:
            archive.extractall(DOWNLOAD_DIR)
        extracted_folder = os.path.join(DOWNLOAD_DIR, "verilator")
        if os.path.exists(os.path.join(extracted_folder, "verilator")):
            shutil.move(os.path.join(extracted_folder, "verilator"), extracted_folder)
        print("Extraction complete.")

    def copy_files(self, extract_dir):
        print("Updating Verilator installation...")
        bin_path = os.path.join(extract_dir, "bin")
        share_path = os.path.join(extract_dir, "share", "verilator")
        pkgconfig_path = os.path.join(extract_dir, "share", "pkgconfig")
        
        shutil.copytree(bin_path, os.path.join(MINGW64_PATH, "bin"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(share_path, "bin"), os.path.join(MINGW64_PATH, "bin"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(share_path, "include"), os.path.join(MINGW64_PATH, "include"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(share_path, "examples"), os.path.join(MINGW64_PATH, "examples"), dirs_exist_ok=True)
        
        shutil.copy(os.path.join(share_path, "verilator-config.cmake"), MINGW64_PATH)
        shutil.copy(os.path.join(share_path, "verilator-config-version.cmake"), MINGW64_PATH)
        
        if os.path.exists(pkgconfig_path):
            shutil.copytree(pkgconfig_path, os.path.join(MINGW64_PATH, "pkgconfig"), dirs_exist_ok=True)
            print(f"Copied 'pkgconfig' to {os.path.join(MINGW64_PATH, 'pkgconfig')}")
        else:
            print("Warning: 'pkgconfig' directory not found, skipping copy.")
        
        print("Update complete.")
        shutil.rmtree(extract_dir, ignore_errors=True)
        print("Extracted folder removed.")

    def install_verilator(self):
        version = self.version_dropdown.currentText()
        package_name = VERILATOR_PACKAGES[version]
        archive_path = os.path.join(DOWNLOAD_DIR, package_name)
        extract_dir = os.path.join(DOWNLOAD_DIR, "verilator")

        if not os.path.exists(archive_path):
            print(f"Error: {package_name} not found in {DOWNLOAD_DIR}")
            return

        self.extract_verilator(archive_path, extract_dir)
        self.copy_files(extract_dir)
        update_information_json(version)

        print(f"Verilator v{version} installation complete!")
        self.installed_version = version
        self.version_label.setText(f"Installed Version: {self.installed_version}")
        self.update_status_label(self.installed_version)
        QMessageBox.information(self, "Update Complete", f"Verilator updated to version {version}.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VerilatorUpdater()
    window.show()
    sys.exit(app.exec_())
