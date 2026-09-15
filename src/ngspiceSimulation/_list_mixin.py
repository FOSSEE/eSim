# ngspiceSimulation/_list_mixin.py
import logging
from typing import List

from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QLabel, QListWidgetItem,
                              QMenu, QColorDialog, QInputDialog, QMessageBox,
                              QWidgetAction, QGridLayout, QPushButton)
from PyQt6.QtGui import QColor, QBrush, QPainter, QPixmap, QPen
from PyQt6.QtCore import Qt

from .constants import (DEFAULT_LINE_THICKNESS, THICKNESS_OPTIONS, LINE_STYLES,
                        LEGEND_FONT_SIZE)
from .trace import Trace

logger = logging.getLogger(__name__)


class _ListMixin:

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
        needle = text.lower()
        for i in range(self.waveform_list.count()):
            item = self.waveform_list.item(i)
            if item:
                item.setHidden(needle not in item.text().lower())

    def on_waveform_toggle(self, item: QListWidgetItem) -> None:
        index = item.data(Qt.ItemDataRole.UserRole)
        # Negative UserRole = function trace item; positive = simulation trace.
        if isinstance(index, int) and index < 0:
            f_idx = -index - 1
            if f_idx < len(self._func_visible):
                self._func_visible[f_idx] = not self._func_visible[f_idx]
                label, _fx, _fy, color, *_ = self._func_traces[f_idx]
                self._update_func_item_appearance(
                    item, label, color, self._func_visible[f_idx])
            self._schedule_refresh()
            return
        # item.isSelected() is unreliable when setItemWidget is used — clicks land
        # on the child widget and never update Qt's selection model. Toggle instead.
        self.traces[index].visible = not self.traces[index].visible
        self.update_list_item_appearance(item, index)
        self._schedule_refresh()

    def update_list_item_appearance(self, item: QListWidgetItem, index: int) -> None:
        t = self.traces[index]
        widget = QWidget()
        # CRITICAL: the row's custom QWidget AND its children must NOT eat
        # mouse events. WA_TransparentForMouseEvents on the parent only
        # affects that exact widget — Qt does NOT auto-propagate to
        # children. Set it on every interactive child so the QListWidget
        # gets press/move events and can initiate drags.
        transparent = Qt.WidgetAttribute.WA_TransparentForMouseEvents
        widget.setAttribute(transparent, True)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(10)
        icon_label = QLabel()
        icon_label.setAttribute(transparent, True)
        color = QColor(t.color) if t.visible else QColor("#9E9E9E")
        icon = self.create_colored_icon(color, t.visible)
        icon_label.setPixmap(icon.pixmap(18, 18))
        text_label = QLabel(t.name)
        text_label.setAttribute(transparent, True)
        text_label.setStyleSheet("color: #212121; font-weight: 500;" if t.visible else "color: #757575; font-weight: normal;")
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()
        self.waveform_list.setItemWidget(item, widget)
        item.setText(t.name)

    def _update_func_item_appearance(self, item: QListWidgetItem,
                                      label: str, color: str,
                                      visible: bool) -> None:
        """Set visual appearance of a function-trace waveform list item.

        Mirrors update_list_item_appearance but for func traces.  The 'ƒ'
        prefix and italic style distinguish them from simulation signals.
        """
        transparent = Qt.WidgetAttribute.WA_TransparentForMouseEvents
        widget = QWidget()
        widget.setAttribute(transparent, True)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(10)
        icon_label = QLabel()
        icon_label.setAttribute(transparent, True)
        icon_color = QColor(color) if visible else QColor("#9E9E9E")
        icon = self.create_colored_icon(icon_color, visible)
        icon_label.setPixmap(icon.pixmap(18, 18))
        display = f"ƒ  {label}"
        text_label = QLabel(display)
        text_label.setAttribute(transparent, True)
        text_label.setStyleSheet(
            f"color: {color}; font-weight: 500; font-style: italic;" if visible
            else "color: #757575; font-weight: normal; font-style: italic;")
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()
        self.waveform_list.setItemWidget(item, widget)
        item.setText(display)

    def _sync_func_trace_list(self) -> None:
        """Remove all func-trace list items and re-add from current _func_traces.

        Called after any mutation of _func_traces so the waveform list stays
        in sync (correct count, correct negative UserRole indices, correct
        labels/colours after a middle-of-list removal re-numbers everything).
        """
        for i in range(self.waveform_list.count() - 1, -1, -1):
            it = self.waveform_list.item(i)
            if it is not None:
                val = it.data(Qt.ItemDataRole.UserRole)
                if isinstance(val, int) and val < 0:
                    self.waveform_list.takeItem(i)
        for f_idx, (label, _fx, _fy, color, *_) in enumerate(self._func_traces):
            visible = (self._func_visible[f_idx]
                       if f_idx < len(self._func_visible) else True)
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, -(f_idx + 1))
            item.setToolTip(f"Function trace: {label}")
            self.waveform_list.addItem(item)
            self._update_func_item_appearance(item, label, color, visible)

    def select_all_waveforms(self) -> None:
        self.waveform_list.setUpdatesEnabled(False)
        try:
            for i in range(self.waveform_list.count()):
                item = self.waveform_list.item(i)
                if item and not item.isHidden():
                    index = item.data(Qt.ItemDataRole.UserRole)
                    if isinstance(index, int) and index < 0:
                        f_idx = -index - 1
                        if f_idx < len(self._func_visible):
                            self._func_visible[f_idx] = True
                            label, _fx, _fy, color, *_ = self._func_traces[f_idx]
                            self._update_func_item_appearance(item, label, color, True)
                    else:
                        self.traces[index].visible = True
                        self.update_list_item_appearance(item, index)
        finally:
            self.waveform_list.setUpdatesEnabled(True)
        self._schedule_refresh()

    def deselect_all_waveforms(self) -> None:
        for t in self.traces.values():
            t.visible = False
        for f_idx in range(len(self._func_visible)):
            self._func_visible[f_idx] = False
        self.waveform_list.setUpdatesEnabled(False)
        try:
            for i in range(self.waveform_list.count()):
                item = self.waveform_list.item(i)
                if item:
                    index = item.data(Qt.ItemDataRole.UserRole)
                    if isinstance(index, int) and index < 0:
                        f_idx = -index - 1
                        if f_idx < len(self._func_traces):
                            label, _fx, _fy, color, *_ = self._func_traces[f_idx]
                            self._update_func_item_appearance(item, label, color, False)
                    else:
                        self.update_list_item_appearance(item, index)
        finally:
            self.waveform_list.setUpdatesEnabled(True)
        self._schedule_refresh()

    def show_list_context_menu(self, position: QtCore.QPoint) -> None:
        item = self.waveform_list.itemAt(position)
        menu = QMenu()

        select_all_action = menu.addAction("Select All")
        select_all_action.setShortcut(QtGui.QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.select_all_waveforms)
        deselect_action = menu.addAction("Deselect All")
        deselect_action.triggered.connect(self.deselect_all_waveforms)

        if item:
            index = item.data(Qt.ItemDataRole.UserRole)
            menu.addSeparator()

            if isinstance(index, int) and index < 0:
                f_idx = -index - 1
                color_menu = menu.addMenu("Change colour ▶")
                self._populate_func_color_menu(color_menu, f_idx)
                thickness_menu = menu.addMenu("Thickness ▶")
                for _thickness, _tlabel in THICKNESS_OPTIONS:
                    _act = thickness_menu.addAction(_tlabel)
                    _act.triggered.connect(
                        lambda checked=False, t=_thickness, fi=f_idx: self._change_func_thickness(fi, t))
                style_menu = menu.addMenu("Style ▶")
                for _style, _slabel in LINE_STYLES:
                    _act = style_menu.addAction(_slabel)
                    _act.triggered.connect(
                        lambda checked=False, s=_style, fi=f_idx: self._change_func_style(fi, s))
                menu.addSeparator()
                is_vis = (f_idx < len(self._func_visible) and self._func_visible[f_idx])
                hide_show_action = menu.addAction("Hide" if is_vis else "Show")
                hide_show_action.triggered.connect(
                    lambda checked=False, fi=f_idx: self._toggle_func_trace_visibility(fi))
                remove_action = menu.addAction("Remove")
                remove_action.triggered.connect(
                    lambda checked=False, fi=f_idx: self._remove_function_pane(fi))
            else:
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
            if self._current_view_mode == 'timing' and self.panes:
                self.update_timing_tick_colors()
                for ann_text in self.timing_annotations.get(index, []):
                    ann_text.set_color(color)
            elif self._current_view_mode == 'stacked' and self.panes:
                for pane_idx, group in enumerate(self._pane_groups):
                    if group and group[0] == index and pane_idx < len(self.panes):
                        self.panes[pane_idx].set_title(
                            self.traces[index].name, loc='left', color=color,
                            fontsize=LEGEND_FONT_SIZE, fontweight='bold', pad=3)
                        break
        self.save_config()
        self.canvas.draw()

    def update_timing_tick_colors(self) -> None:
        # No-op outside timing view: ytick labels in normal/stacked views are
        # numeric voltage/current ticks, not trace names, so colouring them
        # by trace would corrupt the axis legend.
        if self._current_view_mode != 'timing' or not self.panes:
            return
        visible = list(reversed(self.visible_traces))
        ytick_labels = self.axes.get_yticklabels()
        for i, label in enumerate(ytick_labels):
            if i < len(visible):
                label.set_color(visible[i].color)

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
            self._rebuild_nb_sorted()
            self.update_list_item_appearance(item, index)
            if self.legend_check.isChecked():
                # Name change must re-label the legend; signature can't see it.
                self._force_full_refresh = True
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
        self._schedule_refresh()
