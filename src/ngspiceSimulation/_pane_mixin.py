from typing import Any, Dict, List, Optional, Tuple
from PyQt6.QtWidgets import QMenu
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from matplotlib.lines import Line2D
from .constants import (MIN_STACKED_PANE_HEIGHT_PX, DIVIDER_HIT_TOLERANCE_PX,
                        STACKED_REFRESH_DEBOUNCE_MS)


class _PaneMixin:
    def _build_panes(self, n: int, sharex: bool = True,
                     hspace: float = 0.08) -> List[Any]:
        """Create N stacked subplots, store in self.panes, return them.

        n==1 — single Axes (equivalent to add_subplot(111)).
        n>=2 — N vertically stacked Axes with shared X-axis by default.

        In stacked view, self._pane_heights (when present and matching N)
        becomes the gridspec height_ratios so individual panes can be
        resized via the divider-drag handlers.

        Caller must fig.clear() before invoking; this helper does not clear.
        self.axes is aliased to self.panes[0] so legacy single-axes call
        sites keep working unchanged.
        """
        if n <= 1:
            self.panes = [self.fig.add_subplot(111)]
        else:
            gridspec_kw: Dict[str, Any] = {'hspace': hspace}
            if (self._current_view_mode == 'stacked'
                    and self._pane_heights
                    and all(h > 0 for h in self._pane_heights)):
                # _pane_heights tracks group panes only; pad with 1.0 for any
                # trailing function panes so the gridspec still matches N.
                heights = list(self._pane_heights)
                while len(heights) < n:
                    heights.append(1.0)
                gridspec_kw['height_ratios'] = heights[:n]
            axes = self.fig.subplots(
                n, 1, sharex=sharex, gridspec_kw=gridspec_kw,
            )
            # subplots returns ndarray when n>1
            self.panes = list(axes) if hasattr(axes, '__iter__') else [axes]
        self.axes = self.panes[0]
        self._set_canvas_height_for_panes(n)
        return self.panes

    def _set_canvas_height_for_panes(self, n: int) -> None:
        """Force canvas tall enough for N stacked panes; let it shrink elsewhere.

        Without this, QScrollArea.widgetResizable=True squashes the canvas
        to the viewport even when N=20. We set a min-height proportional
        to pane count so the scroll bar appears as soon as panes would
        otherwise become unreadable.
        """
        if not hasattr(self, 'canvas_scroll') or not hasattr(self, 'canvas'):
            return
        viewport_h = self.canvas_scroll.viewport().height()
        if self._current_view_mode == 'stacked' and n > 1:
            wanted = max(viewport_h, int(n * MIN_STACKED_PANE_HEIGHT_PX))
            self.canvas.setMinimumHeight(wanted)
        else:
            # Non-stacked modes fit the viewport — drop the floor.
            self.canvas.setMinimumHeight(0)

    def _sync_pane_groups_to_visible(self) -> None:
        """Reconcile self._pane_groups + heights with current visibility.

        Invariant: each group has exactly ONE trace index. Stacked view is
        always "one signal per pane" in v3.1+.

        - Invisible traces are dropped (their pane disappears).
        - Existing pane order is preserved.
        - Newly-visible traces (not already in any pane) join at the bottom
          with default height 1.0.
        """
        visible_set = {t.index for t in self.visible_traces}
        new_groups: List[List[int]] = []
        kept_heights: List[float] = []
        for orig_idx, group in enumerate(self._pane_groups):
            # Keep only the first surviving trace — enforces 1-per-pane
            # for any legacy config that had multi-trace groups.
            survivor = next((i for i in group if i in visible_set), None)
            if survivor is None:
                continue
            new_groups.append([survivor])
            visible_set.discard(survivor)
            if orig_idx < len(self._pane_heights):
                kept_heights.append(self._pane_heights[orig_idx])
            else:
                kept_heights.append(1.0)
        for idx in sorted(visible_set):
            new_groups.append([idx])
            kept_heights.append(1.0)
        self._pane_groups = new_groups
        self._pane_heights = kept_heights

    def _pane_anchor_name(self, ax) -> Optional[str]:
        """Return the name of the first visible trace plotted on ax, or None.

        Used as the lookup key for per-pane ylim preservation across
        refresh_plot. Walks self.traces in insertion order so anchors stay
        stable even if Y autoscaling slightly changes line ordering.
        """
        for t in self.traces.values():
            if t.visible and t.line_object is not None and t.line_object.axes is ax:
                return t.name
        return None

    def _build_pane_anchor_map(self) -> Dict[int, str]:
        """Return {id(ax): anchor_name} covering all current panes, in O(traces).

        Callers that loop over all panes should build this once and do O(1)
        dict lookups per pane, rather than calling _pane_anchor_name() per pane
        which is O(traces) each and makes capture/restore O(N²) in stacked view.
        """
        result: Dict[int, str] = {}
        for t in self.traces.values():
            lo = t.line_object
            if t.visible and lo is not None:
                ax_id = id(lo.axes)
                if ax_id not in result:
                    result[ax_id] = t.name
        return result

    def _capture_view_state(self) -> None:
        """Snapshot xlim and per-pane ylim before a refresh that rebuilds axes."""
        if not self.panes:
            return
        self._saved_xlim = self.axes.get_xlim()
        self._saved_pane_ylims = {}
        anchor_map = self._build_pane_anchor_map()
        for ax in self.panes:
            anchor = anchor_map.get(id(ax))
            if anchor is not None:
                self._saved_pane_ylims[anchor] = ax.get_ylim()

    def _restore_view_state(self) -> None:
        """Re-apply preserved xlim + per-pane ylim after refresh rebuilds axes.

        Two restore paths, evaluated in order so locks always win:

        1. **Locked panes** — any pane whose anchor is in self._pane_lock_y
           and has a stored ylim in self._locked_ylims gets that ylim
           re-applied. Survives every refresh until the lock is cleared.

        2. **One-shot preserve-zoom** — entries in self._saved_pane_ylims
           (set by _capture_view_state when autoscale is off in a mode-
           preserving refresh) are applied to whatever pane currently
           anchors that trace, then the dict is cleared.

        Calling this with both buckets empty is a no-op, so refresh_plot
        can call it unconditionally.
        """
        if not self.panes:
            return
        anchor_map = self._build_pane_anchor_map()
        # Apply persistent locks first
        for ax in self.panes:
            anchor = anchor_map.get(id(ax))
            if anchor is None:
                continue
            if self._pane_lock_y.get(anchor) and anchor in self._locked_ylims:
                ax.set_ylim(self._locked_ylims[anchor])
        # Then one-shot preserve-zoom — skip panes already pinned by a lock
        if self._saved_xlim is not None:
            self.axes.set_xlim(self._saved_xlim)
        for ax in self.panes:
            anchor = anchor_map.get(id(ax))
            if anchor is None or self._pane_lock_y.get(anchor):
                continue
            if anchor in self._saved_pane_ylims:
                ax.set_ylim(self._saved_pane_ylims[anchor])
        self._saved_xlim = None
        self._saved_pane_ylims = {}

    def _snapshot_pane_for_lock(self, anchor: str) -> None:
        """Capture the current ylim of the pane that anchors `anchor`.

        Used by the (forthcoming) menu's Lock-Y toggle to seed
        self._locked_ylims; without this seed the lock would have nothing
        to restore on the first refresh after locking.
        """
        if not anchor or not self.panes:
            return
        anchor_map = self._build_pane_anchor_map()
        for ax in self.panes:
            if anchor_map.get(id(ax)) == anchor:
                self._locked_ylims[anchor] = ax.get_ylim()
                return

    def _clear_pane_lock(self, anchor: str) -> None:
        """Remove a pane lock so the next refresh autoscales freely."""
        self._pane_lock_y.pop(anchor, None)
        self._locked_ylims.pop(anchor, None)

    # ── Pane divider resize (mouse drag between panes) ───────────────────

    def _divider_under_mouse(self, event) -> Optional[int]:
        """Return upper-pane index when the mouse is near a divider gap.

        Only meaningful in stacked mode with N>=2 panes. Returns the index
        of the pane ABOVE the divider — i.e. the pane whose height changes
        in tandem with the one below during a drag.
        """
        if (self._current_view_mode != 'stacked'
                or len(self.panes) < 2
                or event.y is None):
            return None
        # Only consider the dividers between group panes; func panes are
        # not part of _pane_heights, so don't expose their boundaries.
        upper_count = min(len(self._pane_groups), len(self.panes)) - 1
        for i in range(upper_count):
            bottom = self.panes[i].bbox.y0     # bottom edge of upper pane
            top = self.panes[i + 1].bbox.y1    # top edge of lower pane
            mid = (bottom + top) / 2.0
            if abs(event.y - mid) <= DIVIDER_HIT_TOLERANCE_PX:
                return i
        return None

    def _start_divider_drag(self, upper_idx: int, event) -> None:
        """Capture initial heights + cached pixel geometry for the drag."""
        if upper_idx + 1 >= len(self._pane_heights):
            return
        upper_bb = self.panes[upper_idx].bbox.height
        lower_bb = self.panes[upper_idx + 1].bbox.height
        self._divider_drag = {
            'upper_idx': upper_idx,
            'start_y': event.y,
            'start_height_upper': self._pane_heights[upper_idx],
            'start_height_lower': self._pane_heights[upper_idx + 1],
            'combined_px': max(1.0, upper_bb + lower_bb),
            'moved': False,
        }
        # Capture axis positions in figure coords BEFORE disabling the
        # constrained_layout solver. During drag we reposition axes via
        # ax.set_position() so the solver never runs per mouse-move.
        self._drag_ax_positions = [ax.get_position() for ax in self.panes]
        self.fig.set_layout_engine('none')
        # Decimate line data so each draw_idle renders far fewer segments.
        # Full data is restored in _finish_divider_drag (or by refresh_plot).
        _MAX_DRAG_PTS = 800
        self._saved_line_data: Dict[int, Any] = {}
        for t in self.traces.values():
            if t.line_object is not None:
                xd = t.line_object.get_xdata()
                yd = t.line_object.get_ydata()
                n = len(xd)
                if n > _MAX_DRAG_PTS:
                    step = max(1, n // _MAX_DRAG_PTS)
                    self._saved_line_data[t.index] = (xd, yd)
                    t.line_object.set_data(xd[::step], yd[::step])
        self.canvas.setCursor(Qt.CursorShape.SizeVerCursor)

    def _update_divider_drag(self, event) -> None:
        """Live-redistribute height ratios via in-place gridspec mutation.

        Critically, this does NOT call refresh_plot — a full rebuild on
        every mouse-motion event tanks performance (~50ms × 30Hz = jank).
        Instead it mutates the GridSpec height_ratios on the live axes
        and asks for a deferred redraw. On release, _finish_divider_drag
        does one full refresh to let constrained_layout fully settle.
        """
        d = self._divider_drag
        if d is None or event.y is None:
            return
        i = d['upper_idx']
        # See _start_divider_drag for sign convention. Positive delta_px
        # = cursor moved down = upper pane grows.
        delta_px = d['start_y'] - event.y
        sum_h = d['start_height_upper'] + d['start_height_lower']
        frac = delta_px / d['combined_px']
        new_upper = max(0.1, min(sum_h - 0.1,
                                 d['start_height_upper'] + frac * sum_h))
        new_lower = sum_h - new_upper
        self._pane_heights[i] = new_upper
        self._pane_heights[i + 1] = new_lower
        d['moved'] = True
        self._apply_height_ratios_live()

    def _apply_height_ratios_live(self) -> None:
        """Reposition panes during drag without running the constraint solver."""
        if not self.panes or len(self.panes) < 2:
            return
        self._reposition_panes_from_heights()
        self.canvas.draw_idle()

    def _reposition_panes_from_heights(self) -> None:
        """Distribute pane Bboxes in figure coords from _pane_heights ratios.

        Uses positions captured at drag-start as the outer envelope so the
        figure margins stay exactly as constrained_layout left them. Only
        vertical redistribution changes; horizontal extents are preserved
        per-pane (important when Y-axis labels have different widths).
        """
        positions = getattr(self, '_drag_ax_positions', None)
        if not positions or len(positions) != len(self.panes):
            return
        n = len(self.panes)
        n_heights = min(n, len(self._pane_heights))

        top    = positions[0].y1
        bottom = positions[-1].y0
        # Average gap between adjacent panes (hspace in figure coords)
        if n > 1:
            total_gap = sum(
                max(0.0, positions[i].y0 - positions[i + 1].y1)
                for i in range(n - 1)
            )
            avg_gap = total_gap / (n - 1)
        else:
            avg_gap = 0.0

        usable = max(0.01, (top - bottom) - avg_gap * (n - 1))
        ratios  = [self._pane_heights[i] if i < n_heights else 1.0 for i in range(n)]
        ratio_sum = max(0.01, sum(ratios))

        current_top = top
        for i, ax in enumerate(self.panes):
            h = max(0.005, usable * (ratios[i] / ratio_sum))
            ax.set_position([
                positions[i].x0,
                current_top - h,
                positions[i].x1 - positions[i].x0,
                h,
            ])
            current_top -= h + avg_gap

    def _finish_divider_drag(self) -> None:
        """End drag: restore CL + data, settle layout with one full refresh."""
        if self._divider_drag is None:
            return
        moved = self._divider_drag.get('moved', False)
        self._divider_drag = None
        self._drag_ax_positions = []
        # Restore full line data.  If moved=True, refresh_plot rebuilds
        # everything via fig.clear() anyway; still restore so the
        # no-move path (moved=False) shows correct data after cleanup.
        saved = getattr(self, '_saved_line_data', {})
        for idx, (xd, yd) in saved.items():
            if idx in self.traces and self.traces[idx].line_object is not None:
                self.traces[idx].line_object.set_data(xd, yd)
        self._saved_line_data = {}
        self.fig.set_layout_engine('constrained')
        self.canvas.unsetCursor()
        if moved:
            # Heights changed; pane geometry must be rebuilt + CL re-settled.
            self._force_full_refresh = True
            self.refresh_plot()
        else:
            self.canvas.draw_idle()

    # ── Pane reorder (Alt + left-drag) ───────────────────────────────────

    def _start_pane_drag(self, pane_idx: int) -> None:
        self._pane_drag = {'from_idx': pane_idx}
        self.canvas.setCursor(Qt.CursorShape.ClosedHandCursor)

    def _finish_pane_drag(self, event) -> None:
        d = self._pane_drag
        if d is None:
            return
        self._pane_drag = None
        self.canvas.unsetCursor()
        from_idx = d['from_idx']
        # Determine target pane from release position
        to_idx = None
        if event.inaxes is not None:
            to_idx = self._pane_index_of(event.inaxes)
        if to_idx is None or to_idx == from_idx:
            return
        if not (0 <= from_idx < len(self._pane_groups)
                and 0 <= to_idx < len(self._pane_groups)):
            return
        # Move the group; also move its height entry alongside so the user's
        # custom sizing follows the pane.
        grp = self._pane_groups.pop(from_idx)
        self._pane_groups.insert(to_idx, grp)
        if from_idx < len(self._pane_heights):
            h = self._pane_heights.pop(from_idx)
            if to_idx < len(self._pane_heights):
                self._pane_heights.insert(to_idx, h)
            else:
                self._pane_heights.append(h)
        # Reorder keeps the visible set (signature) the same — force the rebuild.
        self._force_full_refresh = True
        self.refresh_plot()

    def _apply_persisted_layout(self) -> None:
        """Hydrate name-keyed config entries into index-keyed live state.

        Runs once after populate_waveform_list has built self.traces.
        Stale names (signals not present in this simulation) are silently
        dropped — keeps the config forward-compatible across schematic
        edits. Function-trace panes are NOT persisted because their
        underlying expressions may reference signals that no longer exist.
        """
        name_to_idx = {t.name: t.index for t in self.traces.values()}

        groups_named = self.config.get('stacked_pane_groups')
        if isinstance(groups_named, list):
            resolved: List[List[int]] = []
            for group in groups_named:
                if not isinstance(group, list):
                    continue
                indices = [name_to_idx[n] for n in group if n in name_to_idx]
                if indices:
                    resolved.append(indices)
            if resolved:
                self._pane_groups = resolved

        lock = self.config.get('stacked_lock_y')
        if isinstance(lock, dict):
            self._pane_lock_y = {n: bool(v) for n, v in lock.items()
                                 if n in name_to_idx}

        ylims = self.config.get('stacked_locked_ylims')
        if isinstance(ylims, dict):
            for n, lims in ylims.items():
                if (n in name_to_idx and isinstance(lims, (list, tuple))
                        and len(lims) == 2):
                    self._locked_ylims[n] = (float(lims[0]), float(lims[1]))

        stats = self.config.get('stacked_stats_visible')
        if isinstance(stats, bool):
            self.stats_check.setChecked(stats)

        # Pane heights — name-keyed in config, projected back onto the
        # restored _pane_groups order. Missing anchors fall back to 1.0
        # which is the default equal-height ratio.
        heights_named = self.config.get('stacked_pane_heights')
        if isinstance(heights_named, dict) and self._pane_groups:
            resolved_heights: List[float] = []
            for g in self._pane_groups:
                if not g or g[0] not in self.traces:
                    resolved_heights.append(1.0)
                    continue
                anchor = self.traces[g[0]].name
                try:
                    resolved_heights.append(
                        max(0.1, float(heights_named.get(anchor, 1.0))))
                except (TypeError, ValueError):
                    resolved_heights.append(1.0)
            self._pane_heights = resolved_heights

    # ── Stacked-view pane context menu ────────────────────────────────────

    def _pane_index_of(self, ax) -> Optional[int]:
        """Return the index into self._pane_groups for the given Axes."""
        for i, pane in enumerate(self.panes):
            if pane is ax:
                # _pane_groups may include synthetic function panes appended
                # to the bottom; only the first len(_pane_groups) panes are
                # real-trace panes.
                if i < len(self._pane_groups):
                    return i
        return None

    def _func_pane_index_of(self, ax) -> Optional[int]:
        """Return the index into self._func_traces for a function pane."""
        n_groups = len(self._pane_groups)
        for i, pane in enumerate(self.panes):
            if pane is ax and n_groups <= i < n_groups + len(self._func_traces):
                return i - n_groups
        return None

    def _show_pane_context_menu(self, event) -> None:
        """Right-click menu for a stacked-view pane. Each pane holds exactly
        one signal — multi-signal grouping was removed in v3.1 because the
        "graph in a graph" feel was more confusing than useful. Pane order
        and sizing are still user-controlled via Move Up/Down / Alt-drag /
        divider drag; lock-Y, stats, and the function-pane workflow stay.
        """
        # Function pane? Show the slim function-pane menu and exit.
        f_idx = self._func_pane_index_of(event.inaxes)
        if f_idx is not None:
            self._show_function_pane_menu(event, f_idx)
            return

        pane_idx = self._pane_index_of(event.inaxes)
        if pane_idx is None:
            return
        group = self._pane_groups[pane_idx]
        anchor = (self.traces[group[0]].name
                  if group and group[0] in self.traces else None)
        menu = QMenu(self)

        # Cursor placement — top of menu so it's always reachable. lambda
        # accepts the leading 'checked' bool QAction.triggered always emits
        # (forgetting it sinks click_x and lands the cursor at x=0).
        click_x = event.xdata
        if click_x is not None:
            c1 = menu.addAction("Set Cursor 1 here")
            c1.triggered.connect(
                lambda checked=False, x=click_x: self.set_cursor(0, x))
            c2 = menu.addAction("Set Cursor 2 here")
            c2.triggered.connect(
                lambda checked=False, x=click_x: self.set_cursor(1, x))
            menu.addSeparator()

        up_act = menu.addAction("Move pane up")
        up_act.setEnabled(pane_idx > 0)
        up_act.triggered.connect(
            lambda checked=False, p=pane_idx: self._move_pane(p, -1))
        down_act = menu.addAction("Move pane down")
        down_act.setEnabled(pane_idx < len(self._pane_groups) - 1)
        down_act.triggered.connect(
            lambda checked=False, p=pane_idx: self._move_pane(p, +1))

        menu.addSeparator()

        if anchor:
            lock_act = menu.addAction("Lock Y")
            lock_act.setCheckable(True)
            lock_act.setChecked(self._pane_lock_y.get(anchor, False))
            lock_act.triggered.connect(
                lambda checked=False, a=anchor: self._toggle_pane_lock(a))
            reset_act = menu.addAction("Reset Y autoscale")
            reset_act.triggered.connect(
                lambda checked=False, a=anchor: self._reset_pane_y(a))

        menu.addSeparator()

        hide_act = menu.addAction("Hide this signal")
        hide_act.triggered.connect(
            lambda checked=False, p=pane_idx: self._hide_pane_signal(p))

        menu.addSeparator()

        func_act = menu.addAction("Plot function in new pane...")
        func_act.triggered.connect(self._dialog_plot_function)
        clear_func = menu.addAction("Clear function panes")
        clear_func.setEnabled(bool(self._func_traces))
        clear_func.triggered.connect(self._clear_function_panes)

        # Position menu where the click happened. event.guiEvent is a
        # QMouseEvent on Qt backends; fall back to canvas centre if missing.
        if hasattr(event, 'guiEvent') and event.guiEvent is not None:
            menu.exec(event.guiEvent.globalPosition().toPoint())
        else:
            menu.exec(self.canvas.mapToGlobal(QtCore.QPoint(0, 0)))

    def _hide_pane_signal(self, pane_idx: int) -> None:
        """Hide the trace owning this pane (≡ unticking it in the waveform list)."""
        if not (0 <= pane_idx < len(self._pane_groups)):
            return
        grp = self._pane_groups[pane_idx]
        if not grp:
            return
        trace_idx = grp[0]
        if trace_idx in self.traces:
            self.traces[trace_idx].visible = False
            for i in range(self.waveform_list.count()):
                item = self.waveform_list.item(i)
                if item and item.data(Qt.ItemDataRole.UserRole) == trace_idx:
                    self.update_list_item_appearance(item, trace_idx)
                    break
            self._schedule_refresh()

    # ── Pane menu action handlers ────────────────────────────────────────

    def _ensure_heights_match_groups(self) -> None:
        """Pad/truncate self._pane_heights so it parallels self._pane_groups.

        Sync-helpers and the move/reorder paths call this whenever the pane
        count changes. Missing entries default to 1.0 (equal); surplus are
        dropped from the tail.
        """
        n = len(self._pane_groups)
        if len(self._pane_heights) < n:
            self._pane_heights.extend([1.0] * (n - len(self._pane_heights)))
        elif len(self._pane_heights) > n:
            self._pane_heights = self._pane_heights[:n]

    def _move_pane(self, pane_idx: int, direction: int) -> None:
        new_idx = pane_idx + direction
        if 0 <= new_idx < len(self._pane_groups):
            self._pane_groups[pane_idx], self._pane_groups[new_idx] = (
                self._pane_groups[new_idx], self._pane_groups[pane_idx])
            # Heights move with the pane so the user's custom sizing follows.
            if (pane_idx < len(self._pane_heights)
                    and new_idx < len(self._pane_heights)):
                self._pane_heights[pane_idx], self._pane_heights[new_idx] = (
                    self._pane_heights[new_idx], self._pane_heights[pane_idx])
            self._ensure_heights_match_groups()
            # Pane reorder leaves the visible set (and thus the signature)
            # unchanged, so force the rebuild that re-lays-out the panes.
            self._force_full_refresh = True
            self.refresh_plot()

    def _toggle_pane_lock(self, anchor: str) -> None:
        if self._pane_lock_y.get(anchor):
            self._clear_pane_lock(anchor)
        else:
            self._snapshot_pane_for_lock(anchor)
            self._pane_lock_y[anchor] = True
        # Lock/unlock changes ylim handling, which the fast path skips —
        # force the full rebuild so _restore_view_state runs.
        self._force_full_refresh = True
        self.refresh_plot()

    def _reset_pane_y(self, anchor: str) -> None:
        self._clear_pane_lock(anchor)
        # Drop one-shot snapshot too so the upcoming refresh gets a fresh fit
        self._saved_pane_ylims.pop(anchor, None)
        # Need a real re-autoscale of this pane, which only the full path does.
        self._force_full_refresh = True
        self.refresh_plot()

