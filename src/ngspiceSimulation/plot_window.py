# ngspiceSimulation/plot_window.py
"""
Plot Window Module

This module provides the main plotting window for NGSpice simulation results
with support for AC, DC, and Transient analysis visualization.
"""

from __future__ import division
import os
import sys
import json
import traceback
import logging
import ast
import operator
import re
from pathlib import Path
from decimal import Decimal, getcontext
from typing import Dict, List, Optional, Tuple, Any

from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtCore import Qt, QSettings, pyqtSignal
from PyQt6.QtWidgets import (QWidget, QVBoxLayout,
                             QHBoxLayout, QListWidget, QListWidgetItem, QPushButton,
                             QCheckBox, QGroupBox,
                             QLabel, QLineEdit, QSlider, QDoubleSpinBox, QMenu,
                             QFileDialog, QColorDialog, QInputDialog,
                             QMessageBox, QStatusBar,
                             QSplitter, QToolButton, QWidgetAction, QGridLayout,
                             QSizePolicy, QScrollArea)
from PyQt6.QtGui import (QColor, QBrush, QPalette, QKeySequence,
                         QPainter, QPixmap, QFont, QAction)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.text import Text

from configuration.Appconfig import Appconfig
from .plotting_widgets import CollapsibleBox, MultimeterWidgetClass
from .data_extraction import DataExtraction

# Set up logging
logger = logging.getLogger(__name__)

# Constants
DEFAULT_WINDOW_WIDTH = 1400
DEFAULT_WINDOW_HEIGHT = 800
DEFAULT_DPI = 100
DEFAULT_FIGURE_SIZE = (10, 8)
DEFAULT_LINE_THICKNESS = 1.5
DEFAULT_VERTICAL_SPACING = 1.2 # <-- UI Change: Reverted to original value
DEFAULT_ZOOM_FACTOR = 0.9
CURSOR_ALPHA = 0.7
THRESHOLD_ALPHA = 0.5
LEGEND_FONT_SIZE = 9
DEFAULT_EXPORT_DPI = 300

# Color Constants
VIBRANT_COLOR_PALETTE = [
    '#E53935',  # Vivid Red
    '#1E88E5',  # Strong Blue
    '#43A047',  # Rich Green
    '#FB8C00',  # Bright Orange
    '#8E24AA',  # Deep Purple
    '#00ACC1',  # Vibrant Teal
    '#D81B60',  # Strong Pink
    '#6D4C41',  # Earthy Brown
    '#FDD835',  # Visible Amber
    '#039BE5',  # Sky Blue
    '#C0CA33',  # Lime Green
    '#37474F'   # Dark Grey
]

# Time unit conversion thresholds (more precise)
TIME_UNIT_THRESHOLD_PS = 1e-9
TIME_UNIT_THRESHOLD_NS = 1e-6
TIME_UNIT_THRESHOLD_US = 1e-3
TIME_UNIT_THRESHOLD_MS = 1

# Line style options
LINE_STYLES = [
    ('-', "Solid"),
    ('--', "Dashed"),
    (':', "Dotted"),
    ('steps-post', "Step (Post)")
]

# Thickness options
THICKNESS_OPTIONS = [
    (1.0, "1 px"),
    (1.5, "1.5 px"),
    (2.0, "2 px"),
    (3.0, "3 px")
]


class Trace:
    """Single class to manage all trace properties."""

    def __init__(self, index: int, name: str, color: str = None,
                 thickness: float = DEFAULT_LINE_THICKNESS, style: str = '-',
                 visible: bool = False) -> None:
        self.index = index
        self.name = name
        self.color = color or VIBRANT_COLOR_PALETTE[0]
        self.thickness = thickness
        self.style = style
        self.visible = visible
        self.line_object: Optional[Line2D] = None

    def update_line(self, **kwargs) -> None:
        if self.line_object:
            if 'color' in kwargs:
                self.color = kwargs['color']
                self.line_object.set_color(self.color)
            if 'thickness' in kwargs:
                self.thickness = kwargs['thickness']
                self.line_object.set_linewidth(self.thickness)
            if 'style' in kwargs:
                self.style = kwargs['style']
                if self.style != 'steps-post':
                    self.line_object.set_linestyle(self.style)


