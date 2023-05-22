import sys
import subprocess
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import PyQt5.QtCore 
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import py7zr
import os

class AppWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.Logo = QLabel(self)
        self.pixmap = QPixmap('/app/assets/Fossee_logo.png')
        self.Logo.setPixmap(self.pixmap)
        self.Logo.setAlignment(PyQt5.QtCore.Qt.AlignRight)

        self.label = QtWidgets.QLabel('Select package to install:')
        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(['makerchip-app', 'sandpiper-saas', 'matplotlib'])

        self.install_pkg_button = QtWidgets.QPushButton('Install Pip package')
        self.install_pkg_button.clicked.connect(self.install_Pip_package)

        self.install_verilator_from_Archive_button = QtWidgets.QPushButton('Install Verilator from Archive')
        self.install_verilator_from_Archive_button.clicked.connect(self.intall_Verilator_from_Archive)

        self.install_verilator_SRC_button = QtWidgets.QPushButton('Install Verilator from SRC')
        self.install_verilator_SRC_button.clicked.connect(self.install_Verilator_SRC)
        
        self.Install_Output = QtWidgets.QPlainTextEdit()

        self.install_thread = InstallThread_SRC()
        self.install_thread.output_signal.connect(self.update_output)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.Logo)
        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        layout.addWidget(self.install_pkg_button)
        layout.addWidget(self.install_verilator_from_Archive_button)
        layout.addWidget(self.install_verilator_SRC_button)
        layout.addWidget(self.Install_Output)
        self.setLayout(layout)

    def install_Pip_package(self):
        package = self.combo.currentText()
        try:
            subprocess.check_call(['flatpak-spawn', '--host', sys.executable, '-m', 'pip', 'install', package])
            QtWidgets.QMessageBox.information(self, 'Success', f'{package} installed successfully')
            self.Install_Output.appendPlainText(f'Success: {package} installed successfully')
        except Exception as e: 
            QMessageBox.warning(self,"ERROR", str(e))
            self.Install_Output.appendPlainText("[ERROR!]: ")
            self.Install_Output.appendPlainText(str(e))

    def intall_Verilator_from_Archive(self):
        file_name = "/app/assets/packages/verilator.7z"
        output_dir = os.getcwd()

        source_file = f"{output_dir}/verilator/bin/verilator"
        destination_dir = "/usr/bin/" 

        with py7zr.SevenZipFile(file_name, mode='r') as z:
            z.extractall(path=output_dir)

        try:
            subprocess.check_call(['flatpak-spawn', '--host', "pkexec", "cp", source_file, destination_dir])
            QtWidgets.QMessageBox.information(self, 'Success', 'Verilator installed successfully from Archive')
            self.Install_Output.appendPlainText('[Success]: verilator installed successfully from Archive')
        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self,"ERROR", str(e))
            self.Install_Output.appendPlainText("[ERROR!]: ")
            self.Install_Output.appendPlainText(str(e))

    ## Used to show updates for install_Verilator_SRC
    def update_output(self, text):
        self.Install_Output.appendPlainText(text)

    def install_Verilator_SRC(self):
        try:
            self.Install_Output.clear()

            self.Install_Output.clear()
            self.install_thread.start()

        except Exception as e: 
            self.Install_Output.appendPlainText("[ERROR!]: ")
            self.Install_Output.appendPlainText(str(e))
            QtWidgets.QMessageBox.information(self,"Error", str(e))
            print("[ERROR!]: ",e)

class install_verilator(QThread):
    P_progress = pyqtSignal(str)                
    def __init__(self, command, parent=None):
        QThread.__init__(self, parent)
        self.command = command
    def start(self):
        QThread.start(self)
    def run(self):
        try:
            p = subprocess.run(str(self.command),shell=True,capture_output=True)
            status = p.stdout.decode()
            if p:
                print(status)
                self.P_progress.emit(status)
        except Exception as e: 
            self.Install_Output.appendPlainText("[ERROR!]: ")
            self.Install_Output.appendPlainText(str(e))
            QMessageBox.warning(None,"Invalid Install Commands!","Error in install_verilator")

class InstallThread_SRC(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
    
    def run(self):
        command = "/app/assets/scripts/Install_verilator.sh"
        process = subprocess.Popen(["bash", command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                self.output_signal.emit(str(output.strip())[2:-1])
                print(output.strip()[2:-1])

        rc = process.poll()
        if rc == 0:
            self.output_signal.emit("[Info] Installation succeeded!")
            print("Installation succeeded!")
        else:
            self.output_signal.emit("[ERROR] Installation failed!")
            print("Installation failed!")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = AppWindow()
    ex.show()
    sys.exit(app.exec_())