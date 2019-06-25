# =========================================================================
#
#          FILE: Application.py
#
#         USAGE: ---
#
#   DESCRIPTION: This main file use to start the Application
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 21 January 2015
#      REVISION:  ---
# =========================================================================
import pathmagic  # noqa
from PyQt4 import QtGui, QtCore
from configuration.Appconfig import Appconfig
from projManagement.openProject import OpenProjectInfo
from projManagement.newProject import NewProjectInfo
from projManagement.Kicad import Kicad
from projManagement.Validation import Validation
from projManagement import Worker
from frontEnd import ProjectExplorer
from frontEnd import Workspace
from frontEnd import DockArea
import time
from PyQt4.Qt import QSize
import sys
import os

# Its our main window of application.


class Application(QtGui.QMainWindow):
    """This class initializes all objects used in this file(Application.py)."""
    global project_name

    def __init__(self, *args):
        """Initialize main Application window."""
        # Calling __init__ of super class
        QtGui.QMainWindow.__init__(self, *args)

        # Creating require Object
        self.obj_workspace = Workspace.Workspace()
        self.obj_Mainview = MainView()
        self.obj_kicad = Kicad(self.obj_Mainview.obj_dockarea)
        self.obj_appconfig = Appconfig()
        self.obj_validation = Validation()
        # Initialize all widget
        self.setCentralWidget(self.obj_Mainview)
        self.initToolBar()

        self.setGeometry(self.obj_appconfig._app_xpos,
                         self.obj_appconfig._app_ypos,
                         self.obj_appconfig._app_width,
                         self.obj_appconfig._app_heigth)
        self.setWindowTitle(self.obj_appconfig._APPLICATION)
        self.showMaximized()
        self.setWindowIcon(QtGui.QIcon('../../images/logo.png'))
        # self.show()
        self.systemTrayIcon = QtGui.QSystemTrayIcon(self)
        self.systemTrayIcon.setIcon(QtGui.QIcon('../../images/logo.png'))
        self.systemTrayIcon.setVisible(True)

    # This function initializes Tool Bars
    def initToolBar(self):
        """
        In this function we are setting icons, short-cuts,and
        defining functonality for:

            - Top-tool-bar (New project, Open project, Close project,\
                Help option )
            - Left-tool-bar (Open Schematic, Convert KiCad to NgSpice,\
                Simuation, Model Editor, Subcircuit, NGHDL, Modelica\
                Converter, OM Optimisation )
        """
        # Top Tool bar
        self.newproj = QtGui.QAction(
            QtGui.QIcon('../../images/newProject.png'),
            '<b>New Project</b>',
            self)
        self.newproj.setShortcut('Ctrl+N')
        self.newproj.triggered.connect(self.new_project)
        # self.newproj.connect(self.newproj, QtCore.SIGNAL('triggered()'),
        #                      self, QtCore.SLOT(self.new_project()))

        self.openproj = QtGui.QAction(
            QtGui.QIcon('../../images/openProject.png'),
            '<b>Open Project</b>',
            self)
        self.openproj.setShortcut('Ctrl+O')
        self.openproj.triggered.connect(self.open_project)

        self.closeproj = QtGui.QAction(
            QtGui.QIcon('../../images/closeProject.png'),
            '<b>Close Project</b>',
            self)
        self.closeproj.setShortcut('Ctrl+X')
        self.closeproj.triggered.connect(self.close_project)

        self.helpfile = QtGui.QAction(
            QtGui.QIcon('../../images/helpProject.png'), '<b>Help</b>', self)
        self.helpfile.setShortcut('Ctrl+H')
        self.helpfile.triggered.connect(self.help_project)

        self.topToolbar = self.addToolBar('Top Tool Bar')
        self.topToolbar.addAction(self.newproj)
        self.topToolbar.addAction(self.openproj)

        self.topToolbar.addAction(self.closeproj)
        self.topToolbar.addAction(self.helpfile)

        # This part is setting fossee logo to the right
        # corner in the application window.
        self.spacer = QtGui.QWidget()
        self.spacer.setSizePolicy(
            QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding)
        self.topToolbar.addWidget(self.spacer)
        self.logo = QtGui.QLabel()
        self.logopic = QtGui.QPixmap(
            os.path.join(
                os.path.abspath('../..'),
                'images',
                'fosseeLogo.png'))
        self.logopic = self.logopic.scaled(
            QSize(150, 150), QtCore.Qt.KeepAspectRatio)
        self.logo.setPixmap(self.logopic)
        self.logo.setStyleSheet("padding:0 15px 0 0;")
        self.topToolbar.addWidget(self.logo)

        # Left Tool bar Action Widget
        self.kicad = QtGui.QAction(
            QtGui.QIcon('../../images/kicad.png'),
            '<b>Open Schematic</b>',
            self)
        self.kicad.triggered.connect(self.obj_kicad.openSchematic)

        self.conversion = QtGui.QAction(
            QtGui.QIcon('../../images/ki-ng.png'),
            '<b>Convert Kicad to Ngspice</b>',
            self)
        self.conversion.triggered.connect(self.obj_kicad.openKicadToNgspice)

        self.ngspice = QtGui.QAction(
            QtGui.QIcon('../../images/ngspice.png'),
            '<b>Simulation</b>',
            self)
        self.ngspice.triggered.connect(self.open_ngspice)

        self.model = QtGui.QAction(
            QtGui.QIcon('../../images/model.png'),
            '<b>Model Editor</b>',
            self)
        self.model.triggered.connect(self.open_modelEditor)

        self.subcircuit = QtGui.QAction(
            QtGui.QIcon('../../images/subckt.png'),
            '<b>Subcircuit</b>',
            self)
        self.subcircuit.triggered.connect(self.open_subcircuit)

        self.nghdl = QtGui.QAction(
            QtGui.QIcon('../../images/nghdl.png'),
            '<b>Nghdl</b>',
            self)
        self.nghdl.triggered.connect(self.open_nghdl)

        self.omedit = QtGui.QAction(
            QtGui.QIcon('../../images/omedit.png'),
            '<b>Modelica Converter</b>',
            self)
        self.omedit.triggered.connect(self.open_OMedit)

        self.omoptim = QtGui.QAction(
            QtGui.QIcon('../../images/omoptim.png'),
            '<b>OM Optimisation</b>',
            self)
        self.omoptim.triggered.connect(self.open_OMoptim)

        # Adding Action Widget to tool bar
        self.lefttoolbar = QtGui.QToolBar('Left ToolBar')
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.lefttoolbar)
        self.lefttoolbar.addAction(self.kicad)
        self.lefttoolbar.addAction(self.conversion)
        self.lefttoolbar.addAction(self.ngspice)
        self.lefttoolbar.addAction(self.model)
        self.lefttoolbar.addAction(self.subcircuit)
        self.lefttoolbar.addAction(self.nghdl)
        self.lefttoolbar.addAction(self.omedit)
        self.lefttoolbar.addAction(self.omoptim)
        self.lefttoolbar.setOrientation(QtCore.Qt.Vertical)
        self.lefttoolbar.setIconSize(QSize(40, 40))

    # This function closes the ongoing program(process).
    def closeEvent(self, event):
        '''
        When exit button is pressed a Message box pops out with
        exit message and buttons 'Yes', 'No'.

            1. If 'Yes' is pressed:
                - it checks that program(process) in procThread_list\
                    (list made in Appconfig.py):

                    - if available it terminates that program
                    - if the program(process) is not available,\
                        it checks for it
                      in process_obj (list made in Appconfig.py) if found it
                      closes the program.

            2. If 'No' is pressed:
                - the program just continues as it was doing earlier.
        '''
        exit_msg = "Are you sure you want to exit the program\
            ? All unsaved data will be lost."
        reply = QtGui.QMessageBox.question(
            self, 'Message', exit_msg, QtGui.QMessageBox.Yes,
            QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            for proc in self.obj_appconfig.procThread_list:
                try:
                    proc.terminate()
                except BaseException:
                    pass
            try:
                for process_object in self.obj_appconfig.process_obj:
                    try:
                        process_object.close()
                    except BaseException:
                        pass
            except BaseException:
                pass
            # Just checking if open project and New project window is open. If
            # yes just close it when application is closed
            try:
                self.project.close()
            except BaseException:
                pass
            event.accept()
            self.systemTrayIcon.showMessage('Exit', 'eSim is Closed.')

        elif reply == QtGui.QMessageBox.No:
            event.ignore()

    # This function closes the saved project.
    def close_project(self):
        """
        This function first checks whether project(file) is present in list.

            - If present:
                - it first kills that process-id.
                - closes that file.
                - Shows message "Current project <path of file> is closed"

            - If not present: pass
        """
        print("Function : Close Project")
        current_project = self.obj_appconfig.current_project['ProjectName']
        if current_project is None:
            pass
        else:
            temp = self.obj_appconfig.current_project['ProjectName']
            for pid in self.obj_appconfig.proc_dict[temp]:
                try:
                    os.kill(pid, 9)
                except BaseException:
                    pass
            self.obj_Mainview.obj_dockarea.closeDock()
            self.obj_appconfig.current_project['ProjectName'] = None
            self.systemTrayIcon.showMessage(
                'Close',
                'Current project ' +
                os.path.basename(current_project) +
                ' is Closed.')

    # This function call New Project Info class.
    def new_project(self):
        text, ok = QtGui.QInputDialog.getText(
            self, 'New Project Info', 'Enter Project Name:')
        if ok:
            self.projname = (str(text))
            self.project = NewProjectInfo()
            directory, filelist = self.project.createProject(self.projname)

            self.obj_Mainview.obj_projectExplorer.addTreeNode(
                directory, filelist)

        else:
            print("No new project created")
            self.obj_appconfig.print_info('No new project created')
            try:
                self.obj_appconfig.print_info(
                    'Current project is : ' +
                    self.obj_appconfig.current_project["ProjectName"])
            except BaseException:
                pass

    # This project call Open Project Info class
    def open_project(self):
        print("Function : Open Project")
        self.project = OpenProjectInfo()

        try:
            directory, filelist = self.project.body()
            self.obj_Mainview.obj_projectExplorer.addTreeNode(
                directory, filelist)
        except BaseException:
            pass

    # This page opens usermanual in dockarea.
    def help_project(self):
        """
        - It prints the message ""Function : Help""
        - Uses print_info() method of class Appconfig
          from Configuration/Appconfig.py file.
        - Call method usermanual() from ./DockArea.py.
        """
        print("Function : Help")
        self.obj_appconfig.print_info('Help is called')
        print("Current Project is : ", self.obj_appconfig.current_project)
        self.obj_Mainview.obj_dockarea.usermanual()

    # This Function execute ngspice on current project.
    def open_ngspice(self):
        self.projDir = self.obj_appconfig.current_project["ProjectName"]

        if self.projDir is not None:
            self.obj_Mainview.obj_dockarea.ngspiceEditor(self.projDir)

            currTime = time.time()
            count = 0
            while True:
                try:
                    st = os.stat(os.path.join(self.projDir, "plot_data_i.txt"))
                    if st.st_mtime >= currTime:
                        break
                except Exception:
                    pass
                time.sleep(0.2)

                # Fail Safe ===>
                count += 1
                if count >= 100:
                    raise Exception(
                        "ngspice taking too long, check netlist file")

            # Calling Python Plotting
            try:
                self.obj_Mainview.obj_dockarea.plottingEditor()
            except Exception as e:
                self.msg = QtGui.QErrorMessage(None)
                self.msg.showMessage(
                    'Error while opening python plotting Editor.'
                    ' Please look at console for more details')
                print("Exception Message:", str(e))
                self.obj_appconfig.print_error('Exception Message : ' + str(e))
                self.msg.setWindowTitle("Error Message")

        else:
            self.msg = QtGui.QErrorMessage()
            self.msg.showMessage(
                'Please select the project first.'
                ' You can either create new project or open existing project')
            self.msg.setWindowTitle("Error Message")

    # This function opens 'subcircuit' option in left-tool-bar.
    def open_subcircuit(self):
        """
        When 'subcircuit' icon is clicked wich is present in
        left-tool-bar of main page:

            - Meassge shown on screen "Subcircuit editor is called".
            - 'subcircuiteditor()' function is called using object
              'obj_dockarea' of class 'Mainview'.
        """
        print("Function : Subcircuit editor")
        self.obj_appconfig.print_info('Subcircuit editor is called')
        self.obj_Mainview.obj_dockarea.subcircuiteditor()

    # This function calls NGHDl option in left-tool-bar.
    def open_nghdl(self):
        """
        This function uses validateTool() method from
        Validation.py:

            - If 'nghdl' is present in executables list then
              it adds passes command 'nghdl -e' to WorkerThread class of
              Worker.py.
            - If 'nghdl' not present then it shows error message.
        """
        print("Function : Nghdl")
        self.obj_appconfig.print_info('Nghdl is called')

        if self.obj_validation.validateTool('nghdl'):
            self.cmd = 'nghdl -e'
            self.obj_workThread = Worker.WorkerThread(self.cmd)
            self.obj_workThread.start()

        else:
            self.msg = QtGui.QErrorMessage(None)
            self.msg.showMessage('Error while opening nghdl.\
                Please make sure nghdl is installed')
            self.obj_appconfig.print_error('Error while opening nghdl.\
                Please make sure nghdl is installed')
            self.msg.setWindowTitle('nghdl Error Message')

    # This function opens model editor option in left-tool-bar.
    def open_modelEditor(self):
        """
        When model editor icon is clicked which is present in
        left-tool-bar of main page:

            - Meassge shown on screen "Model editor is called".
            - 'modeleditor()' function is called using object
              'obj_dockarea' of class 'Mainview'.
        """
        print("Function : Model editor")
        self.obj_appconfig.print_info('Model editor is called')
        self.obj_Mainview.obj_dockarea.modelEditor()

    # This function call ngspice to OM edit converter
    # and then launch OM edit.
    def open_OMedit(self):
        self.obj_appconfig.print_info('OM edit is called')
        self.projDir = self.obj_appconfig.current_project["ProjectName"]

        if self.projDir is not None:
            if self.obj_validation.validateCirOut(self.projDir):
                self.projName = os.path.basename(self.projDir)
                self.ngspiceNetlist = os.path.join(
                    self.projDir, self.projName + ".cir.out")
                self.modelicaNetlist = os.path.join(
                    self.projDir, self.projName + ".mo")

                self.obj_Mainview.obj_dockarea.modelicaEditor(self.projDir)

            else:
                self.msg = QtGui.QErrorMessage()
                self.msg.showMessage(
                    'Current project does not contain any ngspice file.\
                        Please create ngspice file with extension .cir.out')
                self.msg.setWindowTitle("Missing Ngspice netlist")
        else:
            self.msg = QtGui.QErrorMessage()
            self.msg.showMessage(
                'Please select the project first.\
                    You can either create new project\
                        or open existing project')
            self.msg.setWindowTitle("Error Message")

    # sdf
    def open_OMoptim(self):
        """
        This function uses validateTool() method from
        Validation.py:

            - If 'OMOptim' is present in executables list then
              it adds passes command 'OMOptim' to WorkerThread class of
              Worker.py.
            - If 'OMOptim' not present then it shows error message with
              link to download it on Linux and Windows.
        """
        print("Function : OM Optim")
        self.obj_appconfig.print_info('OM Optim is called')
        # Check if OMOptim is installed
        if self.obj_validation.validateTool("OMOptim"):
            # Creating a command to run
            self.cmd = "OMOptim"
            self.obj_workThread = Worker.WorkerThread(self.cmd)
            self.obj_workThread.start()
        else:
            self.msg = QtGui.QMessageBox()
            self.msgContent = (
                "There was an error while opening OMOptim.<br/>"
                "Please make sure OpenModelica is installed in your"
                " system.<br/>"
                "To install it on Linux : Go to <a href="
                "https://www.openmodelica.org/download/download-linux"
                ">OpenModelica Linux</a> and install nightly build"
                " release.<br/>"
                "To install it on Windows : Go to <a href="
                "https://www.openmodelica.org/download/download-windows"
                ">OpenModelica Windows</a> and install latest version.<br/>"
                )
            self.msg.setTextFormat(QtCore.Qt.RichText)
            self.msg.setText(self.msgContent)
            self.msg.setWindowTitle("Error Message")
            self.obj_appconfig.print_info(self.msgContent)
            self.msg.exec_()


# This class initialize the Main View of Application
class MainView(QtGui.QWidget):
    """
    This class defines whole view and style of main page:

        - Position of tool bars:

         - Top tool bar.
         - Left tool bar.

        - Project explorer Area.
        - Dock area.
        - Console area.

    """

    def __init__(self, *args):
        # call init method of superclass
        QtGui.QWidget.__init__(self, *args)

        self.obj_appconfig = Appconfig()

        self.leftSplit = QtGui.QSplitter()
        self.middleSplit = QtGui.QSplitter()

        self.mainLayout = QtGui.QVBoxLayout()
        # Intermediate Widget
        self.middleContainer = QtGui.QWidget()
        self.middleContainerLayout = QtGui.QVBoxLayout()

        # Area to be included in MainView
        self.noteArea = QtGui.QTextEdit()
        self.noteArea.setReadOnly(True)
        self.obj_appconfig.noteArea['Note'] = self.noteArea
        self.obj_appconfig.noteArea['Note'].append(
            '        eSim Started......')
        self.obj_appconfig.noteArea['Note'].append('Project Selected : None')
        self.obj_appconfig.noteArea['Note'].append('\n')
        # CSS
        self.noteArea.setStyleSheet(" \
        QWidget { border-radius: 15px; border: 1px \
            solid gray; padding: 5px; } \
        ")

        self.obj_dockarea = DockArea.DockArea()
        self.obj_projectExplorer = ProjectExplorer.ProjectExplorer()

        # Adding content to vertical middle Split.
        self.middleSplit.setOrientation(QtCore.Qt.Vertical)
        self.middleSplit.addWidget(self.obj_dockarea)
        self.middleSplit.addWidget(self.noteArea)

        # Adding middle split to Middle Container Widget
        self.middleContainerLayout.addWidget(self.middleSplit)
        self.middleContainer.setLayout(self.middleContainerLayout)

        # Adding content of left split
        self.leftSplit.addWidget(self.obj_projectExplorer)
        self.leftSplit.addWidget(self.middleContainer)

        # Adding to main Layout
        self.mainLayout.addWidget(self.leftSplit)
        self.leftSplit.setSizes([self.width() / 4.5, self.height()])
        self.middleSplit.setSizes([self.width(), self.height() / 2])
        self.setLayout(self.mainLayout)


# It is main function of the module.It starts the application
def main(args):
    """
    The splash screen opened at the starting of screen is performed
    by this function.
    """
    print("Starting eSim......")
    app = QtGui.QApplication(args)

    splash_pix = QtGui.QPixmap('../../images/splash_screen_esim.png')
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    appView = Application()
    appView.splash = splash
    appView.obj_workspace.returnWhetherClickedOrNot(appView)
    appView.hide()
    appView.obj_workspace.show()
    sys.exit(app.exec_())


# Call main function


if __name__ == '__main__':
    # Create and display the splash screen
    main(sys.argv)
