# =========================================================================
#             FILE: Maker.py
#
#            USAGE: ---
#
#      DESCRIPTION: This define all components of the Makerchip Tab.
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

# Import required libraries
import os
import hdlparse.verilog_parser as vlog
import watchdog.events
import watchdog.observers
from os.path import expanduser
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread
from configuration.Appconfig import Appconfig

# Global variables
home = expanduser("~")
verilogFile = []
toggle_flag = []


def makerchipTOSAccepted(display=True):
    """
    Function to accept Terms of Service of Makerchip
    
    Args:
        display (bool): Whether to display the dialog
        
    Returns:
        bool: True if TOS accepted, False otherwise
    """
    if not os.path.isfile(home + "/.makerchip_accepted"):
        if display:
            reply = QtWidgets.QMessageBox.warning(
                None, 
                "Terms of Service", 
                "Please review the Makerchip Terms of Service "
                "(<a href='https://www.makerchip.com/terms/'>"
                "https://www.makerchip.com/terms/</a>). "
                "Have you read and do you accept these Terms of Service?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            
            if reply == QtWidgets.QMessageBox.Yes:
                with open(home + "/.makerchip_accepted", "w") as f:
                    f.close()
                return True
        return False
    return True


class Maker(QtWidgets.QWidget):
    """
    Main class for creating the Makerchip Tab widget
    """
    
    def __init__(self, filecount, is_dark_theme=False):
        """
        Initialize the Maker widget
        
        Args:
            filecount (int): File counter
            is_dark_theme (bool): Whether to use dark theme
        """
        print(self)
        
        QtWidgets.QWidget.__init__(self)
        self.count = 0
        self.text = ""
        self.filecount = filecount
        self.entry_var = {}
        self.obj_Appconfig = Appconfig()
        self.is_dark_theme = is_dark_theme
        
        # Initialize components
        self.createMakerWidget()
        verilogFile.append("")
    
    def createMakerWidget(self):
        """Create the main widget layout"""
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        
        # Add spacing between widgets
        self.grid.setVerticalSpacing(20)
        self.grid.setContentsMargins(10, 10, 10, 10)
        
        # Add options box at the top
        self.grid.addWidget(self.createoptionsBox(), 0, 0)
        
        # Add tlv file group below with proper spacing
        self.grid.addWidget(self.creategroup(), 1, 0)
        
        # Apply initial theme styling
        self.apply_theme_styling()
        
        self.show()
    
    def apply_theme_styling(self):
        """Apply theme styling to the Maker widget."""
        self.setObjectName("maker_widget")
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
                QLineEdit { background: #ffffff; color: #2c3e50; border: 1px solid #1976d2; border-radius: 8px; padding: 8px 12px; min-height: 30px; font-size: 12px; }
                QLineEdit:focus { border: 1.5px solid #1565c0; }
                QLabel { color: #2c3e50; }
            """)
    
    def addverilog(self):
        """Add new Verilog file to the widget"""
        init_path = '../../' if os.name != 'nt' else ''
        
        self.verilogfile = QtCore.QDir.toNativeSeparators(
            QtWidgets.QFileDialog.getOpenFileName(
                self, 
                "Open Verilog Directory",
                init_path + "home", 
                "*v"
            )[0]
        )
        
        if self.verilogfile == "":
            self.verilogfile = self.entry_var[0].text()
        
        if self.verilogfile == "":
            reply = QtWidgets.QMessageBox.critical(
                None,
                "Error Message",
                "<b>No Verilog File Chosen. Please choose a verilog file.</b>",
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
            )
            
            if reply == QtWidgets.QMessageBox.Ok:
                self.addverilog()
                if self.verilogfile == "":
                    return
                self.obj_Appconfig.print_info('Add Verilog File Called')
            
            elif reply == QtWidgets.QMessageBox.Cancel:
                self.obj_Appconfig.print_info('No Verilog File Chosen')
                return
        
        # Read and set file content
        self.text = open(self.verilogfile).read()
        self.entry_var[0].setText(self.verilogfile)
        self.entry_var[1].setText(self.text)
        
        global verilogFile
        verilogFile[self.filecount] = self.verilogfile
        
        # Setup file watching
        self._setup_file_watcher()
    
    def _setup_file_watcher(self):
        """Setup file watcher for automatic refresh"""
        if self.refreshoption in toggle_flag:
            toggle_flag.remove(self.refreshoption)
        
        self.observer = watchdog.observers.Observer()
        self.event_handler = Handler(
            self.verilogfile,
            self.refreshoption,
            self.observer
        )
        
        self.observer.schedule(
            self.event_handler,
            path=self.verilogfile,
            recursive=True
        )
        self.observer.start()
    
    def refresh_change(self):
        """
        Call refresh while running Ngspice to Verilog Converter
        (as the original one gets destroyed)
        """
        if self.refreshoption in toggle_flag:
            self.toggle = toggle(self.refreshoption)
            self.toggle.start()
    
    def refresh(self):
        """Refresh the file content if edited elsewhere"""
        if not hasattr(self, 'verilogfile'):
            return
        
        self.text = open(self.verilogfile).read()
        self.entry_var[1].setText(self.text)
        
        print("NgVeri File: " + self.verilogfile + " Refreshed")
        self.obj_Appconfig.print_info(
            "NgVeri File: " + self.verilogfile + " Refreshed"
        )
        
        # Restart file watcher
        self._setup_file_watcher()
        
        global toggle_flag
        if self.refreshoption in toggle_flag:
            toggle_flag.remove(self.refreshoption)
    
    def save(self):
        """Save the edited file"""
        try:
            wr = self.entry_var[1].toPlainText()
            with open(self.verilogfile, "w+") as f:
                f.write(wr)
        except BaseException as err:
            self._show_error_message(
                "Error in saving verilog file. Please check if it is chosen."
            )
            print("Error in saving verilog file: " + str(err))
    
    def _show_error_message(self, message):
        """Show error message dialog"""
        self.msg = QtWidgets.QErrorMessage(self)
        self.msg.setModal(True)
        self.msg.setWindowTitle("Error Message")
        self.msg.showMessage(message)
        self.msg.exec_()
    
    def runmakerchip(self):
        """Run the Makerchip IDE"""
        init_path = '../../' if os.name != 'nt' else ''
        
        try:
            if not makerchipTOSAccepted(True):
                return
            
            print("Running Makerchip IDE...........................")
            filename = self.verilogfile
            
            if self.verilogfile.split('.')[-1] != "tlv":
                reply = self._show_automation_dialog()
                
                if reply == QtWidgets.QMessageBox.Cancel:
                    return
                
                if reply == QtWidgets.QMessageBox.Yes:
                    filename = self._process_verilog_to_tlv(init_path)
                    if filename is None:
                        return
            
            # Start Makerchip process
            self.process = QtCore.QProcess(self)
            cmd = 'makerchip ' + filename
            print("File: " + filename)
            self.process.start(cmd)
            print("Makerchip IDE command process pid ---------->", self.process.pid())
            
        except BaseException as e:
            print(e)
            self._show_error_message(
                "Error in running Makerchip IDE. Please check if verilog file is chosen."
            )
            print("Error in running Makerchip IDE. Please check if verilog file is chosen.")
    
    def _show_automation_dialog(self):
        """Show automation confirmation dialog"""
        return QtWidgets.QMessageBox.warning(
            None,
            "Do you want to automate the top module? ",
            "<b>Click on YES button if you want the top module to be added automatically. "
            "A .tlv file will be created in the directory of current verilog file "
            "and the Makerchip IDE will be running on this file. Otherwise click on NO button. "
            "To not open Makerchip IDE, click on CANCEL button. </b><br><br> "
            "NOTE: Makerchip IDE requires an active internet connection and a browser.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel
        )
    
    def _process_verilog_to_tlv(self, init_path):
        """Process Verilog file to TLV format"""
        code = open(self.verilogfile).read()
        text = code
        filename = '.'.join(self.verilogfile.split('.')[:-1]) + ".tlv"
        file = os.path.basename('.'.join(self.verilogfile.split('.')[:-1]))
        
        # Process Verilog code
        code = code.replace(" wire ", " ")
        code = code.replace(" reg ", " ")
        
        vlog_ex = vlog.VerilogExtractor()
        vlog_mods = vlog_ex.extract_objects_from_source(code)
        
        # Read lint_off file
        lint_off = open(init_path + "library/tlv/lint_off.txt").readlines()
        
        # Generate TLV content
        string = self._generate_tlv_content(lint_off, text, file, vlog_mods)
        
        # Validate module name
        if not self._validate_module_name(file, vlog_mods):
            return None
        
        # Write TLV file
        with open(filename, 'w') as f:
            f.write(string)
        
        return filename
    
    def _generate_tlv_content(self, lint_off, text, file, vlog_mods):
        """Generate TLV file content"""
        string = '''\\TLV_version 1d: tl-x.org\n\\SV\n'''
        
        # Add lint_off directives
        for item in lint_off:
            string += "/* verilator lint_off " + item.strip("\n") + "*/  "
        
        string += '''\n\n//Your Verilog/System Verilog Code Starts Here:\n''' + text
        string += '''\n\n//Top Module Code Starts here:\n\tmodule top(input logic clk, '''
        string += '''input logic reset, input logic [31:0] cyc_cnt, '''
        string += '''output logic passed, output logic failed);\n'''
        
        print(file)
        
        # Add port declarations
        for m in vlog_mods:
            if m.name.lower() == file.lower():
                for p in m.ports:
                    if str(p.name) not in ["clk", "reset", "cyc_cnt", "passed", "failed"]:
                        string += '\t\tlogic ' + p.data_type + " " + p.name + ";//" + p.mode + "\n"
        
        # Add random assignments
        string += "//The $random() can be replaced if user wants to assign values\n"
        for m in vlog_mods:
            if m.name.lower() == file.lower():
                for p in m.ports:
                    if str(p.mode) in ["input", "inout"]:
                        if str(p.name) not in ["clk", "reset", "cyc_cnt", "passed", "failed"]:
                            string += '\t\tassign ' + p.name + " = " + "$random();\n"
        
        # Add module instantiation
        for m in vlog_mods:
            if m.name.lower() == file.lower():
                string += '\t\t' + m.name + " " + m.name + '('
                i = 0
                for p in m.ports:
                    i = i + 1
                    string += "." + p.name + "(" + p.name + ")"
                    if i == len(m.ports):
                        string += ");\n\t\n\\TLV\n//Add \\TLV here if desired\n\\SV\nendmodule\n\n"
                    else:
                        string += ", "
        
        return string
    
    def _validate_module_name(self, file, vlog_mods):
        """Validate that file name matches module name"""
        for m in vlog_mods:
            if m.name.lower() != file.lower():
                QtWidgets.QMessageBox.critical(
                    None,
                    "Error Message",
                    "<b>Error: File name and module name are not same. "
                    "Please ensure that they are same.</b>",
                    QtWidgets.QMessageBox.Ok
                )
                self.obj_Appconfig.print_info(
                    'NgVeri stopped due to file name and module name not matching error'
                )
                return False
        return True
    
    def createoptionsBox(self):
        """Create the options/buttons box"""
        self.optionsbox = QtWidgets.QGroupBox()
        self.optionsbox.setTitle("Select Options")
        self.optionsgrid = QtWidgets.QGridLayout()
        self.optionsgroupbtn = QtWidgets.QButtonGroup()
        
        # Set margins and spacing for the options grid
        self.optionsgrid.setContentsMargins(15, 20, 15, 15)
        self.optionsgrid.setSpacing(15)
        
        # Add Top Level Verilog Model button
        self.addoptions = QtWidgets.QPushButton("Add Top Level Verilog Model")
        self.optionsgroupbtn.addButton(self.addoptions)
        self.addoptions.clicked.connect(self.addverilog)
        self.optionsgrid.addWidget(self.addoptions, 0, 0)
        
        # Refresh button
        self.refreshoption = QtWidgets.QPushButton("Refresh")
        self.optionsgroupbtn.addButton(self.refreshoption)
        self.refreshoption.clicked.connect(self.refresh)
        self.optionsgrid.addWidget(self.refreshoption, 0, 1)
        
        # Save button
        self.saveoption = QtWidgets.QPushButton("Save")
        self.optionsgroupbtn.addButton(self.saveoption)
        self.saveoption.clicked.connect(self.save)
        self.optionsgrid.addWidget(self.saveoption, 0, 2)
        
        # Edit in Makerchip IDE button
        self.runoptions = QtWidgets.QPushButton("Edit in Makerchip IDE")
        self.runoptions.setToolTip("Requires internet connection and a browser")
        self.runoptions.setToolTipDuration(5000)
        self.optionsgroupbtn.addButton(self.runoptions)
        self.runoptions.clicked.connect(self.runmakerchip)
        self.optionsgrid.addWidget(self.runoptions, 0, 3)
        
        # Accept TOS button (if needed)
        if not makerchipTOSAccepted(False):
            self.acceptTOS = QtWidgets.QPushButton("Accept Makerchip TOS")
            self.optionsgroupbtn.addButton(self.acceptTOS)
            self.acceptTOS.clicked.connect(lambda: makerchipTOSAccepted(True))
            self.optionsgrid.addWidget(self.acceptTOS, 0, 4)
        
        self.optionsbox.setLayout(self.optionsgrid)
        return self.optionsbox
    
    def creategroup(self):
        """Create the text editor group"""
        self.trbox = QtWidgets.QGroupBox()
        self.trbox.setTitle(".tlv file")
        self.trgrid = QtWidgets.QGridLayout()
        
        # Set margins and spacing for the tlv grid
        self.trgrid.setContentsMargins(10, 15, 10, 10)
        self.trgrid.setSpacing(10)
        
        # Path label and field
        self.start = QtWidgets.QLabel("Path to .tlv file")
        self.trgrid.addWidget(self.start, 0, 0)
        
        self.count = 0
        self.entry_var[self.count] = QtWidgets.QLabel()
        self.trgrid.addWidget(self.entry_var[self.count], 0, 1)
        self.entry_var[self.count].setMaximumWidth(1000)
        self.count += 1
        
        # Code editor
        self.start = QtWidgets.QLabel(".tlv code")
        self.trgrid.addWidget(self.start, 1, 0)
        
        self.entry_var[self.count] = QtWidgets.QTextEdit()
        self.trgrid.addWidget(self.entry_var[self.count], 1, 1)
        self.entry_var[self.count].setMaximumWidth(1000)
        self.entry_var[self.count].setMinimumHeight(300)  # Set minimum height
        self.count += 1
        
        self.trbox.setLayout(self.trgrid)
        return self.trbox

    def set_theme(self, is_dark_theme):
        """Update the theme and re-apply styling."""
        self.is_dark_theme = is_dark_theme
        self.apply_theme_styling()


class Handler(watchdog.events.PatternMatchingEventHandler):
    """
    Handler class for file watching using WatchDog
    """
    
    def __init__(self, verilogfile, refreshoption, observer):
        """
        Initialize the file handler
        
        Args:
            verilogfile (str): Path to the Verilog file
            refreshoption (QPushButton): Refresh button reference
            observer (Observer): File observer instance
        """
        watchdog.events.PatternMatchingEventHandler.__init__(
            self, 
            ignore_directories=True, 
            case_sensitive=False
        )
        self.verilogfile = verilogfile
        self.refreshoption = refreshoption
        self.obj_Appconfig = Appconfig()
        self.observer = observer
        self.toggle = toggle(self.refreshoption)
    
    def on_modified(self, event):
        """Handle file modification events"""
        print("Watchdog received modified event - %s." % event.src_path)
        
        msg = QtWidgets.QErrorMessage()
        msg.setWindowTitle("eSim Message")
        msg.showMessage(
            "NgVeri File: " + self.verilogfile + " modified. Please click on Refresh"
        )
        msg.exec_()
        
        print("NgVeri File: " + self.verilogfile + " modified. Please click on Refresh")
        
        global toggle_flag
        if self.refreshoption not in toggle_flag:
            toggle_flag.append(self.refreshoption)
        
        self.observer.stop()
        self.toggle.start()


class toggle(QThread):
    """
    Class to toggle button appearance (change color by toggling)
    """
    
    def __init__(self, option):
        """
        Initialize the toggle thread
        
        Args:
            option (QPushButton): Button to toggle
        """
        QThread.__init__(self)
        self.option = option
    
    def __del__(self):
        """Clean up the thread"""
        self.wait()
    
    def run(self):
        """Run the toggle thread"""
        while True:
            self.option.setStyleSheet("background-color: red")
            self.sleep(1)
            self.option.setStyleSheet("background-color: none")
            self.sleep(1)
            
            print(toggle_flag)
            
            if not self.option.isVisible():
                break
            if self.option not in toggle_flag:
                break