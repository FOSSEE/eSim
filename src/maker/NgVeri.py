# =========================================================================
#             FILE: NgVeri.py
#
#            USAGE: ---
#
#      DESCRIPTION: This define all components of the NgVeri Tab.
#
#          OPTIONS: ---
#     REQUIREMENTS: ---
#             BUGS: ---
#            NOTES: ---
#           AUTHOR: Sumanto Kar, sumantokar@iitb.ac.in, FOSSEE, IIT Bombay
# ACKNOWLEDGEMENTS: Rahul Paknikar, rahulp@iitb.ac.in, FOSSEE, IIT Bombay
#                Digvijay Singh, digvijay.singh@iitb.ac.in, FOSSEE, IIT Bombay
#                Prof. Maheswari R. and Team, VIT Chennai
#     GUIDED BY: Steve Hoover, Founder Redwood EDA
#                Kunal Ghosh, VLSI System Design Corp.Pvt.Ltd
#                Anagha Ghosh, VLSI System Design Corp.Pvt.Ltd
# OTHER CONTRIBUTERS:
#                Prof. Madhuri Kadam, Shree L. R. Tiwari College of Engineering
#                Rohinth Ram, Madras Institue of Technology
#                Charaan S., Madras Institue of Technology
#                Nalinkumar S., Madras Institue of Technology
#  ORGANIZATION: eSim Team at FOSSEE, IIT Bombay
#       CREATED: Monday 29, November 2021
#      REVISION: Tuesday 25, January 2022
# =========================================================================


# importing the files and libraries
from PyQt5 import QtCore, QtWidgets
from . import Maker
from . import ModelGeneration
import os
import shutil
from configuration.Appconfig import Appconfig
from configparser import ConfigParser


