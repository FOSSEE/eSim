import os
import sys
import json
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
)

# Virtual environment directory
VENV_DIR = "python_package_venv"

# Load packages from JSON file
def load_packages(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data.get("pip_packages", [])
    except FileNotFoundError:
        QMessageBox.critical(None, "Error", f"Error: {file_path} not found.")
        return []
    except json.JSONDecodeError as e:
        QMessageBox.critical(None, "Error", f"Error parsing JSON: {e}")
        return []

# Function to check if virtual environment exists
def check_virtual_env():
    return os.path.exists(VENV_DIR)

# Function to create a virtual environment
def create_virtual_env():
    try:
        # Create the virtual environment
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
        venv_python = os.path.join(VENV_DIR, "bin", "python")

        # Check and install pip using ensurepip
        subprocess.check_call([venv_python, "-m", "ensurepip", "--upgrade"])

        # Upgrade pip and setuptools
        subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "pip", "setuptools"])
        QMessageBox.information(None, "Virtual Environment", f"Virtual environment '{VENV_DIR}' created successfully.")
    except subprocess.CalledProcessError as e:
        QMessageBox.critical(None, "Error", f"Failed to create virtual environment: {e}")
        sys.exit(1)

# Function to run a command in the virtual environment
def run_in_venv(commands):
    venv_python = os.path.join(VENV_DIR, "bin", "python")
    try:
        # Check if pip is available
        subprocess.run([venv_python, "-m", "pip", "--version"], check=True)

        # Execute the command
        subprocess.check_call([venv_python, "-m"] + commands)
        return None  # Success
    except subprocess.CalledProcessError as e:
        # If pip is not installed, install it and retry the command
        if "pip" in commands:
            try:
                subprocess.check_call([venv_python, "-m", "ensurepip", "--upgrade"])
                subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "pip", "setuptools"])
                subprocess.check_call([venv_python, "-m"] + commands)
                return None  # Success after retry
            except subprocess.CalledProcessError as e_inner:
                return f"Error running command {commands}: {e_inner}"
        return f"Error running command {commands}: {e}"

# Function to install a pip package
def install_package(package):
    return run_in_venv(["pip", "install", package])

# Function to update a pip package
def update_package(package):
    return run_in_venv(["pip", "install", "--upgrade", package])

# Function to check if a package is installed
def check_package_installed(package):
    venv_python = os.path.join(VENV_DIR, "bin", "python")

    # Handle GitHub URLs by mapping them to the expected package name
    if "github.com" in package:
        if "hdl" in package.lower():
            package_name = "hdlparse"  # Map the GitHub URL to the hdlparse package
        else:
            package_name = package.split('/')[-1].split('.')[0]  # Infer package name from URL
    else:
        package_name = package.split("==")[0]  # For regular packages or versioned packages

    try:
        # Check if the package is installed in the virtual environment
        result = subprocess.run(
            [venv_python, "-m", "pip", "show", package_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.stdout:
            for line in result.stdout.splitlines():
                if line.startswith("Version:"):
                    return line.split(":")[1].strip()  # Return the version
        return None
    except Exception as e:
        return None

# Main Window Class for PyQt5
class PackageManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.pip_packages = load_packages("install_details.json")

        # Ensure virtual environment exists
        if not check_virtual_env():
            create_virtual_env()

    def initUI(self):
        self.setWindowTitle("Package Manager")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        install_button = QPushButton("Install Packages")
        install_button.clicked.connect(self.install_packages)
        layout.addWidget(install_button)

        update_button = QPushButton("Update Packages")
        update_button.clicked.connect(self.update_packages)
        layout.addWidget(update_button)

        check_button = QPushButton("Check Packages")
        check_button.clicked.connect(self.check_packages)
        layout.addWidget(check_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def install_packages(self):
        if not self.pip_packages:
            QMessageBox.warning(self, "No Packages", "No packages found in JSON file.")
            return

        success = []
        failure = []
        for package in self.pip_packages:
            version = check_package_installed(package)
            if version:
                success.append(f"{package} is already installed (version {version}).")
            else:
                result = install_package(package)
                if not result:
                    success.append(f"Successfully installed {package}.")
                else:
                    failure.append(result)

        QMessageBox.information(self, "Install Results", "\n".join(success) if success else "No packages installed.")
        if failure:
            QMessageBox.warning(self, "Install Failures", "\n".join(failure))

    def update_packages(self):
        if not self.pip_packages:
            QMessageBox.warning(self, "No Packages", "No packages found in JSON file.")
            return

        choice = QMessageBox.question(self, "Update Packages", "Do you want to update all packages?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if choice == QMessageBox.Yes:
            success = []
            failure = []
            for package in self.pip_packages:
                result = update_package(package)
                if not result:
                    success.append(f"Successfully updated {package}.")
                else:
                    failure.append(result)

            QMessageBox.information(self, "Update Results", "\n".join(success) if success else "No packages updated.")
            if failure:
                QMessageBox.warning(self, "Update Failures", "\n".join(failure))

    def check_packages(self):
        if not self.pip_packages:
            QMessageBox.warning(self, "No Packages", "No packages found in JSON file.")
            return

        success = []
        not_installed = []
        for package in self.pip_packages:
            version = check_package_installed(package)
            if version:
                success.append(f"{package} is installed (version {version}).")
            else:
                not_installed.append(f"{package} is not installed.")

        QMessageBox.information(self, "Check Results", "\n".join(success) if success else "No packages are installed.")
        if not_installed:
            QMessageBox.warning(self, "Missing Packages", "\n".join(not_installed))

# Main Application Execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PackageManagerApp()
    window.show()
    sys.exit(app.exec_())
