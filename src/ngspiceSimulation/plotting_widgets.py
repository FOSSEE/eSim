"""
Plotting Widgets Module

This module provides custom widgets for the plotting interface including
collapsible boxes and multimeter widgets.
"""

import logging
from typing import Optional
from decimal import Decimal
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolButton,
                             QGridLayout, QLabel)

# Set up logging
logger = logging.getLogger(__name__)

# Default widget dimensions
DEFAULT_WIDGET_WIDTH = 300
DEFAULT_WIDGET_HEIGHT = 100


class CollapsibleBox(QWidget):
    """
    A collapsible widget container with a toggle button.
    
    This widget provides a collapsible container with a title button that
    can be clicked to show/hide the content area.
    """
    
    def __init__(self, title: str = "", parent: Optional[QWidget] = None) -> None:
        """
        Initialize the CollapsibleBox widget.
        
        Args:
            title: Title text to display on the toggle button
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.title = title
        # **FIX**: Set proper size policy
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                          QtWidgets.QSizePolicy.Maximum)
        
        self._setup_toggle_button()
        self._setup_content_area()
        self._setup_layout()
        self._connect_signals()

    def _setup_toggle_button(self) -> None:
        """Set up the toggle button with styling and properties."""
        self.toggle_button = QToolButton()
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.DownArrow)
        self.toggle_button.setText(self.title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)

    def _setup_content_area(self) -> None:
        """Set up the content area and its layout."""
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)

    def _setup_layout(self) -> None:
        """Set up the main layout for the widget."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.toggle_button)
        main_layout.addWidget(self.content_area)

    def _connect_signals(self) -> None:
        """Connect widget signals to their handlers."""
        self.toggle_button.toggled.connect(self.on_toggle)

    def on_toggle(self, is_checked: bool) -> None:
        """
        Handle toggle button state changes.
        
        Args:
            is_checked: Whether the toggle button is checked
        """
        arrow_type = Qt.DownArrow if is_checked else Qt.RightArrow
        self.toggle_button.setArrowType(arrow_type)
        self.content_area.setVisible(is_checked)
        
        logger.debug(f"CollapsibleBox '{self.title}' {'expanded' if is_checked else 'collapsed'}")

    def addWidget(self, widget: QWidget) -> None:
        """
        Add a widget to the content area.
        
        Args:
            widget: Widget to add to the content layout
        """
        if widget is not None:
            self.content_layout.addWidget(widget)
        else:
            logger.warning("Attempted to add None widget to CollapsibleBox")

    def addLayout(self, layout) -> None:
        """
        Add a layout to the content area.
        
        Args:
            layout: Layout to add to the content layout
        """
        if layout is not None:
            self.content_layout.addLayout(layout)
        else:
            logger.warning("Attempted to add None layout to CollapsibleBox")


class MultimeterWidgetClass(QWidget):
    """
    A multimeter widget for displaying RMS values of voltage or current signals.
    
    This widget provides a digital multimeter-like interface showing the RMS
    value of a selected node or branch along with its label.
    """
    
    # Unit labels
    VOLTAGE_UNIT = "Volts"
    CURRENT_UNIT = "Amp"
    
    # Labels
    NODE_LABEL = "Node"
    BRANCH_LABEL = "Branch"
    RMS_LABEL = "RMS Value"
    WINDOW_TITLE = "MultiMeter"

    def __init__(self, node_branch: str, rms_value: Decimal, 
                 location_x: int, location_y: int, is_voltage: bool) -> None:
        """
        Initialize the MultimeterWidget.
        
        Args:
            node_branch: Name of the node or branch being measured
            rms_value: RMS value to display
            location_x: X coordinate for widget positioning
            location_y: Y coordinate for widget positioning
            is_voltage: True if measuring voltage, False for current
        """
        super().__init__()
        
        # **FIX**: Don't force window size, let it be managed by parent
        self.node_branch = node_branch
        self.rms_value = rms_value
        self.location_x = location_x
        self.location_y = location_y
        self.is_voltage = is_voltage
        
        # Set proper size policy instead of fixed geometry
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                          QtWidgets.QSizePolicy.Fixed)
        
        self._setup_ui()
        self._configure_window()
        
        logger.info(f"Created multimeter widget for {'voltage' if is_voltage else 'current'}: "
                   f"{node_branch} = {rms_value}")

    def _setup_ui(self) -> None:
        """Set up the user interface elements."""
        # Create main container widget
        self.multimeter_container = QWidget(self)
        
        # Create labels based on measurement type
        self._create_labels()
        
        # Set up layout
        self._setup_layout()

    def _create_labels(self) -> None:
        """Create and configure the display labels."""
        # Create type label (Node or Branch)
        if self.is_voltage:
            self.type_label = QLabel(self.NODE_LABEL)
            unit_text = self.VOLTAGE_UNIT
        else:
            self.type_label = QLabel(self.BRANCH_LABEL)
            unit_text = self.CURRENT_UNIT

        # Create value labels
        self.rms_title_label = QLabel(self.RMS_LABEL)
        self.node_branch_value_label = QLabel(str(self.node_branch))
        self.rms_value_label = QLabel(f"{self.rms_value} {unit_text}")

    def _setup_layout(self) -> None:
        """Set up the grid layout for the widget."""
        layout = QGridLayout(self)
        layout.addWidget(self.type_label, 0, 0)
        layout.addWidget(self.rms_title_label, 0, 1)
        layout.addWidget(self.node_branch_value_label, 1, 0)
        layout.addWidget(self.rms_value_label, 1, 1)
        
        self.multimeter_container.setLayout(layout)

    def _configure_window(self) -> None:
        """Configure window properties and display the widget."""
        self.setGeometry(
            self.location_x, 
            self.location_y, 
            DEFAULT_WIDGET_WIDTH, 
            DEFAULT_WIDGET_HEIGHT
        )
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.show()

    def update_value(self, new_rms_value: Decimal) -> None:
        """
        Update the displayed RMS value.
        
        Args:
            new_rms_value: New RMS value to display
        """
        self.rms_value = new_rms_value
        unit_text = self.VOLTAGE_UNIT if self.is_voltage else self.CURRENT_UNIT
        self.rms_value_label.setText(f"{new_rms_value} {unit_text}")
        
        logger.debug(f"Updated multimeter value: {self.node_branch} = {new_rms_value}")

    def get_measurement_info(self) -> dict:
        """
        Get measurement information as a dictionary.
        
        Returns:
            Dictionary containing measurement details
        """
        return {
            'node_branch': self.node_branch,
            'rms_value': self.rms_value,
            'is_voltage': self.is_voltage,
            'unit': self.VOLTAGE_UNIT if self.is_voltage else self.CURRENT_UNIT
        }
