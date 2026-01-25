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
from pathlib import Path
from decimal import Decimal, getcontext
from typing import Dict, List, Optional, Tuple, Any, Union

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt, QSettings, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QListWidget, QListWidgetItem, QPushButton,
                             QCheckBox, QRadioButton, QButtonGroup, QGroupBox,
                             QLabel, QLineEdit, QSlider, QDoubleSpinBox, QMenu,
                             QAction, QFileDialog, QColorDialog, QInputDialog,
                             QMessageBox, QErrorMessage, QStatusBar, QStyle,
                             QSplitter, QToolButton, QWidgetAction, QGridLayout,
                             QSpacerItem, QSizePolicy,QScrollArea)
from PyQt5.QtGui import (QColor, QBrush, QPalette, QKeySequence,
                         QPainter, QPixmap, QFont)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
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
        self.setSelectionMode(QListWidget.MultiSelection)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        super().paintEvent(event)


class plotWindow(QWidget):
    """Main plotting widget for NGSpice simulation results."""

    def __init__(self, file_path: str, project_name: str, parent=None) -> None:
        super().__init__(parent)

        self.file_path = file_path
        self.project_name = project_name
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
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
        self.active_traces: Dict[int, Line2D] = {}
        self.trace_visibility: Dict[int, bool] = {}
        self.trace_colors: Dict[int, str] = {}
        self.trace_thickness: Dict[int, float] = {}
        self.trace_style: Dict[int, str] = {}
        self.trace_names: Dict[int, str] = {}
        self.cursor_lines: List[Optional[Line2D]] = []
        self.cursor_positions: List[Optional[float]] = []
        self.timing_annotations: Dict[int, Any] = {}
        self.color_palette = VIBRANT_COLOR_PALETTE.copy()
        self.color: List[str] = []
        self.color_index = 0
        self.logic_threshold: Optional[float] = None
        self.vertical_spacing = DEFAULT_VERTICAL_SPACING

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
            self.config['trace_colours'] = {self.trace_names.get(idx, self.obj_dataext.NBList[idx]): color for idx, color in self.trace_colors.items()}
            self.config['trace_thickness'] = {self.trace_names.get(idx, self.obj_dataext.NBList[idx]): thickness for idx, thickness in self.trace_thickness.items()}
            self.config['trace_style'] = {self.trace_names.get(idx, self.obj_dataext.NBList[idx]): style for idx, style in self.trace_style.items()}
            temp_file = self.config_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as config_file:
                json.dump(self.config, config_file, indent=2)
            temp_file.replace(self.config_file)
        except Exception as e:
            logger.error(f"Error saving config: {e}")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.save_config()
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
        content_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        main_layout = QHBoxLayout(content_widget)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        left_widget = self.create_waveform_list()
        self.splitter.addWidget(left_widget)
        center_widget = self.create_plot_area()
        self.splitter.addWidget(center_widget)
        right_widget = self.create_control_panel()
        scroll_area = QScrollArea()
        scroll_area.setWidget(right_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
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
        self.waveform_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.waveform_list.customContextMenuRequested.connect(self.show_list_context_menu)
        self.waveform_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.waveform_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
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
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.setContextMenuPolicy(Qt.CustomContextMenu)
        self.canvas.customContextMenuRequested.connect(self.show_canvas_context_menu)
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
        self.threshold_spinbox.setSuffix(" V")
        self.threshold_spinbox.setSpecialValueText("Auto")
        self.threshold_spinbox.valueChanged.connect(self.on_threshold_changed)
        threshold_layout.addWidget(self.threshold_spinbox)
        timing_layout.addLayout(threshold_layout)
        spacing_layout = QHBoxLayout()
        spacing_layout.addWidget(QLabel("Spacing:"))
        self.spacing_slider = QSlider(Qt.Horizontal)
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
        for i in range(0, self.data_info[0] - 1):
            color_idx = i % len(self.color_palette)
            self.color.append(self.color_palette[color_idx])
        self.volts_length = self.data_info[1]
        if self.plot_type[0] == DataExtraction.AC_ANALYSIS:
            self.analysis_label.setText("AC Analysis")
        elif self.plot_type[0] == DataExtraction.TRANSIENT_ANALYSIS:
            self.analysis_label.setText("Transient Analysis")
        else:
            self.analysis_label.setText("DC Analysis")
        for i, name in enumerate(self.obj_dataext.NBList):
            self.trace_names[i] = name
        self.populate_waveform_list()

    def create_colored_icon(self, color: QColor, is_selected: bool) -> QtGui.QIcon:
        pixmap = QPixmap(18, 18)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        if is_selected:
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(1, 1, 16, 16)
        else:
            painter.setBrush(Qt.NoBrush)
            pen = QtGui.QPen(QColor("#9E9E9E"))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawEllipse(2, 2, 14, 14)
        painter.end()
        return QtGui.QIcon(pixmap)

    def populate_waveform_list(self) -> None:
        self.waveform_list.clear()
        saved_colors = self.config.get('trace_colours', {})
        saved_thickness = self.config.get('trace_thickness', {})
        saved_style = self.config.get('trace_style', {})
        for i, node_name in enumerate(self.obj_dataext.NBList):
            item = QListWidgetItem()
            item.setData(Qt.UserRole, i)
            if node_name in saved_colors:
                self.trace_colors[i] = saved_colors[node_name]
            elif i < len(self.color):
                self.trace_colors[i] = self.color[i]
            else:
                color_idx = i % len(self.color_palette)
                self.trace_colors[i] = self.color_palette[color_idx]
            if node_name in saved_thickness:
                self.trace_thickness[i] = saved_thickness[node_name]
            else:
                self.trace_thickness[i] = DEFAULT_LINE_THICKNESS
            if node_name in saved_style:
                self.trace_style[i] = saved_style[node_name]
            else:
                self.trace_style[i] = '-'
            item.setToolTip("Voltage signal" if i < self.obj_dataext.volts_length else "Current signal")
            self.trace_visibility[i] = False
            self.waveform_list.addItem(item)
            self.update_list_item_appearance(item, i)

    def filter_waveforms(self, text: str) -> None:
        for i in range(self.waveform_list.count()):
            item = self.waveform_list.item(i)
            if item:
                item.setHidden(text.lower() not in item.text().lower())

    def on_waveform_toggle(self, item: QListWidgetItem) -> None:
        index = item.data(Qt.UserRole)
        self.trace_visibility[index] = item.isSelected()
        if item.isSelected() and index not in self.trace_colors:
            self.assign_trace_color(index)
        self.update_list_item_appearance(item, index)
        self.refresh_plot()

    def assign_trace_color(self, index: int) -> None:
        used_colors = set(self.trace_colors.values())
        available_colors = [color for color in self.color_palette if color not in used_colors]
        if available_colors:
            self.trace_colors[index] = available_colors[0]
        else:
            hue = (0.618033988749895 * len(self.trace_colors)) % 1.0
            color = QtGui.QColor.fromHsvF(hue, 0.7, 0.8)
            self.trace_colors[index] = color.name()
        self.save_config()

    def update_list_item_appearance(self, item: QListWidgetItem, index: int) -> None:
        node_name = self.trace_names.get(index, self.obj_dataext.NBList[index])
        is_selected = self.trace_visibility.get(index, False)
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(10)
        icon_label = QLabel()
        color = QColor(self.trace_colors[index]) if is_selected and index in self.trace_colors else QColor("#9E9E9E")
        icon = self.create_colored_icon(color, is_selected)
        icon_label.setPixmap(icon.pixmap(18, 18))
        text_label = QLabel(node_name)
        text_label.setStyleSheet("color: #212121; font-weight: 500;" if is_selected and index in self.trace_colors else "color: #757575; font-weight: normal;")
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()
        self.waveform_list.setItemWidget(item, widget)
        item.setText(node_name)

    def select_all_waveforms(self) -> None:
        for i in range(self.waveform_list.count()):
            item = self.waveform_list.item(i)
            if item and not item.isHidden():
                item.setSelected(True)
                index = item.data(Qt.UserRole)
                self.trace_visibility[index] = True
                if index not in self.trace_colors:
                    self.assign_trace_color(index)
                self.update_list_item_appearance(item, index)
        self.refresh_plot()

    def deselect_all_waveforms(self) -> None:
        self.waveform_list.clearSelection()
        for index in self.trace_visibility:
            self.trace_visibility[index] = False
        for i in range(self.waveform_list.count()):
            item = self.waveform_list.item(i)
            if item:
                index = item.data(Qt.UserRole)
                self.update_list_item_appearance(item, index)
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
        
        index = item.data(Qt.UserRole)
        visible = False
        if index in self.active_traces and self.active_traces[index]:
            visible = self.active_traces[index].get_visible()
        
        hide_show_action = menu.addAction("Show" if not visible else "Hide")
        if visible:
            hide_show_action.setCheckable(True)
            hide_show_action.setChecked(True)
        hide_show_action.triggered.connect(lambda: self.toggle_trace_visibility([item]))
        
        menu.addSeparator()
        
        properties_action = menu.addAction("Figure Options...")
        properties_action.triggered.connect(self.open_figure_options)
        
        menu.exec_(self.waveform_list.mapToGlobal(position))

    def show_canvas_context_menu(self, position: QtCore.QPoint) -> None:
        menu = QMenu()
        export_action = menu.addAction("Export Image...")
        export_action.triggered.connect(self.export_image)
        menu.addSeparator()
        clear_action = menu.addAction("Clear Plot")
        clear_action.triggered.connect(self.clear_plot)
        menu.exec_(self.canvas.mapToGlobal(position))

    def populate_color_menu(self, menu: QMenu, selected_items: List[QListWidgetItem]) -> None:
        color_widget = QWidget()
        color_widget.setStyleSheet("background-color: #FFFFFF;")
        grid_layout = QGridLayout(color_widget)
        grid_layout.setSpacing(2)
        for i, color in enumerate(self.color_palette):
            btn = QPushButton()
            btn.setFixedSize(24, 24)
            btn.setStyleSheet(f"QPushButton{{background-color:{color};border:1px solid #E0E0E0;border-radius:2px;}}QPushButton:hover{{border:2px solid #212121;}}")
            btn.setCursor(Qt.PointingHandCursor)
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
            index = item.data(Qt.UserRole)
            self.trace_colors[index] = color
            self.update_list_item_appearance(item, index)
            if index in self.active_traces and self.active_traces[index]:
                self.active_traces[index].set_color(color)
            if self.timing_check.isChecked() and hasattr(self, 'axes'):
                self.update_timing_tick_colors()
                if hasattr(self, 'timing_annotations') and index in self.timing_annotations:
                    self.timing_annotations[index].set_color(color)
        self.save_config()
        self.canvas.draw()

    def update_timing_tick_colors(self) -> None:
        if not hasattr(self, 'axes'):
            return
        visible_indices = [i for i, v in self.trace_visibility.items() if v]
        ytick_labels = self.axes.get_yticklabels()
        for i, label in enumerate(ytick_labels):
            if i < len(visible_indices):
                idx = visible_indices[::-1][i]
                if idx in self.trace_colors:
                    label.set_color(self.trace_colors[idx])

    def change_color_dialog(self, items: List[QListWidgetItem]) -> None:
        color = QColorDialog.getColor()
        if color.isValid():
            self.change_color(items, color.name())

    def change_thickness(self, items: List[QListWidgetItem], thickness: float) -> None:
        for item in items:
            index = item.data(Qt.UserRole)
            self.trace_thickness[index] = thickness
            if index in self.active_traces and self.active_traces[index]:
                self.active_traces[index].set_linewidth(thickness)
        self.save_config()
        self.canvas.draw()

    def change_style(self, items: List[QListWidgetItem], style: str) -> None:
        for item in items:
            index = item.data(Qt.UserRole)
            self.trace_style[index] = style
            if index in self.active_traces and self.active_traces[index]:
                if style == 'steps-post':
                    self.refresh_plot()
                    return
                else:
                    self.active_traces[index].set_linestyle(style)
        self.save_config()
        self.canvas.draw()

    def rename_trace(self, item: QListWidgetItem) -> None:
        index = item.data(Qt.UserRole)
        current_name = self.trace_names.get(index, self.obj_dataext.NBList[index])
        new_name, ok = QInputDialog.getText(self, "Rename Trace", "New name:", text=current_name)
        if ok and new_name and new_name != current_name:
            self.trace_names[index] = new_name
            self.update_list_item_appearance(item, index)
            self.obj_dataext.NBList[index] = new_name
            if self.legend_check.isChecked():
                self.refresh_plot()

    def toggle_trace_visibility(self, items: List[QListWidgetItem]) -> None:
        any_visible = any(item.data(Qt.UserRole) in self.active_traces and self.active_traces[item.data(Qt.UserRole)].get_visible() for item in items)
        for item in items:
            index = item.data(Qt.UserRole)
            if index in self.active_traces and self.active_traces[index]:
                self.active_traces[index].set_visible(not any_visible)
        self.canvas.draw()

    def open_figure_options(self) -> None:
        try:
            if hasattr(self.fig.canvas, 'toolbar') and hasattr(self.fig.canvas.toolbar, 'edit_parameters'):
                self.fig.canvas.toolbar.edit_parameters()
                return
            from matplotlib.backends.qt_compat import QtWidgets
            from matplotlib.backends.qt_editor import _formlayout
            if hasattr(_formlayout, 'FormDialog'):
                options = [('Title', self.fig.suptitle('').get_text())]
                if hasattr(self, 'axes'):
                    options.extend([('X Label', self.axes.get_xlabel()), ('Y Label', self.axes.get_ylabel()), ('X Min', self.axes.get_xlim()[0]), ('X Max', self.axes.get_xlim()[1]), ('Y Min', self.axes.get_ylim()[0]), ('Y Max', self.axes.get_ylim()[1])])
                dialog = _formlayout.FormDialog(options, parent=self, title='Figure Options')
                if dialog.exec_():
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
        timing_enabled = state == Qt.Checked
        self.timing_box.content_area.setEnabled(timing_enabled)
        self.autoscale_check.setEnabled(not timing_enabled)
        self.refresh_plot()

    def refresh_plot(self) -> None:
        self.fig.clear()
        self.active_traces.clear()
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
            if self.legend_check.isChecked():
                plt.subplots_adjust(top=0.85, bottom=0.1)
                self.position_legend()
            else:
                plt.subplots_adjust(top=0.95, bottom=0.1)
        self.canvas.draw()

    def position_legend(self) -> None:
        if hasattr(self, 'axes') and self.legend_check.isChecked():
            handles, labels = [], []
            for idx in sorted(self.trace_visibility.keys()):
                if self.trace_visibility.get(idx) and idx in self.active_traces and self.active_traces[idx]:
                    handles.append(self.active_traces[idx])
                    labels.append(self.trace_names.get(idx, self.obj_dataext.NBList[idx]))
            if handles:
                ncol = min(6, len(handles)) if len(handles) > 6 else min(4, len(handles))
                legend = self.axes.legend(handles, labels, bbox_to_anchor=(0.5, 1.02), loc='lower center', ncol=ncol, frameon=True, fancybox=False, shadow=False, fontsize=LEGEND_FONT_SIZE, borderaxespad=0, columnspacing=1.5)
                frame = legend.get_frame()
                frame.set_facecolor('white')
                frame.set_edgecolor('#E0E0E0')
                frame.set_linewidth(1)
                frame.set_alpha(0.95)

    def plot_timing_diagram(self) -> None:
        """
        Plot digital timing diagram with proper time offset handling.
        
        This method now correctly handles transient analysis with non-zero start times
        by detecting and applying the appropriate time offset.
        """
        # Clear any existing timing annotations
        self.timing_annotations.clear()

        visible_indices = [i for i, v in self.trace_visibility.items() if v]
        if not visible_indices:
            self.axes.text(0.5, 0.5, 'Select a waveform to display', 
                           ha='center', va='center', transform=self.axes.transAxes)
            self.axes.set_yticks([])
            self.axes.set_yticklabels([])
            return

        # Collect all voltage data for threshold calculation
        all_voltage_data = []
        for idx in visible_indices:
            if idx < self.obj_dataext.volts_length:
                all_voltage_data.extend(self.obj_dataext.y[idx])
        
        # If no voltage data, use current data
        if not all_voltage_data:
            for idx in visible_indices:
                all_voltage_data.extend(self.obj_dataext.y[idx])
        
        if not all_voltage_data:
            return

        all_voltage_data = np.array(all_voltage_data, dtype=float)
        vmin = np.min(all_voltage_data)
        vmax = np.max(all_voltage_data)

        # Handle threshold setting
        if self.threshold_spinbox.value() == self.threshold_spinbox.minimum():
            self.logic_threshold = vmin + 0.7 * (vmax - vmin)
            self.threshold_spinbox.setSpecialValueText(f"Auto ({self.logic_threshold:.3f} V)")
        else:
            self.logic_threshold = self.threshold_spinbox.value()

        # Get time data
        time_data = np.asarray(self.obj_dataext.x, dtype=float)
        
        # CRITICAL FIX: Detect and handle transient analysis time offset
        # For transient analysis with .tran step stop start, we need to find
        # where the actual analysis begins
        
        # Check if this is a transient analysis
        if self.plot_type[0] == DataExtraction.TRANSIENT_ANALYSIS:
            # Read the analysis file to get the actual start time
            try:
                with open(os.path.join(self.file_path, "analysis"), 'r') as f:
                    analysis_content = f.read().strip()
                    
                # Parse .tran command: .tran step stop start
                if analysis_content.startswith('.tran'):
                    parts = analysis_content.split()
                    if len(parts) >= 4:
                        try:
                            # Convert scientific notation to float
                            start_time = float(parts[3])
                            
                            # If start_time is not 0, we need to offset our data
                            if start_time > 0:
                                # Find the index where time >= start_time
                                start_idx = np.searchsorted(time_data, start_time)
                                
                                # Adjust time_data to start from the correct point
                                if start_idx > 0 and start_idx < len(time_data):
                                    time_data = time_data[start_idx:]
                                    
                                    # Also adjust all data arrays
                                    for idx in list(self.obj_dataext.y.keys()):
                                        if idx < len(self.obj_dataext.y):
                                            self.obj_dataext.y[idx] = self.obj_dataext.y[idx][start_idx:]
                        except (ValueError, IndexError):
                            pass  # If parsing fails, use full data
            except Exception as e:
                logger.debug(f"Could not parse analysis file for time offset: {e}")
        
        # Prepare spacing for multiple traces
        spacing_ref = max(1.0, vmax)
        spacing = self.vertical_spacing * spacing_ref
        yticks, ylabels = [], []
        
        # Calculate annotation offset based on time range
        annotation_offset_base = 0.01 * (time_data[-1] - time_data[0]) if len(time_data) > 1 else 0.01

        # Plot each visible trace as a digital signal
        for rank, idx in enumerate(visible_indices[::-1]):
            # Get the raw data for this trace
            raw_data = np.asarray(self.obj_dataext.y[idx], dtype=float)
            
            # Make sure raw_data matches time_data length after offset adjustment
            if len(raw_data) > len(time_data):
                raw_data = raw_data[:len(time_data)]
            elif len(raw_data) < len(time_data):
                # This shouldn't happen, but handle it gracefully
                time_data = time_data[:len(raw_data)]
            
            trace_vmin, trace_vmax = np.min(raw_data), np.max(raw_data)
            
            # Convert to digital logic levels
            logic_data = np.where(raw_data > self.logic_threshold, trace_vmax, trace_vmin)
            
            # Apply vertical offset for stacking
            logic_offset = logic_data + rank * spacing
            
            # Get trace properties
            color = self.trace_colors.get(idx, 'blue')
            thickness = self.trace_thickness.get(idx, DEFAULT_LINE_THICKNESS)
            label = self.trace_names.get(idx, self.obj_dataext.NBList[idx])
            
            # Plot the digital waveform
            line, = self.axes.step(time_data, logic_offset, where="post", 
                                   linewidth=thickness, color=color, label=label)
            self.active_traces[idx] = line
            
            # Add y-axis tick for this trace
            y_center = rank * spacing + (trace_vmax + trace_vmin) / 2.0
            yticks.append(y_center)
            ylabels.append(label)
            
            # Add voltage annotation at the end
            # Add voltage annotation at the right edge of the graph
            # Add voltage annotation at the right edge of the graph
            if len(raw_data) > 0:
                final_voltage = f"{float(raw_data[-1]):.3f} V"
                # Position the text at the right edge of the plot area
                # Using transform coordinates: 1.01 means just outside the right edge
                text_obj = self.axes.text(1.01, y_center, final_voltage, 
                                          transform=self.axes.get_yaxis_transform(),
                                          va='center', ha='left',
                                          fontsize=8, color=color,
                                          clip_on=False)  # This allows text to appear outside axes
                self.timing_annotations[idx] = text_obj

        # Set y-axis limits and labels
        total_height = (len(visible_indices) - 1) * spacing + vmax
        self.axes.set_ylim(vmin - 0.1 * spacing_ref, total_height + 0.1 * spacing_ref)
        self.axes.set_yticks(yticks)
        self.axes.set_yticklabels(ylabels, fontsize=8)
        
        # Update tick colors to match trace colors
        self.update_timing_tick_colors()
        
        # Set time axis with proper units
        self.set_time_axis_label()
        
        # Add threshold line
        self.axes.axhline(y=self.logic_threshold, color='red', linestyle=':', 
                          alpha=THRESHOLD_ALPHA, linewidth=1)
        
        # Add title if legend is not shown
        if not self.legend_check.isChecked():
            self.axes.set_title(f'Digital Timing Diagram (Threshold: {self.logic_threshold:.3f} V)', 
                                fontsize=10, pad=10)
    def set_time_axis_label(self) -> None:
        if not hasattr(self, 'axes') or not hasattr(self.obj_dataext, 'x'):
            return
        time_data = np.array(self.obj_dataext.x, dtype=float)
        if len(time_data) < 2:
            self.axes.set_xlabel('Time (s)', fontsize=10)
            return
        time_span = abs(time_data[-1] - time_data[0])
        if time_span == 0:
            scale, unit = 1, 's'
        elif time_span < TIME_UNIT_THRESHOLD_PS:
            scale, unit = 1e12, 'ps'
        elif time_span < TIME_UNIT_THRESHOLD_NS:
            scale, unit = 1e9, 'ns'
        elif time_span < TIME_UNIT_THRESHOLD_US:
            scale, unit = 1e6, 'µs'
        elif time_span < TIME_UNIT_THRESHOLD_MS:
            scale, unit = 1e3, 'ms'
        else:
            scale, unit = 1, 's'
        scaled_time = time_data * scale
        for line in self.active_traces.values():
            if line:
                y_data = line.get_ydata()
                # Step plots have one more y-value than x-value
                if len(y_data) == len(scaled_time) + 1:
                     x_step_data = np.append(scaled_time, scaled_time[-1])
                     line.set_data(x_step_data, y_data)
                elif len(y_data) == len(scaled_time):
                    line.set_xdata(scaled_time)

        self.axes.set_xlim(scaled_time[0], scaled_time[-1])
        if hasattr(self, 'cursor_lines'):
            for i, line in enumerate(self.cursor_lines):
                if line and i < len(self.cursor_positions) and self.cursor_positions[i] is not None:
                    line.set_xdata([self.cursor_positions[i] * scale, self.cursor_positions[i] * scale])
        self.axes.set_xlabel(f'Time ({unit})', fontsize=10)

    def on_threshold_changed(self, value: float) -> None:
        if self.timing_check.isChecked():
            self.refresh_plot()

    def on_spacing_changed(self, value: int) -> None:
        self.vertical_spacing = value / 100.0
        self.spacing_label.setText(f"{self.vertical_spacing:.1f}x")
        if self.timing_check.isChecked():
            self.refresh_plot()

    def on_canvas_click(self, event) -> None:
        if hasattr(self, 'axes') and event.inaxes == self.axes:
            if event.button == 1:
                self.set_cursor(0, event.xdata)
            elif event.button == 3:
                self.set_cursor(1, event.xdata)

    def set_cursor(self, cursor_num: int, x_pos_scaled: float) -> None:
        time_data = np.array(self.obj_dataext.x, dtype=float)
        time_span = abs(time_data[-1] - time_data[0]) if len(time_data) > 1 else 0
        if time_span < TIME_UNIT_THRESHOLD_PS: scale = 1e12
        elif time_span < TIME_UNIT_THRESHOLD_NS: scale = 1e9
        elif time_span < TIME_UNIT_THRESHOLD_US: scale = 1e6
        elif time_span < TIME_UNIT_THRESHOLD_MS: scale = 1e3
        else: scale = 1
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
                line.remove()
        self.cursor_lines.clear()
        self.cursor_positions.clear()
        self.cursor1_label.setText("Cursor 1: Not set")
        self.cursor2_label.setText("Cursor 2: Not set")
        self.delta_label.setText("Delta: --")
        self.measure_label.setText("")
        self.canvas.draw()

    def on_mouse_move(self, event) -> None:
        if event.inaxes:
            self.coord_label.setText(f"X: {event.xdata:.6g}, Y: {event.ydata:.6g}")
        else:
            self.coord_label.setText("X: --, Y: --")

    def on_key_press(self, event) -> None:
        if event.key == 'g': self.grid_check.toggle()
        elif event.key == 'l': self.legend_check.toggle()
        elif event.key == 'p': self.open_figure_options()
        elif event.key == 'escape': self.clear_cursors()

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
                format = 'svg' if "svg" in file_filter else 'png'
                if '.' not in os.path.basename(file_name): file_name += f'.{format}'
                self.fig.savefig(file_name, format=format, dpi=DEFAULT_EXPORT_DPI, bbox_inches='tight')
                self.status_bar.showMessage(f"Image exported to {file_name}", 3000)
            except Exception as e:
                logger.error(f"Error exporting image: {e}")
                QMessageBox.warning(self, "Export Error", f"Failed to export image: {str(e)}")

    def clear_plot(self) -> None:
        self.timing_annotations.clear()
        self.deselect_all_waveforms()

    def zoom_in(self) -> None:
        if hasattr(self, 'axes'): self.nav_toolbar.zoom()

    def zoom_out(self) -> None:
        if hasattr(self, 'axes'): self.nav_toolbar.back()

    def reset_view(self) -> None:
        if hasattr(self, 'axes'): self.nav_toolbar.home()

    def toggle_grid(self) -> None:
        if hasattr(self, 'axes'):
            self.axes.grid(self.grid_check.isChecked())
            self.canvas.draw()

    def toggle_legend(self) -> None:
        self.refresh_plot()

    def plot_function(self) -> None:
        # This function remains complex, will copy simplified logic if possible
        # For now, keeping the original logic
        function_text = self.func_input.text()
        if not function_text:
            QMessageBox.warning(self, "Input Error", "Function input cannot be empty.")
            return

        # Basic parsing (this is a simplified example, not a full math parser)
        # It expects "trace1 vs trace2" or a simple expression with +, -, *, /
        # For security, avoid using eval() directly on user input in production.
        # This implementation is for a controlled environment.

        if 'vs' in function_text:
            parts = [p.strip() for p in function_text.split('vs')]
            if len(parts) != 2:
                QMessageBox.warning(self, "Syntax Error", "Use format 'trace1 vs trace2'.")
                return
            y_name, x_name = parts[0], parts[1]
            try:
                x_idx = self.obj_dataext.NBList.index(x_name)
                y_idx = self.obj_dataext.NBList.index(y_name)
                x_data = np.array(self.obj_dataext.y[x_idx], dtype=float)
                y_data = np.array(self.obj_dataext.y[y_idx], dtype=float)

                is_voltage_x = x_idx < self.volts_length
                is_voltage_y = y_idx < self.volts_length

                self.axes.plot(x_data, y_data, label=function_text)
                self.axes.set_xlabel(f"{x_name} ({'V' if is_voltage_x else 'A'})")
                self.axes.set_ylabel(f"{y_name} ({'V' if is_voltage_y else 'A'})")

            except ValueError:
                QMessageBox.warning(self, "Trace Not Found", f"Could not find one of the traces: {x_name}, {y_name}")
                return
        else:
            # Simple expression evaluation (use with caution)
            try:
                # Replace trace names with data arrays
                result_expr = function_text
                for i, name in enumerate(self.obj_dataext.NBList):
                    if name in result_expr:
                        result_expr = result_expr.replace(name, f"np.array(self.obj_dataext.y[{i}], dtype=float)")

                # Evaluate the expression
                y_data = eval(result_expr, {"np": np, "self": self})
                x_data = np.array(self.obj_dataext.x, dtype=float)
                self.axes.plot(x_data, y_data, label=function_text)

            except Exception as e:
                QMessageBox.warning(self, "Evaluation Error", f"Could not plot function: {e}")
                return

        if self.legend_check.isChecked():
            self.position_legend()
        self.canvas.draw()


    def multi_meter(self) -> None:
        visible_indices = [i for i, v in self.trace_visibility.items() if v]
        if not visible_indices:
            QMessageBox.warning(self, "Warning", "Please select at least one waveform")
            return
        location_x, location_y = 300, 300
        for idx in visible_indices:
            is_voltage = idx < self.obj_dataext.volts_length
            rms_value = self.get_rms_value(self.obj_dataext.y[idx])
            meter = MultimeterWidgetClass(self.trace_names.get(idx, self.obj_dataext.NBList[idx]), rms_value, location_x, location_y, is_voltage)
            if hasattr(self.obj_appconfig, 'dock_dict') and self.obj_appconfig.current_project['ProjectName'] in self.obj_appconfig.dock_dict:
                self.obj_appconfig.dock_dict[self.obj_appconfig.current_project['ProjectName']].append(meter)
            location_x += 50
            location_y += 50

    def get_rms_value(self, data_points: List) -> Decimal:
        getcontext().prec = 5
        return Decimal(str(np.sqrt(np.mean(np.square([float(x) for x in data_points])))))

    def redraw_cursors(self) -> None:
        # This function might be redundant if set_time_axis_label handles cursor redraws
        pass

    def _plot_analysis_data(self, analysis_type: str) -> None:
        self.axes = self.fig.add_subplot(111)
        traces_plotted = 0
        for trace_index, is_visible in self.trace_visibility.items():
            if not is_visible:
                continue
            traces_plotted += 1
            color = self.trace_colors.get(trace_index, '#000000')
            label = self.trace_names.get(trace_index, self.obj_dataext.NBList[trace_index])
            thickness = self.trace_thickness.get(trace_index, DEFAULT_LINE_THICKNESS)
            style = self.trace_style.get(trace_index, '-')
            x_data = np.asarray(self.obj_dataext.x, dtype=float)
            y_data = np.asarray(self.obj_dataext.y[trace_index], dtype=float)
            
            plot_style = '-' if style == 'steps-post' else style
            plot_func = self.axes.plot
            if style == 'steps-post' and analysis_type in ['transient', 'dc']:
                plot_func = self.axes.step
            elif analysis_type == 'ac_log':
                plot_func = self.axes.semilogx

            line, = plot_func(x_data, y_data, c=color, label=label, linewidth=thickness, linestyle=plot_style)
            self.active_traces[trace_index] = line

        if analysis_type in ['ac_linear', 'ac_log']:
            self.axes.set_xlabel('Frequency (Hz)')
        elif analysis_type == 'transient':
            # set_time_axis_label is now called from refresh_plot
            pass
        elif analysis_type == 'dc':
            self.axes.set_xlabel('Voltage Sweep (V)')
        
        # Set Y label based on the first plotted trace
        first_visible = next((i for i, v in self.trace_visibility.items() if v), None)
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
