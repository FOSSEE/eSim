# ngspiceSimulation/plot_window.py
"""
Plot Window Module

This module provides the main plotting window for NGSpice simulation results
with support for AC, DC, and Transient analysis visualization.
"""

from __future__ import division
import os
import re
import sys
import json
import traceback
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtCore import Qt, QSettings, pyqtSignal
from PyQt6.QtWidgets import (QWidget, QVBoxLayout,
                             QHBoxLayout, QListWidget, QListWidgetItem, QPushButton,
                             QCheckBox, QGroupBox, QRadioButton, QButtonGroup,
                             QLabel, QLineEdit, QSlider, QDoubleSpinBox, QMenu,
                             QFileDialog, QColorDialog, QInputDialog,
                             QMessageBox, QStatusBar,
                             QSplitter, QToolButton, QWidgetAction, QGridLayout,
                             QSizePolicy, QScrollArea)
from PyQt6.QtGui import (QColor, QBrush, QPalette, QKeySequence, QShortcut,
                         QPainter, QPixmap, QFont, QAction, QIcon, QPen)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.text import Text
from matplotlib.ticker import FuncFormatter, ScalarFormatter

from configuration.Appconfig import Appconfig
from .plotting_widgets import CollapsibleBox
from .data_extraction import DataExtraction

logger = logging.getLogger(__name__)

from .constants import *
from .trace import Trace, CustomListWidget
from ._pane_mixin import _PaneMixin
from ._cursor_mixin import _CursorMixin
from ._func_trace_mixin import _FuncTraceMixin
from ._render_mixin import _RenderMixin
from ._list_mixin import _ListMixin

