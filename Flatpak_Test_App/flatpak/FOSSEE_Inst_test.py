import sys
import subprocess
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import *
#import py7zr
import os

class PipInstaller(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel('Select package to install:')
        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(['makerchip-app', 'sandpiper-saas', 'matplotlib'])
        self.install_pkg_button = QtWidgets.QPushButton('Install')
        self.install_pkg_button.clicked.connect(self.install_package)
        self.install_verilator_button = QtWidgets.QPushButton('verilator')
        self.install_verilator_button.clicked.connect(self.intall_Verilator)
        self.install_verilator_SRC_button = QtWidgets.QPushButton('Verilator from SRC')
        self.install_verilator_SRC_button.clicked.connect(self.install_Verilator_SRC)
        self.Install_Output = QtWidgets.QPlainTextEdit()

        self.install_thread = InstallThread_SRC()
        self.install_thread.output_signal.connect(self.update_output)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        layout.addWidget(self.install_pkg_button)
        layout.addWidget(self.install_verilator_button)
        layout.addWidget(self.install_verilator_SRC_button)
        layout.addWidget(self.Install_Output)
        self.setLayout(layout)

    def install_package(self):
        package = self.combo.currentText()
        try:
            subprocess.check_call(['flatpak-spawn', '--host', sys.executable, '-m', 'pip', 'install', package])
            QtWidgets.QMessageBox.information(self, 'Success', f'{package} installed successfully')
        except Exception as e: print("[ERROR!]: ",e)

    def intall_Verilator(self):
        file_name = "/app/assets/packages/verilator.7z"
        output_dir = os.getcwd()

        source_file = f"{output_dir}/verilator/bin/verilator"
        destination_dir = "/usr/bin/" 

        #with py7zr.SevenZipFile(file_name, mode='r') as z:
        #    z.extractall(path=output_dir)

        try:
            subprocess.check_call(['flatpak-spawn', '--host', "pkexec", "cp", source_file, destination_dir])
            QtWidgets.QMessageBox.information(self, 'Success', 'verilator installed successfully')
            self.Install_Output.appendPlainText('Success!! verilator installed successfully')
        except subprocess.CalledProcessError:
            self.Install_Output.appendPlainText("[Error!]: Failed to copy file")
            print("[Error!]: Failed to copy file")

    def install_status(self,status):
        self.Install_Output.appendPlainText(status)


    ## Used to show updates for install_Verilator_SRC
    def update_output(self, text):
        self.Install_Output.appendPlainText(text)

    def install_Verilator_SRC(self):
        try:
            self.Install_Output.clear()

            ## Sol 3 ##
            self.Install_Output.clear()
            self.install_thread.start()

        except Exception as e: 
            self.Install_Output.appendPlainText("[ERROR!]: ")
            self.Install_Output.appendPlainText(str(e))

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
        except:
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
            self.output_signal.emit("Installation succeeded!")
            print("Installation succeeded!")
        else:
            self.output_signal.emit("Installation failed!")
            print("Installation failed!")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = PipInstaller()
    ex.show()
    sys.exit(app.exec_())