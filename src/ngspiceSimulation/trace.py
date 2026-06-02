from typing import Optional
from PyQt6.QtWidgets import QListWidget, QWidget
from PyQt6 import QtGui
from matplotlib.lines import Line2D
from .constants import DEFAULT_LINE_THICKNESS, VIBRANT_COLOR_PALETTE


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
    """Plain multi-select list. Drag-source removed in v3.1 along with the
    multi-signal-pane model — stacked view now keeps one trace per pane,
    so there's nothing to drag onto. Pane reorder is done via Move Up/Down
    in the right-click menu or by Alt-dragging a pane vertically.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        super().paintEvent(event)