class plotWindow(QWidget, _PaneMixin, _CursorMixin, _FuncTraceMixin, _RenderMixin, _ListMixin):
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
        self._setup_matplotlib_style()

    def _initialize_data_structures(self) -> None:
        self._em_cache: Optional[int] = None  # invalidated by changeEvent on FontChange
        self._resize_timer: QtCore.QTimer = QtCore.QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.setInterval(120)
        self._resize_timer.timeout.connect(self._do_deferred_resize)
        self._controls_timer: QtCore.QTimer = QtCore.QTimer(self)
        self._controls_timer.setSingleShot(True)
        self._controls_timer.setInterval(150)
        self._controls_timer.timeout.connect(self.refresh_plot)
        # debounce: coalesces rapid toggles so stacked rebuild runs once after burst settles
        self._refresh_timer: QtCore.QTimer = QtCore.QTimer(self)
        self._refresh_timer.setSingleShot(True)
        self._refresh_timer.setInterval(REFRESH_DEBOUNCE_MS)
        self._refresh_timer.timeout.connect(self.refresh_plot)
        self.traces: Dict[int, Trace] = {}
        # cursor_lines[i]: axvlines per pane; empty inner list = cursor not yet rendered
        self.cursor_lines: List[List[Optional[Line2D]]] = []
        self.cursor_positions: List[Optional[float]] = []
        self._current_analysis_type: str = ''
        self.timing_annotations: Dict[int, Any] = {}
        self.color_palette = VIBRANT_COLOR_PALETTE.copy()
        self.logic_thresholds: Dict[int, float] = {}
        self.vertical_spacing = DEFAULT_VERTICAL_SPACING
        self._func_line: Optional[Line2D] = None
        self._drag_cursor_idx: Optional[int] = None
        self._current_view_mode: str = 'normal'  # 'normal' | 'timing' | 'stacked'
        self.panes: List[Any] = []
        # incremental-refresh: skip full rebuild when composition unchanged; _force_full_refresh overrides
        self._drawn_signature: Optional[tuple] = None
        self._force_full_refresh: bool = False
        # layout freeze: stacked rebuild sets _pending_freeze; draw callback snapshots geometry and drops solver
        self._pending_freeze: bool = False
        # display-only scale: line data stays in raw SI; ticks formatted as raw * _x_scale
        self._x_scale: float = 1.0
        self._x_unit: str = 's'
        # view state: one-shot ylim snapshots + persistent locks, both keyed by anchor trace name
        self._saved_xlim: Optional[Tuple[float, float]] = None
        self._saved_pane_ylims: Dict[str, Tuple[float, float]] = {}   # one-shot
        self._locked_ylims: Dict[str, Tuple[float, float]] = {}        # persistent
        # pane groups: outer = pane order, inner = trace indices; empty = one trace per pane
        self._pane_groups: List[List[int]] = []
        # pane_lock_y keyed by anchor trace name; actual ylim in _locked_ylims
        self._pane_lock_y: Dict[str, bool] = {}
        self._global_stats_visible: bool = True
        # func traces: (label, x, y, color, thickness, style)
        self._func_traces: List[Tuple[str, "np.ndarray", "np.ndarray", str, float, str]] = []
        # canonical expr per func trace for O(1) dup-check
        self._func_canonical: List[str] = []
        # visibility parallel to _func_traces
        self._func_visible: List[bool] = []
        # sorted longest-first so longer names match before their substrings
        self._nb_sorted: List[Tuple[int, str]] = []
        # pending layout from config, resolved after populate_waveform_list sets up NBList
        self._pending_layout: Optional[Dict[str, Any]] = None
        # pane height ratios; empty = equal heights
        self._pane_heights: List[float] = []
        # transient drag state for divider resize and pane reorder
        self._divider_drag: Optional[Dict[str, Any]] = None
        self._pane_drag: Optional[Dict[str, Any]] = None
        # Mouse-move dedup: skip setText/anchor lookup when state unchanged.
        self._last_hover_axes: Any = None
        self._last_hover_anchor: Optional[str] = None
        self._last_coord_text: str = ''
        self._last_cursor_shape_was_resize: bool = False
        self._blit_background: Optional[Any] = None
        # interp cache per cursor; invalidated by new data or x_pos/visible change
        self._cursor_interp_cache: List[Optional[Dict]] = []
        # .tran start offset parsed once; 0.0 if not a tran sim
        self._tran_start_time: float = 0.0

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
            # Stacked-view layout, keyed by trace NAME so it survives schematic
            # changes that renumber NBList. Lists of names per pane preserve
            # both pane order and intra-pane signal order.
            self.config['stacked_pane_groups'] = [
                [self.traces[i].name for i in g
                 if i in self.traces]
                for g in self._pane_groups
            ]
            self.config['stacked_lock_y'] = dict(self._pane_lock_y)
            self.config['stacked_locked_ylims'] = {
                name: list(lims) for name, lims in self._locked_ylims.items()
            }
            self.config['stacked_stats_visible'] = self.stats_check.isChecked()
            # Persist per-pane height ratios alongside their anchor name so a
            # schematic edit that drops a signal also drops its custom height.
            self.config['stacked_pane_heights'] = {
                self.traces[g[0]].name: float(self._pane_heights[i])
                for i, g in enumerate(self._pane_groups)
                if g and g[0] in self.traces and i < len(self._pane_heights)
            }
            temp_file = self.config_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as config_file:
                json.dump(self.config, config_file, indent=2)
            temp_file.replace(self.config_file)
        except Exception as e:
            logger.error(f"Error saving config: {e}")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.save_config()
        # Cancel deferred timers so no queued tick fires refresh_plot after the
        # figure/canvas below are torn down (would touch a closed figure).
        self._refresh_timer.stop()
        self._controls_timer.stop()
        self._resize_timer.stop()
        if hasattr(self, 'canvas'):
            self.canvas.close()
        if hasattr(self, 'fig'):
            plt.close(self.fig)
        super().closeEvent(event)

    def apply_theme(self) -> None:
        em      = self._em
        sb_w    = max(6,  em // 2)
        ind     = max(12, em - 2)
        sldr    = max(10, em - 4)
        sldr_m  = -(sldr // 2)
        item_h  = max(28, em + 12)
        item_pv = max(4,  em // 4)
        item_ph = max(6,  em // 2)
        btn_pv  = max(3,  em // 4)
        btn_ph  = max(6,  em // 2)
        btn_h   = max(24, em + 8)
        le_p    = max(4,  em // 3)

        theme_stylesheet = f"""
        QMenuBar {{ border-radius: 8px; background-color: #FFFFFF; border: 1px solid #E0E0E0; padding: 2px; }}
        QStatusBar {{ border-radius: 8px; background-color: #FFFFFF; border: 1px solid #E0E0E0; padding: 2px; }}
        QWidget {{ background-color: #FFFFFF; color: #212121; }}
        QListWidget {{ background-color: #FFFFFF; border: 1px solid #E0E0E0; padding: 2px; outline: none; selection-background-color: transparent; selection-color: inherit; }}
        QListWidget::item {{ min-height: {item_h}px; padding: {item_pv}px {item_ph}px; margin: 1px 2px; background-color: transparent; border: none; }}
        QListWidget::item:selected {{ background-color: transparent; border: none; }}
        QListWidget::item:hover {{ background-color: rgba(0, 0, 0, 0.04); }}
        QListWidget::item:focus {{ outline: none; }}
        QGroupBox {{ border: 1px solid #E0E0E0; margin-top: 0.5em; padding-top: 0.5em; }}
        QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px; }}
        QPushButton {{ background-color: #FFFFFF; border: 1px solid #E0E0E0; padding: {btn_pv}px {btn_ph}px; min-height: {btn_h}px; font-weight: 500; }}
        QPushButton:hover {{ background-color: #F2F2F2; border-color: #1976D2; }}
        QPushButton:pressed {{ background-color: #E0E0E0; }}
        QCheckBox::indicator {{ width: {ind}px; height: {ind}px; }}
        QMenu {{ background-color: #FFFFFF; border: 1px solid #E0E0E0; }}
        QMenu::item:selected {{ background-color: #E3F2FD; }}
        QLineEdit {{ border: 1px solid #E0E0E0; padding: {le_p}px {btn_ph}px; background-color: #FAFAFA; }}
        QLineEdit:focus {{ border-color: #1976D2; background-color: #FFFFFF; }}
        QSlider::groove:horizontal {{ border: 1px solid #E0E0E0; height: 4px; background: #E0E0E0; }}
        QSlider::handle:horizontal {{ background: #1976D2; border: 1px solid #1976D2; width: {sldr}px; height: {sldr}px; margin: {sldr_m}px 0; }}
        QScrollBar:vertical {{ background-color: #F5F5F5; width: {sb_w}px; border: none; border-radius: {sb_w // 2}px; }}
        QScrollBar::handle:vertical {{ background-color: #BDBDBD; border-radius: {sb_w // 2}px; min-height: 20px; margin: 2px; }}
        QScrollBar::handle:vertical:hover {{ background-color: #9E9E9E; }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: transparent; }}
        QSplitter::handle:horizontal {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0.49 transparent, stop:0.5 #D0D0D0, stop:0.51 transparent); }}
        QSplitter::handle:horizontal:hover {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0.45 transparent, stop:0.5 #1976D2, stop:0.55 transparent); }}
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
        self.splitter.setHandleWidth(5)
        em = self._em
        self.left_panel = self.create_waveform_list()
        self.left_panel.setMinimumWidth(em * 10)
        self.splitter.addWidget(self.left_panel)
        self.center_widget = self.create_plot_area()
        self.center_widget.setMinimumWidth(em * 18)
        self.splitter.addWidget(self.center_widget)
        right_widget = self.create_control_panel()
        self.right_panel = QScrollArea()
        self.right_panel.setWidget(right_widget)
        self.right_panel.setWidgetResizable(True)
        self.right_panel.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.right_panel.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.right_panel.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.right_panel.setMinimumWidth(em * 9)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setStretchFactor(0, 20)
        self.splitter.setStretchFactor(1, 63)
        self.splitter.setStretchFactor(2, 17)
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
        em = self._em
        self.analysis_label = QLabel()
        self.analysis_label.setStyleSheet(
            f"font-weight: bold; font-size: {max(11, em - 4)}px; padding: {max(3, em // 5)}px;"
        )
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
        self.waveform_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        left_layout.addWidget(self.waveform_list)
        QShortcut(QKeySequence.StandardKey.SelectAll, self.waveform_list,
                  activated=self.select_all_waveforms)
        return left_widget

    def create_plot_area(self) -> QWidget:
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        # constrained_layout handles multi-pane spacing automatically (no manual
        # tight_layout calls needed). Required for the stacked-view feature
        # where N subplots share an X axis and hspace must stay consistent.
        self.fig = Figure(figsize=DEFAULT_FIGURE_SIZE, dpi=DEFAULT_DPI,
                          constrained_layout=True)
        self.canvas = FigureCanvas(self.fig)
        self.nav_toolbar = NavigationToolbar(self.canvas, self)
        for _a in self.nav_toolbar.actions():
            if _a.text() in ('Subplots', 'Customize'):
                self.nav_toolbar.removeAction(_a)
        _icon_sz = self.nav_toolbar.iconSize()
        _tb_h    = self.nav_toolbar.sizeHint().height()
        _btn_style = (
            "QToolButton { border: none; background: transparent; border-radius: 3px; }"
            "QToolButton:hover { background: rgba(0,0,0,0.06); }"
            "QToolButton:checked { background: rgba(25,118,210,0.12); }"
        )
        _fig_btn = QToolButton()
        _fig_btn.setIcon(self.nav_toolbar._icon('qt4_editor_options'))
        _fig_btn.setIconSize(_icon_sz)
        _fig_btn.setFixedSize(_tb_h, _tb_h)
        _fig_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        _fig_btn.setToolTip('Figure Options (P)')
        _fig_btn.setStyleSheet(_btn_style)
        _fig_btn.clicked.connect(self.open_figure_options)
        self._focus_btn = QToolButton()
        self._focus_btn.setIcon(self._make_focus_icon(_icon_sz.width()))
        self._focus_btn.setIconSize(_icon_sz)
        self._focus_btn.setFixedSize(_tb_h, _tb_h)
        self._focus_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self._focus_btn.setCheckable(True)
        self._focus_btn.setToolTip('Focus plot — hide panels (F)')
        self._focus_btn.setStyleSheet(_btn_style)
        self._focus_btn.toggled.connect(self._toggle_focus_mode)
        QShortcut(QKeySequence('F'), self, activated=self._focus_btn.toggle)
        toolbar_row = QHBoxLayout()
        toolbar_row.setContentsMargins(0, 0, 0, 0)
        toolbar_row.setSpacing(0)
        toolbar_row.addWidget(self.nav_toolbar)
        toolbar_row.addWidget(_fig_btn)
        toolbar_row.addWidget(self._focus_btn)
        center_layout.addLayout(toolbar_row)
        # Wrap canvas in QScrollArea so stacked-view with many panes scrolls
        # vertically instead of squashing every signal to ~30 pixels. Canvas
        # min-height is bumped per refresh from _set_canvas_height_for_panes.
        self.canvas_scroll = QScrollArea()
        self.canvas_scroll.setWidget(self.canvas)
        self.canvas_scroll.setWidgetResizable(True)
        self.canvas_scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.canvas_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.canvas_scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        center_layout.addWidget(self.canvas_scroll)
        self.canvas.mpl_connect('resize_event', self._on_canvas_resize)
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)
        self.canvas.mpl_connect('button_release_event', self.on_canvas_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        # Freeze the constrained_layout solver right after a stacked rebuild's
        # draw has solved it — see _pending_freeze / _on_draw_event.
        self.canvas.mpl_connect('draw_event', self._on_draw_event)
        self.canvas.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.canvas.installEventFilter(self)
        return center_widget

    def create_control_panel(self) -> QWidget:
        em = self._em
        iv = max(2, em // 6)
        ih = max(4, em // 4)
        sp = max(1, em // 8)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(4, 4, 4, 4)
        right_layout.setSpacing(0)

        # View Mode
        mode_box = CollapsibleBox("View Mode")
        mode_group = QWidget()
        mode_layout = QVBoxLayout(mode_group)
        mode_layout.setContentsMargins(ih, iv, ih, iv)
        mode_layout.setSpacing(sp)
        self._view_mode_group = QButtonGroup(self)
        self.radio_standard = QRadioButton("Standard")
        self.radio_standard.setChecked(True)
        self.radio_stacked = QRadioButton("Stacked")
        self.radio_stacked.setToolTip(
            "Each signal in its own pane with shared X axis. "
            "Preserves real amplitude and per-signal Y autoscale.")
        self.radio_timing = QRadioButton("Digital Timing (Simplified)")
        self.radio_timing.setToolTip(
            "Square-wave view for digital/logic signals. "
            "Only available for transient analysis.")
        for btn in (self.radio_standard, self.radio_stacked, self.radio_timing):
            self._view_mode_group.addButton(btn)
            mode_layout.addWidget(btn)
        self._view_mode_group.buttonToggled.connect(self.on_view_mode_changed)
        mode_box.addWidget(mode_group)
        right_layout.addWidget(mode_box)

        # Display Options
        display_box = CollapsibleBox("Display Options")
        display_group = QWidget()
        display_layout = QVBoxLayout(display_group)
        display_layout.setContentsMargins(ih, iv, ih, iv)
        display_layout.setSpacing(sp)
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
        self.stats_check = QCheckBox("Show Stats")
        self.stats_check.setToolTip("Show min/max/RMS/frequency stats on each stacked pane")
        self.stats_check.setChecked(True)
        self.stats_check.setVisible(False)
        self.stats_check.stateChanged.connect(self.refresh_plot)
        display_layout.addWidget(self.stats_check)
        display_box.addWidget(display_group)
        right_layout.addWidget(display_box)

        # Digital Timing Controls
        self.timing_box = CollapsibleBox("Digital Timing Controls")
        timing_group = QWidget()
        timing_layout = QVBoxLayout(timing_group)
        timing_layout.setContentsMargins(ih, iv, ih, iv)
        timing_layout.setSpacing(sp)
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(QLabel("Threshold:"))
        self.threshold_spinbox = QDoubleSpinBox()
        self.threshold_spinbox.setRange(-100, 100)
        self.threshold_spinbox.setDecimals(3)
        self.threshold_spinbox.setSingleStep(0.1)
        self.threshold_spinbox.setSuffix("")
        self.threshold_spinbox.setSpecialValueText("Auto")
        self.threshold_spinbox.setValue(self.threshold_spinbox.minimum())
        self.threshold_spinbox.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
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
        self.timing_box.setVisible(False)
        right_layout.addWidget(self.timing_box)

        # Cursor Measurements
        cursor_box = CollapsibleBox("Cursor Measurements")
        cursor_group = QWidget()
        cursor_layout = QVBoxLayout(cursor_group)
        cursor_layout.setContentsMargins(ih, iv, ih, iv)
        cursor_layout.setSpacing(sp)

        self.cursor1_label = QLabel('<b style="color:#e53935">C1</b>  <span style="color:#aaa">not set</span>')
        self.cursor1_label.setWordWrap(True)
        self.cursor1_label.setStyleSheet("font-size: 13px; padding: 3px 0;")
        self.cursor2_label = QLabel('<b style="color:#1976d2">C2</b>  <span style="color:#aaa">not set</span>')
        self.cursor2_label.setWordWrap(True)
        self.cursor2_label.setStyleSheet("font-size: 13px; padding: 3px 0;")
        self.delta_label = QLabel('<b style="color:#e65100">ΔX</b>  <span style="color:#aaa">—</span>')
        self.delta_label.setStyleSheet("font-size: 13px; padding: 3px 0;")

        def _cursor_sep() -> QLabel:
            s = QLabel()
            s.setFixedHeight(1)
            s.setStyleSheet("background-color: #d0d0d0; margin: 2px 0;")
            return s

        cursor_layout.setSpacing(8)
        cursor_layout.addWidget(self.cursor1_label)
        cursor_layout.addWidget(_cursor_sep())
        cursor_layout.addWidget(self.cursor2_label)
        cursor_layout.addWidget(_cursor_sep())
        cursor_layout.addWidget(self.delta_label)
        cursor_help = QLabel(
            "L-click = Cursor 1   ·   Middle / R-click = Cursor 2\n"
            "R-click in stacked view = pane menu")
        cursor_help.setStyleSheet("color: #757575; font-size: 11px;")
        cursor_help.setWordWrap(True)
        cursor_layout.addWidget(cursor_help)
        self.clear_cursors_btn = QPushButton("Clear Cursors")
        self.clear_cursors_btn.clicked.connect(self.clear_cursors)
        cursor_layout.addWidget(self.clear_cursors_btn)
        cursor_box.addWidget(cursor_group)
        right_layout.addWidget(cursor_box)

        # Export Tools
        export_box = CollapsibleBox("Export Tools")
        export_group = QWidget()
        export_layout = QVBoxLayout(export_group)
        export_layout.setContentsMargins(ih, iv, ih, iv)
        export_layout.setSpacing(sp)
        self.export_btn = QPushButton("Export Image")
        self.export_btn.clicked.connect(self.export_image)
        export_layout.addWidget(self.export_btn)
        self.func_input = QLineEdit()
        self.func_input.setPlaceholderText("e.g., v(net1) + v(net2)  or  abs(v(net1))")
        self.func_input.returnPressed.connect(self.plot_function)
        export_layout.addWidget(self.func_input)
        self.plot_func_btn = QPushButton("Plot Function")
        self.plot_func_btn.clicked.connect(self.plot_function)
        export_layout.addWidget(self.plot_func_btn)
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

    def _rebuild_nb_sorted(self) -> None:
        """Cache NBList sorted longest-first for use in _resolve_expr."""
        self._nb_sorted = sorted(
            enumerate(self.obj_dataext.NBList),
            key=lambda t: len(t[1]), reverse=True
        )

    def _parse_tran_start_time(self) -> float:
        try:
            with open(os.path.join(self.file_path, "analysis"), 'r') as f:
                parts = f.read().strip().split()
            if len(parts) >= 4 and parts[0] == '.tran':
                return float(parts[3])
        except Exception:
            pass
        return 0.0

    def load_simulation_data(self) -> None:
        self._cursor_interp_cache.clear()
        # new data → force full rebuild on next refresh
        self._drawn_signature = None
        self._tran_start_time = self._parse_tran_start_time()
        self.obj_dataext = DataExtraction()
        self.plot_type = self.obj_dataext.openFile(self.file_path)
        self.obj_dataext.computeAxes()
        self._rebuild_nb_sorted()
        self.data_info = self.obj_dataext.numVals()
        self.volts_length = self.data_info[1]
        if self.plot_type[0] == DataExtraction.AC_ANALYSIS:
            self.analysis_label.setText("AC Analysis")
        elif self.plot_type[0] == DataExtraction.TRANSIENT_ANALYSIS:
            self.analysis_label.setText("Transient Analysis")
        else:
            self.analysis_label.setText("DC Analysis")
        self.populate_waveform_list()
        # NBList ready; resolve persisted stacked-view layout
        self._apply_persisted_layout()
        is_transient = self.plot_type[0] == DataExtraction.TRANSIENT_ANALYSIS
        self.radio_timing.setEnabled(is_transient)
        if not is_transient:
            if self.radio_timing.isChecked():
                self.radio_standard.setChecked(True)
            self.radio_timing.setToolTip("Only available for transient analysis")
        else:
            self.radio_timing.setToolTip(
                "Square-wave view for digital/logic signals. "
                "Only available for transient analysis.")

    def open_figure_options(self) -> None:
        try:
            if hasattr(self.fig.canvas, 'toolbar') and hasattr(self.fig.canvas.toolbar, 'edit_parameters'):
                # matplotlib's built-in editor already handles multi-axes —
                # it shows a per-axes selector so each pane can be edited.
                self.fig.canvas.toolbar.edit_parameters()
                return
            from matplotlib.backends.qt_compat import QtWidgets
            from matplotlib.backends.qt_editor import _formlayout
            if hasattr(_formlayout, 'FormDialog'):
                current_title = self.fig._suptitle.get_text() if self.fig._suptitle is not None else ''
                options: List[Tuple[str, Any]] = [('Title', current_title)]
                # Multi-pane: only X (shared via sharex) + suptitle are global.
                # Per-pane Y limits and labels are skipped to avoid a 7-field
                # dialog that can only touch one pane meaningfully.
                multi = len(self.panes) > 1
                if self.panes:
                    options.append(('X Label', self.panes[-1].get_xlabel()))
                    options.append(('X Min', self.axes.get_xlim()[0]))
                    options.append(('X Max', self.axes.get_xlim()[1]))
                    if not multi:
                        options.append(('Y Label', self.axes.get_ylabel()))
                        options.append(('Y Min', self.axes.get_ylim()[0]))
                        options.append(('Y Max', self.axes.get_ylim()[1]))
                dialog = _formlayout.FormDialog(options, parent=self, title='Figure Options')
                if dialog.exec():
                    results = dialog.get_results()
                    if not results:
                        return
                    self.fig.suptitle(results[0])
                    if self.panes and len(results) > 1:
                        self.panes[-1].set_xlabel(results[1])
                        self.axes.set_xlim(results[2], results[3])
                        if not multi and len(results) > 4:
                            self.axes.set_ylabel(results[4])
                            self.axes.set_ylim(results[5], results[6])
                    self.canvas.draw()
            else:
                QMessageBox.information(self, "Figure Options", "Figure options are limited in this environment.\nYou can use the zoom and pan tools in the toolbar.")
        except Exception as e:
            logger.error(f"Error opening figure options: {e}")
            QMessageBox.information(self, "Figure Options", "Basic figure editing is available through the toolbar.")

    def _update_mode_controls(self) -> None:
        stacked = self.radio_stacked.isChecked()
        normal  = self.radio_standard.isChecked()
        self.autoscale_check.setVisible(normal)
        self.stats_check.setVisible(stacked)
        self.legend_check.setVisible(not stacked)

    def on_view_mode_changed(self, button, checked: bool) -> None:
        if not checked:
            return
        timing = self.radio_timing.isChecked()
        self.timing_box.setVisible(timing)
        self.timing_box.content_area.setEnabled(timing)
        self._update_mode_controls()
        self.refresh_plot()

    @staticmethod
    def _make_focus_icon(size: int) -> QIcon:
        px = QPixmap(size, size)
        px.fill(Qt.GlobalColor.transparent)
        p = QPainter(px)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(QColor('#444444'), max(1, size // 12), Qt.PenStyle.SolidLine,
                      Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        m = max(2, size // 6)
        a = max(3, size // 4)
        for cx, cy in ((m, m), (size-m, m), (m, size-m), (size-m, size-m)):
            dx = a if cx == m else -a
            dy = a if cy == m else -a
            p.drawLine(cx, cy + dy, cx, cy)
            p.drawLine(cx, cy, cx + dx, cy)
        p.end()
        return QIcon(px)

    def _toggle_focus_mode(self, focused: bool) -> None:
        self.left_panel.setVisible(not focused)
        self.right_panel.setVisible(not focused)
        self._focus_btn.setToolTip('Restore panels (F)' if focused else 'Focus plot — hide panels (F)')

    def on_canvas_click(self, event) -> None:
        if not self.panes:
            return
        if self.nav_toolbar.mode:
            return

        # Divider drag — pressed in the gap between two panes (event.inaxes
        # is None there, so handle it before the inaxes guard below).
        if (self._current_view_mode == 'stacked'
                and event.button == 1
                and event.inaxes is None):
            div = self._divider_under_mouse(event)
            if div is not None:
                self._start_divider_drag(div, event)
                return

        if event.inaxes not in self.panes:
            return

        modifier = (event.key or '').lower()

        # Alt + left-click in stacked: start a pane reorder drag. Finish on
        # release over the destination pane.
        if (self._current_view_mode == 'stacked'
                and event.button == 1
                and 'alt' in modifier):
            idx = self._pane_index_of(event.inaxes)
            if idx is not None:
                self._start_pane_drag(idx)
                return

        # Right-click in stacked mode opens the per-pane context menu. The
        # menu's "Set Cursor N here" items keep cursor placement available
        # to laptop users who don't have a middle mouse button.
        if event.button == 3 and self._current_view_mode == 'stacked':
            self._show_pane_context_menu(event)
            return

        x_target = event.xdata

        near = self._find_nearest_cursor(event)
        if event.button == 1:
            if near is not None:
                self._drag_cursor_idx = near
                self._begin_cursor_blit()
            else:
                self._drag_cursor_idx = None
                self.set_cursor(0, x_target)
        elif event.button == 2:  # middle-click: cursor 2
            self._drag_cursor_idx = None
            self.set_cursor(1, x_target)
        elif event.button == 3:  # right-click (non-stacked): cursor 2
            self._drag_cursor_idx = None
            self.set_cursor(1, x_target)

    def on_canvas_release(self, event) -> None:
        # If a cursor was being dragged, recompute the full per-signal
        # readout now (skipped during motion for performance).
        had_cursor_drag = self._drag_cursor_idx is not None
        last_cursor_idx = self._drag_cursor_idx
        self._drag_cursor_idx = None
        if had_cursor_drag:
            self._end_cursor_blit()
        if had_cursor_drag and last_cursor_idx is not None:
            if last_cursor_idx < len(self.cursor_positions):
                x_pos = self.cursor_positions[last_cursor_idx]
                if x_pos is not None:
                    # Full per-signal Y readout now that drag is done.
                    self._update_cursor_panel(last_cursor_idx, x_pos)
                    two = (len(self.cursor_positions) >= 2
                           and all(p is not None for p in self.cursor_positions[:2]))
                    if not two:
                        self.measure_label.setText(
                            self._format_cursor_readout(x_pos))
        if self._divider_drag is not None:
            self._finish_divider_drag()
        if self._pane_drag is not None:
            self._finish_pane_drag(event)

    def on_mouse_move(self, event) -> None:
        # Active drags get priority — fast path, no allocations.
        if self._divider_drag is not None:
            self._update_divider_drag(event)
            return
        if self._drag_cursor_idx is not None and event.xdata is not None:
            # Cursor drag — only needs the X update; skip coord-label work.
            self._update_cursor_position(self._drag_cursor_idx, event.xdata)
            return

        if event.inaxes:
            base = f"X: {event.xdata:.6g}, Y: {event.ydata:.6g}"
            if self._current_view_mode == 'stacked':
                # Anchor lookup is O(N traces); only walk when the hovered
                # pane actually changes between move events.
                if event.inaxes is not self._last_hover_axes:
                    self._last_hover_axes = event.inaxes
                    self._last_hover_anchor = self._pane_anchor_name(event.inaxes)
                if self._last_hover_anchor:
                    base = f"{base}  |  Pane: {self._last_hover_anchor}"
            if base != self._last_coord_text:
                self.coord_label.setText(base)
                self._last_coord_text = base
            # Reset resize-cursor state when we re-enter an axes
            if self._last_cursor_shape_was_resize:
                self.canvas.unsetCursor()
                self._last_cursor_shape_was_resize = False
        else:
            # Show resize cursor when hovering a divider gap in stacked mode
            want_resize = (self._current_view_mode == 'stacked'
                           and self._divider_under_mouse(event) is not None)
            if want_resize and not self._last_cursor_shape_was_resize:
                self.canvas.setCursor(Qt.CursorShape.SizeVerCursor)
                self._last_cursor_shape_was_resize = True
            elif not want_resize and self._last_cursor_shape_was_resize:
                self.canvas.unsetCursor()
                self._last_cursor_shape_was_resize = False
            if self._last_coord_text != "X: --, Y: --":
                self.coord_label.setText("X: --, Y: --")
                self._last_coord_text = "X: --, Y: --"
            self._last_hover_axes = None
            self._last_hover_anchor = None

    def on_key_press(self, event) -> None:
        if event.key == 'g': self.grid_check.toggle()
        elif event.key == 'l': self.legend_check.toggle()
        elif event.key == 'f': self._focus_btn.toggle()
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

    def eventFilter(self, obj, event) -> bool:
        if (obj is self.canvas and
                event.type() == QtCore.QEvent.Type.Wheel and
                self._current_view_mode == 'stacked'):
            mods = event.modifiers()
            ctrl = Qt.KeyboardModifier.ControlModifier
            shift = Qt.KeyboardModifier.ShiftModifier
            if not (mods & ctrl) and not (mods & shift):
                QtWidgets.QApplication.sendEvent(
                    self.canvas_scroll.verticalScrollBar(), event)
                return True
        return super().eventFilter(obj, event)

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

    def _zoom_panes(self, factor: float) -> None:
        """Apply a symmetric zoom around the centre of each pane.

        factor < 1 zooms in (narrower range); factor > 1 zooms out.
        X is set on self.axes only — sharex propagates to all panes when
        stacked. Y is set per-pane so each retains its own scale.
        """
        if not self.panes:
            return
        xlim = self.axes.get_xlim()
        x_center = (xlim[0] + xlim[1]) / 2
        x_half = (xlim[1] - xlim[0]) * factor / 2
        self.axes.set_xlim(x_center - x_half, x_center + x_half)
        for ax in self.panes:
            ylim = ax.get_ylim()
            y_center = (ylim[0] + ylim[1]) / 2
            y_half = (ylim[1] - ylim[0]) * factor / 2
            ax.set_ylim(y_center - y_half, y_center + y_half)
        self.canvas.draw()

    def zoom_in(self) -> None:
        self._zoom_panes(DEFAULT_ZOOM_FACTOR)

    def zoom_out(self) -> None:
        self._zoom_panes(1 / DEFAULT_ZOOM_FACTOR)

    def reset_view(self) -> None:
        if self.panes:
            self.nav_toolbar.home()

    def toggle_grid(self) -> None:
        if self.panes:
            for ax in self.panes:
                ax.grid(self.grid_check.isChecked())
            self.canvas.draw()

    def toggle_legend(self) -> None:
        self.refresh_plot()

    def _setup_matplotlib_style(self) -> None:
        dpi = max(72, self.logicalDpiY())
        base_pt = max(6.5, round(8.0 * 96.0 / dpi, 1))
        plt.rcParams.update({
            'font.size':         base_pt,
            'axes.labelsize':    base_pt + 1,
            'axes.titlesize':    base_pt + 1,
            'xtick.labelsize':   base_pt,
            'ytick.labelsize':   base_pt,
            'legend.fontsize':   base_pt,
            'keymap.fullscreen': [],
        })

    def _on_canvas_resize(self, event) -> None:
        self._resize_timer.start()  # restart on every event; fires 120ms after last one

    def _do_deferred_resize(self) -> None:
        if hasattr(self, 'canvas'):
            self.canvas.draw_idle()

    @property
    def _em(self) -> int:
        """Font height in pixels — base unit for all adaptive sizing."""
        if self._em_cache is None:
            self._em_cache = max(12, QtGui.QFontMetrics(self.font()).height())
        return self._em_cache

    @property
    def visible_traces(self) -> List[Trace]:
        """Ordered list of visible traces (waveform-list insertion order).

        Single source of truth for "what gets plotted". All plot paths
        (normal/timing/stacked) and multi-pane logic key off this ordering
        so panes, legend, cursor readouts, and exports stay consistent.
        """
        return [self.traces[i] for i in sorted(self.traces.keys())
                if self.traces[i].visible]

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        super().showEvent(event)
        if not getattr(self, '_splitter_initialized', False):
            QtCore.QTimer.singleShot(0, self._init_splitter_sizes)

    def _init_splitter_sizes(self) -> None:
        if getattr(self, '_splitter_initialized', False):
            return
        total = self.splitter.width()
        if total > 100:
            left_w  = int(total * 0.20)
            right_w = max(
                self.right_panel.minimumWidth(),
                self.right_panel.widget().sizeHint().width() + 8,
            )
            center_w = max(self.center_widget.minimumWidth(), total - left_w - right_w)
            self.splitter.setSizes([left_w, center_w, right_w])
            self._splitter_initialized = True
        else:
            QtCore.QTimer.singleShot(50, self._init_splitter_sizes)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        if self.parent():
            self.parent().updateGeometry()

    def changeEvent(self, event: QtCore.QEvent) -> None:
        super().changeEvent(event)
        if event.type() == QtCore.QEvent.Type.FontChange:
            self._em_cache = None

    def sizeHint(self) -> QtCore.QSize:
        em = self._em
        return QtCore.QSize(em * 80, em * 50)

    def minimumSizeHint(self) -> QtCore.QSize:
        em = self._em
        return QtCore.QSize(em * 25, em * 20)
