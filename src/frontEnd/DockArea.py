from PyQt5 import QtCore, QtWidgets
from ngspiceSimulation.pythonPlotting import plotWindow
from ngspiceSimulation.NgspiceWidget import NgspiceWidget
from configuration.Appconfig import Appconfig
from modelEditor.ModelEditor import ModelEditorclass
from subcircuit.Subcircuit import Subcircuit
from maker.makerchip import makerchip
from kicadtoNgspice.KicadtoNgspice import MainWindow
from browser.Welcome import Welcome
from browser.UserManual import UserManual
from ngspicetoModelica.ModelicaUI import OpenModelicaEditor
from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
import os
from converter.pspiceToKicad import PspiceConverter
from converter.ltspiceToKicad import LTspiceConverter
from converter.LtspiceLibConverter import LTspiceLibConverter
from converter.libConverter import PspiceLibConverter
from converter.browseSchematics import browse_path
dockList = ['Welcome']
count = 1
dock = {}


class DockArea(QtWidgets.QMainWindow):
    """
    This class contains function for designing UI of all the editors
    in dock area part:

        - Test Editor.
        - Model Editor.
        - Python Plotting.
        - Ngspice Editor.
        - Kicad to Ngspice Editor.
        - Subcircuit Editor.
        - Modelica editor.
    """

    def __init__(self, is_dark_theme=False):
        """This act as constructor for class DockArea."""
        QtWidgets.QMainWindow.__init__(self)
        self.obj_appconfig = Appconfig()
        
        # Store the theme setting
        self.is_dark_theme = is_dark_theme

        # Set the dock options for better tab appearance
        self.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks | 
                          QtWidgets.QMainWindow.AnimatedDocks)
        
        # Set tab position to top
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QtWidgets.QTabWidget.North)
        
        # Set document mode for modern look
        self.setDocumentMode(True)

        # Set custom style for dock widgets and tabs
        self.setStyleSheet("""
            QDockWidget {
                border: 1px solid #23273a;
                border-radius: 4px;
                margin-top: 4px;
            }
            
            QDockWidget::title {
                text-align: center;
                background: #ffffff;
                color: #2c3e50;
                padding: 6px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-weight: bold;
                font-size: 9pt;
                border: none;
            }
            
            QTabBar::tab {
                background: #808080;
                color: #2c3e50;
                border: 1px solid #e1e4e8;
                border-bottom: none;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                min-width: 180px;
                max-width: 400px;
                font-weight: 600;
                font-size: 8pt;
                letter-spacing: 0.3px;
                padding: 6px 24px;
                margin-right: 4px;
            }
            
            QTabBar::tab:selected {
                background: #8c8c8c;
                color: #1976d2;
                border: 1.5px solid #1976d2;
                border-bottom: 2px solid #1976d2;
            }
            
            QTabBar::tab:hover:!selected {
                background:#e3f0fc;
                color: #1976d2;
            }
            
            # QTabWidget::pane {
            #     border: 1px solid #23273a;
            #     border-radius: 4px;
            #     background: #181b24;
            # }
            
            QTabWidget::tab-bar {
                alignment: center;
            }

            # QTabBar::close-button {
            #     image: url(close.png);
            #     subcontrol-position: right;
            # }
            
            # QTabBar::close-button:hover {
            #     background: #ff4444;
            #     border-radius: 2px;
            # }
        """)

        for dockName in dockList:
            dock[dockName] = QtWidgets.QDockWidget(dockName)
            dock[dockName].setFeatures(QtWidgets.QDockWidget.DockWidgetMovable | 
                                     QtWidgets.QDockWidget.DockWidgetFloatable)
            self.welcomeWidget = QtWidgets.QWidget()
            self.welcomeLayout = QtWidgets.QVBoxLayout()
            # Set smaller margins for the layout
            self.welcomeLayout.setContentsMargins(4, 4, 4, 4)
            self.welcomeLayout.setSpacing(4)
            self.welcomeLayout.addWidget(Welcome(is_dark_theme))  # Call browser

            # Adding to main Layout
            self.welcomeWidget.setLayout(self.welcomeLayout)
            dock[dockName].setWidget(self.welcomeWidget)
            self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock[dockName])

        self.show()

    def update_theme(self, is_dark_theme):
        """Update the theme setting and propagate to child widgets."""
        self.is_dark_theme = is_dark_theme
        
        # Update the plotting window theme if it exists
        try:
            from ngspiceSimulation.pythonPlotting import plotWindow
            if plotWindow.instance:
                plotWindow.instance.is_dark_theme = is_dark_theme
                plotWindow.instance.toggle_theme()  # This will update the theme
        except Exception as e:
            print(f"Error updating plotting window theme: {e}")

    def createTestEditor(self):
        """This function create widget for Library Editor"""
        global count

        self.testWidget = QtWidgets.QWidget()
        self.testArea = QtWidgets.QTextEdit()
        self.testLayout = QtWidgets.QVBoxLayout()
        # Set smaller margins for the layout
        self.testLayout.setContentsMargins(4, 4, 4, 4)
        self.testLayout.setSpacing(4)
        self.testLayout.addWidget(self.testArea)

        # Adding to main Layout
        self.testWidget.setLayout(self.testLayout)
        dock['Tips-' + str(count)] = QtWidgets.QDockWidget('Tips-' + str(count))
        dock['Tips-' + str(count)].setWidget(self.testWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock['Tips-' + str(count)])
        self.tabifyDockWidget(dock['Welcome'], dock['Tips-' + str(count)])

        dock['Tips-' + str(count)].setVisible(True)
        dock['Tips-' + str(count)].setFocus()
        dock['Tips-' + str(count)].raise_()

        temp = self.obj_appconfig.current_project['ProjectName']
        if temp:
            self.obj_appconfig.dock_dict[temp].append(dock['Tips-' + str(count)])
        count = count + 1

    def plottingEditor(self):
        """This function creates or updates the widget for interactive PythonPlotting, now as a single instance with navigation."""
        try:
            self.projDir = self.obj_appconfig.current_project["ProjectName"]
            if not self.projDir:
                raise ValueError("No project is currently open. Please open a project first.")
            
            self.projName = os.path.basename(self.projDir)
            
            # Check if required files exist
            plot_data_v = os.path.join(self.projDir, "plot_data_v.txt")
            plot_data_i = os.path.join(self.projDir, "plot_data_i.txt")
            
            if not os.path.exists(plot_data_v):
                raise FileNotFoundError(f"Required file not found: {plot_data_v}\nPlease run a simulation first to generate plot data.")
            
            if not os.path.exists(plot_data_i):
                raise FileNotFoundError(f"Required file not found: {plot_data_i}\nPlease run a simulation first to generate plot data.")
            
            # Get the current theme from the main application
            # Try to find the main application window to get the current theme
            main_window = None
            current_widget = self
            while current_widget.parent() is not None:
                current_widget = current_widget.parent()
                if hasattr(current_widget, 'is_dark_theme'):
                    main_window = current_widget
                    break
            
            # Use the current theme from main window, or default to False (light theme)
            is_dark_theme = getattr(main_window, 'is_dark_theme', False) if main_window else False
            
            # Use the static add_output method to manage outputs and window
            from ngspiceSimulation.pythonPlotting import plotWindow
            plotWindow.add_output(self.projDir, self.projName, is_dark_theme=is_dark_theme)
            # Bring the window to focus if it exists
            if plotWindow.instance:
                plotWindow.instance.show()
                plotWindow.instance.raise_()
        except Exception as e:
            print(f"Error in plottingEditor: {e}")
            raise

    def ngspiceEditor(self, projName, netlist, simEndSignal, plotFlag):
        """ This function creates widget for Ngspice window."""
        global count
        self.ngspiceWidget = QtWidgets.QWidget()

        self.ngspiceLayout = QtWidgets.QVBoxLayout()
        # Set smaller margins for the layout
        self.ngspiceLayout.setContentsMargins(4, 4, 4, 4)
        self.ngspiceLayout.setSpacing(4)
        self.ngspiceLayout.addWidget(NgspiceWidget(netlist, simEndSignal, plotFlag))

        # Adding to main Layout
        self.ngspiceWidget.setLayout(self.ngspiceLayout)
        dockName = f'Simulation-{projName}-'
        dock[dockName + str(count)] = QtWidgets.QDockWidget(dockName + str(count))
        dock[dockName + str(count)].setWidget(self.ngspiceWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock[dockName + str(count)])
        self.tabifyDockWidget(dock['Welcome'], dock[dockName + str(count)])

        dock[dockName + str(count)].setVisible(True)
        dock[dockName + str(count)].setFocus()
        dock[dockName + str(count)].raise_()

        temp = self.obj_appconfig.current_project['ProjectName']
        if temp:
            self.obj_appconfig.dock_dict[temp].append(dock[dockName + str(count)])
        count = count + 1

    def eSimConverter(self):
        """This function creates a widget for eSimConverter."""
        global count

        dockName = 'Schematics Converter-'

        self.eConWidget = QtWidgets.QWidget()
        self.eConLayout = QVBoxLayout()  # QVBoxLayout for the main layout

        # Set margins and spacing for better layout
        self.eConLayout.setContentsMargins(15, 20, 15, 15)
        self.eConLayout.setSpacing(15)

        # Create a group box for the converter section
        converter_group = QtWidgets.QGroupBox("Schematic Converter")
        
        converter_layout = QVBoxLayout()
        converter_layout.setContentsMargins(15, 20, 15, 15)
        converter_layout.setSpacing(15)

        file_path_layout = QHBoxLayout()  # QHBoxLayout for file path line
        lib_path_layout = QHBoxLayout()

        file_path_text_box = QLineEdit()
        file_path_text_box.setFixedHeight(40)
        file_path_text_box.setMinimumWidth(600)
        file_path_text_box.setPlaceholderText("Select a schematic file to convert...")
        file_path_layout.setAlignment(Qt.AlignCenter)
        file_path_layout.addWidget(file_path_text_box)

        browse_button = QPushButton("Browse Files")
        browse_button.setFixedSize(140, 40)
        browse_button.clicked.connect(lambda: browse_path(self,file_path_text_box))
        file_path_layout.addWidget(browse_button)

        converter_layout.addLayout(file_path_layout)  # Add file path layout to converter layout

        button_layout = QHBoxLayout()  # QHBoxLayout for the buttons
        button_layout.setSpacing(15)  # Add spacing between buttons

        self.pspice_converter = PspiceConverter(self)
        self.ltspice_converter = LTspiceConverter(self)
        self.pspiceLib_converter = PspiceLibConverter(self)
        self.ltspiceLib_converter = LTspiceLibConverter(self)

        upload_button2 = QPushButton("Convert PSpice Library")
        upload_button2.setMinimumSize(280, 45)
        upload_button2.clicked.connect(lambda: self.pspiceLib_converter.upload_file_Pspice(file_path_text_box.text()))
        button_layout.addWidget(upload_button2)

        upload_button1 = QPushButton("Convert PSpice Schematics")
        upload_button1.setMinimumSize(280, 45)
        upload_button1.clicked.connect(lambda: self.pspice_converter.upload_file_Pspice(file_path_text_box.text()))
        button_layout.addWidget(upload_button1)

        upload_button3 = QPushButton("Convert LTspice Library")
        upload_button3.setMinimumSize(280, 45)
        upload_button3.clicked.connect(lambda: self.ltspiceLib_converter.upload_file_LTspice(file_path_text_box.text()))
        button_layout.addWidget(upload_button3)

        upload_button = QPushButton("Convert LTspice Schematics")
        upload_button.setMinimumSize(280, 45)
        upload_button.clicked.connect(lambda: self.ltspice_converter.upload_file_LTspice(file_path_text_box.text()))
        button_layout.addWidget(upload_button)

        converter_layout.addLayout(button_layout)
        converter_group.setLayout(converter_layout)
        self.eConLayout.addWidget(converter_group)

        # Add the description HTML content with theme-responsive styling
        description_html = """
            <html>
                <head>
                    <style>
                        body {
                            font-family: 'Segoe UI', 'Arial', sans-serif;
                            margin: 0px;
                            padding: 20px;
                            border: 2px solid;
                            border-radius: 14px;
                            font-size: 12px;
                            line-height: 1.5;
                        }

                        h1{
                            font-weight: bold;
                            font-size: 16px;
                            padding: 10px 0;
                            margin: 0 0 15px 0;
                            border-bottom: 2px solid;
                        }
                        
                        p {
                            margin: 10px 0;
                            text-align: justify;
                        }
                        
                        b {
                            font-weight: 600;
                        }
                    </style>
                </head>

                <body>
                    <h1>About eSim Converter</h1>
                    <p>
                        <b>Pspice to eSim</b> will convert the PSpice Schematic and Library files to KiCad Schematic and
                        Library files respectively with proper mapping of the components and the wiring. By this way one 
                        will be able to simulate their schematics in PSpice and get the PCB layout in KiCad.
                    </p>
                    <p>
                        <b>LTspice to eSim</b> will convert symbols and schematics from LTspice to Kicad. The goal is to design and
                        simulate under LTspice and to automatically transfer the circuit under Kicad to draw the PCB.
                    </p>
                </body>
            </html>
        """

        self.description_label = QLabel()
        self.description_label.setFixedHeight(180)
        self.description_label.setMinimumWidth(950)
        self.description_label.setAlignment(Qt.AlignTop)
        self.description_label.setWordWrap(True)
        self.description_label.setText(description_html)
        self.eConLayout.addWidget(self.description_label)  # Add the description label to the layout

        self.eConWidget.setLayout(self.eConLayout)

        dock[dockName + str(count)] = QtWidgets.QDockWidget(dockName + str(count))
        dock[dockName + str(count)].setWidget(self.eConWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock[dockName + str(count)])
        self.tabifyDockWidget(dock['Welcome'], dock[dockName + str(count)])

        dock[dockName + str(count)].setVisible(True)
        dock[dockName + str(count)].setFocus()
        dock[dockName + str(count)].raise_()

        count = count + 1

    def modelEditor(self):
        """This function creates a widget for model editor and ensures the correct theme is applied."""
        global count

        self.modelwidget = QtWidgets.QWidget()
        self.modellayout = QtWidgets.QVBoxLayout()
        self.modellayout.setContentsMargins(4, 4, 4, 4)
        self.modellayout.setSpacing(4)
        # --- Create the actual ModelEditorclass widget and store reference ---
        self.modeleditor_instance = ModelEditorclass()
        self.modellayout.addWidget(self.modeleditor_instance)

        self.modelwidget.setLayout(self.modellayout)
        dock['Model Editor-' + str(count)] = QtWidgets.QDockWidget('Model Editor-' + str(count))
        dock['Model Editor-' + str(count)].setWidget(self.modelwidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock['Model Editor-' + str(count)])
        self.tabifyDockWidget(dock['Welcome'], dock['Model Editor-' + str(count)])

        dock['Model Editor-' + str(count)].setVisible(True)
        dock['Model Editor-' + str(count)].setFocus()
        dock['Model Editor-' + str(count)].raise_()

        # --- Ensure the correct theme is applied immediately ---
        app_parent = self.parent()
        is_dark_theme = False
        while app_parent is not None:
            if hasattr(app_parent, 'is_dark_theme'):
                is_dark_theme = app_parent.is_dark_theme
                break
            app_parent = app_parent.parent() if hasattr(app_parent, 'parent') else None
        if hasattr(self, 'modeleditor_instance') and hasattr(self.modeleditor_instance, 'set_theme'):
            self.modeleditor_instance.set_theme(is_dark_theme)

        temp = self.obj_appconfig.current_project['ProjectName']
        if temp:
            self.obj_appconfig.dock_dict[temp].append(dock['Model Editor-' + str(count)])
        count = count + 1

    def kicadToNgspiceEditor(self, clarg1, clarg2=None):
        """
        This function is creating Editor UI for Kicad to Ngspice conversion.
        """
        global count

        projDir = self.obj_appconfig.current_project["ProjectName"]
        projName = os.path.basename(projDir)
        dockName = f'Netlist-{projName}-'

        self.kicadToNgspiceWidget = QtWidgets.QWidget()
        self.kicadToNgspiceLayout = QtWidgets.QVBoxLayout()
        self.kicadToNgspiceLayout.addWidget(MainWindow(clarg1, clarg2))

        self.kicadToNgspiceWidget.setLayout(self.kicadToNgspiceLayout)
        dock[dockName + str(count)] = \
            QtWidgets.QDockWidget(dockName + str(count))
        dock[dockName +
             str(count)].setWidget(self.kicadToNgspiceWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock[dockName + str(count)])
        self.tabifyDockWidget(dock['Welcome'],
                              dock[dockName + str(count)])

        # CSS
        dock[dockName + str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray;\
            padding: 5px; width: 200px; height: 150px;  } \
        ")

        dock[dockName + str(count)].setVisible(True)
        dock[dockName + str(count)].setFocus()
        dock[dockName + str(count)].raise_()
        dock[dockName + str(count)].activateWindow()

        temp = self.obj_appconfig.current_project['ProjectName']
        if temp:
            self.obj_appconfig.dock_dict[temp].append(
                dock[dockName + str(count)]
            )
        count = count + 1

    def subcircuiteditor(self):
        """This function creates a widget for different subcircuit options."""
        global count

        projDir = self.obj_appconfig.current_project["ProjectName"]

        """ Checks projDir variable has valid value 
        & is not None before calling os.path.basename """

        if projDir is not None:
            projName = os.path.basename(projDir)
            dockName = f'Subcircuit-{projName}-'

            self.subcktWidget = QtWidgets.QWidget()
            self.subcktLayout = QtWidgets.QVBoxLayout()
            self.subcktLayout.addWidget(Subcircuit(self))

            self.subcktWidget.setLayout(self.subcktLayout)
            dock[dockName +
                str(count)] = QtWidgets.QDockWidget(dockName
                                                    + str(count))
            dock[dockName + str(count)] \
                .setWidget(self.subcktWidget)
            self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                            dock[dockName + str(count)])
            self.tabifyDockWidget(dock['Welcome'],
                                dock[dockName + str(count)])

            # CSS
            dock[dockName + str(count)].setStyleSheet(" \
            .QWidget { border-radius: 15px; border: 1px solid gray;\
                padding: 5px; width: 200px; height: 150px;  } \
            ")

            dock[dockName + str(count)].setVisible(True)
            dock[dockName + str(count)].setFocus()
            dock[dockName + str(count)].raise_()

            count = count + 1

        else:
            """ when projDir is None that is clicking on subcircuit icon
                without any project selection """
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                'Please select the project first.'
                ' You can either create new project or open existing project'
            )
            self.msg.exec_()

    def makerchip(self):
        """This function creates a widget for Makerchip/NgVeri and ensures the correct theme is applied."""
        global count

        projDir = self.obj_appconfig.current_project["ProjectName"]
        if projDir is None:
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                'Please select the project first.'
                ' You can either create new project or open existing project'
            )
            self.msg.exec_()
            return
        projName = os.path.basename(projDir)
        dockName = f'Makerchip-{projName}-'

        self.makerWidget = QtWidgets.QWidget()
        self.makerLayout = QtWidgets.QVBoxLayout()
        # --- Create the actual makerchip widget and store reference ---
        self.makerchip_instance = makerchip(self)
        self.makerLayout.addWidget(self.makerchip_instance)
        self.makerWidget.setLayout(self.makerLayout)
        dock[dockName + str(count)] = QtWidgets.QDockWidget(dockName + str(count))
        dock[dockName + str(count)].setWidget(self.makerWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock[dockName + str(count)])
        self.tabifyDockWidget(dock['Welcome'], dock[dockName + str(count)])

        # CSS
        dock[dockName + str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray;\
            padding: 5px; width: 200px; height: 150px;  } \
        ")

        dock[dockName + str(count)].setVisible(True)
        dock[dockName + str(count)].setFocus()
        dock[dockName + str(count)].raise_()

        # --- Ensure the correct theme is applied immediately ---
        # Find the Application parent and get the current theme
        app_parent = self.parent()
        is_dark_theme = False
        while app_parent is not None:
            if hasattr(app_parent, 'is_dark_theme'):
                is_dark_theme = app_parent.is_dark_theme
                break
            app_parent = app_parent.parent() if hasattr(app_parent, 'parent') else None
        if hasattr(self, 'makerchip_instance') and hasattr(self.makerchip_instance, 'set_theme'):
            self.makerchip_instance.set_theme(is_dark_theme)

        count = count + 1

    def usermanual(self, is_dark_theme=False):
        """This function creates a widget for user manual."""
        global count
        self.usermanualWidget = QtWidgets.QWidget()
        self.usermanualLayout = QtWidgets.QVBoxLayout()
        self.usermanualLayout.addWidget(UserManual(is_dark_theme))

        self.usermanualWidget.setLayout(self.usermanualLayout)
        dock['User Manual-' +
             str(count)] = QtWidgets.QDockWidget('User Manual-' + str(count))
        dock['User Manual-' + str(count)].setWidget(self.usermanualWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock['User Manual-' + str(count)])
        self.tabifyDockWidget(dock['Welcome'],
                              dock['User Manual-' + str(count)])

        # CSS
        dock['User Manual-' + str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray;\
            padding: 5px; width: 200px; height: 150px;  } \
        ")

        dock['User Manual-' + str(count)].setVisible(True)
        dock['User Manual-' + str(count)].setFocus()
        dock['User Manual-' + str(count)].raise_()

        count = count + 1

    def modelicaEditor(self, projDir):
        """This function sets up the UI for ngspice to modelica conversion."""
        global count

        projName = os.path.basename(projDir)
        dockName = f'Modelica-{projName}-'

        self.modelicaWidget = QtWidgets.QWidget()
        self.modelicaLayout = QtWidgets.QVBoxLayout()
        self.modelicaLayout.addWidget(OpenModelicaEditor(projDir))

        self.modelicaWidget.setLayout(self.modelicaLayout)
        dock[dockName + str(count)
             ] = QtWidgets.QDockWidget(dockName + str(count))
        dock[dockName + str(count)] \
            .setWidget(self.modelicaWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock[dockName
                                + str(count)])
        self.tabifyDockWidget(dock['Welcome'], dock[dockName
                                                    + str(count)])

        dock[dockName + str(count)].setVisible(True)
        dock[dockName + str(count)].setFocus()
        dock[dockName + str(count)].raise_()

        # CSS
        dock[dockName + str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray;\
            padding: 5px; width: 200px; height: 150px;  } \
        ")
        temp = self.obj_appconfig.current_project['ProjectName']
        if temp:
            self.obj_appconfig.dock_dict[temp].append(
                dock[dockName + str(count)]
            )

        count = count + 1

    def closeDock(self):
        """
        This function checks for the project in **dock_dict**
        and closes it.
        """
        self.temp = self.obj_appconfig.current_project['ProjectName']
        for dockwidget in self.obj_appconfig.dock_dict[self.temp]:
            dockwidget.close()