class NgVeri(QtWidgets.QWidget):
    '''
        This class create the NgVeri Tab
    '''
    def __init__(self, filecount, is_dark_theme=False):
        QtWidgets.QWidget.__init__(self)
        # Maker.addverilog(self)
        self.obj_Appconfig = Appconfig()
        self.is_dark_theme = is_dark_theme

        if os.name == 'nt':
            self.home = os.path.join('library', 'config')
        else:
            self.home = os.path.expanduser('~')

        self.parser = ConfigParser()
        self.parser.read(os.path.join(
            self.home, os.path.join('.nghdl', 'config.ini')))
        self.nghdl_home = self.parser.get('NGHDL', 'NGHDL_HOME')
        self.release_dir = self.parser.get('NGHDL', 'RELEASE')
        self.src_home = self.parser.get('SRC', 'SRC_HOME')
        self.licensefile = self.parser.get('SRC', 'LICENSE')
        self.digital_home = self.parser.get('NGHDL', 'DIGITAL_MODEL')
        self.digital_home = self.digital_home + "/Ngveri"
        self.count = 0
        self.text = ""
        self.entry_var = {}
        self.createNgveriWidget()
        self.fname = ""
        self.filecount = filecount

    def createNgveriWidget(self):
        '''
            Creating the various components of the Widget(Ngveri Tab)
        '''
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        self.grid.addWidget(self.createoptionsBox(), 0, 0, QtCore.Qt.AlignTop)
        self.grid.addWidget(self.creategroup(), 1, 0, 5, 0)

        # Apply initial theme styling
        self.apply_theme_styling()

        self.show()

    def apply_theme_styling(self):
        """Apply theme styling to the NgVeri widget."""
        self.setObjectName("ngveri_widget")
        
        if self.is_dark_theme:
            self.setStyleSheet("""
                QWidget { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #23273a, stop:1 #181b24); color: #e8eaed; }
                QGroupBox { border: 2px solid #40c4ff; border-radius: 14px; margin-top: 1em; padding: 15px; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #23273a, stop:1 #181b24); color: #e8eaed; }
                QGroupBox::title { subcontrol-origin: margin; left: 15px; padding: 0 5px; color: #40c4ff; font-weight: bold; font-size: 14px; }
                QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #40c4ff, stop:1 #1976d2); color: #181b24; border: 1px solid #40c4ff; min-height: 35px; min-width: 120px; padding: 8px 15px; border-radius: 10px; font-weight: 700; font-size: 12px; }
                QPushButton:hover { background: #1976d2; color: #fff; border: 1.5px solid #1976d2; }
                QPushButton:pressed { background: #23273a; color: #40c4ff; border: 1.5px solid #40c4ff; }
                QPushButton:disabled { background: #23273a; color: #888; border: 1px solid #23273a; }
                QTextEdit { background: #23273a; color: #e8eaed; border: 1px solid #40c4ff; border-radius: 8px; padding: 10px; font-size: 12px; font-family: 'Consolas', 'Monaco', monospace; }
                QComboBox { background: #23273a; color: #e8eaed; border: 1px solid #40c4ff; border-radius: 8px; padding: 5px 10px; min-height: 30px; font-size: 12px; }
                QComboBox:hover { border: 1.5px solid #1976d2; }
                QComboBox::drop-down { border: none; width: 20px; }
                QComboBox::down-arrow { width: 12px; height: 12px; }
                QLineEdit { background: #23273a; color: #e8eaed; border: 1px solid #40c4ff; border-radius: 8px; padding: 8px 12px; min-height: 30px; font-size: 12px; }
                QLineEdit:focus { border: 1.5px solid #1976d2; }
                QLabel { color: #e8eaed; }
            """)
        else:
            self.setStyleSheet("""
                QWidget { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #f8f9fa); color: #2c3e50; }
                QGroupBox { border: 2px solid #1976d2; border-radius: 14px; margin-top: 1em; padding: 15px; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #f8f9fa); color: #2c3e50; }
                QGroupBox::title { subcontrol-origin: margin; left: 15px; padding: 0 5px; color: #1976d2; font-weight: bold; font-size: 14px; }
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f5f7fa, stop:1 #e3e8ee);
                    color: #1976d2;
                    border: 1px solid #b0bec5;
                    min-height: 35px;
                    min-width: 120px;
                    padding: 8px 15px;
                    border-radius: 10px;
                    font-weight: 700;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background: #e3e8ee;
                    color: #1565c0;
                    border: 1.5px solid #1976d2;
                }
                QPushButton:pressed {
                    background: #cfd8dc;
                    color: #1976d2;
                    border: 1.5px solid #1976d2;
                }
                QPushButton:disabled {
                    background: #e1e4e8;
                    color: #7f8c8d;
                    border: 1px solid #e1e4e8;
                }
                QTextEdit { background: #ffffff; color: #2c3e50; border: 1px solid #1976d2; border-radius: 8px; padding: 10px; font-size: 12px; font-family: 'Consolas', 'Monaco', monospace; }
                QComboBox { background: #ffffff; color: #2c3e50; border: 1px solid #1976d2; border-radius: 8px; padding: 5px 10px; min-height: 30px; font-size: 12px; }
                QComboBox:hover { border: 1.5px solid #1565c0; }
                QComboBox::drop-down { border: none; width: 20px; }
                QComboBox::down-arrow { width: 12px; height: 12px; }
                QLineEdit { background: #ffffff; color: #2c3e50; border: 1px solid #1976d2; border-radius: 8px; padding: 8px 12px; min-height: 30px; font-size: 12px; }
                QLineEdit:focus { border: 1.5px solid #1565c0; }
                QLabel { color: #2c3e50; }
            """)

    def addverilog(self):
        '''
            Adding the verilog file in Maker tab to Ngveri Tab automatically
        '''
        # b=Maker.Maker(self)
        print(Maker.verilogFile)
        if Maker.verilogFile[self.filecount] == "":
            reply = QtWidgets.QMessageBox.critical(
                None,
                "Error Message",
                "<b>Error: No Verilog File Chosen. \
                Please choose a verilog file in Makerchip Tab</b>",
                QtWidgets.QMessageBox.Ok)
            if reply == QtWidgets.QMessageBox.Ok:
                self.obj_Appconfig.print_error(
                    'No Verilog File Chosen. '
                    'Please choose a verilog file in Makerchip Tab'
                )
                return

        self.fname = Maker.verilogFile[self.filecount]
        currentTermLogs = QtWidgets.QTextEdit()
        model = ModelGeneration.ModelGeneration(self.fname, currentTermLogs)
        file = (os.path.basename(self.fname)).split('.')[0]
        if self.entry_var[1].findText(file) == -1:
            self.entry_var[1].addItem(file)

        if not Maker.makerchipTOSAccepted(True):
            QtWidgets.QMessageBox.warning(
                None, "Warning Message",
                "Please accept the Makerchip Terms of Service "
                "to proceed further.",
                QtWidgets.QMessageBox.Ok
            )

            return

        try:
            model.verilogfile()
            error = model.verilogParse()
            if error != "Error":
                model.getPortInfo()
                model.cfuncmod()
                model.ifspecwrite()
                model.sim_main_header()
                model.sim_main()
                model.modpathlst()
                model.run_verilator()
                model.make_verilator()
                model.copy_verilator()
                model.runMake()

                if os.name != 'nt':
                    model.runMakeInstall()
                else:
                    try:
                        shutil.copy(
                            self.release_dir +
                            "/src/xspice/icm/Ngveri/Ngveri.cm",
                            self.nghdl_home + "/lib/ngspice/"
                        )
                    except FileNotFoundError as err:
                        currentTermLogs.append(
                            "Error in copying Ngveri code model: " + str(err)
                        )

                if "error" not in currentTermLogs.toPlainText().lower():
                    currentTermLogs.append('''
                        <p style=\" font-size:16pt; font-weight:1000;
                        color:#00FF00;\"> Model Created Successfully!
                        </p>
                    ''')

        except BaseException as err:
            currentTermLogs.append(
                "Error in Ngspice code model generation " +
                "from Verilog: " + str(err)
            )

        if "error" in currentTermLogs.toPlainText().lower():
            currentTermLogs.append('''
                <p style=\" font-size:16pt; font-weight:1000;
                color:#FF0000;\">There was an error during model creation,
                <br/>Please rectify the error and try again!
                </p>
            ''')

        self.entry_var[0].append(currentTermLogs.toHtml())

        # Force scroll the terminal widget at bottom
        self.entry_var[0].verticalScrollBar().setValue(
            self.entry_var[0].verticalScrollBar().maximum()
        )

    def addfile(self):
        '''
            This function is used to add additional files required
            by the verilog top module
        '''
        if len(Maker.verilogFile) < (self.filecount + 1):
            reply = QtWidgets.QMessageBox.critical(
                None,
                "Error Message",
                "<b>Error: No Verilog File Chosen. \
                Please choose a verilog file in Makerchip Tab</b>",
                QtWidgets.QMessageBox.Ok)
            if reply == QtWidgets.QMessageBox.Ok:
                self.obj_Appconfig.print_error(
                    'No Verilog File Chosen. Please choose \
                     a verilog file in Makerchip Tab')
                return

        self.fname = Maker.verilogFile[self.filecount]
        model = ModelGeneration.ModelGeneration(self.fname, self.entry_var[0])
        # model.verilogfile()
        model.addfile()

    def addfolder(self):
        '''
            This function is used to add additional folder required
            by the verilog top module.
        '''
        if len(Maker.verilogFile) < (self.filecount + 1):
            reply = QtWidgets.QMessageBox.critical(
                None,
                "Error Message",
                "<b>Error: No Verilog File Chosen. \
                Please choose a verilog file in Makerchip Tab</b>",
                QtWidgets.QMessageBox.Ok)
            if reply == QtWidgets.QMessageBox.Ok:
                self.obj_Appconfig.print_error(
                    'No Verilog File Chosen. Please choose \
                    a verilog file in Makerchip Tab')
                return
        self.fname = Maker.verilogFile[self.filecount]
        model = ModelGeneration.ModelGeneration(self.fname, self.entry_var[0])
        # model.verilogfile()
        model.addfolder()

    def clearTerminal(self):
        '''
            This function is used to clear the terminal
        '''
        self.entry_var[0].setText("")

    def createoptionsBox(self):
        '''
            This function is used to create buttons/options
        '''
        self.optionsbox = QtWidgets.QGroupBox()
        self.optionsbox.setTitle("Select Options")
        self.optionsgrid = QtWidgets.QGridLayout()
        self.optionsgroupbtn = QtWidgets.QButtonGroup()

        # Set margins and spacing for better layout
        self.optionsgrid.setContentsMargins(15, 20, 15, 15)
        self.optionsgrid.setSpacing(15)

        self.addverilogbutton = QtWidgets.QPushButton(
            "Convert Verilog to Ngspice")
        self.addverilogbutton.setToolTip(
            "Requires internet connection for converting TL-Verilog models"
        )
        self.addverilogbutton.setToolTipDuration(5000)
        self.optionsgroupbtn.addButton(self.addverilogbutton)
        self.addverilogbutton.clicked.connect(self.addverilog)
        self.optionsgrid.addWidget(self.addverilogbutton, 0, 1)

        self.addfilebutton = QtWidgets.QPushButton("Add dependency files")
        self.optionsgroupbtn.addButton(self.addfilebutton)
        self.addfilebutton.clicked.connect(self.addfile)
        self.optionsgrid.addWidget(self.addfilebutton, 0, 2)

        self.addfolderbutton = QtWidgets.QPushButton("Add dependency folder")
        self.optionsgroupbtn.addButton(self.addfolderbutton)
        self.addfolderbutton.clicked.connect(self.addfolder)
        self.optionsgrid.addWidget(self.addfolderbutton, 0, 3)

        self.clearTerminalBtn = QtWidgets.QPushButton("Clear Terminal")
        self.optionsgroupbtn.addButton(self.clearTerminalBtn)
        self.clearTerminalBtn.clicked.connect(self.clearTerminal)
        self.optionsgrid.addWidget(self.clearTerminalBtn, 0, 4)

        self.optionsbox.setLayout(self.optionsgrid)
        return self.optionsbox

    def edit_modlst(self, text):
        '''
            This is used to remove models in modlst of Ngspice folder if
            the user wants to remove a model. Note: files do not get removed.
        '''
        if text == "Remove Verilog Models":
            return
        index = self.entry_var[1].findText(text)
        self.entry_var[1].removeItem(index)
        self.entry_var[1].setCurrentIndex(0)
        ret = QtWidgets.QMessageBox.warning(
            None, "Warning", '''<b>Do you want to remove the model: ''' +
            text,
            QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel
        )
        if ret == QtWidgets.QMessageBox.Ok:
            mod = open(self.digital_home + '/modpath.lst', 'r')
            data = mod.readlines()
            mod.close()

            data.remove(text + "\n")
            mod = open(self.digital_home + '/modpath.lst', 'w')
            for item in data:
                mod.write(item)
            self.fname = Maker.verilogFile[self.filecount]
            model = ModelGeneration.ModelGeneration(
                self.fname, self.entry_var[0])

            try:
                model.runMake()

                if os.name != 'nt':
                    model.runMakeInstall()
                else:
                    shutil.copy(
                        self.release_dir + "/src/xspice/icm/Ngveri/Ngveri.cm",
                        self.nghdl_home + "/lib/ngspice/"
                    )
            except BaseException as err:
                QtWidgets.QMessageBox.critical(
                    None, "Error Message",
                    "The verilog model '" + str(text) +
                    "' could not be removed: " + str(err),
                    QtWidgets.QMessageBox.Ok
                )

    def lint_off_edit(self, text):
        '''
          This is to remove lint_off comments needed by the verilator warnings.
          This function writes to the lint_off.txt in the library/tlv folder.
        '''
        init_path = '../../'
        if os.name == 'nt':
            init_path = ''

        if text == "Remove lint_off":
            return
        index = self.entry_var[2].findText(text)
        self.entry_var[2].removeItem(index)
        self.entry_var[2].setCurrentIndex(0)
        ret = QtWidgets.QMessageBox.warning(
            None,
            "Warning",
            '''<b>Do you want to remove the lint off error: ''' +
            text,
            QtWidgets.QMessageBox.Ok,
            QtWidgets.QMessageBox.Cancel)

        if ret == QtWidgets.QMessageBox.Ok:
            file = open(init_path + "library/tlv/lint_off.txt", 'r')
            data = file.readlines()
            file.close()

            data.remove(text + "\n")
            file = open(init_path + "library/tlv/lint_off.txt", 'w')
            for item in data:
                file.write(item)

    def add_lint_off(self):
        '''
            This is to add lint_off comments needed by the verilator warnings.
            This function writes to the lint_off.txt in the library/tlv folder.
        '''
        init_path = '../../'
        if os.name == 'nt':
            init_path = ''

        text = self.entry_var[3].text()

        if self.entry_var[2].findText(text) == -1:
            self.entry_var[2].addItem(text)
            file = open(init_path + "library/tlv/lint_off.txt", 'a+')
            file.write(text + "\n")
            file.close()
        self.entry_var[3].setText("")

    def creategroup(self):
        '''
            Creates various other groups like terminal, remove modlst,
            remove lint_off and add lint_off
        '''
        self.trbox = QtWidgets.QGroupBox()
        self.trbox.setTitle("Terminal")
        self.trgrid = QtWidgets.QGridLayout()
        self.trbox.setLayout(self.trgrid)
        self.count = 0

        # Set margins and spacing for better layout
        self.trgrid.setContentsMargins(15, 20, 15, 15)
        self.trgrid.setSpacing(15)

        self.start = QtWidgets.QLabel("Terminal")
        self.entry_var[self.count] = QtWidgets.QTextEdit()
        self.entry_var[self.count].setReadOnly(1)
        self.trgrid.addWidget(self.entry_var[self.count], 1, 1, 5, 3)
        self.entry_var[self.count].setMaximumWidth(1000)
        self.entry_var[self.count].setMaximumHeight(1000)
        self.count += 1

        self.entry_var[self.count] = QtWidgets.QComboBox()
        self.entry_var[self.count].addItem("Remove Verilog Models")
        self.modlst = open(self.digital_home + '/modpath.lst', 'r')
        self.data = self.modlst.readlines()
        self.modlst.close()
        for item in self.data:
            if item != "\n":
                self.entry_var[self.count].addItem(item.strip())
        self.entry_var[self.count].activated[str].connect(self.edit_modlst)
        self.trgrid.addWidget(self.entry_var[self.count], 1, 4, 1, 2)
        self.count += 1

        self.entry_var[self.count] = QtWidgets.QComboBox()
        self.entry_var[self.count].addItem("Remove lint_off")

        init_path = '../../'
        if os.name == 'nt':
            init_path = ''
        self.lint_off = open(init_path + "library/tlv/lint_off.txt", 'r')

        self.data = self.lint_off.readlines()
        self.lint_off.close()
        for item in self.data:
            if item != "\n":
                self.entry_var[self.count].addItem(item.strip())
        self.entry_var[self.count].activated[str].connect(self.lint_off_edit)
        self.trgrid.addWidget(self.entry_var[self.count], 2, 4, 1, 2)
        self.count += 1

        self.entry_var[self.count] = QtWidgets.QLineEdit(self)
        self.trgrid.addWidget(self.entry_var[self.count], 3, 4)
        self.entry_var[self.count].setMaximumWidth(200)
        self.count += 1

        self.entry_var[self.count] = QtWidgets.QPushButton("Add lint_off")
        self.entry_var[self.count].setMaximumWidth(150)
        self.trgrid.addWidget(self.entry_var[self.count], 3, 5)
        self.entry_var[self.count].clicked.connect(self.add_lint_off)

        self.count += 1

        self.trbox.setLayout(self.trgrid)
        return self.trbox

    def set_theme(self, is_dark_theme):
        """Update the theme and re-apply styling."""
        self.is_dark_theme = is_dark_theme
        self.apply_theme_styling()
