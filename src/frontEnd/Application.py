# =========================================================================
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
#    MAINTAINED: Rahul Paknikar, rahulp@iitb.ac.in
#                Sumanto Kar, sumantokar@iitb.ac.in
#                Pranav P, pranavsdreams@gmail.com
#  ORGANIZATION: eSim Team at FOSSEE, IIT Bombay
#       CREATED: Tuesday 24 February 2015
#      REVISION: Wednesday 07 June 2023
# =========================================================================

import os
import sys
import traceback
import webbrowser

# Launched as a script (esim.bat / Ubuntu launcher run Application.py by
# path), so sys.path[0] is this file's dir (src/frontEnd) on every platform
# -> pathmagic is importable directly, and it puts src/ on the path for the
# top-level package imports below.
import pathmagic    # noqa:F401

from PyQt6 import QtGui, QtCore, QtWidgets
from configuration import Dialogs
from configuration import paths
from PyQt6.QtCore import QSize
from configuration.Appconfig import Appconfig
from frontEnd import ProjectExplorer
from frontEnd import TimeExplorer
from frontEnd import Workspace
from frontEnd import DockArea
from frontEnd import theme_utils
from projManagement.openProject import OpenProjectInfo
from projManagement.newProject import NewProjectInfo
from projManagement.Kicad import Kicad
from projManagement.Validation import Validation
from projManagement import Worker

# The AI assistant is an optional install; eSim must still start without it.
try:
    from frontEnd.Chatbot import ChatbotGUI
except ImportError:
    ChatbotGUI = None

# Its our main window of application.


def create_rounded_icon(path, radius_ratio=0.08):
    """Load a PNG and clip it to softly rounded corners so the colourful
    toolbar icons sit on the Aurora chrome without hard black squares."""
    pixmap = QtGui.QPixmap(path)
    if pixmap.isNull():
        return QtGui.QIcon()

    radius = int(min(pixmap.width(), pixmap.height()) * radius_ratio)

    rounded = QtGui.QPixmap(pixmap.size())
    rounded.fill(QtCore.Qt.GlobalColor.transparent)

    painter = QtGui.QPainter(rounded)
    painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
    path_obj = QtGui.QPainterPath()
    path_obj.addRoundedRect(0, 0, pixmap.width(), pixmap.height(), radius, radius)
    painter.setClipPath(path_obj)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()

    return QtGui.QIcon(rounded)


class _SnapshotWindow(QtWidgets.QWidget):
    """Independent top-level window hosting the Project Snapshots panel.

    Parentless + ``Qt.Window`` so the window manager draws a full title bar
    (drag to move, minimise, maximise, close) and gives it a taskbar entry.
    Geometry is saved whenever the user closes it, so the next open restores
    the same size and position. Closing only hides it; the kept TimeExplorer
    instance lives on for re-use."""

    def __init__(self):
        super().__init__(None)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Window
            | QtCore.Qt.WindowType.WindowMinimizeButtonHint
            | QtCore.Qt.WindowType.WindowMaximizeButtonHint
            | QtCore.Qt.WindowType.WindowCloseButtonHint)
        # Hard floor so the panel can never reopen as a compressed mess, even
        # if a stale/odd saved geometry tries to shrink it below usability.
        self.setMinimumSize(820, 600)

    def closeEvent(self, event):
        QtCore.QSettings('eSim', 'eSim').setValue(
            'snapshotsWindow/geometry', self.saveGeometry())
        super().closeEvent(event)


