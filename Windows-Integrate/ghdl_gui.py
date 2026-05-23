import sys
import os
import shutil
import tarfile
import zstandard
import subprocess
import json
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import QCoreApplication

# Define paths
INSTALL_DIR = r"C:\FOSSEE"
DOWNLOAD_DIR = os.path.join(INSTALL_DIR, "Tool-Manager", "Download")
MSYS_DIR = os.path.join(INSTALL_DIR, "MSYS", "mingw64")
GHDL_DIR = os.path.join(INSTALL_DIR, "GHDL")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INFO_JSON = os.path.join(BASE_DIR, "information.json")

# Available GHDL versions (first entry is the latest)
GHDL_VERSIONS = ["4.1.0", "4.0.0", "3.0.0"]
LATEST_VERSION = GHDL_VERSIONS[0]  # Use the first version as the latest
GHDL_PACKAGES = {v: f"ghdl-v{v}.pkg.tar.zst" for v in GHDL_VERSIONS}

def get_installed_version():
    ghdl_path = os.path.join(MSYS_DIR, "bin", "ghdl.exe")

    print("Checking GHDL path:", ghdl_path)

    if not os.path.exists(ghdl_path):
        print("GHDL NOT FOUND")
        return "Unknown"

    try:
        result = subprocess.run([ghdl_path, "--version"], capture_output=True, text=True)
        print("OUTPUT:", result.stdout)
        version_line = result.stdout.splitlines()[0]
        return version_line.split()[1]
    except Exception as e:
        print("ERROR:", e)
        return "Unknown"
    
def update_information_json(version):
    """Update the information.json file with the installed version and date."""
    if os.path.exists(INFO_JSON):
        with open(INFO_JSON, "r") as f:
            data = json.load(f)
    else:
        data = {"important_packages": []}
    
    for package in data["important_packages"]:
        if package["package_name"] == "ghdl":
            package["version"] = version
            package["installed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    
    with open(INFO_JSON, "w") as f:
        json.dump(data, f, indent=4)

class GHDLUpdater(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GHDL Updater")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        self.title_label = QLabel("GHDL Updater", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; padding: 10px 0;")
        layout.addWidget(self.title_label)

        # Installed version display
        self.installed_version = get_installed_version()
        self.version_label = QLabel(f"Installed Version: {self.installed_version}")
        self.version_label.setStyleSheet("font-size: 14px; padding: 10px 0;")
        layout.addWidget(self.version_label)

        # Status message
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.update_status_label(self.installed_version)  # Initial status update
        layout.addWidget(self.status_label)

        # Dropdown for version selection
        self.dropdown_label = QLabel("Select the GHDL version to update:")
        self.dropdown_label.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.dropdown_label)

        self.version_dropdown = QComboBox()
        self.version_dropdown.addItems(GHDL_VERSIONS) 
        self.version_dropdown.setStyleSheet("font-size: 14px; padding: 5px 0;")
        layout.addWidget(self.version_dropdown)
       
        # Update button
        self.update_button = QPushButton("Update GHDL")
        self.update_button.clicked.connect(self.install_ghdl)
        self.update_button.setStyleSheet("font-size: 14px; padding: 10px 0;")
        layout.addWidget(self.update_button)
         # Progress Bar (same like KiCad)
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)

# Green style (KiCad-like)
        self.progress.setStyleSheet("""
        QProgressBar {
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #4CAF50;
            width: 20px;
        }
        """)

        layout.addWidget(self.progress)
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

    def extract_zst(self, archive_path, extract_path):
        """Extract .pkg.tar.zst file."""
        os.makedirs(extract_path, exist_ok=True)

        print(f"Extracting {os.path.basename(archive_path)}...")

        with open(archive_path, 'rb') as f:
            dctx = zstandard.ZstdDecompressor()
            with dctx.stream_reader(f) as reader:
                with open(archive_path.replace('.zst', ''), 'wb') as out_f:
                    shutil.copyfileobj(reader, out_f)

        with tarfile.open(archive_path.replace('.zst', ''), 'r') as tar:
            tar.extractall(path=extract_path)

    def install_ghdl(self):
        self.progress.setValue(5)
        QCoreApplication.processEvents()
        shutil.rmtree(GHDL_DIR, ignore_errors=True)

        """Installs the selected GHDL version."""
        version = self.version_dropdown.currentText()
        package_name = GHDL_PACKAGES[version]
        archive_path = os.path.join(DOWNLOAD_DIR, package_name)
        extract_dir = os.path.join(DOWNLOAD_DIR, f"ghdl-v{version}")
        tar_file = archive_path.replace(".zst", "")

        if not os.path.exists(archive_path):
            print(f"Error: {package_name} not found in {DOWNLOAD_DIR}")
            return

        self.extract_zst(archive_path, extract_dir)
        self.progress.setValue(30)
        QCoreApplication.processEvents()

        # Copy binaries
        shutil.copytree(os.path.join(extract_dir, "mingw64", "bin"), os.path.join(MSYS_DIR, "bin"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(extract_dir, "mingw64", "lib"), os.path.join(MSYS_DIR, "lib"), dirs_exist_ok=True)
        self.progress.setValue(60)
        QCoreApplication.processEvents()
        # Copy include files from extracted include/ghdl to include
        include_src = os.path.join(extract_dir, "mingw64", "include", "ghdl")
        include_dest = os.path.join(GHDL_DIR, "include")
        self.progress.setValue(80)
        QCoreApplication.processEvents()
        os.makedirs(include_dest, exist_ok=True)
        for item in os.listdir(include_src):
            src_path = os.path.join(include_src, item)
            dest_path = os.path.join(include_dest, item)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dest_path)

        shutil.copytree(include_dest, os.path.join(MSYS_DIR, "include"), dirs_exist_ok=True)

        # Copy GHDL files
        shutil.copytree(os.path.join(extract_dir, "mingw64", "bin"), os.path.join(GHDL_DIR, "bin"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(extract_dir, "mingw64", "lib"), os.path.join(GHDL_DIR, "lib"), dirs_exist_ok=True)
        self.progress.setValue(90)
        QCoreApplication.processEvents()
        # Remove old GHDL directory

        # Cleanup
        shutil.rmtree(extract_dir, ignore_errors=True)
        if os.path.exists(tar_file):
            os.remove(tar_file)

        print(f"GHDL v{version} installation complete!")

        # **Update UI after installation**
        self.installed_version = version  # Set installed version to selected version
        update_information_json(version)
        self.version_label.setText(f"Installed Version: {self.installed_version}")  # Update version label
        self.update_status_label(self.installed_version)  # Update status message
        self.progress.setValue(100)
        QCoreApplication.processEvents()
        # **Show popup message**
        QMessageBox.information(self, "Update Complete", f"The GHDL is updated to version {version}.")
        self.progress.setValue(0)
# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GHDLUpdater()
    window.show()
    sys.exit(app.exec_())
