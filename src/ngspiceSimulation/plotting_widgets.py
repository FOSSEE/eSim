import logging
from typing import Optional
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QToolButton)

logger = logging.getLogger(__name__)


class CollapsibleBox(QWidget):
    """A collapsible widget container with a toggle button."""

    def __init__(self, title: str = "", parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.title = title
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                          QtWidgets.QSizePolicy.Policy.Preferred)

        self._setup_toggle_button()
        self._setup_content_area()
        self._setup_layout()
        self._connect_signals()

    def _setup_toggle_button(self) -> None:
        self.toggle_button = QToolButton()
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.ArrowType.DownArrow)
        self.toggle_button.setText(self.title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )

    def _setup_content_area(self) -> None:
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(4, 2, 4, 4)
        self.content_layout.setSpacing(3)
        self.content_area.setLayout(self.content_layout)

    def _setup_layout(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 2, 0, 6)
        main_layout.addWidget(self.toggle_button)
        main_layout.addWidget(self.content_area)

    def _connect_signals(self) -> None:
        self.toggle_button.toggled.connect(self.on_toggle)

    def on_toggle(self, is_checked: bool) -> None:
        arrow_type = Qt.ArrowType.DownArrow if is_checked else Qt.ArrowType.RightArrow
        self.toggle_button.setArrowType(arrow_type)
        self.content_area.setVisible(is_checked)

    def addWidget(self, widget: QWidget) -> None:
        if widget is not None:
            self.content_layout.addWidget(widget)

    def addLayout(self, layout) -> None:
        if layout is not None:
            self.content_layout.addLayout(layout)