class Application(QtWidgets.QMainWindow):
    """This class initializes all objects used in this file."""
    simulationEndSignal = QtCore.pyqtSignal(QtCore.QProcess.ExitStatus, int)
    chatbot_dock = None

    def __init__(self, *args):
        """Initialize main Application window."""

        # Calling __init__ of super class
        QtWidgets.QMainWindow.__init__(self, *args)

        # Set slot for simulation end signal to plot simulation data
        self.simulationEndSignal.connect(self.plotSimulationData)

        #the plotFlag
        self.plotFlag = False

        # Seed Appconfig's shared state from disk once, up front. This was
        # formerly done at import time in Appconfig; doing it here (before any
        # object below reads the workspace/registry) keeps the module import
        # side-effect-free while preserving startup behaviour.
        Appconfig.load_workspace()
        Appconfig.load_config()
        Appconfig.load_project_explorer()

        # Creating require Object
        self.obj_workspace = Workspace.Workspace()
        self.obj_Mainview = MainView()
        self.obj_kicad = Kicad(self.obj_Mainview.obj_dockarea)
        self.obj_appconfig = Appconfig()
        self.obj_validation = Validation()
        # Initialize all widget
        self.setCentralWidget(self.obj_Mainview)
        self.initchatbot()   # before initToolBar: it builds the View menu
        self.initToolBar()
        self.initMenuAndStatus()

        self.setGeometry(self.obj_appconfig._app_xpos,
                         self.obj_appconfig._app_ypos,
                         self.obj_appconfig._app_width,
                         self.obj_appconfig._app_heigth)
        self.setWindowTitle(
            self.obj_appconfig._APPLICATION + "-" + self.obj_appconfig._VERSION
        )
        # NOTE: do NOT showMaximized() here. __init__ runs behind the splash and
        # main() immediately hide()s the window, so maximizing now is a full
        # layout+paint thrown away (and an extra transient top-level the flash
        # watcher used to catch). The workspace flow maximizes it once, when the
        # window is actually revealed (Workspace._finish_workspace_change).
        self.setWindowIcon(QtGui.QIcon(paths.image_path('logo.png')))

        # Aurora micro-interactions: install hover/press glow on the main
        # window's buttons. Gated inside (no-op unless the user enabled motion
        # in prefs); dock content added later re-installs this from DockArea.
        try:
            from frontEnd.motion import install_button_motion, apply_toolbar_depth
            install_button_motion(self)
            # Static floating-depth shadow on both toolbars (always on — only
            # the animated glow is perf-gated).
            apply_toolbar_depth(self)
        except Exception:
            pass

        self.systemTrayIcon = QtWidgets.QSystemTrayIcon(self)
        self.systemTrayIcon.setIcon(QtGui.QIcon(paths.image_path('logo.png')))
        self.systemTrayIcon.setVisible(True)

    def initchatbot(self):
        """
        This function initializes the ChatbotIcon and embeds the ChatbotGUI
        as a dockable panel on the right side of the main window.
        Clicking the icon toggles the panel open/closed.
        """
        self.chatbot_dock = None
        if ChatbotGUI is None:
            return
        self.chatbot_window = ChatbotGUI()

        # ── Dock widget (embedded in main window) ──────────────────────
        self.chatbot_dock = QtWidgets.QDockWidget("🤖 eSim AI Assistant", self)
        self.chatbot_dock.setObjectName("chatbotDock")
        self.chatbot_dock.setWidget(self.chatbot_window)
        self.chatbot_dock.setMinimumWidth(360)
        self.chatbot_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetClosable |
            QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.chatbot_dock)
        self.chatbot_dock.show()
        # When user closes dock via the X button, reposition the floating icon.
        # A bound slot (not a lambda) is disconnected by PyQt when the window
        # is destroyed, so the dock hiding during teardown cannot call into it.
        self.chatbot_dock.visibilityChanged.connect(self._on_chatbot_visibility)
        self.chatbot_dock.installEventFilter(self)

        # ── Floating icon button (bottom-right corner) ──────────────────
        self.chatboticon = QtWidgets.QPushButton(
            self, icon=QtGui.QIcon(paths.image_path('chatbot.png'))
        )
        self.chatboticon.setIconSize(QtCore.QSize(30, 30))
        self.chatboticon.setToolTip("Toggle AI Assistant")
        self.chatboticon.setStyleSheet("""
            QPushButton {
                border-radius: 26px;
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(0, 120, 212, 0.12);
                border: 2px solid #0078d4;
            }
            QPushButton:pressed {
                background-color: rgba(0, 63, 110, 0.18);
                border: 2px solid #003f6e;
            }
        """)
        self.chatboticon.setFixedSize(52, 52)
        self.chatboticon.clicked.connect(self.openChatbot)

    def openChatbot(self):
        """Toggle the chatbot dock panel open or closed."""
        if self.chatbot_dock.isVisible():
            self.chatbot_dock.hide()
        else:
            self.chatbot_dock.show()
            self.chatbot_dock.raise_()
            self.obj_appconfig.print_info('Chat Bot function is called')
        self._reposition_chatbot_icon()

    def _on_chatbot_visibility(self, _visible):
        self._reposition_chatbot_icon()

    def _reposition_chatbot_icon(self):
        """
        Keep the icon in the bottom-right corner of the visible area.
        When the dock is open, shift the icon left so it sits just
        outside the dock panel instead of on top of it.
        """
        margin = 12
        btn_w = self.chatboticon.width()
        btn_h = self.chatboticon.height()
        bottom_y = self.height() - btn_h - margin

        if self.chatbot_dock.isVisible():
            dock_w = self.chatbot_dock.width()
            # Clamp so a very wide dock cannot push the icon off-screen
            x = max(0, self.width() - dock_w - btn_w - margin)
        else:
            x = self.width() - btn_w - margin

        self.chatboticon.move(x, bottom_y)
        self.chatboticon.raise_()

    def eventFilter(self, obj, event):
        """
        Detect resize events on the dock widget so the icon stays aligned.
        """
        if (obj is self.chatbot_dock
                and event.type() == QtCore.QEvent.Type.Resize):
            self._reposition_chatbot_icon()
        return super().eventFilter(obj, event)

    def resizeEvent(self, event):
        """
        Adjust chatbot icon button position during window resize.
        """
        super().resizeEvent(event)
        if self.chatbot_dock is not None:
            self._reposition_chatbot_icon()

    def initToolBar(self):
        """
        This function initializes Tool Bars.
        It setups the icons, short-cuts and defining functonality for:

            - Top-tool-bar (New project, Open project, Close project, \
                Mode switch, Help option)
            - Left-tool-bar (Open Schematic, Convert KiCad to Ngspice, \
                Simuation, Model Editor, Subcircuit, NGHDL, Modelica \
                Converter, OM Optimisation)
        """
        from frontEnd.icon_paths import (
            timeline_icon, workspace_icon,
            help_icon, dev_docs_icon, settings_icon, home_icon,
            theme_toggle_icon
        )

        # Top Tool bar
        self.newproj = QtGui.QAction(
            create_rounded_icon(paths.image_path('newProject.png')),
            'New Project', self
        )
        self.newproj.setShortcut('Ctrl+N')
        self.newproj.setToolTip('New Project (Ctrl+N) — Create a new eSim project')
        self.newproj.triggered.connect(self.new_project)

        self.openproj = QtGui.QAction(
            create_rounded_icon(paths.image_path('openProject.png')),
            'Open Project', self
        )
        self.openproj.setShortcut('Ctrl+O')
        self.openproj.setToolTip('Open Project (Ctrl+O) — Open an existing project')
        self.openproj.triggered.connect(self.open_project)

        self.closeproj = QtGui.QAction(
            create_rounded_icon(paths.image_path('closeProject.png')),
            'Close Project', self
        )
        self.closeproj.setShortcut('Ctrl+X')
        self.closeproj.setToolTip('Close Project (Ctrl+X) — Close the active project')
        self.closeproj.triggered.connect(self.close_project)

        self.wrkspce = QtGui.QAction(
            workspace_icon(),
            'Workspace', self
        )
        self.wrkspce.setShortcut('Ctrl+W')
        self.wrkspce.setToolTip('Change Workspace (Ctrl+W) — Choose another workspace')
        self.wrkspce.triggered.connect(self.change_workspace)

        # Project Snapshots — back up & restore project files.
        self.timeline_action = QtGui.QAction(
            timeline_icon(),
            'Project Snapshots', self
        )
        self.timeline_action.setToolTip(
            'Project Snapshots — back up and restore your project files')
        self.timeline_action.triggered.connect(self.show_snapshots)
        # Back-compat alias (older code referenced act_snapshots).
        self.act_snapshots = self.timeline_action

        self.helpfile = QtGui.QAction(
            help_icon(),
            'User Manual', self
        )
        self.helpfile.setShortcut('F1')
        self.helpfile.setToolTip('User Manual (F1) — Open the eSim user manual')
        self.helpfile.triggered.connect(self.help_project)

        # added devDocs logo and called functions
        self.devdocs = QtGui.QAction(
            dev_docs_icon(),
            'Developer Docs', self
        )
        self.devdocs.setShortcut('Shift+F1')
        self.devdocs.setToolTip('Developer Docs (Shift+F1) — Open eSim developer docs')
        self.devdocs.triggered.connect(self.dev_docs)

        # Simulation-toolchain doctor: probes ngspice/iverilog/verilator/
        # ghdl/make/gcc (+ MSYS2 on Windows) and reports missing pieces with
        # fix hints. Same report as `esim --doctor`.
        self.doctor_action = QtGui.QAction(
            'Check Simulation Toolchain...', self
        )
        self.doctor_action.setToolTip(
            'Verify every simulator/HDL tool eSim needs is installed')
        self.doctor_action.triggered.connect(self.show_toolchain_doctor)

        # Preferences: Aurora theme (Dark/Light/System) + accent picker.
        # Gear icon is theme-aware; theme_utils.apply_theme also refreshes it.
        self.preferences_action = QtGui.QAction(
            settings_icon(), 'Preferences', self
        )
        self.preferences_action.setShortcut('Ctrl+,')
        self.preferences_action.setToolTip(
            'Preferences (Ctrl+,) — Configure eSim'
        )
        self.preferences_action.triggered.connect(self.open_preferences)

        # Exit / About actions live in the menu bar (built later).
        self.exit_action = QtGui.QAction('Exit', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setToolTip('Quit eSim (Ctrl+Q)')
        self.exit_action.setMenuRole(QtGui.QAction.MenuRole.QuitRole)
        self.exit_action.triggered.connect(self.close)

        self.about_action = QtGui.QAction('About eSim', self)
        self.about_action.setMenuRole(QtGui.QAction.MenuRole.AboutRole)
        self.about_action.triggered.connect(self.show_about)

        # Home: browser-style fallback that always returns to the Welcome
        # dashboard, from which the user can navigate anywhere again.
        self.home_action = QtGui.QAction('Home', self)
        self.home_action.setIcon(home_icon())
        self.home_action.setToolTip("Home - Back to the Welcome dashboard")
        self.home_action.triggered.connect(self.open_home)

        # --- Top toolbar: icon-only tool actions; labels live in the menu bar.
        self.topToolbar = self.addToolBar('Top Tool Bar')
        self.topToolbar.setObjectName('topToolbar')
        self.topToolbar.setMovable(True)
        self.topToolbar.setFloatable(False)
        self.topToolbar.setToolButtonStyle(
            QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.topToolbar.setIconSize(QSize(28, 28))
        self.topToolbar.addAction(self.home_action)
        self.topToolbar.addSeparator()
        self.topToolbar.addAction(self.newproj)
        self.topToolbar.addAction(self.openproj)
        self.topToolbar.addAction(self.closeproj)
        self.topToolbar.addSeparator()
        self.topToolbar.addAction(self.wrkspce)
        self.topToolbar.addSeparator()
        self.topToolbar.addAction(self.timeline_action)
        self.topToolbar.addSeparator()
        self.topToolbar.addAction(self.helpfile)
        self.topToolbar.addAction(self.devdocs)
        self.topToolbar.addAction(self.preferences_action)

        # ## This part is meant for SoC Generation which is currently  ##
        # ## under development and will be will be required in future. ##
        # self.soc = QtWidgets.QToolButton(self)
        # self.soc.setText('Generate SoC')
        # self.soc.setToolTip(
        #     '<b>SPICE to Verilog Conversion</b><br>' + \
        #     '<br>The feature is under development.' + \
        #     '<br>It will be released soon.' + \
        #     '<br><br>Thank you for your patience!!!'
        # )
        # self.soc.setStyleSheet(" \
        # QWidget { border-radius: 15px; border: 1px \
        #     solid gray; padding: 10px; margin-left: 20px; } \
        # ")
        # self.soc.clicked.connect(self.showSoCRelease)
        # self.topToolbar.addWidget(self.soc)

        # Expanding spacer pushes the view controls (zoom, theme toggle) and
        # the FOSSEE logo to the right edge — the 'view controls live right'
        # convention.
        self.topToolbar.addSeparator()
        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred)
        self.topToolbar.addWidget(self.spacer)

        # Zoom box rendered as one segmented pill: [ − ] 100% [ + ].
        # The pill (objectName zoomPill) paints the border/background; the
        # inner buttons are flat so the group reads as a single control that
        # visually matches the weight of the left-rail buttons. Every size
        # here is a 100%-zoom baseline -- _apply_view_control_metrics() is what
        # actually sizes the pill, and it re-runs on every zoom change.
        self.zoom_container = QtWidgets.QWidget()
        self.zoom_container.setObjectName("zoomPill")
        self.zoom_layout = QtWidgets.QHBoxLayout(self.zoom_container)
        zoom_layout = self.zoom_layout
        zoom_layout.setContentsMargins(3, 2, 3, 2)
        zoom_layout.setSpacing(0)

        self.zoom_out_btn = QtWidgets.QToolButton()
        self.zoom_out_btn.setText("−")
        self.zoom_out_btn.setToolTip("Decrease Zoom (-10%)")
        self.zoom_out_btn.setProperty("cssClass", "toolbarZoom")
        self.zoom_out_btn.clicked.connect(lambda: self.change_zoom(-10))
        zoom_layout.addWidget(self.zoom_out_btn)

        self.zoom_label = QtWidgets.QLabel(" 100% ")
        self.zoom_label.setObjectName("zoomLabel")
        self.zoom_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.zoom_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed)
        zoom_layout.addWidget(self.zoom_label)

        self.zoom_in_btn = QtWidgets.QToolButton()
        self.zoom_in_btn.setText("+")
        self.zoom_in_btn.setToolTip("Increase Zoom (+10%)")
        self.zoom_in_btn.setProperty("cssClass", "toolbarZoom")
        self.zoom_in_btn.clicked.connect(lambda: self.change_zoom(10))
        zoom_layout.addWidget(self.zoom_in_btn)

        self.topToolbar.addWidget(self.zoom_container)

        # Quick light/dark toggle on the right of the action bar. It carries a
        # real icon rather than the "◐" glyph so it scales off the toolbar's
        # icon size, exactly like the File / Workspace buttons on the left.
        self.theme_toggle_btn = QtWidgets.QToolButton()
        self.theme_toggle_btn.setObjectName("themeToggleBtn")
        self.theme_toggle_btn.setIcon(theme_toggle_icon())
        self.theme_toggle_btn.setToolTip("Toggle light / dark theme")
        self.theme_toggle_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.theme_toggle_btn.clicked.connect(self._toggle_theme)
        self.topToolbar.addWidget(self.theme_toggle_btn)

        # Init zoom label from saved preference.
        from frontEnd.theme_utils import get_preferences
        zp = get_preferences().get("zoom_level", 100)
        self.zoom_label.setText(f" {zp}% ")

        # Divider so the view controls aren't glued to the brand logo.
        self.topToolbar.addSeparator()

        # FOSSEE logo kept top-right of the action bar (eSim brand).
        # The *source* pixmap is kept unscaled: _apply_view_control_metrics()
        # re-derives the displayed height on every zoom change, and re-scaling
        # an already-scaled copy would compound the resampling loss. The
        # padding lives in the QSS (QLabel#brandLogo) rather than an inline
        # stylesheet, because build_qss() only rewrites px metrics inside the
        # .qss file -- px values in an inline sheet are invisible to the zoom
        # scaler and would stay frozen at their 100% size.
        self.logo = QtWidgets.QLabel()
        self.logo.setObjectName("brandLogo")
        self._logo_src = QtGui.QPixmap(paths.image_path('fosseeLogo.png'))
        self.topToolbar.addWidget(self.logo)

        # Left Tool bar Action Widget
        self.kicad = QtGui.QAction(
            create_rounded_icon(paths.image_path('kicad.png')),
            'Open Schematic', self
        )
        self.kicad.setShortcut("Ctrl+K")
        self.kicad.setToolTip(
            "Open Schematic (Ctrl+K) - Design your circuit in KiCad")
        self.kicad.triggered.connect(self.obj_kicad.openSchematic)

        self.conversion = QtGui.QAction(
            create_rounded_icon(paths.image_path('ki-ng.png')),
            'Convert to Ngspice', self
        )
        self.conversion.setShortcut("Ctrl+Alt+C")
        self.conversion.setToolTip(
            "Convert to Ngspice - Generate Ngspice netlist")
        self.conversion.triggered.connect(self.obj_kicad.openKicadToNgspice)

        self.ngspice = QtGui.QAction(
            create_rounded_icon(paths.image_path('ngspice.png')),
            'Simulate', self
        )
        self.ngspice.setShortcut("Ctrl+G")
        self.ngspice.setToolTip("Simulate (Ctrl+G) - Run circuit simulation")
        self.ngspice.triggered.connect(self.plotFlagPopBox)

        self.model = QtGui.QAction(
            create_rounded_icon(paths.image_path('model.png')),
            'Model Editor', self
        )
        self.model.setShortcut("Ctrl+M")
        self.model.setToolTip(
            "Model Editor (Ctrl+M) - Create or edit SPICE models")
        self.model.triggered.connect(self.open_modelEditor)

        self.subcircuit = QtGui.QAction(
            create_rounded_icon(paths.image_path('subckt.png')),
            'Subcircuit', self
        )
        self.subcircuit.setShortcut("Ctrl+B")
        self.subcircuit.setToolTip(
            "Subcircuit (Ctrl+B) - Build reusable subcircuits")
        self.subcircuit.triggered.connect(self.open_subcircuit)

        # NGHDL is no longer a standalone toolbar button: it now lives as a
        # tab inside the Makerchip dock (Makerchip / NgVeri / NGHDL), so model
        # creation for both Verilog and VHDL is in one place.
        self.makerchip = QtGui.QAction(
            create_rounded_icon(paths.image_path('makerchip.png')),
            'Model Creation (Verilog / VHDL)', self
        )
        self.makerchip.setToolTip(
            "Model Creation - Verilog / VHDL via Makerchip, NgVeri & NGHDL")
        self.makerchip.triggered.connect(self.open_makerchip)

        # NGHDL is a tab inside Model Creation; this is a shortcut that opens
        # Makerchip straight on the VHDL / NGHDL path so the feature stays
        # discoverable from the launcher even after the merge.
        self.nghdl = QtGui.QAction(
            create_rounded_icon(paths.image_path('nghdl.png')),
            'NGHDL', self
        )
        self.nghdl.setToolTip(
            "NGHDL - Add VHDL digital models (opens the VHDL tab in Makerchip)")
        self.nghdl.triggered.connect(self.open_nghdl)

        self.omedit = QtGui.QAction(
            create_rounded_icon(paths.image_path('omedit.png')),
            'Modelica Converter', self
        )
        self.omedit.setToolTip(
            "Modelica Converter - Convert to Modelica format")
        self.omedit.triggered.connect(self.open_OMedit)

        self.omoptim = QtGui.QAction(
            create_rounded_icon(paths.image_path('omoptim.png')),
            'OM Optimisation', self
        )
        self.omoptim.setToolTip("OM Optimisation - Run OpenModelica optimizer")
        self.omoptim.triggered.connect(self.open_OMoptim)

        self.conToeSim = QtGui.QAction(
            create_rounded_icon(paths.image_path('icon.png')),
            'Schematic Converter', self
        )
        self.conToeSim.setToolTip(
            "Schematic Converter - Import PSpice/LTspice files")
        self.conToeSim.triggered.connect(self.open_conToeSim)

        # Adding Action Widget to tool bar — grouped into labelled clusters so
        # a new user can parse the rail at a glance instead of staring at ten
        # cryptic icons.
        self.lefttoolbar = QtWidgets.QToolBar('Left ToolBar')
        self.lefttoolbar.setObjectName('leftToolBar')
        self.lefttoolbar.setMovable(True)
        self.addToolBar(QtCore.Qt.ToolBarArea.LeftToolBarArea, self.lefttoolbar)

        def _rail_caption(text):
            lbl = QtWidgets.QLabel(text)
            lbl.setProperty("cssClass", "railCaption")
            lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            return lbl

        # Pipeline order: Design the schematic -> Simulate it (netlist + run)
        # -> author Models that feed it -> Convert/interop with other tools.
        self.lefttoolbar.addWidget(_rail_caption("DESIGN"))
        self.lefttoolbar.addAction(self.kicad)
        self.lefttoolbar.addSeparator()
        self.lefttoolbar.addWidget(_rail_caption("SIMULATE"))
        self.lefttoolbar.addAction(self.conversion)
        self.lefttoolbar.addAction(self.ngspice)
        self.lefttoolbar.addSeparator()
        self.lefttoolbar.addWidget(_rail_caption("MODEL"))
        self.lefttoolbar.addAction(self.model)
        self.lefttoolbar.addAction(self.subcircuit)
        self.lefttoolbar.addAction(self.makerchip)
        self.lefttoolbar.addAction(self.nghdl)
        self.lefttoolbar.addSeparator()
        self.lefttoolbar.addWidget(_rail_caption("CONVERT"))
        self.lefttoolbar.addAction(self.omedit)
        self.lefttoolbar.addAction(self.omoptim)
        self.lefttoolbar.addAction(self.conToeSim)
        self.lefttoolbar.setOrientation(QtCore.Qt.Orientation.Vertical)

        # Both toolbars exist now, so size everything for the saved zoom.
        from frontEnd.theme_utils import get_preferences
        self._apply_view_control_metrics(
            get_preferences().get("zoom_level", 100))

        # Build the menu bar now that every toolbar action exists.
        self._build_menu_bar()

    def _build_menu_bar(self):
        """Build a proper menu bar with File/Edit/View/Tools/Help, wired to
        the same QAction objects the toolbar uses (our handlers)."""
        bar = self.menuBar()

        # ----- File -----
        file_menu = bar.addMenu('&File')
        file_menu.addAction(self.newproj)
        file_menu.addAction(self.openproj)
        file_menu.addAction(self.closeproj)
        file_menu.addSeparator()
        file_menu.addAction(self.wrkspce)
        file_menu.addSeparator()
        self.recent_projects_menu = file_menu.addMenu('Recent Projects')
        self._refresh_recent_projects_menu()
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # ----- Edit -----
        # Each action dispatches to the matching slot on whatever widget has
        # focus (a QLineEdit / QTextEdit / QScintilla editor), so the menu
        # actually does something instead of being five dead entries.
        edit_menu = bar.addMenu('&Edit')
        undo_action = QtGui.QAction('Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(lambda: self._edit_dispatch('undo'))
        edit_menu.addAction(undo_action)
        redo_action = QtGui.QAction('Redo', self)
        redo_action.setShortcut('Ctrl+Shift+Z')
        redo_action.triggered.connect(lambda: self._edit_dispatch('redo'))
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()
        cut_action = QtGui.QAction('Cut', self)
        # No Ctrl+X here: it belongs to Close Project; a duplicate would make
        # the shortcut ambiguous and break both.
        cut_action.triggered.connect(lambda: self._edit_dispatch('cut'))
        edit_menu.addAction(cut_action)
        copy_action = QtGui.QAction('Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(lambda: self._edit_dispatch('copy'))
        edit_menu.addAction(copy_action)
        paste_action = QtGui.QAction('Paste', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(lambda: self._edit_dispatch('paste'))
        edit_menu.addAction(paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.preferences_action)

        # ----- View -----
        view_menu = bar.addMenu('&View')
        fullscreen_action = QtGui.QAction('Toggle Fullscreen', self)
        fullscreen_action.setShortcut('F11')
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(self._toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        view_menu.addSeparator()
        project_explorer_action = QtGui.QAction('Project Explorer', self)
        project_explorer_action.setCheckable(True)
        project_explorer_action.setChecked(True)
        project_explorer_action.triggered.connect(
            lambda: self.obj_Mainview.obj_projectExplorer.setVisible(
                project_explorer_action.isChecked()
            )
        )
        view_menu.addAction(project_explorer_action)
        self.console_action = console_action = QtGui.QAction('Console', self)
        console_action.setCheckable(True)
        console_action.setChecked(False)
        console_action.triggered.connect(
            lambda: self.btn_log.setChecked(console_action.isChecked())
        )
        view_menu.addAction(console_action)
        if self.chatbot_dock is not None:
            assistant_action = self.chatbot_dock.toggleViewAction()
            assistant_action.setText('AI Assistant')
            view_menu.addAction(assistant_action)

        # ----- Tools -----
        tools_menu = bar.addMenu('&Tools')
        tools_menu.addAction(self.kicad)
        tools_menu.addAction(self.conversion)
        tools_menu.addAction(self.ngspice)
        tools_menu.addSeparator()
        tools_menu.addAction(self.model)
        tools_menu.addAction(self.subcircuit)
        tools_menu.addSeparator()
        tools_menu.addAction(self.makerchip)
        tools_menu.addAction(self.nghdl)
        tools_menu.addSeparator()
        tools_menu.addAction(self.omedit)
        tools_menu.addAction(self.omoptim)
        tools_menu.addSeparator()
        tools_menu.addAction(self.conToeSim)

        # The rail's rounded photo-style icons look butchered shrunk into 16px
        # menu rows, so hide them in the menu only -- the toolbar still shows
        # them (toolbar icon visibility is independent of this flag).
        for act in (self.kicad, self.conversion, self.ngspice, self.model,
                    self.subcircuit, self.makerchip, self.nghdl,
                    self.omedit, self.omoptim, self.conToeSim):
            act.setIconVisibleInMenu(False)

        # ----- Help -----
        help_menu = bar.addMenu('&Help')
        help_menu.addAction(self.helpfile)
        help_menu.addAction(self.devdocs)
        help_menu.addSeparator()
        help_menu.addAction(self.doctor_action)
        help_menu.addSeparator()
        help_menu.addAction(self.about_action)

        # Round the corners of every menu-bar dropdown (no black squares).
        try:
            from frontEnd.motion import make_menu_rounded
            for _m in bar.findChildren(QtWidgets.QMenu):
                make_menu_rounded(_m)
        except Exception:
            pass

    def _refresh_recent_projects_menu(self):
        """Populate the Recent Projects submenu from project_explorer."""
        if not hasattr(self, 'recent_projects_menu'):
            return
        self.recent_projects_menu.clear()
        recent = list(self.obj_appconfig.project_explorer.keys())
        recent = [p for p in recent if os.path.isdir(p)][:8]
        if not recent:
            empty = QtGui.QAction('(none)', self)
            empty.setEnabled(False)
            self.recent_projects_menu.addAction(empty)
            return
        for path in recent:
            action = QtGui.QAction(os.path.basename(path) or path, self)
            action.setToolTip(path)
            action.triggered.connect(
                lambda checked=False, p=path: self._open_recent_project(p)
            )
            self.recent_projects_menu.addAction(action)

    def _open_recent_project(self, path):
        """Open a recent project by path."""
        try:
            open_proj = OpenProjectInfo()
            directory, filelist = open_proj.body(path)
            if directory and filelist:
                self.obj_Mainview.obj_projectExplorer.addTreeNode(
                    directory, filelist
                )
                self.obj_appconfig.set_current_project(directory)
                project_name = self.obj_appconfig.get_proj_stem()
                self.obj_Mainview.obj_timeExplorer.load_snapshots(project_name)
                self.obj_appconfig.save_current_project()
        except Exception as e:
            from frontEnd.dialogs import show_error
            show_error(self, "Open Project", f"Could not open {path}:\n{e}")
            self.obj_appconfig.print_warning(
                f"Recent project open failed: {e}")

    def _toggle_fullscreen(self):
        if self.isFullScreen():
            self.showMaximized()
        else:
            self.showFullScreen()

    def _edit_dispatch(self, method):
        """Route an Edit-menu action (undo/redo/cut/copy/paste) to the
        matching slot on the currently focused widget, if it has one. Keeps
        the menu honest without owning any clipboard state itself."""
        widget = QtWidgets.QApplication.focusWidget()
        slot = getattr(widget, method, None)
        if callable(slot):
            slot()

    def _toggle_theme(self):
        """Flip between forced Light and Dark and persist the choice."""
        from frontEnd.theme_utils import get_preferences
        prefs = get_preferences()
        cur = prefs.get("theme_mode", "System")
        if cur == "Dark":
            new_mode = "Light"
        elif cur == "Light":
            new_mode = "Dark"
        else:
            from frontEnd.theme_utils import system_is_dark
            new_mode = "Light" if system_is_dark() else "Dark"
        prefs["theme_mode"] = new_mode
        path = paths.esim_config_path("preferences.json")
        try:
            paths.write_json_atomic(path, prefs)
        except Exception:
            pass
        app = QtWidgets.QApplication.instance()
        fn = getattr(app, "apply_theme", None)
        if callable(fn):
            fn()
        self._refresh_toolbar_icons()

    def change_zoom(self, delta):
        """Adjust the global UI zoom (50–300%); persists + re-applies theme."""
        from frontEnd.theme_utils import get_preferences
        prefs = get_preferences()
        current_zoom = prefs.get("zoom_level", 100)
        new_zoom = max(50, min(300, current_zoom + delta))
        if new_zoom != current_zoom:
            prefs["zoom_level"] = new_zoom
            path = paths.esim_config_path("preferences.json")
            try:
                paths.write_json_atomic(path, prefs)
            except Exception:
                pass
            # The readout is the part the user is watching, so it moves NOW.
            if hasattr(self, 'zoom_label'):
                self.zoom_label.setText(f" {new_zoom}% ")
            self._schedule_zoom_apply()

    def _schedule_zoom_apply(self):
        """Collapse a burst of zoom clicks into ONE app-wide restyle.

        Every click used to run a full ``QApplication.setStyleSheet()`` repolish
        synchronously, from inside the button's own ``clicked`` handler. Clicking
        the pill repeatedly (or holding it) therefore stacked repolish on
        repolish: each new one re-entered Qt's style engine while the previous
        one's deferred work -- the graphics-effect refresh, the palette-change
        handlers, the queued repaints -- was still in flight, and every widget
        pointer the outer pass was still holding could be freed under it. That
        window is where eSim was crashing (0xC0000005 inside setStyleSheet, no
        Python frame to blame; ~/.esim/crash.log 2026-07-25 session).

        The zoom label already updated, so the control still feels instant; the
        expensive part lands once, shortly after the last click. Timer is
        parented to the window, so it dies with it.
        """
        timer = getattr(self, '_zoom_apply_timer', None)
        if timer is None:
            timer = QtCore.QTimer(self)
            timer.setSingleShot(True)
            timer.setInterval(90)
            timer.timeout.connect(self._apply_zoom_now)
            self._zoom_apply_timer = timer
        timer.start()

    def _apply_zoom_now(self):
        """Trailing edge of _schedule_zoom_apply: restyle at the settled zoom."""
        from frontEnd.theme_utils import (get_preferences, apply_theme,
                                          reapply_zoom_metrics)
        zoom_level = get_preferences().get("zoom_level", 100)
        apply_theme(QtWidgets.QApplication.instance())
        self._apply_view_control_metrics(zoom_level)
        # Python-set sizes elsewhere in the app (panel widths, tile heights)
        # were measured at the zoom in force when their surface was built.
        # Re-measure the long-lived ones now that the sheet has settled, so
        # they do not stay frozen while the QSS metrics around them move.
        reapply_zoom_metrics(zoom_level)

    def _apply_view_control_metrics(self, zoom_level):
        """Scale every toolbar size that the QSS cannot reach.

        build_qss() multiplies the px metrics inside the stylesheet, but sizes
        set from Python (icon sizes, the zoom pill's width, the toggle's box)
        are invisible to it -- which is why the pill used to keep its 132px
        width while the text inside it shrank. Both toolbars' icon boxes are
        derived from the same numbers here so the zoom pill and the theme
        toggle stay the exact height of a top-toolbar icon button.
        """
        scale = zoom_level / 100.0
        top_icon = int(round(28 * scale))

        if hasattr(self, 'topToolbar'):
            self.topToolbar.setIconSize(QtCore.QSize(top_icon, top_icon))

        # Measure a real icon button rather than re-deriving its box from the
        # QSS metrics: Qt adds a few px of its own frame on top of the
        # padding/border/margin, and the pill has to land on the same height.
        btn_box = top_icon + 2 * int(round(7 * scale)) + 4
        if hasattr(self, 'topToolbar') and hasattr(self, 'home_action'):
            probe = self.topToolbar.widgetForAction(self.home_action)
            if probe is not None:
                probe.ensurePolished()
                btn_box = max(btn_box, probe.sizeHint().height())
        if hasattr(self, 'lefttoolbar'):
            s = int(round(40 * scale))
            self.lefttoolbar.setIconSize(QtCore.QSize(s, s))
        if hasattr(self, 'zoom_container'):
            self.zoom_container.setFixedHeight(btn_box)
            self.zoom_container.setMinimumWidth(int(round(132 * scale)))
            pad_h, pad_v = int(round(3 * scale)), int(round(2 * scale))
            self.zoom_layout.setContentsMargins(pad_h, pad_v, pad_h, pad_v)
        if hasattr(self, 'zoom_label'):
            self.zoom_label.setMinimumWidth(int(round(50 * scale)))
        if hasattr(self, 'theme_toggle_btn'):
            self.theme_toggle_btn.setFixedSize(btn_box, btn_box)
            self.theme_toggle_btn.setIconSize(
                QtCore.QSize(top_icon, top_icon))
        # The brand logo used to be frozen at a hard-coded scaled(150, 150)
        # box, which made it the top toolbar's *height floor*: at 50% zoom the
        # buttons only needed a ~34px bar, but the 55px-tall logo held it at
        # ~63px and left a band of dead space above and below the shrunken
        # icons. The same constant inverted at 300%, where the untouched 55px
        # logo sat beside 130px buttons. Sizing it off btn_box puts it on the
        # same "exactly one top-toolbar icon button tall" rule the zoom pill
        # and the theme toggle follow, so the bar shrinks and grows as one.
        src = getattr(self, '_logo_src', None)
        if hasattr(self, 'logo') and src is not None and not src.isNull():
            # Rasterise at the device pixel ratio so the logo stays sharp on
            # the fractionally-scaled displays PassThrough rounding gives us
            # (a 175% Windows display reports 1.75, not 2).
            dpr = self.logo.devicePixelRatioF()
            pix = src.scaledToHeight(
                max(1, int(round(max(12, int(btn_box)) * dpr))),
                QtCore.Qt.TransformationMode.SmoothTransformation)
            pix.setDevicePixelRatio(dpr)
            self.logo.setPixmap(pix)

    def _refresh_toolbar_icons(self):
        """Re-render the inline-SVG icons: they bake in the theme's foreground
        colour at build time, so a light/dark flip leaves them the old colour
        until they are rebuilt."""
        from frontEnd.icon_paths import (
            timeline_icon, workspace_icon, help_icon, dev_docs_icon,
            settings_icon, home_icon, theme_toggle_icon
        )
        for attr, factory in (
                ('home_action', home_icon),
                ('wrkspce', workspace_icon),
                ('timeline_action', timeline_icon),
                ('helpfile', help_icon),
                ('devdocs', dev_docs_icon),
                ('preferences_action', settings_icon)):
            if hasattr(self, attr):
                getattr(self, attr).setIcon(factory())
        if hasattr(self, 'theme_toggle_btn'):
            self.theme_toggle_btn.setIcon(theme_toggle_icon())

    def show_about(self):
        """Show the About eSim dialog with gradient-rich premium styling."""
        from frontEnd.dialogs import show_about_dialog
        show_about_dialog(self)

    def createPopupMenu(self):
        """Qt builds the toolbar/dock right-click menu internally and shows it
        immediately, so round its corners here before it is shown."""
        menu = super().createPopupMenu()
        if menu is not None:
            try:
                from frontEnd.motion import make_menu_rounded
                make_menu_rounded(menu)
            except Exception:
                pass
        return menu

    def _set_sim_status(self, state):
        """Tint the status-bar simulation dot: idle/running/ok/failed."""
        colors = {
            "idle": "#5F728D", "running": "#FACC15",
            "ok": "#42E6A4", "failed": "#FB7185",
        }
        c = colors.get(state, "#5F728D")
        if hasattr(self, 'sim_status_dot'):
            self.sim_status_dot.setStyleSheet(
                "color: %s; font-size: 13px; padding: 0 6px;" % c)

    def initMenuAndStatus(self):
        """No menu bar -- eSim is icon-driven. The snapshots panel is a
        top-toolbar icon (added in initToolBar), and the full console log
        toggles from a status-bar button while the status bar shows the latest
        log line."""
        # Status bar: mirrors the newest print_info/warning/error line; the
        # button toggles the full console log panel.
        bar = self.statusBar()
        self.obj_appconfig.__class__.statusbar = bar
        self.btn_log = QtWidgets.QToolButton()
        self.btn_log.setText('Console Log  ▴')
        self.btn_log.setCheckable(True)
        self.btn_log.setAutoRaise(True)
        self.btn_log.setToolTip('Show / hide the full console log')
        self.btn_log.toggled.connect(self._toggle_console_btn)
        # Keep the View ▸ Console menu checkbox in sync when the console is
        # toggled from this status-bar button (otherwise the menu tick went
        # stale). setChecked emits `toggled`, not `triggered`, so this does not
        # re-fire the menu action's handler -- no feedback loop.
        self.btn_log.toggled.connect(self.console_action.setChecked)
        bar.addPermanentWidget(self.btn_log)

        # Right-zone simulation-status dot: a tiny premium affordance —
        # grey idle, amber running, green ok, red failed.
        self.sim_status_dot = QtWidgets.QLabel("●")
        self.sim_status_dot.setObjectName("simStatusDot")
        self.sim_status_dot.setToolTip("Simulation status")
        self._set_sim_status("idle")
        bar.addPermanentWidget(self.sim_status_dot)
        bar.showMessage('eSim ready')

    def _toggle_console_btn(self, show):
        self.obj_Mainview.toggle_console(show)
        self.btn_log.setText('Console Log  ▾' if show else 'Console Log  ▴')

    def show_snapshots(self):
        """Open the Project Snapshots panel as a normal top-level window.

        It is an independent window with a real title bar — move it, minimise,
        maximise or close it, and it gets its own taskbar entry. It opens at a
        comfortable size the first time, then restores whatever size/position
        the user last left it at (persisted via QSettings)."""
        te = self.obj_Mainview.obj_timeExplorer
        te.reload()
        win = getattr(self, '_snap_win', None)
        if win is None:
            win = _SnapshotWindow()
            win.setWindowTitle('Project Snapshots')
            win.setWindowIcon(QtGui.QIcon(paths.image_path('logo.png')))
            lay = QtWidgets.QVBoxLayout(win)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.addWidget(te)

            geo = QtCore.QSettings('eSim', 'eSim').value(
                'snapshotsWindow/geometry')
            if geo is not None:
                win.restoreGeometry(geo)
            else:
                win.resize(960, 640)
            self._snap_win = win
        elif win.layout().indexOf(te) == -1:
            # te was reparented away (defensive); remount it.
            win.layout().addWidget(te)

        if win.isMinimized():
            win.showNormal()
        win.show()
        win.raise_()
        win.activateWindow()

    def _save_snapshot_dock_state(self):
        """Persist the snapshots window geometry and close it on app exit."""
        win = getattr(self, '_snap_win', None)
        if win is None:
            return
        QtCore.QSettings('eSim', 'eSim').setValue(
            'snapshotsWindow/geometry', win.saveGeometry())
        win.close()

    def plotFlagPopBox(self):
        """Ask whether the user wants native Ngspice plots, then run.

        If Yes, both the NgSpice and python plots are displayed; if No, only the
        python plots. The popup + its "remember my choice" persistence live in
        ``dialogs.ask_ngspice_plots`` (shared with TerminalUi's redo path)."""
        from frontEnd.dialogs import ask_ngspice_plots
        self.plotFlag = ask_ngspice_plots(self)
        self.open_ngspice()

    def closeEvent(self, event):
        '''
        This function closes the ongoing program (process).
        When exit button is pressed a Message box pops out with \
        exit message and buttons 'Yes', 'No'.

            1. If 'Yes' is pressed:
                - check that program (process) in procThread_list \
                  (a list made in Appconfig.py):

                    - if available it terminates that program.
                    - if the program (process) is not available, \
                      then check it in process_obj (a list made in \
                      Appconfig.py) and if found, it closes the program.

            2. If 'No' is pressed:
                - the program just continues as it was doing earlier.
        '''
        exit_msg = "Are you sure you want to exit the program?"
        exit_msg += " All unsaved data will be lost."
        reply = Dialogs.question(
            self, 'Message', exit_msg,
            QtWidgets.QMessageBox.StandardButton.Yes |
            QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self._save_snapshot_dock_state()
            # Terminate every tracked child in one batch with a shared wait
            # budget, so exit stays bounded (~2 s) regardless of how many
            # external windows are open, instead of blocking the GUI thread for
            # 2-3 s per child. Copy the lists: WorkerThreads may be reaping them
            # concurrently as children exit. (QProcess.close() only shuts I/O
            # channels, it does NOT stop the process -- terminate_all kills it.)
            Worker.terminate_all(
                list(self.obj_appconfig.procThread_list) +
                list(self.obj_appconfig.process_obj))

            # Check if "Open project" and "New project" window is open.
            # If yes, just close it when application is closed.
            try:
                self.project.close()
            except BaseException:
                pass
            if self.chatbot_dock is not None:
                self.chatbot_dock.close()
                self.chatbot_window.close()
            event.accept()
            self.systemTrayIcon.showMessage('Exit', 'eSim is Closed.')

        else:
            # 'No', the dialog's window-X (NoButton), or Escape all mean
            # "do not exit" -- otherwise the QCloseEvent defaults to accept
            # and the app quits anyway.
            event.ignore()

    def new_project(self):
        """This function call New Project Info class."""
        text, ok = QtWidgets.QInputDialog.getText(
            self, 'New Project Info', 'Enter Project Name:'
        )
        updated = False

        if ok:
            self.projname = (str(text))
            self.project = NewProjectInfo()
            directory, filelist = self.project.createProject(self.projname)

            if directory and filelist:
                self.obj_Mainview.obj_projectExplorer.addTreeNode(
                    directory, filelist
                )
                self.obj_appconfig.set_current_project(directory)
                project_name = self.obj_appconfig.get_proj_stem()
                self.obj_Mainview.obj_timeExplorer.load_snapshots(project_name)
                self.obj_appconfig.save_current_project()
                updated = True

        if not updated:
            print("No new project created")
            self.obj_appconfig.print_info('No new project created')
            try:
                self.obj_appconfig.print_info(
                    'Current project is : ' +
                    self.obj_appconfig.current_project["ProjectName"]
                )
            except Exception:
                pass

    def open_project(self):
        """This project call Open Project Info class."""
        print("Function : Open Project")
        self.project = OpenProjectInfo()
        try:
            directory, filelist = self.project.body()
            if not directory:
                return
            self.obj_appconfig.set_current_project(directory)
            self.obj_Mainview.obj_projectExplorer.addTreeNode(
                directory, filelist)
            project_name = self.obj_appconfig.get_proj_stem()
            self.obj_Mainview.obj_timeExplorer.load_snapshots(project_name)
            self.obj_appconfig.save_current_project()
        except Exception as e:
            # Never swallow a real open failure: log it and tell the user
            # instead of a silent no-op that reads as "nothing happened".
            traceback.print_exc()
            from frontEnd.dialogs import show_error
            show_error(self, "Open Project",
                       f"Could not open the project:\n{e}")
            self.obj_appconfig.print_error(f"Open project failed: {e}")

    def close_project(self):
        """
        This function closes the saved project.
        It first checks whether project (file) is present in list.

            - If present:
                - it first kills that process-id.
                - closes that file.
                - Shows message "Current project <path_to_file> is closed"

            - If not present: pass
        """
        print("Function : Close Project")
        current_project = self.obj_appconfig.current_project['ProjectName']
        if current_project is None:
            pass
        else:
            temp = self.obj_appconfig.current_project['ProjectName']
            # Terminate each tracked child through its handle (copy the list:
            # a WorkerThread may be reaping the same list as its child exits).
            # Graceful terminate, never os.kill on a bare recycled pid.
            for handle in list(self.obj_appconfig.proc_dict.get(temp, [])):
                Worker.terminate_handle(handle)
            self.obj_appconfig.proc_dict[temp] = []
            self.obj_Mainview.obj_dockarea.closeDock()
            closed_stem = self.obj_appconfig.get_proj_stem() \
                or os.path.basename(current_project)
            self.obj_appconfig.set_current_project(None)
            self.obj_appconfig.save_current_project()
            self.systemTrayIcon.showMessage(
                'Close', 'Current project ' +
                closed_stem + ' is Closed.'
            )

    def change_workspace(self):
        """
        Show the workspace picker as a modal popup on top of the main
        window.

        The main window stays visible (no more ``self.hide()``, which made
        the whole app vanish until a workspace was chosen) and the picker is
        re-parented onto the main window and run with ``exec()``, so it
        behaves like an in-window dialog that can't slip behind the app.
        """
        print("Function : Change Workspace")
        self.obj_workspace.returnWhetherClickedOrNot(self)
        # Glue the picker to the main window so it centers over it and stays
        # on top, instead of floating as a free top-level window.
        self.obj_workspace.setParent(self, QtCore.Qt.WindowType.Dialog)
        self.obj_workspace.setModal(True)
        self.obj_workspace.exec()

    def help_project(self):
        """
        This function opens the user manual in the system viewer / browser.
            - It prints the message ""Function : Help""
            - Uses print_info() method of class Appconfig
              from Configuration/Appconfig.py file.
        """
        print("Function : Help")
        self.obj_appconfig.print_info('Help is called')
        print("Current Project is : ", self.obj_appconfig.current_project)
        from browser.UserManual import open_user_manual
        open_user_manual(self)

    def dev_docs(self):
        """
        This function guides the user to readthedocs website for the developer docs
        """
        print("Function : DevDocs")
        self.obj_appconfig.print_info('DevDocs is called')
        print("Current Project is : ", self.obj_appconfig.current_project)
        webbrowser.open("https://esim.readthedocs.io/en/latest/index.html")

    def show_toolchain_doctor(self):
        """Help menu -> Check Simulation Toolchain: the doctor dialog."""
        self.obj_appconfig.print_info('Toolchain doctor is called')
        from maker import ToolchainCheck
        ToolchainCheck.show_dialog(self)

    def open_preferences(self):
        """Open the Aurora Preferences dialog (theme + accent picker). The
        dialog live-applies via app.apply_theme(), wired in main()."""
        from frontEnd.PreferencesDialog import PreferencesDialog
        dlg = PreferencesDialog(self)
        dlg.exec()

    @QtCore.pyqtSlot(QtCore.QProcess.ExitStatus, int)
    def plotSimulationData(self, exitStatus, exitCode):
        """Enables interaction for new simulation and
           displays the plotter dock where graphs can be plotted.
        """
        self.ngspice.setEnabled(True)
        self.conversion.setEnabled(True)
        self.closeproj.setEnabled(True)
        self.wrkspce.setEnabled(True)

        if exitStatus == QtCore.QProcess.ExitStatus.NormalExit and exitCode == 0:
            self._set_sim_status("ok")
            try:
                self.obj_Mainview.obj_dockarea.plottingEditor()
            except Exception as e:
                self._set_sim_status("failed")
                self.msg = Dialogs.make_error_message(self)
                self.msg.setModal(True)
                self.msg.setWindowTitle("Error Message")
                self.msg.showMessage(
                    'Data could not be plotted. Please try again.'
                )
                self.msg.exec()
                print("Exception Message:", str(e), traceback.format_exc())
                self.obj_appconfig.print_error('Exception Message : '
                                               + str(e))
        else:
            self._set_sim_status("failed")
            self._explain_simulation_error()

    def _explain_simulation_error(self):
        """Hand a failed run's ngspice log to the AI assistant, if installed.

        NgspiceWidget saves the log only for a real failure and removes it
        when a run starts, so a cancelled or abandoned run finds none.
        """
        project = self.obj_appconfig.current_project["ProjectName"]
        if self.chatbot_dock is None or project is None:
            return
        log = os.path.join(project, "ngspice_error.log")
        if not os.path.isfile(log):
            return
        self.chatbot_dock.show()
        self.chatbot_dock.raise_()
        self.chatbot_window.debug_error(log)

    def open_ngspice(self):
        """This Function execute ngspice on current project."""
        # Flush any unsaved edits in the code editor first, so the
        # simulation reads the netlist the user is actually looking at.
        try:
            from codeEditor import EditorWindow
            EditorWindow.flush_all_dirty()
        except Exception:
            pass

        projDir = self.obj_appconfig.current_project["ProjectName"]

        if projDir is not None:
            projName = self.obj_appconfig.get_proj_stem()
            ngspiceNetlist = os.path.join(projDir, projName + ".cir.out")

            if not os.path.isfile(ngspiceNetlist):
                print(
                    "Netlist file (*.cir.out) not found."
                )
                self.msg = Dialogs.make_error_message(self)
                self.msg.setModal(True)
                self.msg.setWindowTitle("Error Message")
                self.msg.showMessage(
                    'Netlist (*.cir.out) not found.'
                )
                self.msg.exec()
                return

            self.obj_Mainview.obj_dockarea.ngspiceEditor(
                projName, ngspiceNetlist, self.simulationEndSignal, self.plotFlag)

            self._set_sim_status("running")
            self.ngspice.setEnabled(False)
            self.conversion.setEnabled(False)
            self.closeproj.setEnabled(False)
            self.wrkspce.setEnabled(False)

        else:
            self.msg = Dialogs.make_error_message(self)
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                'Please select the project first.'
                ' You can either create new project or open existing project'
            )
            self.msg.exec()

    def open_subcircuit(self):
        """
        This function opens 'subcircuit' option in left-tool-bar.
        When 'subcircuit' icon is clicked wich is present in
        left-tool-bar of main page:

            - Meassge shown on screen "Subcircuit editor is called".
            - 'subcircuiteditor()' function is called using object
              'obj_dockarea' of class 'Mainview'.
        """
        print("Function : Subcircuit editor")
        self.obj_appconfig.print_info('Subcircuit editor is called')
        self.obj_Mainview.obj_dockarea.subcircuiteditor()

    def open_makerchip(self):
        """
        This function opens 'subcircuit' option in left-tool-bar.
        When 'subcircuit' icon is clicked wich is present in
        left-tool-bar of main page:

            - Meassge shown on screen "Subcircuit editor is called".
            - 'subcircuiteditor()' function is called using object
              'obj_dockarea' of class 'Mainview'.
        """
        print("Function : Makerchip and Verilator to Ngspice Converter")
        self.obj_appconfig.print_info('Makerchip is called')
        self.obj_Mainview.obj_dockarea.makerchip()

    def open_nghdl(self):
        """Open Model Creation straight on the VHDL / NGHDL stage.

        NGHDL now lives as the VHDL path inside Makerchip's Flow Navigator;
        this launcher keeps it one click away.
        """
        self.obj_appconfig.print_info('NGHDL (VHDL model creation) is called')
        self.obj_Mainview.obj_dockarea.makerchip(select_vhdl=True)

    def open_home(self):
        """Bring the permanent Welcome (home) dashboard to the front."""
        self.obj_Mainview.obj_dockarea.show_welcome()

    def open_modelEditor(self):
        """
        This function opens model editor option in left-tool-bar.
        When model editor icon is clicked which is present in
        left-tool-bar of main page:

            - Meassge shown on screen "Model editor is called".
            - 'modeleditor()' function is called using object
              'obj_dockarea' of class 'Mainview'.
        """
        print("Function : Model editor")
        self.obj_appconfig.print_info('Model editor is called')
        self.obj_Mainview.obj_dockarea.modelEditor()

    def open_OMedit(self):
        """
        This function calls ngspice to OMEdit converter and then launch OMEdit.
        """
        self.obj_appconfig.print_info('OMEdit is called')
        self.projDir = self.obj_appconfig.current_project["ProjectName"]

        if self.projDir is not None:
            if self.obj_validation.validateCirOut(self.projDir):
                self.projName = self.obj_appconfig.get_proj_stem()
                self.ngspiceNetlist = os.path.join(
                    self.projDir, self.projName + ".cir.out"
                )
                self.modelicaNetlist = os.path.join(
                    self.projDir, self.projName + ".mo"
                )

                """
                try:
                    # Creating a command for Ngspice to Modelica converter
                    self.cmd1 = "
                        python3 ../ngspicetoModelica/NgspicetoModelica.py "\
                            + self.ngspiceNetlist
                    self.obj_workThread1 = Worker.WorkerThread(self.cmd1)
                    self.obj_workThread1.start()
                    if self.obj_validation.validateTool("OMEdit"):
                        # Creating command to run OMEdit
                        self.cmd2 = "OMEdit "+self.modelicaNetlist
                        self.obj_workThread2 = Worker.WorkerThread(self.cmd2)
                        self.obj_workThread2.start()
                    else:
                        self.msg = Dialogs.make_message_box(self)
                        self.msgContent = "There was an error while
                            opening OMEdit.<br/>\
                        Please make sure OpenModelica is installed in your\
                            system. <br/>\
                        To install it on Linux : Go to\
                            <a href=https://www.openmodelica.org/download/\
                                download-linux>OpenModelica Linux</a> and  \
                                    install nigthly build release.<br/>\
                        To install it on Windows : Go to\
                         <a href=https://www.openmodelica.org/download/\
                        download-windows>OpenModelica Windows</a>\
                         and install latest version.<br/>"
                        self.msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
                        self.msg.setText(self.msgContent)
                        self.msg.setWindowTitle("Missing OpenModelica")
                        self.obj_appconfig.print_info(self.msgContent)
                        self.msg.exec()

                except Exception as e:
                    self.msg = Dialogs.make_error_message(self)
                    self.msg.setModal(True)
                    self.msg.setWindowTitle(
                        "Ngspice to Modelica conversion error")
                    self.msg.showMessage(
                        'Unable to convert NgSpice netlist to\
                            Modelica netlist :'+str(e))
                    self.msg.exec()
                    self.obj_appconfig.print_error(str(e))
                """

                self.obj_Mainview.obj_dockarea.modelicaEditor(self.projDir)

            else:
                self.msg = Dialogs.make_error_message(self)
                self.msg.setModal(True)
                self.msg.setWindowTitle("Missing Ngspice Netlist")
                self.msg.showMessage(
                    'Current project does not contain any Ngspice file. ' +
                    'Please create Ngspice file with extension .cir.out'
                )
                self.msg.exec()
        else:
            self.msg = Dialogs.make_error_message(self)
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                'Please select the project first. You can either ' +
                'create a new project or open an existing project'
            )
            self.msg.exec()

    def open_OMoptim(self):
        """
        This function uses validateTool() method from Validation.py:

            - If 'OMOptim' is present in executables list then
              it passes command 'OMOptim' to WorkerThread class of Worker.py
            - If 'OMOptim' is not present, then it shows error message with
              link to download it on Linux and Windows.
        """
        print("Function : OMOptim")
        self.obj_appconfig.print_info('OMOptim is called')
        # Check if OMOptim is installed
        if self.obj_validation.validateTool("OMOptim"):
            # Creating a command to run
            self.cmd = "OMOptim"
            self.obj_workThread = Worker.WorkerThread(self.cmd)
            self.obj_workThread.start()
        else:
            self.msg = Dialogs.make_message_box(self)
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
            self.msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
            self.msg.setText(self.msgContent)
            self.msg.setWindowTitle("Error Message")
            self.obj_appconfig.print_info(self.msgContent)
            self.msg.exec()

    def open_conToeSim(self):
        print("Function : Schematic converter")
        self.obj_appconfig.print_info('Schematic converter is called')
        self.obj_Mainview.obj_dockarea.eSimConverter()

# This class initialize the Main View of Application
class MainView(QtWidgets.QWidget):
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
        QtWidgets.QWidget.__init__(self, *args)

        self.obj_appconfig = Appconfig()

        self.leftSplit = QtWidgets.QSplitter()
        self.middleSplit = QtWidgets.QSplitter()

        self.mainLayout = QtWidgets.QVBoxLayout()
        # Intermediate Widget
        self.middleContainer = QtWidgets.QWidget()
        self.middleContainerLayout = QtWidgets.QVBoxLayout()

        # Area to be included in MainView
        self.noteArea = QtWidgets.QTextEdit()
        self.noteArea.setReadOnly(True)

        # Set explicit scrollbar policy
        self.noteArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.noteArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.obj_appconfig.noteArea['Note'] = self.noteArea
        self.obj_appconfig.noteArea['Note'].append(
            '        eSim Started......')
        self.obj_appconfig.noteArea['Note'].append('Project Selected : None')
        self.obj_appconfig.noteArea['Note'].append('\n')

        # The console sink is now a live QTextEdit (and the status bar a live
        # QStatusBar). Both may only be touched from the GUI thread, so stand up
        # the GUI-thread reporter that print_info/warning/error marshal through
        # -- we are on the GUI thread here (Application is built after
        # QApplication in main()). See Appconfig.attach_gui_reporter.
        self.obj_appconfig.attach_gui_reporter()

        # Enhanced CSS with proper scrollbar styling
        self.noteArea.setObjectName("mainNoteConsole")

        self.obj_dockarea = DockArea.DockArea()
        self.obj_projectExplorer = ProjectExplorer.ProjectExplorer()
        self.obj_timeExplorer = TimeExplorer.TimeExplorer()
        self.obj_projectExplorer.set_time_explorer(self.obj_timeExplorer)

        # Adding content to vertical middle Split.
        self.middleSplit.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.middleSplit.addWidget(self.obj_dockarea)
        self.middleSplit.addWidget(self.noteArea)

        # Adding middle split to Middle Container Widget
        self.middleContainerLayout.addWidget(self.middleSplit)
        self.middleContainer.setLayout(self.middleContainerLayout)

        # Adding content of left split. The TimeExplorer (snapshots) used to
        # sit here under the project tree; it now lives in the View menu
        # (Application.show_snapshots), so the project tree gets the full
        # column. The instance is still created above and kept loaded.
        self.leftPanel = QtWidgets.QVBoxLayout()
        self.leftPanelWidget = QtWidgets.QWidget()
        self.leftPanel.addWidget(self.obj_projectExplorer)
        self.leftPanelWidget.setLayout(self.leftPanel)
        self.leftSplit.addWidget(self.leftPanelWidget)
        self.leftSplit.addWidget(self.middleContainer)

        # Adding to main Layout
        self.mainLayout.addWidget(self.leftSplit)
        # leftSplit is horizontal, so both sizes are widths: give the explorer
        # ~1/4.5 of the width and the rest to the work area. (The old second
        # value was self.height() -- a height passed as a width; Qt normalised
        # it so it was harmless, but the intent is now explicit.)
        left = int(self.width() / 4.5)
        self.leftSplit.setSizes([left, self.width() - left])
        # Console starts collapsed: the dock area owns the full work height and
        # the status bar carries the latest message. Expand on demand via the
        # View menu / status-bar log button (toggle_console).
        self.collapse_console_area()
        self.setLayout(self.mainLayout)

    def collapse_console_area(self):
        """Collapse the console panel; the dock area takes the full height."""
        total = sum(self.middleSplit.sizes()) or self.height()
        self.middleSplit.setSizes([total, 0])

    def restore_console_area(self):
        """Expand the console panel to ~28% of the work-area height."""
        total = sum(self.middleSplit.sizes()) or self.height()
        console = int(total * 0.28)
        self.middleSplit.setSizes([total - console, console])

    def is_console_visible(self):
        sizes = self.middleSplit.sizes()
        return len(sizes) > 1 and sizes[1] > 4

    def toggle_console(self, show):
        """Show/hide the full console log panel (View menu / status bar)."""
        if show:
            self.restore_console_area()
        else:
            self.collapse_console_area()


# It is main function of the module and starts the application
def _install_excepthook():
    """Keep the app alive when a Qt slot raises.

    PyQt6 calls qFatal() -- killing the whole process, silently under
    pythonw -- whenever an unhandled Python exception escapes a slot while
    ``sys.excepthook`` is still the interpreter default. Installing any
    custom hook disables that abort. The hook records the traceback in
    ``~/.esim/error.log`` and shows it once per exception site, so a broken
    button degrades to an error dialog instead of the window vanishing.
    """
    from datetime import datetime
    seen_sites = set()

    def hook(etype, value, tb):
        if issubclass(etype, KeyboardInterrupt):
            sys.__excepthook__(etype, value, tb)
            return
        text = ''.join(traceback.format_exception(etype, value, tb))
        sys.stderr.write(text)
        try:
            log_path = paths.esim_config_path('error.log')
            os.makedirs(paths.esim_config_dir(), exist_ok=True)
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write('\n=== %s ===\n%s' % (datetime.now().isoformat(), text))
        except OSError:
            log_path = None

        # One dialog per raise site: a failure inside a paint/timer slot must
        # not queue an endless stack of identical modal boxes.
        site = (etype.__name__, tb.tb_frame.f_code.co_filename if tb else '',
                tb.tb_lineno if tb else 0)
        if site in seen_sites:
            return
        seen_sites.add(site)

        app = QtWidgets.QApplication.instance()
        if app is None:
            return
        summary = (
            'An internal error occurred; the app will keep running, '
            'but the last action may be incomplete.\n\n'
            + ''.join(traceback.format_exception_only(etype, value)).strip()
            + ('\n\nDetails: %s' % log_path if log_path else ''))

        def show():
            try:
                Dialogs.critical(None, 'eSim - Unexpected error', summary)
            except Exception:
                pass

        # Always POST the dialog, never show it inline -- for two reasons:
        #
        #  1. Thread: sys.excepthook runs on whichever thread raised, and a
        #     raise inside a WorkerThread (a missing eeschema/OMEdit binary is
        #     the easy one) lands here off the GUI thread. Creating or showing a
        #     QWidget from a non-GUI thread is undefined behaviour in Qt and can
        #     kill the process natively -- the crash net itself becoming the
        #     crash.
        #  2. Re-entrancy: even ON the GUI thread, Dialogs.critical runs a
        #     nested modal loop (exec()). If the exception escaped a paint /
        #     close / teardown handler, exec()ing there re-enters the event loop
        #     -- and can re-enter the very handler that just raised. The
        #     seen_sites dedupe stops an infinite dialog storm but not that
        #     first re-entrancy.
        #
        # Appconfig.post_to_gui emits the reporter's QueuedConnection 'deferred'
        # signal: from a worker thread it marshals to the GUI thread; on the GUI
        # thread it still defers to the next event-loop turn, so the current
        # (paint/close) stack fully unwinds before the modal box opens. NOTE:
        # PyQt6's QTimer.singleShot has NO (msec, context, slot) overload, so
        # the old singleShot(0, app, show) silently raised TypeError and the
        # worker-thread dialog never appeared -- the reporter is the only API
        # that crosses threads correctly.
        #
        # The log write above already happened, so a failure is never silent
        # even if no event loop is left to service the queued call (e.g. the
        # raise came from app teardown -- exactly when a modal box is unwanted).
        try:
            if not Appconfig.post_to_gui(show):
                # No GUI reporter yet (a crash during early startup, before
                # Application built it) -- there is no other thread's loop to
                # marshal to, so defer on THIS thread's loop. Fires only if this
                # is the GUI thread (the sole event loop that early); a
                # pre-reporter worker crash is already in error.log above.
                QtCore.QTimer.singleShot(0, show)
        except Exception:
            pass

    sys.excepthook = hook


#: Kept alive for the whole session: faulthandler writes into this handle from
#: a signal/exception context, so it must outlive the function that opened it.
_crash_log_file = None


def _install_crash_log():
    """Leave a stack trace behind when the process dies *natively*.

    ``sys.excepthook`` only ever sees Python exceptions. A C-stack overflow
    (an event handler that re-raises the event it handles: changeEvent ->
    setStyleSheet -> PaletteChange -> changeEvent ...) or a sip use-after-free
    kills the process outright -- under pythonw that means the window simply
    disappears, leaving nothing to debug from. faulthandler catches those at
    the OS level, so the trace lands in ~/.esim/crash.log instead.
    """
    global _crash_log_file
    try:
        import faulthandler
        from datetime import datetime
        os.makedirs(paths.esim_config_dir(), exist_ok=True)
        _crash_log_file = open(
            paths.esim_config_path('crash.log'), 'a', encoding='utf-8')
        _crash_log_file.write(
            '\n=== eSim session %s ===\n' % datetime.now().isoformat())
        _crash_log_file.flush()
        # all_threads: a crash in a worker (ngspice reader, plot thread) is
        # just as fatal, and its stack is the one worth having.
        faulthandler.enable(file=_crash_log_file, all_threads=True)
    except Exception:
        pass


def _app_teardown(apply_theme_slot=None):
    """Quiesce animation/timer/figure state at exit BEFORE Qt frees the widgets
    those callbacks touch -- the ordering that avoids the recurring sip
    use-after-free at teardown (0xc0000005 in sip.*.pyd). Every step is guarded
    so teardown can never raise. Called from app.aboutToQuit.
    """
    # 1. Stop every button-glow animation so none ticks against a freed effect.
    try:
        from frontEnd import motion
        motion.stop_all_glow()
    except Exception:
        pass
    # 2. Stop the OS light/dark signal re-entering apply_theme during teardown.
    #    The signal now drives a debounce timer, so stop that first (a pending
    #    trailing-edge fire would otherwise repolish a half-freed widget tree),
    #    then drop the connection.
    try:
        app = QtWidgets.QApplication.instance()
        timer = getattr(app, "_esim_os_theme_timer", None)
        if timer is not None:
            timer.stop()
    except Exception:
        pass
    if apply_theme_slot is not None:
        try:
            QtGui.QGuiApplication.styleHints().colorSchemeChanged.disconnect()
        except Exception:
            pass
    # 3. Stop lingering widget timers (plot refresh/resize/decimate) so a late
    #    tick can't touch a half-destroyed canvas.
    try:
        for w in QtWidgets.QApplication.topLevelWidgets():
            for timer in w.findChildren(QtCore.QTimer):
                timer.stop()
    except Exception:
        pass
    # 4. Close matplotlib figures (plot docks) -- only if it was ever loaded, so
    #    teardown never forces the heavy import.
    if 'matplotlib.pyplot' in sys.modules:
        try:
            sys.modules['matplotlib.pyplot'].close('all')
        except Exception:
            pass


def main(args):
    """
    The splash screen opened at the starting of screen is performed
    by this function.
    """
    # Windows: configure the tool environment and run per-user bootstrap in
    # THIS interpreter, so a direct `pythonw Application.py` launch needs no
    # esim.bat and no second interpreter. Both are sentinel-/idempotency-guarded,
    # so launching via esim.bat (which still sets the env) stays correct.
    if os.name == 'nt':
        try:
            from frontEnd import launcher_windows
            launcher_windows.setup_environment()
            launcher_windows.run_bootstrap()
        except Exception as e:
            print("Windows launcher setup skipped:", e)
    # Headless doctor mode: report the simulation-toolchain state and exit
    # BEFORE any QApplication/GUI work, so `esim --doctor` works over ssh and
    # in installer self-checks.
    if '--doctor' in args:
        from maker import ToolchainCheck
        print(ToolchainCheck.report())
        sys.exit(0 if not ToolchainCheck.failures() else 1)

    print("Starting eSim......")
    _install_excepthook()

    # Startup breadcrumb trail. Under pythonw there is no console, so a hang
    # or crash during startup leaves no trace; ~/.esim/startup.log (rewritten
    # every launch) shows the last stage reached instead.
    def _stage(msg):
        try:
            os.makedirs(paths.esim_config_dir(), exist_ok=True)
            with open(paths.esim_config_path('startup.log'), 'a',
                      encoding='utf-8') as f:
                import time as _time
                f.write('%.3f %s\n' % (_time.time() - _stage.t0, msg))
        except OSError:
            pass
    import time as _time
    _stage.t0 = _time.time()
    try:
        os.remove(paths.esim_config_path('startup.log'))
    except OSError:
        pass
    _stage('interpreter up, excepthook installed')

    _install_crash_log()

    # Startup watchdog: under pythonw a wedged startup is just a frozen
    # splash with zero diagnostics. If startup is still running after 25s,
    # dump every thread's stack to ~/.esim/startup-hang.log (startup keeps
    # going -- exit=False); cancelled the moment the event loop is reached.
    watchdog_file = None
    try:
        import faulthandler
        watchdog_file = open(
            paths.esim_config_path('startup-hang.log'), 'w')
        faulthandler.dump_traceback_later(25, file=watchdog_file, exit=False)
    except Exception:
        pass

    # A stale workspace pointer -- unplugged drive, folder deleted, or a
    # directory this (non-elevated) process cannot write -- must never reach
    # Application(): ProjectExplorer persists the registry into the workspace
    # during construction, and a bad path turns that into a frozen splash.
    # Reset the pointer and let the normal flow show the workspace picker.
    try:
        check, home = paths.read_workspace()
        if int(check) != 0 and not paths.workspace_is_usable(home):
            _stage('workspace unusable, resetting to picker: %s' % home)
            os.remove(paths.esim_config_path('workspace.txt'))
    except (OSError, ValueError):
        pass

    # Set non-native dialogs globally
    # NOTE: AA_DontUseNativeDialogs removed in Qt6.
    # Native dialog behavior is now controlled per-dialog via QFileDialog.Option.
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    # Windows: give the process an explicit AppUserModelID BEFORE the
    # QApplication (and thus any window) exists, so the taskbar groups eSim
    # under its own icon/identity instead of the generic pythonw host.
    if os.name == 'nt':
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "FOSSEE.eSim.2.5")
            # Startup blocks the GUI thread for seconds at a time (window
            # build, project-tree load). A click on the splash during such a
            # block makes DWM swap in a white "(Not Responding)" ghost window
            # -- it looks like a crash, and its close button really does
            # terminate the process. With ghosting off the splash stays
            # painted through the block and startup simply finishes.
            ctypes.windll.user32.DisableProcessWindowsGhosting()
        except Exception:
            pass
    app = QtWidgets.QApplication(args)
    app.setApplicationName("eSim")
    # One app-wide icon: every top-level window -- the splash and the
    # workspace picker included -- shows the eSim logo in the taskbar
    # instead of the generic pythonw icon.
    app.setWindowIcon(QtGui.QIcon(paths.image_path('logo.png')))

    # First launch on this machine: size the UI to the screen we actually got
    # before the first stylesheet is built, so the opening frame is already
    # right rather than something the user has to dial in by hand. Runs once --
    # after this the stored zoom_level is the user's preference and is left
    # alone. Guarded: a bad screen must not stop startup.
    try:
        theme_utils.ensure_zoom_calibrated()
    except Exception:
        pass
    _stage('zoom calibrated')

    # Aurora design system: attach a bound apply_theme to the app instance so
    # the Preferences dialog can live-apply, theme once before widgets build,
    # and follow OS light/dark changes. Guarded so theming cannot block startup.
    try:
        def _apply_theme(*_args):
            theme_utils.apply_theme(app)
        app.apply_theme = _apply_theme
        _apply_theme()
        # colorSchemeChanged only exists on Qt >= 6.5; on Ubuntu 24.04 (Qt 6.4)
        # there is no live OS light/dark signal — users toggle via the menu.
        hints = QtGui.QGuiApplication.styleHints()
        if hasattr(hints, "colorSchemeChanged"):
            # Debounce the OS light/dark signal. The user (or Windows auto
            # theme) flipping it rapidly used to fire a full repolish per event;
            # collapse a storm into a single apply on a 120ms trailing edge so
            # the theme engine is never asked to churn graphics effects faster
            # than it can settle them. Timer parented to app so it outlives this
            # scope and is reachable at teardown.
            _os_theme_timer = QtCore.QTimer(app)
            _os_theme_timer.setSingleShot(True)
            _os_theme_timer.setInterval(120)
            _os_theme_timer.timeout.connect(_apply_theme)
            app._esim_os_theme_timer = _os_theme_timer
            hints.colorSchemeChanged.connect(
                lambda *_: _os_theme_timer.start())
        # Ordered teardown at exit to avoid the sip use-after-free crash: stop
        # glow animations + this signal + plot timers/figures before Qt frees
        # the widgets they touch.
        app.aboutToQuit.connect(lambda: _app_teardown(_apply_theme))
        # Bundled Ubuntu font for the Aurora type scale (QSS has fallbacks).
        # This is the warm, rounded humanist face that ships as Ubuntu's own
        # desktop default -- so eSim reads the same soft way on Windows as it
        # does natively on Ubuntu. Static weights register under the single
        # family "Ubuntu"; QSS font-weight values snap to the nearest of
        # 400/500/700 (600/800 fall back to Bold, which Qt does not synthesize).
        fonts_dir = os.path.join(
            os.path.dirname(__file__), '..', '..', 'images', 'fonts'
        )
        for fname in ('Ubuntu-Regular.ttf', 'Ubuntu-Medium.ttf',
                      'Ubuntu-Bold.ttf'):
            font_path = os.path.join(fonts_dir, fname)
            if not os.path.exists(font_path):
                print("Font missing, using system fallback:", fname)
                continue
            fid = QtGui.QFontDatabase.addApplicationFont(font_path)
            if fid == -1:
                print("Font failed to register, using fallback:", fname)
    except Exception as e:
        print("Theme load failed, continuing unthemed:", str(e))

    # App-wide Aurora polish: translucent menus (so the QSS rounded corners are
    # genuine, not square) + a Show-time effect refresh so drop-shadows never
    # render stale after a tab/page switch or maximize. Static; guarded so they
    # cannot block startup.
    try:
        from frontEnd.motion import install_app_motion
        install_app_motion(app)
    except Exception:
        pass

    # Replace Qt's square-cornered native tooltip with the Aurora rounded card.
    try:
        from frontEnd.tooltips import install_tooltips
        install_tooltips(app)
    except Exception:
        pass

    # Show the splash FIRST -- before the slow Application() construction and
    # last-project restore -- so the user sees it *during* the wait instead of
    # after it. The old sequence built the whole window first (blank screen
    # while that ran), then spent 1500ms fading the splash in inside a nested
    # QEventLoop: the animation was the only thing the user watched, and it ran
    # after the slow part was already done. Both are gone: the splash appears
    # instantly and closes the moment the workspace/main window shows.
    splash_pix = QtGui.QPixmap(paths.image_path('splash_screen_esim.png'))
    if splash_pix.isNull():
        # Missing/unreadable splash_screen_esim.png yields a null (0x0) pixmap.
        # Feeding it through the scale/rounded-mask/QPainter chain below only
        # spams "QPainter::begin: Paint device returned engine == 0" warnings
        # and produces an invisible splash. Skip the splash entirely and let
        # startup continue -- the window build below runs the same either way.
        # Every downstream consumer already guards `splash is not None`
        # (Workspace._finish_workspace_change, the workspace-picker branch).
        print("Splash image missing; starting without splash screen.")
        splash = None
    else:
        splash_pix = splash_pix.scaledToWidth(
            int(splash_pix.width() * 0.8),
            QtCore.Qt.TransformationMode.SmoothTransformation)

        # Proportional rounded mask cuts the heavy black splash corners.
        radius = int(min(splash_pix.width(), splash_pix.height()) * 0.10)
        rounded_splash = QtGui.QPixmap(splash_pix.size())
        rounded_splash.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(rounded_splash)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        path_obj = QtGui.QPainterPath()
        path_obj.addRoundedRect(
            0, 0, splash_pix.width(), splash_pix.height(), radius, radius)
        painter.setClipPath(path_obj)
        painter.drawPixmap(0, 0, splash_pix)
        painter.end()

        class FadingSplash(QtWidgets.QSplashScreen):
            def __init__(self, pixmap):
                transparent_base = QtGui.QPixmap(pixmap.size())
                transparent_base.fill(QtCore.Qt.GlobalColor.transparent)
                super().__init__(
                    transparent_base,
                    QtCore.Qt.WindowType.WindowStaysOnTopHint)
                self.setAttribute(
                    QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
                self.base_pixmap = pixmap
                self.opacity = 1.0

            def setOpacity(self, opacity):
                self.opacity = opacity
                self.repaint()

            def paintEvent(self, event):
                painter = QtGui.QPainter(self)
                painter.setOpacity(self.opacity)
                painter.drawPixmap(0, 0, self.base_pixmap)
                painter.end()

        splash = FadingSplash(rounded_splash)
        splash.setDisabled(True)
        # Busy cursor over the splash: tells the user "loading, don't worry"
        # during the long blocking phases below.
        splash.setCursor(QtCore.Qt.CursorShape.BusyCursor)
        splash.show()
        # Force one paint now so the splash is actually on screen before we
        # block the event loop building the main window.
        app.processEvents()

    # The slow part -- window construction + last-project restore -- now runs
    # with the splash already visible.
    _stage('splash shown, building main window')
    appView = Application()
    _stage('main window built')
    # Drain the input queued during the multi-second window build (the
    # disabled splash discards it) so Windows stops counting the process as
    # unresponsive before the next blocking phase starts.
    app.processEvents()
    last_project_path = appView.obj_appconfig.load_last_project()
    if last_project_path:
        try:
            open_proj = OpenProjectInfo()
            directory, filelist = open_proj.body(last_project_path)
            if directory:
                appView.obj_Mainview.obj_projectExplorer.addTreeNode(
                    directory, filelist)
        except Exception as e:
            print("Could not restore last project:", str(e))
    appView.obj_Mainview.obj_timeExplorer.load_last_snapshots()
    appView.hide()
    app.processEvents()

    appView.splash = splash
    appView.obj_workspace.returnWhetherClickedOrNot(appView)

    try:
        work = int(paths.read_workspace()[0])
    # ValueError: an empty/truncated workspace.txt makes int('') fail; treat it
    # the same as a missing file and fall back to the workspace picker, rather
    # than letting the exception abort startup.
    except (IOError, ValueError):
        work = 0

    if work != 0:
        appView.obj_workspace.defaultWorkspace()
    else:
        # First run (or reset workspace): the splash is a disabled
        # stays-on-top window, so it must be gone before the picker asks for
        # input -- otherwise the dialog opens underneath it, can't be raised
        # past it, and the app looks hung. The splash's only job (covering
        # the slow window build) is already done at this point.
        if splash is not None:
            splash.close()
        appView.splash = None
        appView.obj_workspace.show()
        appView.obj_workspace.raise_()
        appView.obj_workspace.activateWindow()

    # Pre-warm every tool's imports in the background once startup has
    # settled, so the first click on any launcher (plot, Model Creation,
    # KiCad-to-Ngspice, Model/Subcircuit editor, converters, manual) never
    # pays a cold import inline -- on a cold Windows boot Defender scans each
    # native module on first load, which is exactly the multi-second "why is
    # this tab taking so long" stall. Python's import lock makes daemon-thread
    # imports safe (a click racing the prewarm just waits on the same lock it
    # would have paid anyway); only modules are imported, no QWidget is
    # constructed off the GUI thread. Ordered heaviest-first so the biggest
    # win lands earliest. Fire-and-forget, gated so a failure can never
    # affect startup.
    def _prewarm_tool_imports():
        import threading

        def _warm():
            for mod in (
                'matplotlib.pyplot',
                'ngspiceSimulation.plot_window',
                'ngspiceSimulation.NgspiceWidget',
                'maker.makerchip',
                'kicadtoNgspice.KicadtoNgspice',
                'modelEditor.ModelEditor',
                'subcircuit.Subcircuit',
                'converter.pspiceToKicad',
                'converter.ltspiceToKicad',
                'converter.LtspiceLibConverter',
                'converter.libConverter',
                'ngspicetoModelica.ModelicaUI',
                'browser.UserManual',
            ):
                try:
                    __import__(mod)
                except Exception:
                    pass

        threading.Thread(target=_warm, daemon=True).start()

    QtCore.QTimer.singleShot(3000, _prewarm_tool_imports)

    # Startup made it to the event loop: stand down the hang watchdog and
    # drop its (empty) log so a stale file never reads as a current freeze.
    try:
        import faulthandler
        faulthandler.cancel_dump_traceback_later()
        if watchdog_file is not None:
            watchdog_file.close()
            if os.path.getsize(watchdog_file.name) == 0:
                os.remove(watchdog_file.name)
    except Exception:
        pass

    _stage('startup complete, entering event loop')
    sys.exit(app.exec())


# Call main function
if __name__ == '__main__':
    # Create and display the splash screen
    try:
        main(sys.argv)
    except Exception as err:
        print("Error: ", err)
        # Full traceback so a startup crash is diagnosable, not a bare message.
        traceback.print_exc()
