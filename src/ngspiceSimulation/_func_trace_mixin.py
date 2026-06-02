from typing import Dict, List, Optional, Tuple
import re
import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QMenu, QMessageBox, QColorDialog, QInputDialog,
                             QListWidgetItem, QWidget, QPushButton,
                             QGridLayout, QWidgetAction)
from PyQt6.QtGui import QColor
from .constants import DEFAULT_LINE_THICKNESS
from .math_utils import _safe_eval, _canonical_expr


class _FuncTraceMixin:
    def _dialog_plot_function(self) -> None:
        text, ok = QInputDialog.getText(
            self, "Plot function in new pane",
            "Expression (e.g. v(in) - v(out)):")
        if ok and text:
            prev = self.func_input.text()
            try:
                self.func_input.setText(text)
                self.plot_function()
            finally:
                # Restore the right-panel input so the user's persistent
                # expression isn't clobbered by the menu-driven dialog.
                self.func_input.setText(prev)

    def _toggle_func_trace_visibility(self, f_idx: int) -> None:
        if not (0 <= f_idx < len(self._func_visible)):
            return
        self._func_visible[f_idx] = not self._func_visible[f_idx]
        label, _fx, _fy, color, *_ = self._func_traces[f_idx]
        for i in range(self.waveform_list.count()):
            it = self.waveform_list.item(i)
            if it and it.data(Qt.ItemDataRole.UserRole) == -(f_idx + 1):
                self._update_func_item_appearance(it, label, color, self._func_visible[f_idx])
                break
        self._schedule_refresh()

    def _populate_func_color_menu(self, menu: QMenu, f_idx: int) -> None:
        color_widget = QWidget()
        color_widget.setStyleSheet("background-color: #FFFFFF;")
        grid_layout = QGridLayout(color_widget)
        grid_layout.setSpacing(2)
        for i, c in enumerate(self.color_palette):
            btn = QPushButton()
            btn.setFixedSize(24, 24)
            btn.setStyleSheet(
                f"QPushButton{{background-color:{c};border:1px solid #E0E0E0;border-radius:2px;}}"
                f"QPushButton:hover{{border:2px solid #212121;}}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(
                lambda checked=False, col=c, fi=f_idx, m=menu: (
                    self._change_func_color(fi, col), m.close()))
            grid_layout.addWidget(btn, i // 4, i % 4)
        wa = QWidgetAction(menu)
        wa.setDefaultWidget(color_widget)
        menu.addAction(wa)
        menu.addSeparator()
        more = menu.addAction("More...")
        more.triggered.connect(lambda: self._change_func_color_dialog(f_idx))

    def _change_func_color(self, f_idx: int, color: str) -> None:
        if not (0 <= f_idx < len(self._func_traces)):
            return
        label, fx, fy, _, thickness, style = self._func_traces[f_idx]
        self._func_traces[f_idx] = (label, fx, fy, color, thickness, style)
        for i in range(self.waveform_list.count()):
            it = self.waveform_list.item(i)
            if it and it.data(Qt.ItemDataRole.UserRole) == -(f_idx + 1):
                vis = f_idx < len(self._func_visible) and self._func_visible[f_idx]
                self._update_func_item_appearance(it, label, color, vis)
                break
        self.refresh_plot()

    def _change_func_color_dialog(self, f_idx: int) -> None:
        color = QColorDialog.getColor()
        if color.isValid():
            self._change_func_color(f_idx, color.name())

    def _change_func_thickness(self, f_idx: int, thickness: float) -> None:
        if not (0 <= f_idx < len(self._func_traces)):
            return
        label, fx, fy, color, _, style = self._func_traces[f_idx]
        self._func_traces[f_idx] = (label, fx, fy, color, thickness, style)
        self.refresh_plot()

    def _change_func_style(self, f_idx: int, style: str) -> None:
        if not (0 <= f_idx < len(self._func_traces)):
            return
        label, fx, fy, color, thickness, _ = self._func_traces[f_idx]
        self._func_traces[f_idx] = (label, fx, fy, color, thickness, style)
        self.refresh_plot()

    def _clear_function_panes(self) -> None:
        if self._func_traces:
            self._func_traces.clear()
            self._func_canonical.clear()
            self._func_visible.clear()
            self._sync_func_trace_list()
            self.refresh_plot()

    def _remove_function_pane(self, f_idx: int) -> None:
        if 0 <= f_idx < len(self._func_traces):
            del self._func_traces[f_idx]
            if f_idx < len(self._func_canonical):
                del self._func_canonical[f_idx]
            if f_idx < len(self._func_visible):
                del self._func_visible[f_idx]
            self._sync_func_trace_list()
            self.refresh_plot()

    def _show_function_pane_menu(self, event, f_idx: int) -> None:
        """Slim context menu for a function pane: cursor placement + remove."""
        menu = QMenu(self)
        click_x = event.xdata
        if click_x is not None:
            c1 = menu.addAction("Set Cursor 1 here")
            c1.triggered.connect(lambda checked=False, x=click_x: self.set_cursor(0, x))
            c2 = menu.addAction("Set Cursor 2 here")
            c2.triggered.connect(lambda checked=False, x=click_x: self.set_cursor(1, x))
            menu.addSeparator()
        label = self._func_traces[f_idx][0] if f_idx < len(self._func_traces) else ''
        rem = menu.addAction(f'Remove "{label}"')
        rem.triggered.connect(lambda i=f_idx: self._remove_function_pane(i))
        clear = menu.addAction("Clear all function panes")
        clear.setEnabled(bool(self._func_traces))
        clear.triggered.connect(self._clear_function_panes)
        if hasattr(event, 'guiEvent') and event.guiEvent is not None:
            menu.exec(event.guiEvent.globalPosition().toPoint())
        else:
            menu.exec(self.canvas.mapToGlobal(QtCore.QPoint(0, 0)))

    def _resolve_expr(self, expr: str) -> "Tuple[str, Dict[str, np.ndarray]]":
        """Substitute NGSpice trace names in expr with safe Python identifiers.

        NGSpice names like v(net1), i(r1), v-minus contain characters that
        are invalid Python identifiers and would cause SyntaxError or wrong
        AST parses.  This method finds every known trace name in `expr`
        (longest first to prevent partial-match corruption, e.g. v(n1) inside
        v(n10)), replaces each with _trace_N_, and builds the corresponding
        data_map for _safe_eval.

        Pure-identifier names (no special characters) use regex word boundaries
        so that trace 'v' does not silently replace 'v' inside 'vout'.

        Returns (sanitized_expr, {identifier: array}).
        """
        indexed = self._nb_sorted
        x_len = len(self.obj_dataext.x)
        data_map: Dict[str, np.ndarray] = {}
        sanitized = expr
        for idx, name in indexed:
            if not name:
                continue
            placeholder = f'_trace_{idx}_'
            escaped = re.escape(name)
            has_special = bool(re.search(r'[^A-Za-z0-9_]', name))
            pattern = escaped if has_special else (
                r'(?<![A-Za-z0-9_])' + escaped + r'(?![A-Za-z0-9_])')
            if not re.search(pattern, sanitized):
                continue
            sanitized = re.sub(pattern, placeholder, sanitized)
            raw = np.asarray(self.obj_dataext.y[idx], dtype=float)
            data_map[placeholder] = raw[:x_len]
        return sanitized, data_map

    def plot_function(self) -> None:
        function_text = self.func_input.text().strip()
        if not function_text:
            QMessageBox.warning(self, "Input Error", "Function expression cannot be empty.")
            return
        if not hasattr(self.obj_dataext, 'NBList') or not self.obj_dataext.NBList:
            QMessageBox.warning(self, "No Data", "No simulation data loaded.")
            return

        if ' vs ' in function_text:
            self._plot_lissajous(function_text)
            return

        # Resolve NGSpice trace names → safe identifiers, then evaluate.
        try:
            sanitized, data_map = self._resolve_expr(function_text)
            canonical = _canonical_expr(sanitized)
            for i, (existing_text, *_) in enumerate(self._func_traces):
                ex_canonical = (self._func_canonical[i]
                                if i < len(self._func_canonical) else None)
                if ex_canonical is None:
                    try:
                        ex_san, _ = self._resolve_expr(existing_text)
                        ex_canonical = _canonical_expr(ex_san)
                    except Exception:
                        ex_canonical = existing_text.replace(' ', '')
                match = ex_canonical == canonical
                if match:
                    QMessageBox.information(
                        self, "Already Plotted",
                        f"'{existing_text}' is already on the plot.\n"
                        "(Note: a+b and b+a are treated as equal.)")
                    return
            y_data = _safe_eval(sanitized, data_map)
            x_data = np.asarray(self.obj_dataext.x, dtype=float)
            n = min(len(x_data), len(y_data))
            x_data, y_data = x_data[:n], y_data[:n]
        except ValueError as exc:
            names = self.obj_dataext.NBList
            preview = ', '.join(names[:8])
            if len(names) > 8:
                preview += f'  … ({len(names)} total)'
            QMessageBox.warning(
                self, "Evaluation Error",
                f"{exc}\n\nAvailable traces:\n{preview}\n\n"
                "Allowed functions: abs sqrt log log10 exp sin cos tan\n"
                "Allowed operators: + - * / **")
            return
        except Exception as exc:
            QMessageBox.warning(self, "Evaluation Error", f"Unexpected error: {exc}")
            return

        func_palette = ['#9C27B0', '#FF6D00', '#00897B', '#5E35B1', '#F4511E']
        color = func_palette[len(self._func_traces) % len(func_palette)]
        self._func_traces.append((function_text, x_data, y_data, color, DEFAULT_LINE_THICKNESS, '-'))
        self._func_canonical.append(canonical)
        self._func_visible.append(True)
        self._sync_func_trace_list()
        self.refresh_plot()
        self.func_input.clear()

    def _plot_lissajous(self, function_text: str) -> None:
        """Plot 'signal_y vs signal_x' as an X-Y (Lissajous) curve.

        Lissajous plots repurpose the X axis to a signal rather than time/freq,
        so they can't coexist with stacked view (shared-X constraint).  The
        result is drawn directly on self.axes and is NOT stored in _func_traces
        — it does not survive refresh_plot.  Users who need persistence should
        disable Stacked View before plotting.
        """
        if self._current_view_mode == 'stacked':
            QMessageBox.information(
                self, "Lissajous Plot",
                "X-Y (Lissajous) plotting requires a single time/frequency axis.\n"
                "Disable Stacked View first.")
            return
        parts = function_text.split(' vs ', 1)
        y_name, x_name = parts[0].strip(), parts[1].strip()
        if not y_name or not x_name:
            QMessageBox.warning(self, "Syntax Error",
                                "Lissajous format: 'signal_y vs signal_x'")
            return
        names = self.obj_dataext.NBList
        missing = [n for n in (y_name, x_name) if n not in names]
        if missing:
            preview = ', '.join(names[:8])
            if len(names) > 8:
                preview += f'  … ({len(names)} total)'
            QMessageBox.warning(
                self, "Trace Not Found",
                f"Not found: {', '.join(missing)}\n\nAvailable traces:\n{preview}")
            return
        x_idx = names.index(x_name)
        y_idx = names.index(y_name)
        x_data = np.asarray(self.obj_dataext.y[x_idx], dtype=float)
        y_data = np.asarray(self.obj_dataext.y[y_idx], dtype=float)
        n = min(len(x_data), len(y_data))
        if n == 0:
            QMessageBox.warning(self, "No Data", "Selected traces contain no data.")
            return
        # Remove any previous lissajous line before drawing the new one.
        if self._func_line is not None:
            try:
                self._func_line.remove()
            except ValueError:
                pass
            self._func_line = None
        self._reset_x_axis_scaling()
        is_voltage_x = x_idx < self.volts_length
        is_voltage_y = y_idx < self.volts_length
        line, = self.axes.plot(x_data[:n], y_data[:n], label=function_text)
        self._func_line = line
        self.axes.set_xlabel(f"{x_name} ({'V' if is_voltage_x else 'A'})")
        self.axes.set_ylabel(f"{y_name} ({'V' if is_voltage_y else 'A'})")
        if self.legend_check.isChecked():
            self.position_legend()
        self.canvas.draw()