class CustomListWidget(QListWidget):
    """Custom QListWidget that handles selection without default styling."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        super().paintEvent(event)


def _safe_eval(expr: str, data_map: dict) -> "np.ndarray":
    """Evaluate a math expression over trace arrays without using eval() on raw user input.

    Allowed: trace names, numeric literals, +  -  *  /  **  unary minus, numpy via 'np'.
    Raises ValueError for anything else (attribute access, calls, etc.).
    """
    import ast, operator as op

    ALLOWED_OPS = {
        ast.Add: op.add, ast.Sub: op.sub,
        ast.Mult: op.mul, ast.Div: op.truediv,
        ast.Pow: op.pow, ast.USub: op.neg,
    }

    def _eval(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.Name):
            if node.id in data_map:
                return data_map[node.id]
            raise ValueError(f"Unknown trace: '{node.id}'")
        if isinstance(node, ast.BinOp):
            op_fn = ALLOWED_OPS.get(type(node.op))
            if op_fn is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return op_fn(_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return op.neg(_eval(node.operand))
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

    tree = ast.parse(expr, mode='eval')
    return np.array(_eval(tree.body), dtype=float)


def _format_measurement(value: float, unit: str) -> str:
    """Format a voltage or current with an appropriate SI prefix."""
    abs_val = abs(value)
    if unit == "A":
        if abs_val >= 1:      return f"{value:.3g} A"
        if abs_val >= 1e-3:   return f"{value * 1e3:.3g} mA"
        if abs_val >= 1e-6:   return f"{value * 1e6:.3g} µA"
        if abs_val >= 1e-9:   return f"{value * 1e9:.3g} nA"
        return "0 A"
    else:
        if abs_val >= 1:      return f"{value:.3g} V"
        if abs_val >= 1e-3:   return f"{value * 1e3:.3g} mV"
        if abs_val >= 1e-6:   return f"{value * 1e6:.3g} µV"
        return "0 V"


def _format_frequency(freq_hz: float) -> str:
    """Format a frequency in Hz with an appropriate SI prefix."""
    if freq_hz >= 1e9:   return f"{freq_hz / 1e9:.3g} GHz"
    if freq_hz >= 1e6:   return f"{freq_hz / 1e6:.3g} MHz"
    if freq_hz >= 1e3:   return f"{freq_hz / 1e3:.3g} kHz"
    return                      f"{freq_hz:.3g} Hz"


def _detect_frequency(time_data: "np.ndarray",
                      logic_normalized: "np.ndarray") -> "Optional[float]":
    """Return signal frequency in Hz if periodic, else None.

    Uses rising-edge timing. Requires ≥2 complete cycles and a coefficient of
    variation below 10% — rejects glitchy or non-periodic signals.
    """
    transitions = np.diff(logic_normalized.astype(np.int8))
    rising_idx = np.where(transitions == 1)[0]
    if len(rising_idx) < 3:  # need 2+ periods to verify consistency
        return None
    periods = np.diff(time_data[rising_idx])
    if len(periods) == 0:
        return None
    mean_p = float(np.mean(periods))
    if mean_p <= 0:
        return None
    if len(periods) > 1 and float(np.std(periods)) / mean_p > 0.10:
        return None
    return 1.0 / mean_p


class plotWindow(QWidget):
    """Main plotting widget for NGSpice simulation results."""

    def __init__(self, file_path: str, project_name: str, parent=None) -> None:
        super().__init__(parent)

        self.file_path = file_path
        self.project_name = project_name
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.setMinimumSize(400, 300)
        self.obj_appconfig = Appconfig()
        logger.info(f"Complete Project Path: {self.file_path}")
        logger.info(f"Project Name: {self.project_name}")
        self.obj_appconfig.print_info(f'NGSpice simulation called: {self.file_path}')
        self.obj_appconfig.print_info(f'PythonPlotting called: {self.file_path}')

        self._initialize_data_structures()
        self._initialize_configuration()
        self.create_main_frame()
        self.load_simulation_data()
        self.apply_theme()

    def _initialize_data_structures(self) -> None:
        self.traces: Dict[int, Trace] = {}
        self.cursor_lines: List[Optional[Line2D]] = []
        self.cursor_positions: List[Optional[float]] = []
        self.timing_annotations: Dict[int, Any] = {}
        self.color_palette = VIBRANT_COLOR_PALETTE.copy()
        self.logic_thresholds: Dict[int, float] = {}
        self.vertical_spacing = DEFAULT_VERTICAL_SPACING
        self._func_line: Optional[Line2D] = None
        self._drag_cursor_idx: Optional[int] = None
        self._meters: List[Any] = []
        self._last_was_timing: bool = False

    def _initialize_configuration(self) -> None:
        self.config_dir = Path.home() / '.pythonPlotting'
        self.config_file = self.config_dir / 'config.json'
        self.config: Dict[str, Any] = self.load_config()
        self.settings = QSettings('eSim', 'PythonPlotting')

    def load_config(self) -> Dict[str, Any]:
        try:
            self.config_dir.mkdir(exist_ok=True)
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as config_file:
                    config = json.load(config_file)
                    if 'theme' in config:
                        del config['theme']
                    return config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
        return {'trace_colours': {}, 'trace_thickness': {}, 'trace_style': {}, 'experimental_acdc': False}

    def save_config(self) -> None:
        try:
            self.config_dir.mkdir(exist_ok=True)
            self.config['trace_colours'] = {t.name: t.color for t in self.traces.values()}
            self.config['trace_thickness'] = {t.name: t.thickness for t in self.traces.values()}
            self.config['trace_style'] = {t.name: t.style for t in self.traces.values()}
            temp_file = self.config_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as config_file:
                json.dump(self.config, config_file, indent=2)
            temp_file.replace(self.config_file)
        except Exception as e:
            logger.error(f"Error saving config: {e}")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.save_config()
        for meter in self._meters:
            meter.close()
        self._meters.clear()
        if hasattr(self, 'canvas'):
            self.canvas.close()
        if hasattr(self, 'fig'):
            plt.close(self.fig)
        super().closeEvent(event)

    def apply_theme(self) -> None:
        theme_stylesheet = """
        QMenuBar { border-radius: 8px; background-color: #FFFFFF; border: 1px solid #E0E0E0; padding: 2px; }
        QStatusBar { border-radius: 8px; background-color: #FFFFFF; border: 1px solid #E0E0E0; padding: 2px; }
        QWidget { background-color: #FFFFFF; color: #212121; }
        QListWidget { background-color: #FFFFFF; border: 1px solid #E0E0E0; padding: 2px; outline: none; selection-background-color: transparent; selection-color: inherit; }
        QListWidget::item { min-height: 32px; padding: 6px 8px; margin: 2px 4px; background-color: transparent; border: none; }
        QListWidget::item:selected { background-color: transparent; border: none; }
        QListWidget::item:hover { background-color: rgba(0, 0, 0, 0.04); }
        QListWidget::item:focus { outline: none; }
        QGroupBox { border: 1px solid #E0E0E0; margin-top: 0.5em; padding-top: 0.5em; }
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px; }
        QPushButton { background-color: #FFFFFF; border: 1px solid #E0E0E0; padding: 6px 12px; font-weight: 500; }
        QPushButton:hover { background-color: #F2F2F2; border-color: #1976D2; }
        QPushButton:pressed { background-color: #E0E0E0; }
        QCheckBox::indicator { width: 16px; height: 16px; }
        QMenu { background-color: #FFFFFF; border: 1px solid #E0E0E0; }
        QMenu::item:selected { background-color: #E3F2FD; }
        QLineEdit { border: 1px solid #E0E0E0; padding: 6px 12px; background-color: #FAFAFA; }
        QLineEdit:focus { border-color: #1976D2; background-color: #FFFFFF; }
        QSlider::groove:horizontal { border: 1px solid #E0E0E0; height: 4px; background: #E0E0E0; }
        QSlider::handle:horizontal { background: #1976D2; border: 1px solid #1976D2; width: 16px; height: 16px; margin: -6px 0; }
        QScrollBar:vertical { background-color: #F5F5F5; width: 8px; border: none; border-radius: 4px; }
        QScrollBar::handle:vertical { background-color: #BDBDBD; border-radius: 4px; min-height: 20px; margin: 2px; }
        QScrollBar::handle:vertical:hover { background-color: #9E9E9E; }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
        """
        self.setStyleSheet(theme_stylesheet)

    def create_main_frame(self) -> None:
        main_widget_layout = QVBoxLayout(self)
        main_widget_layout.setContentsMargins(5, 5, 5, 5)
        self.menu_bar = QtWidgets.QMenuBar(self)
        main_widget_layout.addWidget(self.menu_bar)
        content_widget = QWidget()
        content_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        main_layout = QHBoxLayout(content_widget)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        left_widget = self.create_waveform_list()
        self.splitter.addWidget(left_widget)
        center_widget = self.create_plot_area()
        self.splitter.addWidget(center_widget)
        right_widget = self.create_control_panel()
        scroll_area = QScrollArea()
        scroll_area.setWidget(right_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollbar_style = "QScrollBar:vertical{background-color:#F5F5F5;width:8px;border:none;border-radius:4px;}QScrollBar::handle:vertical{background-color:#BDBDBD;border-radius:4px;min-height:20px;margin:2px;}QScrollBar::handle:vertical:hover{background-color:#9E9E9E;}QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0px;}QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background:transparent;}"
        scroll_area.verticalScrollBar().setStyleSheet(scrollbar_style)
        self.splitter.addWidget(scroll_area)
        self.splitter.setSizes([280, 840, 280])
        main_layout.addWidget(self.splitter)
        main_widget_layout.addWidget(content_widget)
        self.status_bar = QStatusBar()
        self.coord_label = QLabel("X: --, Y: --")
        self.status_bar.addWidget(self.coord_label)
        self.measure_label = QLabel("")
        self.status_bar.addPermanentWidget(self.measure_label)
        main_widget_layout.addWidget(self.status_bar)
        self.create_menu_bar()
        self.setWindowTitle(f'Python Plotting - {self.project_name}')

    def create_waveform_list(self) -> QWidget:
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        self.analysis_label = QLabel()
        self.analysis_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        left_layout.addWidget(self.analysis_label)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search waveforms...")
        self.search_box.textChanged.connect(self.filter_waveforms)
        left_layout.addWidget(self.search_box)
        self.waveform_list = CustomListWidget()
        self.waveform_list.itemClicked.connect(self.on_waveform_toggle)
        self.waveform_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.waveform_list.customContextMenuRequested.connect(self.show_list_context_menu)
        self.waveform_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.waveform_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        left_layout.addWidget(self.waveform_list)
        button_layout = QHBoxLayout()
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.select_all_waveforms)
        self.deselect_all_btn = QPushButton("Deselect All")
        self.deselect_all_btn.clicked.connect(self.deselect_all_waveforms)
        button_layout.addWidget(self.select_all_btn)
        button_layout.addWidget(self.deselect_all_btn)
        left_layout.addLayout(button_layout)
        return left_widget

    def create_plot_area(self) -> QWidget:
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        self.fig = Figure(figsize=DEFAULT_FIGURE_SIZE, dpi=DEFAULT_DPI)
        self.canvas = FigureCanvas(self.fig)
        self.nav_toolbar = NavigationToolbar(self.canvas, self)
        self.nav_toolbar.addSeparator()
        fig_options_action = QAction('⚙', self.nav_toolbar)
        fig_options_action.triggered.connect(self.open_figure_options)
        fig_options_action.setToolTip('Figure Options (P)')
        self.nav_toolbar.addAction(fig_options_action)
        center_layout.addWidget(self.nav_toolbar)
        center_layout.addWidget(self.canvas)
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)
        self.canvas.mpl_connect('button_release_event', self.on_canvas_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        return center_widget

    def create_control_panel(self) -> QWidget:
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Display Options
        display_box = CollapsibleBox("Display Options")
        display_group = QWidget()
        display_layout = QVBoxLayout(display_group)
        self.grid_check = QCheckBox("Show Grid")
        self.grid_check.setChecked(True)
        self.grid_check.stateChanged.connect(self.toggle_grid)
        display_layout.addWidget(self.grid_check)
        self.legend_check = QCheckBox("Show Legend")
        self.legend_check.setChecked(False)
        self.legend_check.stateChanged.connect(self.toggle_legend)
        display_layout.addWidget(self.legend_check)
        self.autoscale_check = QCheckBox("Autoscale")
        self.autoscale_check.setChecked(True)
        self.autoscale_check.stateChanged.connect(self.refresh_plot)
        display_layout.addWidget(self.autoscale_check)
        self.timing_check = QCheckBox("Digital Timing View")
        self.timing_check.stateChanged.connect(self.on_timing_view_changed)
        display_layout.addWidget(self.timing_check)
        display_box.addWidget(display_group)
        right_layout.addWidget(display_box)

        # Digital Timing Controls (UI Reverted to Original)
        self.timing_box = CollapsibleBox("Digital Timing Controls")
        timing_group = QWidget()
        timing_layout = QVBoxLayout(timing_group)
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(QLabel("Threshold:"))
        self.threshold_spinbox = QDoubleSpinBox()
        self.threshold_spinbox.setRange(-100, 100)
        self.threshold_spinbox.setDecimals(3)
        self.threshold_spinbox.setSingleStep(0.1)
        self.threshold_spinbox.setSuffix("")
        self.threshold_spinbox.setSpecialValueText("Auto")
        self.threshold_spinbox.setValue(self.threshold_spinbox.minimum())
        self.threshold_spinbox.valueChanged.connect(self.on_threshold_changed)
        threshold_layout.addWidget(self.threshold_spinbox)
        timing_layout.addLayout(threshold_layout)
        spacing_layout = QHBoxLayout()
        spacing_layout.addWidget(QLabel("Spacing:"))
        self.spacing_slider = QSlider(Qt.Orientation.Horizontal)
        self.spacing_slider.setRange(100, 200)
        self.spacing_slider.setValue(120)
        self.spacing_slider.valueChanged.connect(self.on_spacing_changed)
        self.spacing_label = QLabel("1.2x")
        spacing_layout.addWidget(self.spacing_slider)
        spacing_layout.addWidget(self.spacing_label)
        timing_layout.addLayout(spacing_layout)
        self.timing_box.addWidget(timing_group)
        self.timing_box.content_area.setEnabled(False)
        right_layout.addWidget(self.timing_box)

        # Cursor Measurements
        cursor_box = CollapsibleBox("Cursor Measurements")
        cursor_group = QWidget()
        cursor_layout = QVBoxLayout(cursor_group)
        cursor_hint = QLabel("Left click: C1  ·  Right click: C2  ·  Drag to move")
        cursor_hint.setStyleSheet("color: #757575; font-size: 10px;")
        cursor_layout.addWidget(cursor_hint)
        self.cursor1_label = QLabel("Cursor 1: Not set")
        self.cursor2_label = QLabel("Cursor 2: Not set")
        self.delta_label = QLabel("Delta: --")
        cursor_layout.addWidget(self.cursor1_label)
        cursor_layout.addWidget(self.cursor2_label)
        cursor_layout.addWidget(self.delta_label)
        self.clear_cursors_btn = QPushButton("Clear Cursors")
        self.clear_cursors_btn.clicked.connect(self.clear_cursors)
        cursor_layout.addWidget(self.clear_cursors_btn)
        cursor_box.addWidget(cursor_group)
        right_layout.addWidget(cursor_box)

        # Export Tools
        export_box = CollapsibleBox("Export Tools")
        export_group = QWidget()
        export_layout = QVBoxLayout(export_group)
        self.export_btn = QPushButton("Export Image")
        self.export_btn.clicked.connect(self.export_image)
        export_layout.addWidget(self.export_btn)
        self.func_input = QLineEdit()
        self.func_input.setPlaceholderText("e.g., v(in) + v(out)")
        export_layout.addWidget(self.func_input)
        self.plot_func_btn = QPushButton("Plot Function")
        self.plot_func_btn.clicked.connect(self.plot_function)
        export_layout.addWidget(self.plot_func_btn)
        self.multimeter_btn = QPushButton("Multimeter")
        self.multimeter_btn.clicked.connect(self.multi_meter)
        export_layout.addWidget(self.multimeter_btn)
        export_box.addWidget(export_group)
        right_layout.addWidget(export_box)

        right_layout.addStretch()
        return right_widget

    def create_menu_bar(self) -> None:
        file_menu = self.menu_bar.addMenu('File')
        export_action = QAction('Export Image...', self)
        export_action.triggered.connect(self.export_image)
        file_menu.addAction(export_action)
        view_menu = self.menu_bar.addMenu('View')
        zoom_in_action = QAction('Zoom In', self)
        zoom_in_action.setShortcut('Ctrl++')
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        zoom_out_action = QAction('Zoom Out', self)
        zoom_out_action.setShortcut('Ctrl+-')
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        reset_view_action = QAction('Reset View', self)
        reset_view_action.setShortcut('Ctrl+0')
        reset_view_action.triggered.connect(self.reset_view)
        view_menu.addAction(reset_view_action)

    def load_simulation_data(self) -> None:
        self.obj_dataext = DataExtraction()
        self.plot_type = self.obj_dataext.openFile(self.file_path)
        self.obj_dataext.computeAxes()
        self.data_info = self.obj_dataext.numVals()
        self.volts_length = self.data_info[1]
        if self.plot_type[0] == DataExtraction.AC_ANALYSIS:
            self.analysis_label.setText("AC Analysis")
        elif self.plot_type[0] == DataExtraction.TRANSIENT_ANALYSIS:
            self.analysis_label.setText("Transient Analysis")
        else:
            self.analysis_label.setText("DC Analysis")
        self.populate_waveform_list()
        is_transient = self.plot_type[0] == DataExtraction.TRANSIENT_ANALYSIS
        self.timing_check.setEnabled(is_transient)
        if not is_transient:
            self.timing_check.setChecked(False)
            self.timing_check.setToolTip("Digital timing view is only available for transient analysis")
        else:
            self.timing_check.setToolTip("")

    def create_colored_icon(self, color: QColor, is_selected: bool) -> QtGui.QIcon:
        pixmap = QPixmap(18, 18)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if is_selected:
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(1, 1, 16, 16)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            pen = QtGui.QPen(QColor("#9E9E9E"))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawEllipse(2, 2, 14, 14)
        painter.end()
        return QtGui.QIcon(pixmap)

    def populate_waveform_list(self) -> None:
        self.waveform_list.clear()
        self.traces.clear()
        saved_colors = self.config.get('trace_colours', {})
        saved_thickness = self.config.get('trace_thickness', {})
        saved_style = self.config.get('trace_style', {})
        for i, node_name in enumerate(self.obj_dataext.NBList):
            color = saved_colors.get(node_name, self.color_palette[i % len(self.color_palette)])
            thickness = saved_thickness.get(node_name, DEFAULT_LINE_THICKNESS)
            style = saved_style.get(node_name, '-')
            self.traces[i] = Trace(index=i, name=node_name, color=color, thickness=thickness, style=style)
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, i)
            item.setToolTip("Voltage signal" if i < self.obj_dataext.volts_length else "Current signal")
            self.waveform_list.addItem(item)
            self.update_list_item_appearance(item, i)

    def filter_waveforms(self, text: str) -> None:
        for i in range(self.waveform_list.count()):
            item = self.waveform_list.item(i)
            if item:
                item.setHidden(text.lower() not in item.text().lower())

    def on_waveform_toggle(self, item: QListWidgetItem) -> None:
        index = item.data(Qt.ItemDataRole.UserRole)
        # item.isSelected() is unreliable when setItemWidget is used — clicks land
        # on the child widget and never update Qt's selection model. Toggle instead.
        self.traces[index].visible = not self.traces[index].visible
        self.update_list_item_appearance(item, index)
        self.refresh_plot()

    def update_list_item_appearance(self, item: QListWidgetItem, index: int) -> None:
        t = self.traces[index]
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(10)
        icon_label = QLabel()
        color = QColor(t.color) if t.visible else QColor("#9E9E9E")
        icon = self.create_colored_icon(color, t.visible)
        icon_label.setPixmap(icon.pixmap(18, 18))
        text_label = QLabel(t.name)
        text_label.setStyleSheet("color: #212121; font-weight: 500;" if t.visible else "color: #757575; font-weight: normal;")
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()
        self.waveform_list.setItemWidget(item, widget)
        item.setText(t.name)

    def select_all_waveforms(self) -> None:
        for i in range(self.waveform_list.count()):
            item = self.waveform_list.item(i)
            if item and not item.isHidden():
                index = item.data(Qt.ItemDataRole.UserRole)
                self.traces[index].visible = True
                self.update_list_item_appearance(item, index)
        self.refresh_plot()

    def deselect_all_waveforms(self) -> None:
        for t in self.traces.values():
            t.visible = False
        for i in range(self.waveform_list.count()):
            item = self.waveform_list.item(i)
            if item:
                self.update_list_item_appearance(item, item.data(Qt.ItemDataRole.UserRole))
        self.refresh_plot()

    def show_list_context_menu(self, position: QtCore.QPoint) -> None:
        item = self.waveform_list.itemAt(position)
        if not item:
            return
        
        # Always work with just the right-clicked item
        menu = QMenu()
        
        # All menus apply only to the right-clicked item
        color_menu = menu.addMenu("Change colour ▶")
        self.populate_color_menu(color_menu, [item])
        
        thickness_menu = menu.addMenu("Thickness ▶")
        for thickness, label in THICKNESS_OPTIONS:
            action = thickness_menu.addAction(label)
            action.triggered.connect(lambda checked, t=thickness: self.change_thickness([item], t))
        
        style_menu = menu.addMenu("Style ▶")
        for style, label in LINE_STYLES:
            action = style_menu.addAction(label)
            action.triggered.connect(lambda checked, s=style: self.change_style([item], s))
        
        menu.addSeparator()
        
        rename_action = menu.addAction("Rename...")
        rename_action.triggered.connect(lambda: self.rename_trace(item))
        
        index = item.data(Qt.ItemDataRole.UserRole)
        t = self.traces[index]

        hide_show_action = menu.addAction("Hide" if t.visible else "Show")
        hide_show_action.triggered.connect(lambda: self.toggle_trace_visibility([item]))
        
        menu.addSeparator()
        
        properties_action = menu.addAction("Figure Options...")
        properties_action.triggered.connect(self.open_figure_options)
        
        menu.exec(self.waveform_list.mapToGlobal(position))

    def populate_color_menu(self, menu: QMenu, selected_items: List[QListWidgetItem]) -> None:
        color_widget = QWidget()
        color_widget.setStyleSheet("background-color: #FFFFFF;")
        grid_layout = QGridLayout(color_widget)
        grid_layout.setSpacing(2)
        for i, color in enumerate(self.color_palette):
            btn = QPushButton()
            btn.setFixedSize(24, 24)
            btn.setStyleSheet(f"QPushButton{{background-color:{color};border:1px solid #E0E0E0;border-radius:2px;}}QPushButton:hover{{border:2px solid #212121;}}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, c=color: self.change_color_and_close(selected_items, c, menu))
            grid_layout.addWidget(btn, i // 4, i % 4)
        widget_action = QWidgetAction(menu)
        widget_action.setDefaultWidget(color_widget)
        menu.addAction(widget_action)
        menu.addSeparator()
        more_action = menu.addAction("More...")
        more_action.triggered.connect(lambda: self.change_color_dialog(selected_items))

    def change_color_and_close(self, items: List[QListWidgetItem], color: str, menu: QMenu) -> None:
        self.change_color(items, color)
        parent = menu.parent()
        while isinstance(parent, QMenu):
            parent.close()
            parent = parent.parent()

    def change_color(self, items: List[QListWidgetItem], color: str) -> None:
        for item in items:
            index = item.data(Qt.ItemDataRole.UserRole)
            self.traces[index].update_line(color=color)
            self.update_list_item_appearance(item, index)
            if self.timing_check.isChecked() and hasattr(self, 'axes'):
                self.update_timing_tick_colors()
                for ann_text in self.timing_annotations.get(index, []):
                    ann_text.set_color(color)
        self.save_config()
        self.canvas.draw()

    def update_timing_tick_colors(self) -> None:
        if not hasattr(self, 'axes'):
            return
        visible_indices = [i for i, t in self.traces.items() if t.visible]
        ytick_labels = self.axes.get_yticklabels()
        for i, label in enumerate(ytick_labels):
            if i < len(visible_indices):
                idx = visible_indices[::-1][i]
                label.set_color(self.traces[idx].color)

    def change_color_dialog(self, items: List[QListWidgetItem]) -> None:
        color = QColorDialog.getColor()
        if color.isValid():
            self.change_color(items, color.name())

    def change_thickness(self, items: List[QListWidgetItem], thickness: float) -> None:
        for item in items:
            self.traces[item.data(Qt.ItemDataRole.UserRole)].update_line(thickness=thickness)
        self.save_config()
        self.canvas.draw()

    def change_style(self, items: List[QListWidgetItem], style: str) -> None:
        needs_replot = style == 'steps-post'
        for item in items:
            index = item.data(Qt.ItemDataRole.UserRole)
            if needs_replot:
                self.traces[index].style = style
            else:
                self.traces[index].update_line(style=style)
        self.save_config()
        if needs_replot:
            self.refresh_plot()
        else:
            self.canvas.draw()

    def rename_trace(self, item: QListWidgetItem) -> None:
        index = item.data(Qt.ItemDataRole.UserRole)
        t = self.traces[index]
        new_name, ok = QInputDialog.getText(self, "Rename Trace", "New name:", text=t.name)
        if ok and new_name and new_name != t.name:
            t.name = new_name
            self.obj_dataext.NBList[index] = new_name
            self.update_list_item_appearance(item, index)
            if self.legend_check.isChecked():
                self.refresh_plot()

    def toggle_trace_visibility(self, items: List[QListWidgetItem]) -> None:
        # Use t.visible as single source of truth — same path as left-click toggle.
        # Going directly to line_object.set_visible() bypasses refresh_plot and
        # gets stomped the next time anything triggers a redraw.
        any_visible = any(self.traces[item.data(Qt.ItemDataRole.UserRole)].visible for item in items)
        for item in items:
            index = item.data(Qt.ItemDataRole.UserRole)
            self.traces[index].visible = not any_visible
            self.update_list_item_appearance(item, index)
        self.refresh_plot()

    def open_figure_options(self) -> None:
        try:
            if hasattr(self.fig.canvas, 'toolbar') and hasattr(self.fig.canvas.toolbar, 'edit_parameters'):
                self.fig.canvas.toolbar.edit_parameters()
                return
            from matplotlib.backends.qt_compat import QtWidgets
            from matplotlib.backends.qt_editor import _formlayout
            if hasattr(_formlayout, 'FormDialog'):
                current_title = self.fig._suptitle.get_text() if self.fig._suptitle is not None else ''
                options = [('Title', current_title)]
                if hasattr(self, 'axes'):
                    options.extend([('X Label', self.axes.get_xlabel()), ('Y Label', self.axes.get_ylabel()), ('X Min', self.axes.get_xlim()[0]), ('X Max', self.axes.get_xlim()[1]), ('Y Min', self.axes.get_ylim()[0]), ('Y Max', self.axes.get_ylim()[1])])
                dialog = _formlayout.FormDialog(options, parent=self, title='Figure Options')
                if dialog.exec():
                    results = dialog.get_results()
                    if results:
                        self.fig.suptitle(results[0])
                        if hasattr(self, 'axes') and len(results) > 1:
                            self.axes.set_xlabel(results[1])
                            self.axes.set_ylabel(results[2])
                            self.axes.set_xlim(results[3], results[4])
                            self.axes.set_ylim(results[5], results[6])
                        self.canvas.draw()
            else:
                QMessageBox.information(self, "Figure Options", "Figure options are limited in this environment.\nYou can use the zoom and pan tools in the toolbar.")
        except Exception as e:
            logger.error(f"Error opening figure options: {e}")
            QMessageBox.information(self, "Figure Options", "Basic figure editing is available through the toolbar.")

    def on_timing_view_changed(self, state: int) -> None:
        timing_enabled = state == Qt.CheckState.Checked.value
        self.timing_box.content_area.setEnabled(timing_enabled)
        self.autoscale_check.setEnabled(not timing_enabled)
        self.refresh_plot()

    def refresh_plot(self) -> None:
        # Preserve zoom when autoscale is off.
        # Guard _last_was_timing: timing view y-axis is normalized [0..N] space,
        # not voltage/current — restoring it into a normal view clips all signals.
        saved_xlim = saved_ylim = None
        if (not self.autoscale_check.isChecked()
                and not self.timing_check.isChecked()
                and not self._last_was_timing
                and hasattr(self, 'axes')):
            saved_xlim = self.axes.get_xlim()
            saved_ylim = self.axes.get_ylim()

        self._func_line = None  # fig.clear() below wipes all artists
        self.timing_annotations.clear()
        self.fig.clear()
        for t in self.traces.values():
            t.line_object = None
        if self.timing_check.isChecked():
            self.axes = self.fig.add_subplot(111)
            self.plot_timing_diagram()
        else:
            if self.plot_type[0] == DataExtraction.AC_ANALYSIS:
                if self.plot_type[1] == 1:
                    self.on_push_decade()
                else:
                    self.on_push_ac()
            elif self.plot_type[0] == DataExtraction.TRANSIENT_ANALYSIS:
                self.on_push_trans()
            else:
                self.on_push_dc()
        if hasattr(self, 'axes'):
            self.axes.grid(self.grid_check.isChecked())
            if saved_xlim is not None:
                self.axes.set_xlim(saved_xlim)
                self.axes.set_ylim(saved_ylim)
            if self.legend_check.isChecked():
                self.fig.subplots_adjust(top=0.85, bottom=0.1)
                self.position_legend()
            else:
                self.fig.subplots_adjust(top=0.95, bottom=0.1)
        self._restore_cursors()
        self.canvas.draw()
        self._last_was_timing = self.timing_check.isChecked()

    def position_legend(self) -> None:
        if hasattr(self, 'axes') and self.legend_check.isChecked():
            handles, labels = [], []
            for idx in sorted(self.traces.keys()):
                t = self.traces[idx]
                if t.visible and t.line_object:
                    handles.append(t.line_object)
                    labels.append(t.name)
            if handles:
                ncol = min(6, len(handles)) if len(handles) > 6 else min(4, len(handles))
                legend = self.axes.legend(handles, labels, bbox_to_anchor=(0.5, 1.02), loc='lower center', ncol=ncol, frameon=True, fancybox=False, shadow=False, fontsize=LEGEND_FONT_SIZE, borderaxespad=0, columnspacing=1.5)
                frame = legend.get_frame()
                frame.set_facecolor('white')
                frame.set_edgecolor('#E0E0E0')
                frame.set_linewidth(1)
                frame.set_alpha(0.95)

    def _get_transient_start_idx(self, time_data: "np.ndarray") -> int:
        """Return the index into time_data where the .tran start time begins, or 0."""
        try:
            with open(os.path.join(self.file_path, "analysis"), 'r') as f:
                parts = f.read().strip().split()
            if len(parts) >= 4 and parts[0] == '.tran':
                start_time = float(parts[3])
                if start_time > 0:
                    return int(np.searchsorted(time_data, start_time))
        except Exception:
            pass
        return 0

    def plot_timing_diagram(self) -> None:
        """Plot digital timing diagram with normalized trace heights."""
        self.timing_annotations.clear()

        if self.plot_type[0] != DataExtraction.TRANSIENT_ANALYSIS:
            self.axes.text(0.5, 0.5, 'Digital timing view is only\navailable for transient analysis.',
                           ha='center', va='center', transform=self.axes.transAxes,
                           fontsize=11, color='#757575')
            self.axes.set_yticks([])
            self.axes.set_yticklabels([])
            return

        visible_indices = [i for i, t in self.traces.items() if t.visible]
        if not visible_indices:
            self.axes.text(0.5, 0.5, 'Select a waveform to display',
                           ha='center', va='center', transform=self.axes.transAxes)
            self.axes.set_yticks([])
            self.axes.set_yticklabels([])
            return

        manual_threshold = (None if self.threshold_spinbox.value() == self.threshold_spinbox.minimum()
                            else self.threshold_spinbox.value())
        if manual_threshold is None:
            self.threshold_spinbox.setSpecialValueText("Auto (midpoint)")
        self.logic_thresholds = {}

        # Build local float arrays for all traces — never touch obj_dataext
        time_data = np.asarray(self.obj_dataext.x, dtype=float)
        y_data = {i: np.asarray(self.obj_dataext.y[i], dtype=float)
                  for i in range(len(self.obj_dataext.y))}

        if self.plot_type[0] == DataExtraction.TRANSIENT_ANALYSIS:
            start_idx = self._get_transient_start_idx(time_data)
            if 0 < start_idx < len(time_data):
                time_data = time_data[start_idx:]
                y_data = {i: arr[start_idx:] for i, arr in y_data.items()}

        # Each trace occupies exactly 1.0 normalized unit of y-space.
        # spacing = vertical_spacing (e.g. 1.2 → 20% gap between traces).
        # This guarantees uniform height for all signals regardless of voltage domain.
        spacing = self.vertical_spacing
        yticks, ylabels = [], []

        for rank, idx in enumerate(visible_indices[::-1]):
            raw_data = y_data[idx]

            # Safety clamp — guards against malformed simulation output where a
            # y array is shorter or longer than the time axis. Use a local
            # trace_time so time_data is never mutated across iterations.
            n = min(len(raw_data), len(time_data))
            raw_data = raw_data[:n]
            trace_time = time_data[:n]

            trace_vmin, trace_vmax = np.min(raw_data), np.max(raw_data)
            trace_unit = "V" if idx < self.obj_dataext.volts_length else "A"

            if trace_vmax - trace_vmin < 1e-10:
                # Constant (DC) signal — state indeterminate, park at 0.5.
                # No threshold line drawn (nothing to threshold against).
                logic_normalized = np.full(n, 0.5)
            else:
                # Per-trace threshold: midpoint of its own swing (CMOS VDD/2 convention).
                # Manual override applies the user's voltage, normalized into [0,1] for
                # this trace so the axhline always sits within the trace bounds.
                threshold = (manual_threshold if manual_threshold is not None
                             else (trace_vmin + trace_vmax) / 2.0)
                logic_normalized = np.where(raw_data > threshold, 1.0, 0.0)
                threshold_norm = float(np.clip(
                    (threshold - trace_vmin) / (trace_vmax - trace_vmin), 0.0, 1.0
                ))
                self.logic_thresholds[idx] = threshold_norm

            logic_offset = logic_normalized + rank * spacing

            t = self.traces[idx]
            line, = self.axes.step(trace_time, logic_offset, where="post",
                                   linewidth=t.thickness, color=t.color, label=t.name)
            t.line_object = line

            # y_center is always rank * spacing + 0.5 in normalized space.
            y_center = rank * spacing + 0.5
            yticks.append(y_center)
            ylabels.append(t.name)

            ann = []
            xform = self.axes.get_yaxis_transform()
            if trace_vmax - trace_vmin < 1e-10:
                ann.append(self.axes.text(
                    1.01, y_center,
                    f"DC: {_format_measurement(float(trace_vmax), trace_unit)}",
                    transform=xform, va='center', ha='left',
                    fontsize=8, color=t.color, clip_on=False))
            else:
                ann.append(self.axes.text(
                    1.01, rank * spacing + 0.82,
                    f"H: {_format_measurement(float(trace_vmax), trace_unit)}",
                    transform=xform, va='center', ha='left',
                    fontsize=8, color=t.color, clip_on=False))
                ann.append(self.axes.text(
                    1.01, rank * spacing + 0.18,
                    f"L: {_format_measurement(float(trace_vmin), trace_unit)}",
                    transform=xform, va='center', ha='left',
                    fontsize=8, color=t.color, clip_on=False))
                freq = _detect_frequency(trace_time, logic_normalized)
                if freq is not None:
                    ann.append(self.axes.text(
                        1.01, y_center, _format_frequency(freq),
                        transform=xform, va='center', ha='left',
                        fontsize=7.5, color=t.color, alpha=0.75, clip_on=False))
            self.timing_annotations[idx] = ann

        # Y-axis bounds: normalized traces sit in [0,1] per rank, evenly spaced.
        total_height = (len(visible_indices) - 1) * spacing + 1.0
        margin = 0.15 * spacing
        self.axes.set_ylim(-margin, total_height + margin)
        self.axes.set_yticks(yticks)
        self.axes.set_yticklabels(ylabels, fontsize=8)

        self.update_timing_tick_colors()
        self.set_time_axis_label(time_data)

        # Threshold lines: logic_thresholds stores normalized [0,1] position,
        # so axhline y = threshold_norm + rank * spacing sits correctly within the trace.
        for rank, idx in enumerate(visible_indices[::-1]):
            if idx in self.logic_thresholds:
                self.axes.axhline(y=self.logic_thresholds[idx] + rank * spacing,
                                  color='red', linestyle=':', alpha=THRESHOLD_ALPHA, linewidth=0.8)

        if not self.legend_check.isChecked():
            self.axes.set_title('Digital Timing Diagram', fontsize=10, pad=10)

    def set_time_axis_label(self, time_data: Optional["np.ndarray"] = None) -> None:
        if not hasattr(self, 'axes') or not hasattr(self.obj_dataext, 'x'):
            return
        if time_data is None:
            time_data = np.asarray(self.obj_dataext.x, dtype=float)
        if len(time_data) < 2:
            self.axes.set_xlabel('Time (s)', fontsize=10)
            return
        scale, unit = self._get_time_scale_and_unit(time_data)
        scaled_time = time_data * scale
        for line in (t.line_object for t in self.traces.values()):
            if line:
                line.set_xdata(line.get_xdata() * scale)
        self.axes.set_xlim(scaled_time[0], scaled_time[-1])
        self.axes.set_xlabel(f'Time ({unit})', fontsize=10)

    def on_threshold_changed(self, value: float) -> None:
        if self.timing_check.isChecked():
            self.refresh_plot()

    def on_spacing_changed(self, value: int) -> None:
        self.vertical_spacing = value / 100.0
        self.spacing_label.setText(f"{self.vertical_spacing:.1f}x")
        if self.timing_check.isChecked():
            self.refresh_plot()

    def _find_nearest_cursor(self, event) -> Optional[int]:
        """Return cursor index if the click is within 8px of an existing cursor line."""
        if not self.cursor_lines or not hasattr(self, 'axes') or event.xdata is None:
            return None
        xlim = self.axes.get_xlim()
        width_px = self.axes.get_window_extent().width
        if width_px == 0:
            return None
        threshold = 8 * (xlim[1] - xlim[0]) / width_px
        for i, line in enumerate(self.cursor_lines):
            if line is None:
                continue
            if abs(event.xdata - line.get_xdata()[0]) < threshold:
                return i
        return None

    def _update_cursor_position(self, cursor_num: int, x_pos_scaled: float) -> None:
        """Move an existing cursor line without recreating it (fast path for dragging)."""
        if cursor_num >= len(self.cursor_lines) or self.cursor_lines[cursor_num] is None:
            self.set_cursor(cursor_num, x_pos_scaled)
            return
        self.cursor_lines[cursor_num].set_xdata([x_pos_scaled, x_pos_scaled])
        scale = self._current_time_scale()
        x_pos_original = x_pos_scaled / scale
        self.cursor_positions[cursor_num] = x_pos_original
        label = self.cursor1_label if cursor_num == 0 else self.cursor2_label
        label.setText(f"Cursor {cursor_num + 1}: {x_pos_scaled:.6g}")
        if len(self.cursor_positions) >= 2 and all(p is not None for p in self.cursor_positions[:2]):
            delta_original = abs(self.cursor_positions[1] - self.cursor_positions[0])
            self.delta_label.setText(f"Delta: {delta_original * scale:.6g}")
            if delta_original > 0:
                self.measure_label.setText(f"Freq: {1.0 / delta_original:.6g} Hz")
        self.canvas.draw_idle()

    def _get_time_scale_and_unit(self, time_data: Optional["np.ndarray"] = None) -> Tuple[float, str]:
        """Single source of truth for time-axis unit selection.

        All callers (set_time_axis_label, _current_time_scale, set_cursor)
        derive their scale factor from here — ensures they can never diverge.
        time_data defaults to obj_dataext.x; pass a trimmed slice when a
        subset of the axis is being displayed (e.g. transient start offset).
        """
        if time_data is None:
            time_data = np.asarray(self.obj_dataext.x, dtype=float)
        time_span = abs(time_data[-1] - time_data[0]) if len(time_data) > 1 else 0.0
        if time_span == 0:                         return 1.0,  's'
        if time_span < TIME_UNIT_THRESHOLD_PS:     return 1e12, 'ps'
        if time_span < TIME_UNIT_THRESHOLD_NS:     return 1e9,  'ns'
        if time_span < TIME_UNIT_THRESHOLD_US:     return 1e6,  'µs'
        if time_span < TIME_UNIT_THRESHOLD_MS:     return 1e3,  'ms'
        return 1.0, 's'

    def _current_time_scale(self) -> float:
        return self._get_time_scale_and_unit()[0]

    def on_canvas_click(self, event) -> None:
        if not hasattr(self, 'axes') or event.inaxes != self.axes:
            return
        if self.nav_toolbar.mode:
            return
        near = self._find_nearest_cursor(event)
        if event.button == 1:
            if near is not None:
                self._drag_cursor_idx = near
            else:
                self._drag_cursor_idx = None
                self.set_cursor(0, event.xdata)
        elif event.button == 3:
            if near is not None:
                self._drag_cursor_idx = near
            else:
                self._drag_cursor_idx = None
                self.set_cursor(1, event.xdata)

    def on_canvas_release(self, event) -> None:
        self._drag_cursor_idx = None

    def set_cursor(self, cursor_num: int, x_pos_scaled: float) -> None:
        scale = self._current_time_scale()
        x_pos_original = x_pos_scaled / scale

        if cursor_num < len(self.cursor_lines) and self.cursor_lines[cursor_num]:
            self.cursor_lines[cursor_num].remove()
        
        color = 'red' if cursor_num == 0 else 'blue'
        line = self.axes.axvline(x=x_pos_scaled, color=color, linestyle='--', alpha=CURSOR_ALPHA)

        if cursor_num >= len(self.cursor_lines):
            self.cursor_lines.append(line)
            self.cursor_positions.append(x_pos_original)
        else:
            self.cursor_lines[cursor_num] = line
            self.cursor_positions[cursor_num] = x_pos_original

        label_widget = self.cursor1_label if cursor_num == 0 else self.cursor2_label
        label_widget.setText(f"Cursor {cursor_num + 1}: {x_pos_scaled:.6g}")

        if len(self.cursor_positions) >= 2 and all(p is not None for p in self.cursor_positions[:2]):
            delta_original = abs(self.cursor_positions[1] - self.cursor_positions[0])
            delta_scaled = delta_original * scale
            self.delta_label.setText(f"Delta: {delta_scaled:.6g}")
            if delta_original > 0:
                freq_delta = 1.0 / delta_original
                self.measure_label.setText(f"Freq: {freq_delta:.6g} Hz")
        self.canvas.draw()

    def clear_cursors(self) -> None:
        for line in self.cursor_lines:
            if line:
                try:
                    line.remove()
                except ValueError:
                    pass  # already removed by fig.clear()
        self.cursor_lines.clear()
        self.cursor_positions.clear()
        self.cursor1_label.setText("Cursor 1: Not set")
        self.cursor2_label.setText("Cursor 2: Not set")
        self.delta_label.setText("Delta: --")
        self.measure_label.setText("")
        self.canvas.draw()

    def _restore_cursors(self) -> None:
        """Re-create cursor axvlines after fig.clear(), using stored positions."""
        if not hasattr(self, 'axes') or not self.cursor_positions:
            return
        scale = self._current_time_scale()
        colors = ['red', 'blue']
        new_lines: List[Optional[Line2D]] = []
        for i, x_orig in enumerate(self.cursor_positions):
            if x_orig is None:
                new_lines.append(None)
                continue
            color = colors[i] if i < len(colors) else 'green'
            line = self.axes.axvline(
                x=x_orig * scale, color=color, linestyle='--', alpha=CURSOR_ALPHA
            )
            new_lines.append(line)
        self.cursor_lines = new_lines
        if new_lines:
            logger.debug("Restored %d cursor(s) after plot refresh", len(new_lines))

    def on_mouse_move(self, event) -> None:
        if event.inaxes:
            self.coord_label.setText(f"X: {event.xdata:.6g}, Y: {event.ydata:.6g}")
            if self._drag_cursor_idx is not None:
                self._update_cursor_position(self._drag_cursor_idx, event.xdata)
        else:
            self.coord_label.setText("X: --, Y: --")

    def on_key_press(self, event) -> None:
        if event.key == 'g': self.grid_check.toggle()
        elif event.key == 'l': self.legend_check.toggle()
        elif event.key == 'p': self.open_figure_options()
        elif event.key == 'escape':
            mode = str(self.nav_toolbar.mode).lower()
            if 'zoom' in mode:
                self.nav_toolbar.zoom()
            elif 'pan' in mode:
                self.nav_toolbar.pan()
            else:
                self.clear_cursors()

    def on_scroll(self, event) -> None:
        if not event.inaxes: return
        xlim, ylim = event.inaxes.get_xlim(), event.inaxes.get_ylim()
        zoom_factor = DEFAULT_ZOOM_FACTOR if event.button == 'up' else 1 / DEFAULT_ZOOM_FACTOR
        if event.key == 'control':
            x_center, y_center = event.xdata, event.ydata
            x_range, y_range = (xlim[1] - xlim[0]) * zoom_factor, (ylim[1] - ylim[0]) * zoom_factor
            x_ratio, y_ratio = (x_center - xlim[0]) / (xlim[1] - xlim[0]), (y_center - ylim[0]) / (ylim[1] - ylim[0])
            event.inaxes.set_xlim(x_center - x_range * x_ratio, x_center + x_range * (1 - x_ratio))
            event.inaxes.set_ylim(y_center - y_range * y_ratio, y_center + y_range * (1 - y_ratio))
        elif event.key == 'shift':
            pan_distance = (xlim[1] - xlim[0]) * 0.1 * (-1 if event.button == 'up' else 1)
            event.inaxes.set_xlim(xlim[0] + pan_distance, xlim[1] + pan_distance)
        self.canvas.draw()

    def export_image(self) -> None:
        file_name, file_filter = QFileDialog.getSaveFileName(self, "Export Image", "", "PNG Files (*.png);;SVG Files (*.svg);;All Files (*)")
        if file_name:
            try:
                fmt = 'svg' if "svg" in file_filter else 'png'
                if '.' not in os.path.basename(file_name): file_name += f'.{fmt}'
                self.fig.savefig(file_name, format=fmt, dpi=DEFAULT_EXPORT_DPI, bbox_inches='tight')
                self.status_bar.showMessage(f"Image exported to {file_name}", 3000)
            except Exception as e:
                logger.error(f"Error exporting image: {e}")
                QMessageBox.warning(self, "Export Error", f"Failed to export image: {str(e)}")

    def clear_plot(self) -> None:
        self.timing_annotations.clear()
        self.deselect_all_waveforms()

    def zoom_in(self) -> None:
        if not hasattr(self, 'axes'):
            return
        xlim, ylim = self.axes.get_xlim(), self.axes.get_ylim()
        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        x_half = (xlim[1] - xlim[0]) * DEFAULT_ZOOM_FACTOR / 2
        y_half = (ylim[1] - ylim[0]) * DEFAULT_ZOOM_FACTOR / 2
        self.axes.set_xlim(x_center - x_half, x_center + x_half)
        self.axes.set_ylim(y_center - y_half, y_center + y_half)
        self.canvas.draw()

    def zoom_out(self) -> None:
        if not hasattr(self, 'axes'):
            return
        xlim, ylim = self.axes.get_xlim(), self.axes.get_ylim()
        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        x_half = (xlim[1] - xlim[0]) / (DEFAULT_ZOOM_FACTOR * 2)
        y_half = (ylim[1] - ylim[0]) / (DEFAULT_ZOOM_FACTOR * 2)
        self.axes.set_xlim(x_center - x_half, x_center + x_half)
        self.axes.set_ylim(y_center - y_half, y_center + y_half)
        self.canvas.draw()

    def reset_view(self) -> None:
        if hasattr(self, 'axes'): self.nav_toolbar.home()

    def toggle_grid(self) -> None:
        if hasattr(self, 'axes'):
            self.axes.grid(self.grid_check.isChecked())
            self.canvas.draw()

    def toggle_legend(self) -> None:
        self.refresh_plot()

    @staticmethod
    def _safe_eval_expr(expr_str, variables):
        """
        Safely evaluate a math expression string containing only arithmetic
        operations (+, -, *, /, **) on known trace-name variables.

        Uses Python's ast module to parse the expression into a syntax tree,
        then walks it to reject any node that is not a safe arithmetic
        operation, numeric literal, or known variable name.

        This replaces the previous eval() call which allowed arbitrary code
        execution (file I/O, os.system, __import__, etc.).

        Args:
            expr_str: The user-supplied expression string.
            variables: Dict mapping trace names to numpy arrays.

        Returns:
            The result of evaluating the expression (typically a numpy array).

        Raises:
            ValueError: If the expression contains unsafe constructs.
        """
        _SAFE_BINOPS = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
        }
        _SAFE_UNARYOPS = {
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
        }

        def _eval_node(node):
            # Numeric constants: 3, 2.5, etc.
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            # Variable names — must be a known trace name
            if isinstance(node, ast.Name):
                if node.id in variables:
                    return variables[node.id]
                raise ValueError(
                    f"Unknown variable '{node.id}'. "
                    f"Available traces: {list(variables.keys())}"
                )
            # Binary operations: a + b, a * b, etc.
            if isinstance(node, ast.BinOp):
                op_func = _SAFE_BINOPS.get(type(node.op))
                if op_func is None:
                    raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
                return op_func(_eval_node(node.left), _eval_node(node.right))
            # Unary operations: -a, +a
            if isinstance(node, ast.UnaryOp):
                op_func = _SAFE_UNARYOPS.get(type(node.op))
                if op_func is None:
                    raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
                return op_func(_eval_node(node.operand))
            # Function calls — only allow safe numpy functions
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    # Allow np.abs(), np.sqrt(), np.log(), np.sin(), etc.
                    if (isinstance(node.func.value, ast.Name)
                            and node.func.value.id == 'np'
                            and node.func.attr in (
                                'abs', 'sqrt', 'log', 'log10', 'log2',
                                'sin', 'cos', 'tan', 'exp', 'mean',
                                'max', 'min', 'sum', 'diff',
                            )):
                        func = getattr(np, node.func.attr)
                        args = [_eval_node(a) for a in node.args]
                        return func(*args)
                raise ValueError(
                    f"Function calls are not allowed except: "
                    f"np.abs, np.sqrt, np.log, np.sin, np.cos, np.tan, "
                    f"np.exp, np.mean, np.max, np.min, np.sum, np.diff"
                )
            raise ValueError(
                f"Unsafe expression element: {type(node).__name__}. "
                f"Only arithmetic (+, -, *, /, **) on trace names is allowed."
            )

        try:
            tree = ast.parse(expr_str, mode='eval')
        except SyntaxError as e:
            raise ValueError(f"Invalid expression syntax: {e}")

        return _eval_node(tree.body)

    def plot_function(self) -> None:
        """Plot a user-defined function expression.

        Supports two formats:
          - "trace1 vs trace2"  — X-Y plot of one trace against another
          - Arithmetic expression — e.g. "v(out) + v(in)", "v(out) * 2"

        The expression evaluator uses a safe AST-based parser that only
        allows arithmetic operations on known trace names, preventing
        arbitrary code execution.
        """
        function_text = self.func_input.text()
        if not function_text:
            QMessageBox.warning(self, "Input Error", "Function input cannot be empty.")
            return

        # Remove previous function trace before adding new one
        if self._func_line is not None:
            try:
                self._func_line.remove()
            except ValueError:
                pass  # already cleared by a refresh_plot
            self._func_line = None

        if ' vs ' in function_text:
            parts = function_text.split(' vs ', 1)
            y_name, x_name = parts[0].strip(), parts[1].strip()
            if not y_name or not x_name:
                QMessageBox.warning(self, "Syntax Error", "Use format 'trace1 vs trace2'.")
                return
            try:
                x_idx = self.obj_dataext.NBList.index(x_name)
                y_idx = self.obj_dataext.NBList.index(y_name)
                x_data = np.array(self.obj_dataext.y[x_idx], dtype=float)
                y_data = np.array(self.obj_dataext.y[y_idx], dtype=float)
                is_voltage_x = x_idx < self.volts_length
                is_voltage_y = y_idx < self.volts_length
                line, = self.axes.plot(x_data, y_data, label=function_text)
                self._func_line = line
                self.axes.set_xlabel(f"{x_name} ({'V' if is_voltage_x else 'A'})")
                self.axes.set_ylabel(f"{y_name} ({'V' if is_voltage_y else 'A'})")
            except ValueError:
                QMessageBox.warning(self, "Trace Not Found", f"Could not find one of the traces: {x_name}, {y_name}")
                return
        else:
            # Safe expression evaluation using AST-based parser.
            # Only arithmetic operations on known trace names are allowed.
            #
            # Trace names like "v(out)" contain parentheses which Python's
            # AST would parse as function calls. We substitute them with
            # safe placeholder identifiers before parsing.
            try:
                # Build placeholder mapping: sorted longest-first to avoid
                # partial-match collisions (e.g. "v(out)" before "v(o)")
                trace_variables = {}
                expr_safe = function_text
                sorted_names = sorted(
                    self.obj_dataext.NBList, key=len, reverse=True
                )
                for i, name in enumerate(sorted_names):
                    placeholder = f"_trace_{i}_"
                    if name in expr_safe:
                        # Use regex with negative lookbehind/lookahead for word characters
                        # to ensure we only replace exact trace names and not substrings
                        # of other words. e.g. replacing 'in' should not affect 'sin(in)'.
                        # Because trace names contain parens (v(out)), we use \w boundaries.
                        pattern = r'(?<![\w])' + re.escape(name) + r'(?![\w])'
                        expr_safe = re.sub(pattern, placeholder, expr_safe)
                        orig_idx = self.obj_dataext.NBList.index(name)
                        trace_variables[placeholder] = np.array(
                            self.obj_dataext.y[orig_idx], dtype=float
                        )
                # Expose 'np' so np.func() calls work
                trace_variables['np'] = np

                y_data = self._safe_eval_expr(expr_safe, trace_variables)
                x_data = np.array(self.obj_dataext.x, dtype=float)
                line, = self.axes.plot(x_data, y_data, label=function_text)
                self._func_line = line

            except (ValueError, TypeError) as e:
                QMessageBox.warning(self, "Evaluation Error", f"Could not plot function: {e}")
                return
            except Exception as e:
                logger.error(f"Unexpected error in plot_function: {e}")
                QMessageBox.warning(self, "Evaluation Error", f"Could not plot function: {e}")
                return

        if self.legend_check.isChecked():
            self.position_legend()
        self.canvas.draw()


    def multi_meter(self) -> None:
        visible = [(idx, t) for idx, t in self.traces.items() if t.visible]
        if not visible:
            QMessageBox.warning(self, "Warning", "Please select at least one waveform")
            return
        location_x, location_y = 300, 300
        for idx, t in visible:
            rms_value = self.get_rms_value(self.obj_dataext.y[idx])
            meter = MultimeterWidgetClass(t.name, rms_value, location_x, location_y, idx < self.obj_dataext.volts_length)
            self._meters.append(meter)  # keep strong ref — no parent, otherwise GC'd
            if hasattr(self.obj_appconfig, 'dock_dict') and self.obj_appconfig.current_project['ProjectName'] in self.obj_appconfig.dock_dict:
                self.obj_appconfig.dock_dict[self.obj_appconfig.current_project['ProjectName']].append(meter)
            location_x += 50
            location_y += 50

    def get_rms_value(self, data_points: List) -> Decimal:
        getcontext().prec = 5
        return Decimal(str(np.sqrt(np.mean(np.square([float(x) for x in data_points])))))

    def _plot_analysis_data(self, analysis_type: str) -> None:
        self.axes = self.fig.add_subplot(111)
        traces_plotted = 0
        first_visible = None
        x_data = np.asarray(self.obj_dataext.x, dtype=float)
        for idx, t in self.traces.items():
            if not t.visible:
                continue
            traces_plotted += 1
            if first_visible is None:
                first_visible = idx
            y_data = np.asarray(self.obj_dataext.y[idx], dtype=float)
            plot_style = '-' if t.style == 'steps-post' else t.style
            plot_kwargs: dict = {}
            if t.style == 'steps-post' and analysis_type in ['transient', 'dc']:
                plot_func = self.axes.step
                plot_kwargs['where'] = 'post'
            elif analysis_type == 'ac_log':
                plot_func = self.axes.semilogx
            else:
                plot_func = self.axes.plot
            line, = plot_func(x_data, y_data, color=t.color, label=t.name,
                              linewidth=t.thickness, linestyle=plot_style, **plot_kwargs)
            t.line_object = line

        if analysis_type in ['ac_linear', 'ac_log']:
            self.axes.set_xlabel('Frequency (Hz)')
        elif analysis_type == 'dc':
            self.axes.set_xlabel('Voltage Sweep (V)')

        if first_visible is not None:
            self.axes.set_ylabel('Voltage (V)' if first_visible < self.volts_length else 'Current (A)')

        if traces_plotted == 0:
            self.axes.text(0.5, 0.5, 'Please select a waveform to plot', ha='center', va='center', transform=self.axes.transAxes)

        if analysis_type == 'transient':
            self.set_time_axis_label()


    def on_push_decade(self) -> None:
        self._plot_analysis_data('ac_log')

    def on_push_ac(self) -> None:
        self._plot_analysis_data('ac_linear')

    def on_push_trans(self) -> None:
        self._plot_analysis_data('transient')

    def on_push_dc(self) -> None:
        self._plot_analysis_data('dc')

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        if self.parent():
            self.parent().updateGeometry()
        if hasattr(self, 'canvas') and self.canvas:
            self.canvas.draw_idle()

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(1200, 800)

    def minimumSizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(400, 300)
