import os
import subprocess
import json
from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from logging_setup import log_info, log_error, log_warning

# Define the virtual environment name and path
venv_name = "toolmanagervenv"
venv_path = os.path.join(os.getcwd(), venv_name)

# Load pip packages from the JSON file
def load_pip_packages():
    json_path = "install_details.json"
    if not os.path.exists(json_path):
        log_warning(f"Error: {json_path} not found.")
        return []

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
            return data.get("pip_packages", [])
    except json.JSONDecodeError as e:
        log_error(f"Error: Failed to parse {json_path}: {e}")
        return []

pip_packages = load_pip_packages()

# Utility to run a system command
def run_command(command):
    """Run a system command and handle errors"""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        log_error(f"Error: Command '{e.cmd}' failed with exit code {e.returncode}")

# Create the virtual environment if it does not exist
def create_virtual_environment():
    log_info(f"Virtual environment '{venv_name}' not found. Creating one...")
    try:
        subprocess.run(f"python -m venv {venv_name}", check=True, shell=True)
        log_info(f"Virtual environment '{venv_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        log_error(f"Failed to create virtual environment: {e}")

def ensure_virtualenv_exists():
    if not os.path.exists(venv_path):
        create_virtual_environment()
    return os.path.exists(venv_path)

# Ensure pip is installed in the virtual environment
def ensure_pip_installed(venv_path):
    python_path = os.path.join(venv_path, "Scripts", "python")
    python_path_quoted = f'"{python_path}"'
    log_info(f"Ensuring pip is installed in {venv_name}...")
    run_command(f"{python_path_quoted} -m ensurepip --upgrade")
    run_command(f"{python_path_quoted} -m pip install --upgrade pip")

# Install packages in the virtual environment
def install_packages_in_venv(venv_path, packages):
    pip_path = os.path.join(venv_path, "Scripts", "pip")
    pip_path_quoted = f'"{pip_path}"'  # Enclose the path in double quotes
    for package in packages:
        log_info(f"Installing {package} in {venv_name}...")
        run_command(f"{pip_path_quoted} install {package}")

# Update packages in the virtual environment
def update_packages_in_venv(venv_path, packages):
    pip_path = os.path.join(venv_path, "Scripts", "pip")
    pip_path_quoted = f'"{pip_path}"'
    for package in packages:
        log_info(f"Updating {package} in {venv_name}...")
        run_command(f"{pip_path_quoted} install --upgrade {package}")

# Check if all packages are installed
def check_installed_packages(venv_path, packages):
    pip_path = os.path.join(venv_path, "Scripts", "pip")
    pip_path_quoted = f'"{pip_path}"'
    not_installed = []
    for package in packages:
        if package == "https://github.com/hdl/pyhdlparser/tarball/master":
            package_name = "hdlparse"
        else:
            package_name = package

        result = subprocess.run(f"{pip_path_quoted} show {package_name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            not_installed.append(package)
    return not_installed

# Update the JSON file after package installation
def update_install_details():
    json_path = "install_details.json"
    if not os.path.exists(json_path):
        log_warning(f"Error: {json_path} not found.")
        return

    try:
        with open(json_path, "r") as f:
            data = json.load(f)

        # Update the 'installed' field for 'pip_packages'
        for package in data.get("important_packages", []):
            if package.get("package_name") == "pip_packages":
                package["installed"] = "Yes"
                package["installed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)
        log_info("install_details.json updated successfully.")
    except json.JSONDecodeError as e:
        log_error(f"Error: Failed to parse {json_path}: {e}")
    except Exception as e:
        log_error(f"Error: {e}")

class PackageManagerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Package Manager")
        self.resize(400, 300)
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title label
        title_label = QtWidgets.QLabel("Package Manager for Virtual Environment")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        # Install button
        install_button = QtWidgets.QPushButton("Install Packages")
        install_button.setStyleSheet(self.get_button_style())
        install_button.clicked.connect(self.install_packages)
        layout.addWidget(install_button)

        # Update button
        update_button = QtWidgets.QPushButton("Update Packages")
        update_button.setStyleSheet(self.get_button_style())
        update_button.clicked.connect(self.update_packages)
        layout.addWidget(update_button)

        # Check button
        check_button = QtWidgets.QPushButton("Check Installed Packages")
        check_button.setStyleSheet(self.get_button_style())
        check_button.clicked.connect(self.check_installed_packages)
        layout.addWidget(check_button)

        self.setLayout(layout)

    def get_button_style(self):
        return (
            """
            QPushButton {
                font-size: 16px;
                padding: 10px;
                border-radius: 10px;
                border: 1px solid gray;
            }
            QPushButton:hover {
                background-color: #87CEFA;
                border: 1px solid #4682B4;
                color: white;
            }
            """
        )

    def install_packages(self):
        if not ensure_virtualenv_exists():
            QMessageBox.critical(self, "Error", f"Virtual environment '{venv_name}' could not be created.")
            return
        ensure_pip_installed(venv_path)
        install_packages_in_venv(venv_path, pip_packages)
        update_install_details()  # Update the JSON file
        QMessageBox.information(self, "Success", "All packages installed successfully.")

    def update_packages(self):
        if not ensure_virtualenv_exists():
            QMessageBox.critical(self, "Error", f"Virtual environment '{venv_name}' could not be created.")
            return
        ensure_pip_installed(venv_path)
        update_packages_in_venv(venv_path, pip_packages)
        QMessageBox.information(self, "Success", "All packages updated successfully.")

    def check_installed_packages(self):
        if not ensure_virtualenv_exists():
            QMessageBox.critical(self, "Error", f"Virtual environment '{venv_name}' could not be created.")
            return
        not_installed = check_installed_packages(venv_path, pip_packages)
        if not not_installed:
            QMessageBox.information(self, "Success", "All packages are installed.")
        else:
            QMessageBox.warning(self, "Missing Packages", f"The following packages are not installed: {', '.join(not_installed)}")

# Run the GUI
def create_gui():
    app = QtWidgets.QApplication([])
    window = PackageManagerApp()
    window.show()
    app.exec_()

create_gui()
