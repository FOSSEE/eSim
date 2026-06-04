import logging
from typing import Dict, List, Optional, Tuple
import numpy as np
from matplotlib.lines import Line2D
from .constants import (CURSOR_ALPHA, FREQ_UNIT_THRESHOLD_KHZ, FREQ_UNIT_THRESHOLD_MHZ,
                        FREQ_UNIT_THRESHOLD_GHZ)
from .math_utils import _format_measurement, _format_frequency
from .trace import Trace

logger = logging.getLogger(__name__)


class _CursorMixin:
    def _find_nearest_cursor(self, event) -> Optional[int]:
        """Return cursor index if the click is within 8px of an existing cursor.

        Reads from cursor_positions (raw units) rather than per-pane line
        xdata — keeps multi-pane hit-testing simple and pane-agnostic, since
        all panes share the same X under sharex.
        """
        if (not self.cursor_positions
                or not self.panes
                or event.xdata is None):
            return None
        xlim = self.axes.get_xlim()
        width_px = self.axes.get_window_extent().width
        if width_px == 0:
            return None
        threshold = 8 * (xlim[1] - xlim[0]) / width_px
        for i, x_pos in enumerate(self.cursor_positions):
            if x_pos is None:
                continue
            if abs(event.xdata - x_pos) < threshold:
                return i
        return None

    def _update_cursor_position(self, cursor_num: int, x_pos: float) -> None:
        """Move an existing cursor line without recreating it (fast drag path).

        Skips the per-trace interpolated readout during active drag — that
        was O(N_traces × log(samples)) per mouse-move event and produced
        visible lag with 5+ traces. The full readout is rebuilt on release
        via on_canvas_release → set_cursor-equivalent retouch.
        """
        if (cursor_num >= len(self.cursor_lines)
                or not self.cursor_lines[cursor_num]):
            self.set_cursor(cursor_num, x_pos)
            return
        for line in self.cursor_lines[cursor_num]:
            if line is not None:
                line.set_xdata([x_pos, x_pos])
        scale = self._current_axis_scale()
        self.cursor_positions[cursor_num] = x_pos
        # Lightweight X-only update during drag — full per-signal Y readout
        # is deferred to on_canvas_release to keep drag smooth.
        unit_str = (self._x_unit or '').strip()
        label = self.cursor1_label if cursor_num == 0 else self.cursor2_label
        _c_color = '#e53935' if cursor_num == 0 else '#1976d2'
        label.setText(
            f'<span style="font-weight:700;color:{_c_color}">C{cursor_num + 1}</span>'
            f'<span style="color:#999"> @ </span>'
            f'<span style="font-weight:600;color:#333">{x_pos * scale:.4g} {unit_str}</span>'
        )
        two_cursors = (len(self.cursor_positions) >= 2
                       and all(p is not None for p in self.cursor_positions[:2]))
        if two_cursors:
            delta_raw = abs(self.cursor_positions[1] - self.cursor_positions[0])
            self.delta_label.setText(
                f'<span style="font-weight:700;color:#e65100">ΔX</span>'
                f' <span style="font-family:monospace;font-weight:600;color:#333">{delta_raw * scale:.4g} {unit_str}</span>'
            )
            self._update_measure_label(delta_raw, scale)
        # Blit path: restore static background, draw only cursor lines, blit.
        # Falls back to draw_idle() if snapshot is stale/missing.
        if self._blit_background is not None:
            self.canvas.restore_region(self._blit_background)
            for pane_lines in self.cursor_lines:
                for pane_idx, line in enumerate(pane_lines):
                    if line is not None and pane_idx < len(self.panes):
                        self.panes[pane_idx].draw_artist(line)
            self.canvas.blit(self.fig.bbox)
        else:
            self.canvas.draw_idle()

    def _cursor_visible_key(self) -> tuple:
        sim_key = tuple(t.index for t in self.visible_traces)
        func_key = tuple(i for i, v in enumerate(self._func_visible) if v)
        return (sim_key, func_key)

    def _get_cursor_interp(self, x_pos: float, cursor_num: int) -> Optional[Dict]:
        if cursor_num >= len(self._cursor_interp_cache):
            return None
        entry = self._cursor_interp_cache[cursor_num]
        if entry is None:
            return None
        if entry['x_pos'] == x_pos and entry['visible_key'] == self._cursor_visible_key():
            return entry
        return None

    def _set_cursor_interp(self, x_pos: float, cursor_num: int,
                           sim_y: Dict, func_y: Dict) -> None:
        while len(self._cursor_interp_cache) <= cursor_num:
            self._cursor_interp_cache.append(None)
        self._cursor_interp_cache[cursor_num] = {
            'x_pos': x_pos,
            'visible_key': self._cursor_visible_key(),
            'sim_y': sim_y,
            'func_y': func_y,
        }

    def _update_cursor_panel(self, cursor_num: int, x_pos: Optional[float]) -> None:
        """Rebuild the sidebar cursor label with X position + per-signal Y values.

        Shows one line per visible trace so users can read the exact value at
        the cursor for every pane simultaneously — especially useful in stacked
        view where each pane has its own Y scale.
        """
        label_widget = self.cursor1_label if cursor_num == 0 else self.cursor2_label
        color = '#e53935' if cursor_num == 0 else '#1976d2'
        c_label = f'C{cursor_num + 1}'

        if x_pos is None or not hasattr(self.obj_dataext, 'x'):
            label_widget.setText(
                f'<b style="color:{color}">{c_label}</b>'
                f'  <span style="color:#aaa">not set</span>'
            )
            return

        x_full = np.asarray(self.obj_dataext.x, dtype=float)
        scale = self._x_scale or 1.0
        unit_label = (self._x_unit or '').strip()
        x_display = f"{x_pos * scale:.4g}"
        if unit_label:
            x_display += f" {unit_label}"

        html = (f'<span style="font-weight:700;color:{color}">{c_label}</span>'
                f'<span style="color:#999"> @ </span>'
                f'<span style="font-weight:600;color:#333">{x_display}</span>')

        visible = self.visible_traces
        rows = ''

        cached = self._get_cursor_interp(x_pos, cursor_num)
        if cached:
            sim_y = cached['sim_y']
            func_y = cached['func_y']
        else:
            sim_y: Dict[int, float] = {}
            if visible and len(x_full) >= 2:
                for t in visible:
                    try:
                        y_arr = np.asarray(self.obj_dataext.y[t.index], dtype=float)
                    except (IndexError, TypeError):
                        continue
                    n_pts = min(len(y_arr), len(x_full))
                    if n_pts < 2:
                        continue
                    sim_y[t.index] = float(np.interp(x_pos, x_full[:n_pts], y_arr[:n_pts]))
            func_y: Dict[int, float] = {}
            for f_idx, (_, fx, fy, _fcolor, *_) in enumerate(self._func_traces):
                if not (f_idx < len(self._func_visible) and self._func_visible[f_idx]):
                    continue
                n_pts = min(len(fx), len(fy))
                if n_pts < 2:
                    continue
                try:
                    func_y[f_idx] = float(np.interp(x_pos, fx[:n_pts], fy[:n_pts]))
                except Exception:
                    continue
            self._set_cursor_interp(x_pos, cursor_num, sim_y, func_y)

        for t in visible:
            y_val = sim_y.get(t.index)
            if y_val is None:
                continue
            unit = 'V' if t.index < self.obj_dataext.volts_length else 'A'
            value = _format_measurement(y_val, unit)
            rows += (f'<tr>'
                     f'<td style="color:#555;padding-right:8px">{t.name}</td>'
                     f'<td style="font-family:monospace;font-weight:600;color:#333">{value}</td>'
                     f'</tr>')

        for f_idx, (flabel, _fx, _fy, fcolor, *_) in enumerate(self._func_traces):
            if not (f_idx < len(self._func_visible) and self._func_visible[f_idx]):
                continue
            y_val = func_y.get(f_idx)
            if y_val is None:
                continue
            short = flabel if len(flabel) <= 20 else flabel[:18] + '…'
            rows += (f'<tr>'
                     f'<td style="color:{fcolor};padding-right:8px">'
                     f'ƒ {short}</td>'
                     f'<td style="font-family:monospace;font-weight:600;color:#333">{y_val:.4g}</td>'
                     f'</tr>')

        if rows:
            html += f'<table style="margin-top:4px;margin-bottom:4px">{rows}</table>'
        label_widget.setText(html)
        label_widget.updateGeometry()

    def _format_cursor_readout(self, x_pos: float) -> str:
        """Single-line "X | sig1=Y1 | sig2=Y2 …" readout at the cursor X.

        Uses np.interp against the raw simulation x/y arrays so the values
        are accurate even between sample points. SI prefix per signal via
        _format_measurement. Truncated to keep the status bar one line.
        """
        visible = self.visible_traces
        if not visible or not hasattr(self.obj_dataext, 'x'):
            return ''
        x_full = np.asarray(self.obj_dataext.x, dtype=float)
        if len(x_full) < 2:
            return ''
        scale = self._x_scale or 1.0
        unit_label = self._x_unit or ''
        parts = [f"X={x_pos * scale:.4g} {unit_label}".rstrip()]

        # Cursor readout is always for cursor 0 (single-cursor mode).
        cached = self._get_cursor_interp(x_pos, 0)
        if cached:
            sim_y = cached['sim_y']
            func_y = cached['func_y']
        else:
            sim_y = {}
            for t in visible:
                try:
                    y_arr = np.asarray(self.obj_dataext.y[t.index], dtype=float)
                except (IndexError, TypeError):
                    continue
                n_pts = min(len(y_arr), len(x_full))
                if n_pts < 2:
                    continue
                try:
                    sim_y[t.index] = float(np.interp(x_pos, x_full[:n_pts], y_arr[:n_pts]))
                except Exception:
                    continue
            func_y = {}
            for f_idx, (_, fx, fy, _color, *_) in enumerate(self._func_traces):
                if not (f_idx < len(self._func_visible) and self._func_visible[f_idx]):
                    continue
                n_pts = min(len(fx), len(fy))
                if n_pts < 2:
                    continue
                try:
                    func_y[f_idx] = float(np.interp(x_pos, fx[:n_pts], fy[:n_pts]))
                except Exception:
                    continue
            self._set_cursor_interp(x_pos, 0, sim_y, func_y)

        for t in visible:
            y_val = sim_y.get(t.index)
            if y_val is None:
                continue
            is_voltage = t.index < self.obj_dataext.volts_length
            unit = 'V' if is_voltage else 'A'
            parts.append(f"{t.name}={_format_measurement(y_val, unit)}")

        for f_idx, (flabel, _fx, _fy, _color, *_) in enumerate(self._func_traces):
            if not (f_idx < len(self._func_visible) and self._func_visible[f_idx]):
                continue
            y_val = func_y.get(f_idx)
            if y_val is None:
                continue
            short = flabel if len(flabel) <= 14 else flabel[:12] + '…'
            parts.append(f"ƒ({short})={y_val:.4g}")

        # Limit total length so it never wraps the status bar
        readout = " | ".join(parts)
        return readout if len(readout) < 220 else readout[:217] + '…'

    def _get_freq_scale_and_unit(self, freq_data: Optional["np.ndarray"] = None) -> Tuple[float, str]:
        if freq_data is None:
            freq_data = np.asarray(self.obj_dataext.x, dtype=float)
        freq_max = np.max(np.abs(freq_data)) if len(freq_data) > 0 else 0.0
        if freq_max == 0:                                return 1.0,   'Hz'
        if freq_max >= FREQ_UNIT_THRESHOLD_GHZ:          return 1e-9,  'GHz'
        if freq_max >= FREQ_UNIT_THRESHOLD_MHZ:          return 1e-6,  'MHz'
        if freq_max >= FREQ_UNIT_THRESHOLD_KHZ:          return 1e-3,  'kHz'
        return 1.0, 'Hz'

    def set_freq_axis_label(self, freq_data: Optional["np.ndarray"] = None) -> None:
        if not self.panes or not hasattr(self.obj_dataext, 'x'):
            return
        if freq_data is None:
            freq_data = np.asarray(self.obj_dataext.x, dtype=float)
        if len(freq_data) < 2:
            self._x_scale, self._x_unit = 1.0, 'Hz'
            self.panes[-1].set_xlabel('Frequency (Hz)')
            return
        scale, unit = self._get_freq_scale_and_unit(freq_data)
        self._apply_x_axis_scaling(scale, unit, 'Frequency')
        self.axes.set_xlim(float(freq_data[0]), float(freq_data[-1]))

    def _begin_cursor_blit(self) -> None:
        """Save static background for blit-based cursor drag.

        Marks all cursor lines animated=True so canvas.draw() excludes them,
        then snapshots the result. Each move then does restore+draw_artist+blit
        — O(cursor lines) instead of O(full figure). Called once at drag start.
        """
        for pane_lines in self.cursor_lines:
            for line in pane_lines:
                if line is not None:
                    line.set_animated(True)
        self.canvas.draw()
        self._blit_background = self.canvas.copy_from_bbox(self.fig.bbox)

    def _end_cursor_blit(self) -> None:
        """Restore normal render path after cursor drag ends."""
        if self._blit_background is None:
            return
        self._blit_background = None
        for pane_lines in self.cursor_lines:
            for line in pane_lines:
                if line is not None:
                    line.set_animated(False)
        self.canvas.draw_idle()

    def set_cursor(self, cursor_num: int, x_pos: float) -> None:
        # x_pos is in raw SI units (matches line data + xlim post-formatter).
        # Stored positions are raw; displayed labels apply _x_scale at format time.
        # In multi-pane mode the cursor draws one axvline per pane so the
        # vertical line spans the full stack.
        if not self.panes:
            return
        if x_pos is None:
            return
        self._end_cursor_blit()  # no-op if not blitting; clears stale snapshot
        scale = self._current_axis_scale()

        # Pad lists so cursor_num is a valid index. Without this, calling
        # set_cursor(1, x) on empty cursor_lines would silently append at
        # slot 0 → "cursor 2" lands in cursor 1's slot.
        while len(self.cursor_lines) <= cursor_num:
            self.cursor_lines.append([])
            self.cursor_positions.append(None)

        # Tear down old lines for this cursor (every pane) before re-drawing
        for old in self.cursor_lines[cursor_num]:
            if old is None:
                continue
            try:
                old.remove()
            except ValueError:
                pass  # already cleared by fig.clear()

        color = 'red' if cursor_num == 0 else 'blue'
        new_lines: List[Optional[Line2D]] = [
            ax.axvline(x=x_pos, color=color, linestyle='--', alpha=CURSOR_ALPHA)
            for ax in self.panes
        ]
        self.cursor_lines[cursor_num] = new_lines
        self.cursor_positions[cursor_num] = x_pos

        self._update_cursor_panel(cursor_num, x_pos)

        two_cursors = (len(self.cursor_positions) >= 2
                       and all(p is not None for p in self.cursor_positions[:2]))
        if two_cursors:
            delta_raw = abs(self.cursor_positions[1] - self.cursor_positions[0])
            self.delta_label.setText(
                f'<span style="font-weight:700;color:#e65100">ΔX</span>'
                f' <span style="font-family:monospace;font-weight:600;color:#333">{delta_raw * scale:.4g} {(self._x_unit or "").strip()}</span>'
            )
            self._update_measure_label(delta_raw, scale)
        else:
            self.measure_label.setText(self._format_cursor_readout(x_pos))
        self.canvas.draw()

    def clear_cursors(self) -> None:
        for pane_lines in self.cursor_lines:
            for line in pane_lines:
                if line is None:
                    continue
                try:
                    line.remove()
                except ValueError:
                    pass  # already removed by fig.clear()
        self.cursor_lines.clear()
        self.cursor_positions.clear()
        self.cursor1_label.setText('<b style="color:#e53935">C1</b>  <span style="color:#aaa">not set</span>')
        self.cursor2_label.setText('<b style="color:#1976d2">C2</b>  <span style="color:#aaa">not set</span>')
        self.delta_label.setText('<b style="color:#e65100">ΔX</b>  <span style="color:#aaa">—</span>')
        self.measure_label.setText("")
        self.canvas.draw()

    def _restore_cursors(self) -> None:
        """Re-create cursor axvlines after fig.clear(), using stored positions.

        Positions are raw SI units and match the current xlim directly — no
        scale factor applied at draw time (formatter handles tick display).
        Each cursor draws one axvline per pane so the line spans the full stack.
        """
        if not self.panes or not self.cursor_positions:
            return
        colors = ['red', 'blue']
        rebuilt: List[List[Optional[Line2D]]] = []
        for i, x_pos in enumerate(self.cursor_positions):
            if x_pos is None:
                rebuilt.append([])
                continue
            color = colors[i] if i < len(colors) else 'green'
            pane_lines: List[Optional[Line2D]] = [
                ax.axvline(x=x_pos, color=color,
                           linestyle='--', alpha=CURSOR_ALPHA)
                for ax in self.panes
            ]
            rebuilt.append(pane_lines)
        self.cursor_lines = rebuilt
        if rebuilt:
            logger.debug("Restored %d cursor(s) after plot refresh", len(rebuilt))
        self._refresh_cursor_readouts()

    def _refresh_cursor_readouts(self) -> None:
        """Recompute the sidebar cursor labels (C1/C2/ΔX/measure) in place.

        Does interpolated Y lookups against the current visible-trace set, so
        it must run after panes and _x_scale/_x_unit are set up. Split out of
        _restore_cursors so the incremental refresh — where the axvlines
        already exist and must NOT be re-created — can refresh just the
        readouts when the visible set changes.
        """
        scale = self._current_axis_scale()
        for i, x_pos in enumerate(self.cursor_positions):
            if x_pos is not None:
                self._update_cursor_panel(i, x_pos)
        two_cursors = (len(self.cursor_positions) >= 2
                       and all(p is not None for p in self.cursor_positions[:2]))
        if two_cursors:
            delta_raw = abs(self.cursor_positions[1] - self.cursor_positions[0])
            self.delta_label.setText(
                f'<span style="font-weight:700;color:#e65100">ΔX</span>'
                f' <span style="font-family:monospace;font-weight:600;color:#333">'
                f'{delta_raw * scale:.4g} {(self._x_unit or "").strip()}</span>'
            )
            self._update_measure_label(delta_raw, scale)
        elif self.cursor_positions and self.cursor_positions[0] is not None:
            self.measure_label.setText(
                self._format_cursor_readout(self.cursor_positions[0]))

