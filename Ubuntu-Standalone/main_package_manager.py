import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

# Define the mapping of buttons to their respective Python scripts
PACKAGE_SCRIPTS = {
    "Ngspice Package Manager": "ngspice_package_manager.py",
    "KiCad Package Manager": "kicad_package_manager.py",
    "GHDL Package Manager": "ghdl_package_manager.py",
    "LLVM Package Manager": "llvm_package_manager.py",
    "Verilator Package Manager": "verilator_package_manager.py",
    "Python Packages Manager": "python_packages_manager.py",
}

class PackageManagerGUI(QWidget):
    def __init__(self):
        super().__init__()

        # GUI Setup
        self.setWindowTitle("Main Package Manager")
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        # Title
        self.title = QLabel("Select a Package Manager")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Create buttons for each package manager
        for name, script in PACKAGE_SCRIPTS.items():
            button = QPushButton(name)
            button.clicked.connect(lambda checked, s=script: self.open_script(s))
            layout.addWidget(button)

        self.setLayout(layout)

    def open_script(self, script):
        """Run the respective Python script when a button is clicked."""
        subprocess.run(["python3", script])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PackageManagerGUI()
    window.show()
    sys.exit(app.exec_())
