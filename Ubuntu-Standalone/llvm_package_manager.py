
import os
import sys
import json
import subprocess
import shutil
import tarfile
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QComboBox,
    QPushButton, QProgressBar, QMessageBox
)

# Configuration
LLVM_TAR_FILES = {
    "15": "clang+llvm-15.0.0-x86_64-linux-gnu-rhel-8.4.tar.xz",
    "16": "clang+llvm-16.0.0-x86_64-linux-gnu-ubuntu-18.04.tar.xz",
}
CMAKE_TAR_FILES = {
    "15": "cmake-15.0.0.src.tar.xz",
    "16": "cmake-16.0.0.src.tar.xz",
}
INSTALL_DIR = "/usr/local/bin/llvm"
JSON_FILE = "install_details.json"

if not os.path.exists(INSTALL_DIR):
    os.makedirs(INSTALL_DIR)
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
        for package in data["important_packages"]:
            if package["package_name"].lower() in ["llvm", "cmake"]:
                package["installed"] = "No"
                package["version"] = "-"
                package["installed_date"] = "-"
                package["install_directory"] = "-"
        with open(JSON_FILE, "w") as file:
            json.dump(data, file, indent=4)

def load_json():
    """Load JSON data from the file."""
    if not os.path.exists(JSON_FILE):
        return {"important_packages": []}
    with open(JSON_FILE, "r") as file:
        return json.load(file)

def save_json(data):
    """Save updates to the JSON file."""
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

def update_package_status(package_name, version, installed, directory):
    """Update the package status in the JSON file."""
    data = load_json()
    for package in data["important_packages"]:
        if package["package_name"].lower() == package_name.lower():
            package["version"] = version
            package["installed"] = "Yes" if installed else "No"
            package["installed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if installed else "-"
            package["install_directory"] = directory if installed else "-"
            break
    else:
        data["important_packages"].append({
            "package_name": package_name,
            "version": version,
            "installed": "Yes" if installed else "No",
            "installed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S") if installed else "-",
            "install_directory": directory if installed else "-"
        })
    save_json(data)

def extract_tar_file(tar_file, target_dir):
    """Extract the .tar.xz file to the target directory."""
    if not os.path.isfile(tar_file):
        print(f"Error: {tar_file} not found.")
        sys.exit(1)

    print(f"Extracting {tar_file} to {target_dir}...")
    with tarfile.open(tar_file, "r:xz") as tar:
        tar.extractall(path=target_dir)
    
    extracted_dir = next(
        (os.path.join(target_dir, d) for d in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, d))),
        None,
    )
    if not extracted_dir:
        print("Error: Unable to locate extracted directory.")
        sys.exit(1)

    print(f"Extracted {tar_file} to {extracted_dir}.")
    return extracted_dir

def install_package(tar_file, package_name, version):
    """Install a single package."""
    install_path = os.path.join(INSTALL_DIR, package_name.lower())
    if os.path.exists(install_path):
        shutil.rmtree(install_path)
    
    extracted_dir = extract_tar_file(tar_file, INSTALL_DIR)
    update_package_status(package_name, version, True, extracted_dir)

def install_llvm_and_cmake(version):
    """Install LLVM and CMake for a specific version."""
    print(f"Installing LLVM and CMake version {version}...")
    install_package(LLVM_TAR_FILES[version], "LLVM", version)
    install_package(CMAKE_TAR_FILES[version], "CMake", version)
    print(f"Installation of LLVM and CMake version {version} complete!")

class InstallerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("LLVM and CMake Installer")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("LLVM and CMake Installer")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)

        # Status Labels
        self.llvm_label = QLabel()
        self.cmake_label = QLabel()
        layout.addWidget(self.llvm_label)
        layout.addWidget(self.cmake_label)
        self.refresh_package_status()

        # Dropdown for Version Selection
        layout.addWidget(QLabel("Select Version:"))
        self.version_dropdown = QComboBox()
        self.version_dropdown.addItems(LLVM_TAR_FILES.keys())
        layout.addWidget(self.version_dropdown)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Install Button
        install_button = QPushButton("Install")
        install_button.clicked.connect(self.install_action)
        layout.addWidget(install_button)

        self.setLayout(layout)

    def refresh_package_status(self):
        data = load_json()
        llvm = next((p for p in data["important_packages"] if p["package_name"].lower() == "llvm"), None)
        cmake = next((p for p in data["important_packages"] if p["package_name"].lower() == "cmake"), None)
        self.llvm_label.setText(f"LLVM Installed: {llvm['installed']} (Version: {llvm['version']})")
        self.cmake_label.setText(f"CMake Installed: {cmake['installed']} (Version: {cmake['version']})")

    def install_action(self):
        version = self.version_dropdown.currentText()
        self.progress_bar.show()
        install_llvm_and_cmake(version)
        self.progress_bar.hide()
        QMessageBox.information(self, "Installation Complete", f"LLVM and CMake {version} installed successfully!")
        self.refresh_package_status()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InstallerApp()
    window.show()
    sys.exit(app.exec())
