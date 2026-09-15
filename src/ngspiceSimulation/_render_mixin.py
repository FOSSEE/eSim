from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, ScalarFormatter
from PyQt6.QtWidgets import QMenu
from PyQt6.QtCore import Qt
from .data_extraction import DataExtraction
from .trace import Trace
from .constants import (DEFAULT_VERTICAL_SPACING, DEFAULT_ZOOM_FACTOR, LEGEND_FONT_SIZE,
                        CURSOR_ALPHA, THRESHOLD_ALPHA, VIBRANT_COLOR_PALETTE,
                        TIME_UNIT_THRESHOLD_PS, TIME_UNIT_THRESHOLD_NS,
                        TIME_UNIT_THRESHOLD_US, TIME_UNIT_THRESHOLD_MS,
                        FREQ_UNIT_THRESHOLD_KHZ, FREQ_UNIT_THRESHOLD_MHZ,
                        FREQ_UNIT_THRESHOLD_GHZ, REFRESH_DEBOUNCE_MS,
                        STACKED_REFRESH_DEBOUNCE_MS)
from .math_utils import (_format_measurement, _format_frequency, _detect_frequency, _trapz)


class _RenderMixin:
    def _schedule_refresh(self) -> None:
        """Coalesce rapid visibility toggles into a single deferred refresh.

        Restarting the single-shot timer on each call means a burst of clicks
        collapses to one refresh_plot once the user stops. Used by every
        waveform/func-trace visibility toggle; direct refresh_plot calls
        (view-mode change, autoscale, etc.) cancel any pending tick via the
        stop() at the top of refresh_plot so they never double-rebuild.

        The window is mode-aware: a stacked toggle is a full pane rebuild
        (tens of ms, growing with pane count), so a wider window is needed to
        actually collapse a human-paced click burst — otherwise each click
        (>80ms apart) fires its own rebuild and the view stutters. Normal view
        toggles take the cheap incremental path, so they stay snappy at 80ms.
        The list item icon/text update synchronously either way, so clicks
        always feel instant; only the plot redraw is deferred.
        """
        self._refresh_timer.setInterval(
            STACKED_REFRESH_DEBOUNCE_MS if self.radio_stacked.isChecked()
            else REFRESH_DEBOUNCE_MS)
        self._refresh_timer.start()

    def _composition_signature(self, mode: str) -> tuple:
        """Fingerprint of everything that determines the pane/artist structure.

        When this is unchanged between two refreshes, the existing axes and
        Line2D objects are already correct (trace data is static after load),
        so refresh_plot can skip the full fig.clear() teardown.

        Per mode it captures only what is *structural* for that mode:

        - normal: one shared Axes regardless of how many traces are visible,
          so the visible set is deliberately EXCLUDED — visibility toggles are
          handled incrementally via set_visible. What IS structural: the
          analysis path (plot vs semilogx vs step), which traces use steps
          (changes the artist type), the visible function-overlay set, and
          whether the legend is shown.
        - stacked: one pane per visible trace, so the visible set + per-trace
          steps flag + visible func panes + stats overlay are all structural.
        - timing: rows are laid out by the visible set; threshold and spacing
          change every row's geometry.

        Changes the signature cannot see (pane reorder, divider resize, lock
        toggle, rename) set self._force_full_refresh instead.
        """
        vis_func = tuple(i for i in range(len(self._func_traces))
                         if i < len(self._func_visible) and self._func_visible[i])
        if mode == 'normal':
            steps = tuple(sorted(i for i, t in self.traces.items()
                                 if t.style == 'steps-post'))
            return ('normal', self._current_analysis_type, steps, vis_func,
                    self.legend_check.isChecked())
        if mode == 'stacked':
            vis = self.visible_traces
            return ('stacked',
                    tuple(t.index for t in vis),
                    tuple(t.style == 'steps-post' for t in vis),
                    vis_func,
                    self.stats_check.isChecked())
        # timing
        return ('timing',
                tuple(t.index for t in self.visible_traces),
                vis_func,
                self.threshold_spinbox.value(),
                self.vertical_spacing)

    def refresh_plot(self) -> None:
        # Cancel any pending debounced refresh — this call supersedes it, so a
        # queued timer tick must not fire a second redundant rebuild afterwards.
        self._refresh_timer.stop()
        force_full = self._force_full_refresh
        self._force_full_refresh = False

        next_mode = ('timing' if self.radio_timing.isChecked()
                     else 'stacked' if self.radio_stacked.isChecked()
                     else 'normal')
        new_sig = self._composition_signature(next_mode)

        # ── Incremental fast path ────────────────────────────────────────
        # Taken only when the pane composition is provably unchanged from what
        # is currently drawn: same mode, matching signature, live panes, and no
        # caller-forced full rebuild. Then the axes + lines already exist and
        # are correct, so we avoid fig.clear() entirely.
        if (not force_full and self.panes
                and self._drawn_signature is not None
                and new_sig == self._drawn_signature
                and self._current_view_mode == next_mode):
            if next_mode == 'normal':
                # Normal view keeps ALL prior limits/cursors; only line
                # visibility may differ. 0-visible needs the placeholder text,
                # so fall through to the full rebuild for that case.
                if self.visible_traces:
                    self._incremental_refresh_normal()
                    return
            else:
                # Stacked/timing: identical composition + static data means the
                # rendered figure is already correct. Just redraw.
                for ax in self.panes:
                    ax.grid(self.grid_check.isChecked())
                self.canvas.draw_idle()
                return

        # ── Full rebuild ─────────────────────────────────────────────────
        # Preserve zoom when autoscale is off.
        # Capture only when staying in the SAME ylim-meaningful mode: timing
        # uses [0..N] normalized space, stacked uses per-trace SI units —
        # restoring one across modes would clip signals or scramble panes.
        capture_state = (not self.autoscale_check.isChecked()
                         and self._current_view_mode == next_mode
                         and next_mode in ('normal', 'stacked')
                         and bool(self.panes))
        if capture_state:
            self._capture_view_state()

        # Re-enable constrained_layout before rebuilding: a previous stacked
        # refresh may have frozen it (engine off + pinned positions). The new
        # panes must be solved once by CL; _freeze_layout re-freezes at the end
        # for multi-pane stacked. Cheap single-pane modes stay CL-managed.
        self.fig.set_layout_engine('constrained')

        self._func_line = None  # fig.clear() below wipes all artists
        self.timing_annotations.clear()
        # Any in-progress cursor drag and the blit snapshot become invalid
        # once fig.clear() tears down the figure.  Reset them here so the
        # restore path that follows starts from a clean state.
        self._drag_cursor_idx = None
        self._blit_background = None
        self.fig.clear()
        # Hover-cache held references to the old Axes; invalidate before
        # _build_panes hands out fresh ones.
        self._last_hover_axes = None
        self._last_hover_anchor = None
        for t in self.traces.values():
            t.line_object = None
        # Set view mode BEFORE plot path runs so callees (update_timing_tick_colors,
        # legend handling, etc.) can branch on the new mode instead of the prior one.
        self._current_view_mode = next_mode
        if next_mode == 'timing':
            self._build_panes(1)
            self.plot_timing_diagram()
        elif next_mode == 'stacked':
            self.plot_stacked_diagram()
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
        if self.panes:
            for ax in self.panes:
                ax.grid(self.grid_check.isChecked())
            # Restore unconditionally: capture_state fills saved_pane_ylims
            # for the preserve-zoom path, AND lock-Y entries persist there
            # independently. _restore_view_state is a no-op when both are
            # empty, so calling it is always safe.
            self._restore_view_state()
            if self.legend_check.isChecked():
                self.position_legend()
        self._restore_cursors()
        # Record what we just drew so the next refresh can skip the rebuild if
        # nothing structural changed.
        self._drawn_signature = new_sig
        # Arm the free post-draw freeze for multi-pane stacked: the draw below
        # solves CL once, then _on_draw_event pins the result and drops the
        # engine so later draws skip the solver. Doing this inline (an extra
        # synchronous layout pass) is what made rapid toggling lag, so we let
        # the draw we already need do the work. Single-pane modes keep CL on —
        # cheap there, and it keeps tick-label margins adaptive.
        self._pending_freeze = (self._current_view_mode == 'stacked'
                                and len(self.panes) > 1)
        self.canvas.draw_idle()

    def _incremental_refresh_normal(self) -> None:
        """Update the shared-axes normal view in place — no fig.clear().

        Used when the composition signature is unchanged but trace visibility
        may have toggled. Reconciles each trace's Line2D (lazily creating one
        for a newly-visible trace, hiding rather than destroying one that was
        switched off), then re-fits/legends/cursors exactly as a full rebuild
        would, all without tearing the figure down.
        """
        for idx, t in self.traces.items():
            if t.visible:
                if t.line_object is None:
                    self._draw_normal_trace_line(t)
                else:
                    t.line_object.set_visible(True)
            elif t.line_object is not None:
                # Keep the artist for cheap re-show; just hide it.
                t.line_object.set_visible(False)

        # Re-fit only when autoscale is on; otherwise leave the user's zoom.
        # visible_only=True excludes the hidden (kept) lines from the bounds.
        if self.autoscale_check.isChecked():
            self.axes.relim(visible_only=True)
            self.axes.autoscale_view()

        first_visible = next((i for i in sorted(self.traces)
                              if self.traces[i].visible), None)
        if first_visible is not None:
            self.axes.set_ylabel('Voltage (V)' if first_visible < self.volts_length
                                 else 'Current (A)')

        if self.legend_check.isChecked():
            # legend() replaces any existing legend; ≥1 visible is guaranteed
            # by the caller, so position_legend always has a handle to draw.
            self.position_legend()

        # Cursor axvlines persist on the live axes (no fig.clear), so they need
        # no re-creation — but the sidebar readouts depend on the visible set,
        # which just changed, so refresh those.
        if any(p is not None for p in self.cursor_positions):
            self._refresh_cursor_readouts()

        self.canvas.draw_idle()

    def _on_draw_event(self, event) -> None:
        """Freeze the layout for FREE, right after a stacked rebuild's draw.

        The CL solver (~60% of a stacked draw's Python time) re-runs on every
        draw — even when pane geometry is unchanged. We can't avoid the one
        solve that the rebuild's own draw performs, but we CAN stop it repeating
        on subsequent zoom/pan/cursor draws: this fires after that draw has
        already solved CL, so we snapshot the EXACT solved positions (margins
        match CL by construction — rotated y-labels, stats titles included) and
        drop the engine. No extra layout pass, so rapid toggling stays cheap.
        """
        if not (self._pending_freeze and self.panes
                and self._current_view_mode == 'stacked'
                and len(self.panes) > 1):
            return
        self._pending_freeze = False
        positions = [ax.get_position().frozen() for ax in self.panes]
        self.fig.set_layout_engine('none')       # stop the solver
        for ax, pos in zip(self.panes, positions):
            ax.set_position(pos)                 # pin the CL-solved geometry

    def position_legend(self) -> None:
        if not (self.panes and self.legend_check.isChecked()):
            return
        # Stacked view: each pane already has a single-trace caption (set by
        # the stacked plot path), so a combined legend on the top pane would
        # be redundant noise.
        if self._current_view_mode == 'stacked':
            return
        handles, labels = [], []
        for idx in sorted(self.traces.keys()):
            t = self.traces[idx]
            if t.visible and t.line_object:
                handles.append(t.line_object)
                labels.append(t.name)
        if not handles:
            return
        ncol = max(1, min(4, len(handles)))
        legend = self.axes.legend(
            handles, labels,
            loc='best',
            ncol=ncol,
            frameon=True,
            fancybox=False,
            shadow=False,
            framealpha=0.95,
            columnspacing=1.2,
            handlelength=1.5,
        )
        legend.get_frame().set_facecolor('white')
        legend.get_frame().set_edgecolor('#E0E0E0')
        legend.get_frame().set_linewidth(1)

    def _get_transient_start_idx(self, time_data: "np.ndarray") -> int:
        """Return the index into time_data where the .tran start time begins, or 0."""
        if self._tran_start_time > 0:
            return int(np.searchsorted(time_data, self._tran_start_time))
        return 0

    def plot_timing_diagram(self) -> None:
        """Plot digital timing diagram with normalized trace heights."""
        self.timing_annotations.clear()

        if self.plot_type[0] != DataExtraction.TRANSIENT_ANALYSIS:
            self.axes.text(0.5, 0.5, 'Digital timing view is only\navailable for transient analysis.',
                           ha='center', va='center', transform=self.axes.transAxes,
                           color='#757575')
            self.axes.set_yticks([])
            self.axes.set_yticklabels([])
            return

        visible_indices = [t.index for t in self.visible_traces]
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
                    color=t.color, clip_on=False))
            else:
                ann.append(self.axes.text(
                    1.01, rank * spacing + 0.82,
                    f"H: {_format_measurement(float(trace_vmax), trace_unit)}",
                    transform=xform, va='center', ha='left',
                    color=t.color, clip_on=False))
                ann.append(self.axes.text(
                    1.01, rank * spacing + 0.18,
                    f"L: {_format_measurement(float(trace_vmin), trace_unit)}",
                    transform=xform, va='center', ha='left',
                    color=t.color, clip_on=False))
                freq = _detect_frequency(trace_time, logic_normalized)
                if freq is not None:
                    ann.append(self.axes.text(
                        1.01, y_center, _format_frequency(freq),
                        transform=xform, va='center', ha='left',
                        color=t.color, alpha=0.75, clip_on=False))
            self.timing_annotations[idx] = ann

        # Func traces as additional timing channels — normalized same as sim signals.
        n_sim = len(visible_indices)
        vis_func = [
            (f_idx, self._func_traces[f_idx])
            for f_idx in range(len(self._func_traces))
            if f_idx < len(self._func_visible) and self._func_visible[f_idx]
        ]
        xform = self.axes.get_yaxis_transform()
        for func_slot, (f_idx, (flabel, fx, fy, fcolor, fthickness, _fs)) in enumerate(vis_func):
            rank = n_sim + func_slot
            n_pts = min(len(fx), len(fy))
            if n_pts < 2:
                continue
            fy_arr = np.asarray(fy[:n_pts], dtype=float)
            fx_arr = np.asarray(fx[:n_pts], dtype=float)
            fmin, fmax = float(np.min(fy_arr)), float(np.max(fy_arr))
            y_center = rank * spacing + 0.5
            if fmax - fmin < 1e-10:
                logic = np.full(n_pts, 0.5)
                self.axes.text(1.01, y_center, f"DC: {fmax:.4g}",
                               transform=xform, va='center', ha='left',
                               color=fcolor, clip_on=False,
                               fontsize=max(7, LEGEND_FONT_SIZE - 1))
            else:
                logic = np.where(fy_arr > (fmin + fmax) / 2.0, 1.0, 0.0)
                self.axes.text(1.01, rank * spacing + 0.82, f"H: {fmax:.4g}",
                               transform=xform, va='center', ha='left',
                               color=fcolor, clip_on=False,
                               fontsize=max(7, LEGEND_FONT_SIZE - 1))
                self.axes.text(1.01, rank * spacing + 0.18, f"L: {fmin:.4g}",
                               transform=xform, va='center', ha='left',
                               color=fcolor, clip_on=False,
                               fontsize=max(7, LEGEND_FONT_SIZE - 1))
                freq = _detect_frequency(fx_arr, logic)
                if freq is not None:
                    self.axes.text(1.01, y_center, _format_frequency(freq),
                                   transform=xform, va='center', ha='left',
                                   color=fcolor, alpha=0.75, clip_on=False,
                                   fontsize=max(7, LEGEND_FONT_SIZE - 1))
            self.axes.step(fx_arr, logic + rank * spacing, where='post',
                           color=fcolor, linewidth=fthickness, label=flabel)
            yticks.append(y_center)
            ylabels.append(f'ƒ {flabel}')

        # Y-axis bounds: total count includes func trace slots.
        total_count = n_sim + len(vis_func)
        total_height = max(total_count - 1, 0) * spacing + 1.0
        margin = 0.15 * spacing
        self.axes.set_ylim(-margin, total_height + margin)
        self.axes.set_yticks(yticks)
        self.axes.set_yticklabels(ylabels)

        self.update_timing_tick_colors()
        self.set_time_axis_label(time_data)

        # Threshold lines for sim signals only.
        for rank, idx in enumerate(visible_indices[::-1]):
            if idx in self.logic_thresholds:
                self.axes.axhline(y=self.logic_thresholds[idx] + rank * spacing,
                                  color='red', linestyle=':', alpha=THRESHOLD_ALPHA, linewidth=0.8)

    def _render_pane_stats(self, ax, group: List[int],
                           x_arr: "np.ndarray") -> None:
        """Draw a min/max/p-p/RMS (+ freq for periodic transient) overlay.

        One text row per trace in the group, anchored top-right via axes
        fraction so it survives pane resize / zoom. Skipped silently when
        the group has no plottable traces.
        """
        if not group:
            return
        rows: List[str] = []
        for trace_idx in group:
            t = self.traces.get(trace_idx)
            if t is None:
                continue
            y_arr = np.asarray(self.obj_dataext.y[trace_idx], dtype=float)
            n_pts = min(len(y_arr), len(x_arr))
            if n_pts < 2:
                continue
            y = y_arr[:n_pts]
            x = x_arr[:n_pts]
            unit = 'V' if trace_idx < self.obj_dataext.volts_length else 'A'
            ymin = float(np.min(y))
            ymax = float(np.max(y))
            pp = ymax - ymin
            # Trapezoid integration is correct for adaptive-timestep ngspice
            # output where sample spacing is non-uniform (up to 200x ratio).
            # Simple mean/mean² gives wrong DC and RMS on such data.
            T = float(x[-1] - x[0])
            dc = float(_trapz(y, x) / T)
            rms_total_sq = float(_trapz(y * y, x) / T)
            # AC RMS = sqrt(RMS² - DC²) — signal amplitude without DC offset.
            rms_ac = float(np.sqrt(max(0.0, rms_total_sq - dc * dc)))
            # Drop min/max (already visible from Y-axis ticks) and name
            # (already the left title). Keep only the high-value stats.
            parts = [f"p-p={_format_measurement(pp, unit)}",
                     f"DC={_format_measurement(dc, unit)}",
                     f"RMS={_format_measurement(rms_ac, unit)}"]
            if self._current_analysis_type == 'transient' and pp > 1e-12:
                mid = (ymin + ymax) / 2.0
                logic = np.where(y > mid, 1.0, 0.0)
                freq = _detect_frequency(x, logic)
                if freq is not None:
                    parts.append(f"f={_format_frequency(freq)}")
            rows.append("  ".join(parts))
        if not rows:
            return
        # No bbox — stats are in the title margin above the spine, no waveform
        # behind them, so a white background box is unnecessary and its padding
        # would straddle the spine into the axes area.
        ax.set_title("\n".join(rows), loc='right',
                     fontsize=max(7, LEGEND_FONT_SIZE - 1),
                     color='#444444', pad=4)

    def _render_func_pane_stats(self, ax, fx: "np.ndarray", fy: "np.ndarray") -> None:
        x = np.asarray(fx, dtype=float)
        y = np.asarray(fy, dtype=float)
        n = min(len(x), len(y))
        if n < 2:
            return
        x, y = x[:n], y[:n]
        ymin, ymax = float(np.min(y)), float(np.max(y))
        pp = ymax - ymin
        T = float(x[-1] - x[0])
        if T <= 0:
            return
        dc = float(_trapz(y, x) / T)
        rms_ac = float(np.sqrt(max(0.0, float(_trapz(y * y, x) / T) - dc * dc)))

        def _fmt(v: float) -> str:
            a = abs(v)
            if a >= 1:      return f"{v:.3g}"
            if a >= 1e-3:   return f"{v * 1e3:.3g}m"
            if a >= 1e-6:   return f"{v * 1e6:.3g}µ"
            if a >= 1e-9:   return f"{v * 1e9:.3g}n"
            return f"{v:.3g}"

        parts = [f"p-p={_fmt(pp)}", f"DC={_fmt(dc)}", f"RMS={_fmt(rms_ac)}"]
        if self._current_analysis_type == 'transient' and pp > 1e-12:
            freq = _detect_frequency(x, np.where(y > (ymin + ymax) / 2.0, 1.0, 0.0))
            if freq is not None:
                parts.append(f"f={_format_frequency(freq)}")
        ax.set_title("  ".join(parts), loc='right',
                     fontsize=max(7, LEGEND_FONT_SIZE - 1),
                     color='#444444', pad=4)

    def plot_stacked_diagram(self) -> None:
        """Stacked-pane view: one pane per visible trace + one per func trace.

        Each entry in self._pane_groups is a single-element list containing
        the trace.index of that pane's signal. Function panes follow at the
        bottom. Heights, lock-Y, stats, and pane-name anchor live on the
        first (and only) trace in the group.

        Function traces (set by plot_function while stacked is active) tail
        at the bottom as one extra pane each.
        """
        # Bring _pane_groups in line with the current visibility set
        self._sync_pane_groups_to_visible()

        if not self._pane_groups and not self._func_traces:
            self._build_panes(1)
            self.axes.text(0.5, 0.5, 'Select a waveform to display',
                           ha='center', va='center',
                           transform=self.axes.transAxes)
            self.axes.set_yticks([])
            self.axes.set_yticklabels([])
            return

        is_transient = self.plot_type[0] == DataExtraction.TRANSIENT_ANALYSIS
        is_ac        = self.plot_type[0] == DataExtraction.AC_ANALYSIS
        is_log       = is_ac and self.plot_type[1] == 1
        is_dc        = self.plot_type[0] == DataExtraction.DC_ANALYSIS

        x_data = np.asarray(self.obj_dataext.x, dtype=float)
        if is_transient:
            start_idx = self._get_transient_start_idx(x_data)
            if 0 < start_idx < len(x_data):
                x_data = x_data[start_idx:]

        n_groups = len(self._pane_groups)
        # Only visible func traces get their own pane.
        _vis_func = [i for i in range(len(self._func_traces))
                     if i < len(self._func_visible) and self._func_visible[i]]
        n_funcs = len(_vis_func)
        n = n_groups + n_funcs
        self._build_panes(n)

        for pane_idx, group in enumerate(self._pane_groups):
            ax = self.panes[pane_idx]
            if not group or group[0] not in self.traces:
                ax.set_ylim(-1, 1)
                if pane_idx < n - 1:
                    ax.tick_params(labelbottom=False)
                continue
            t = self.traces[group[0]]
            raw_y = np.asarray(self.obj_dataext.y[t.index], dtype=float)
            n_pts = min(len(raw_y), len(x_data))
            if n_pts == 0:
                ax.set_ylim(-1, 1)
                if pane_idx < n - 1:
                    ax.tick_params(labelbottom=False)
                continue
            y = raw_y[:n_pts]
            trace_x = x_data[:n_pts]

            plot_style = '-' if t.style == 'steps-post' else t.style
            if is_log:
                line, = ax.semilogx(trace_x, y, color=t.color,
                                    linewidth=t.thickness,
                                    linestyle=plot_style)
            elif t.style == 'steps-post' and (is_transient or is_dc):
                line, = ax.step(trace_x, y, where='post', color=t.color,
                                linewidth=t.thickness)
            else:
                line, = ax.plot(trace_x, y, color=t.color,
                                linewidth=t.thickness, linestyle=plot_style)
            t.line_object = line

            ax.set_title(t.name, loc='left', color=t.color,
                         fontsize=LEGEND_FONT_SIZE, fontweight='bold', pad=3)

            is_voltage = t.index < self.obj_dataext.volts_length
            unit = 'V' if is_voltage else 'A'
            ax.set_ylabel(unit, rotation=0, labelpad=8, va='center')
            ax.yaxis.set_major_formatter(FuncFormatter(
                lambda v, _pos, _u=unit: _format_measurement(float(v), _u)))

            ymin = float(np.min(y))
            ymax = float(np.max(y))
            if abs(ymax - ymin) < 1e-12:
                center = (ymin + ymax) / 2.0
                ax.set_ylim(center - 1.0, center + 1.0)
            else:
                margin = 0.1 * (ymax - ymin)
                ax.set_ylim(ymin - margin, ymax + margin)

            if pane_idx < n - 1:
                ax.tick_params(labelbottom=False)
                # Visible separator hint: gray bottom spine reads as a row
                # divider in the strip chart.
                ax.spines['bottom'].set_color('#BDBDBD')
                ax.spines['bottom'].set_linewidth(1.0)

            if self.stats_check.isChecked():
                self._render_pane_stats(ax, group, x_data)

        # Trailing function-trace panes. Only visible func traces get a pane.
        # _vis_func holds the original indices into _func_traces so labels
        # and colours stay correct after partial hide/show.
        for pane_slot, f_idx in enumerate(_vis_func):
            pane_offset = n_groups + pane_slot
            if pane_offset >= len(self.panes):
                break
            label, fx, fy, color, thickness, style = self._func_traces[f_idx]
            ax = self.panes[pane_offset]
            plot_style = '-' if style == 'steps-post' else style
            if style == 'steps-post':
                ax.step(fx, fy, where='post', color=color, linewidth=thickness)
            else:
                ax.plot(fx, fy, color=color, linewidth=thickness, linestyle=plot_style)
            ax.set_title(label, loc='left', color=color,
                         fontsize=LEGEND_FONT_SIZE, fontweight='bold', pad=3)
            if len(fy):
                ymin = float(np.min(fy))
                ymax = float(np.max(fy))
                if abs(ymax - ymin) < 1e-12:
                    center = (ymin + ymax) / 2.0
                    ax.set_ylim(center - 1.0, center + 1.0)
                else:
                    margin = 0.1 * (ymax - ymin)
                    ax.set_ylim(ymin - margin, ymax + margin)
            if pane_offset < n - 1:
                ax.tick_params(labelbottom=False)
                ax.spines['bottom'].set_color('#BDBDBD')
                ax.spines['bottom'].set_linewidth(1.0)

            if self.stats_check.isChecked():
                self._render_func_pane_stats(ax, fx, fy)

        # Bottom-pane X label / formatter. Existing helpers already target
        # self.panes[-1], so the multi-pane case is free.
        if is_ac:
            self.set_freq_axis_label()
        elif is_transient:
            self.set_time_axis_label(x_data)
        else:  # DC sweep
            self._reset_x_axis_scaling()
            self.panes[-1].set_xlabel('Voltage Sweep (V)')


    def _reset_x_axis_scaling(self) -> None:
        """Drop any SI-unit formatter on the X axis (identity tick labels).

        Used when the X axis no longer represents time/frequency — e.g. the
        Lissajous case in plot_function where X becomes a voltage trace.
        """
        self._x_scale = 1.0
        self._x_unit = ''
        for ax in self.panes:
            ax.xaxis.set_major_formatter(ScalarFormatter())

    def _apply_x_axis_scaling(self, scale: float, unit: str,
                              label_prefix: str) -> None:
        """Display-only X-axis scaling via FuncFormatter.

        Line data and xlim stay in raw SI units; tick labels show raw * scale.
        This keeps event.xdata, cursor positions, and stored data coherent and
        eliminates the previous mutate-on-every-refresh xdata bug. The label
        is only attached to the bottom-most pane so stacked panes share one
        unified X axis caption.
        """
        self._x_scale = scale
        self._x_unit = unit
        fmt = FuncFormatter(lambda v, _pos, _s=scale: f"{v * _s:g}")
        for ax in self.panes:
            ax.xaxis.set_major_formatter(fmt)
            ax.set_xlabel('')
        if self.panes:
            self.panes[-1].set_xlabel(f'{label_prefix} ({unit})')

    def set_time_axis_label(self, time_data: Optional["np.ndarray"] = None) -> None:
        if not self.panes or not hasattr(self.obj_dataext, 'x'):
            return
        if time_data is None:
            time_data = np.asarray(self.obj_dataext.x, dtype=float)
        if len(time_data) < 2:
            self._x_scale, self._x_unit = 1.0, 's'
            self.panes[-1].set_xlabel('Time (s)')
            return
        scale, unit = self._get_time_scale_and_unit(time_data)
        self._apply_x_axis_scaling(scale, unit, 'Time')
        self.axes.set_xlim(float(time_data[0]), float(time_data[-1]))

    def on_threshold_changed(self, value: float) -> None:
        if self.radio_timing.isChecked():
            self._controls_timer.start()

    def on_spacing_changed(self, value: int) -> None:
        self.vertical_spacing = value / 100.0
        self.spacing_label.setText(f"{self.vertical_spacing:.1f}x")
        if self.radio_timing.isChecked():
            self._controls_timer.start()

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

    def _current_axis_scale(self) -> float:
        if self._current_analysis_type in ('ac_log', 'ac_linear'):
            return self._get_freq_scale_and_unit()[0]
        return self._get_time_scale_and_unit()[0]

    def _update_measure_label(self, delta_original: float, scale: float) -> None:
        if self._current_analysis_type in ('ac_log', 'ac_linear'):
            _, unit = self._get_freq_scale_and_unit()
            self.measure_label.setText(f"ΔF: {delta_original * scale:.6g} {unit}")
        else:
            if delta_original > 0:
                self.measure_label.setText(f"Freq: {1.0 / delta_original:.6g} Hz")

    def _draw_normal_trace_line(self, t: "Trace",
                                x_data: "Optional[np.ndarray]" = None) -> "Line2D":
        """Plot one trace on the shared normal-view axes and store its line.

        Shared by the full rebuild (_plot_analysis_data) and the incremental
        refresh (_incremental_refresh_normal) so the artist type — step vs
        semilogx vs plot — is chosen identically on both paths. Branches on
        self._current_analysis_type, which the full rebuild sets first.
        """
        if x_data is None:
            x_data = np.asarray(self.obj_dataext.x, dtype=float)
        y_data = np.asarray(self.obj_dataext.y[t.index], dtype=float)
        n_pts = min(len(x_data), len(y_data))
        x_plot, y_plot = x_data[:n_pts], y_data[:n_pts]
        analysis_type = self._current_analysis_type
        plot_style = '-' if t.style == 'steps-post' else t.style
        plot_kwargs: dict = {}
        if t.style == 'steps-post' and analysis_type in ['transient', 'dc']:
            plot_func = self.axes.step
            plot_kwargs['where'] = 'post'
        elif analysis_type == 'ac_log':
            plot_func = self.axes.semilogx
        else:
            plot_func = self.axes.plot
        line, = plot_func(x_plot, y_plot, color=t.color, label=t.name,
                          linewidth=t.thickness, linestyle=plot_style, **plot_kwargs)
        t.line_object = line
        return line

    def _plot_analysis_data(self, analysis_type: str) -> None:
        self._current_analysis_type = analysis_type
        self._build_panes(1)
        traces_plotted = 0
        first_visible = None
        x_data = np.asarray(self.obj_dataext.x, dtype=float)
        for idx, t in self.traces.items():
            if not t.visible:
                continue
            traces_plotted += 1
            if first_visible is None:
                first_visible = idx
            self._draw_normal_trace_line(t, x_data)

        if analysis_type in ['ac_linear', 'ac_log']:
            self.set_freq_axis_label()
        elif analysis_type == 'dc':
            self.axes.set_xlabel('Voltage Sweep (V)')

        if first_visible is not None:
            self.axes.set_ylabel('Voltage (V)' if first_visible < self.volts_length else 'Current (A)')

        if traces_plotted == 0:
            self.axes.text(0.5, 0.5, 'Please select a waveform to plot', ha='center', va='center', transform=self.axes.transAxes)

        if analysis_type == 'transient':
            self.set_time_axis_label()

        # Overlay visible function traces on the shared axes.
        # Stacked mode renders these as separate panes in plot_stacked_diagram,
        # so this block is normal-mode-only (single axes).
        for _f_idx, (_label, _fx, _fy, _color, _thickness, _style) in enumerate(self._func_traces):
            if not (_f_idx < len(self._func_visible) and self._func_visible[_f_idx]):
                continue
            _n = min(len(_fx), len(_fy))
            if _n > 0:
                _plot_style = '-' if _style == 'steps-post' else _style
                if _style == 'steps-post':
                    self.axes.step(_fx[:_n], _fy[:_n], where='post',
                                   color=_color, label=_label, linewidth=_thickness)
                else:
                    self.axes.plot(_fx[:_n], _fy[:_n], color=_color,
                                   label=_label, linewidth=_thickness, linestyle=_plot_style)


    def on_push_decade(self) -> None:
        self._plot_analysis_data('ac_log')

    def on_push_ac(self) -> None:
        self._plot_analysis_data('ac_linear')

    def on_push_trans(self) -> None:
        self._plot_analysis_data('transient')

    def on_push_dc(self) -> None:
        self._plot_analysis_data('dc')

