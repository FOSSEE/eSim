"""
Data extraction module for NGSpice simulation results.

Parses plot_data_v.txt and plot_data_i.txt produced by ngspice.

Transient / DC format (two variants):

  Variant A — older ngspice / multi-group files (has * markers):
  * /path/to/circuit.cir          <- marks start of each column group
  Transient Analysis  date        <- analysis type line
  ----...                         <- separator
  Index   time   node1   node2    <- header (parts[1]=x-axis, parts[2:]=node names)
  ----...
  0\tt0\tv1\tv2\t                 <- data rows (tab-separated, trailing \t)
  ...
  * /path/to/circuit.cir          <- new column group (additional nodes, same x axis)
  Transient Analysis  date
  Index   time   node3   node4
  0\tt0\tv3\tv4\t

  Variant B — newer ngspice files (no * markers), one or more column groups:
  <title text>                    <- any non-Index, non-dash text, skipped
  Transient Analysis  date
  ----...
  Index   time   node1   node2    <- first Index treated as new group directly
  ----...
  0\tt0\tv1\tv2\t
  ...
  Index   time   node3   node4    <- DIFFERENT column names = new group, same x axis
  ----...
  0\tt0\tv3\tv4\t

  Page-break header (both variants, every ~55 rows within same group):
  Index   time   node1   node2    <- SAME column names = page-break, ignored

AC format (differs from Transient/DC):
  Each node value is split into TWO tab columns per row:
    real_part,\timaginary_part
  The real_part has a trailing comma (ngspice artifact).
  Example: 0\t1.0e+03\t9.96e+00,\t-4.50e+00\t
  Only the real part is stored; the imaginary part is discarded,
  matching the original implementation behaviour.

Performance note (vectorized rewrite):
  The structural scan (group/page-break detection) stays a cheap per-line
  branch walk that never converts a number.  All numeric conversion is
  deferred and done ONCE PER COLUMN GROUP with a single numpy reader
  (np.loadtxt over the group's data rows), instead of the previous
  per-cell float() + list.append() loop.  For large transient files
  (1e5-1e6 rows x N nodes) this turns millions of interpreted float()
  calls into a handful of C-level parses.
"""

import io
import os
import logging
import numpy as np
from typing import List, Tuple, Optional
from PyQt6 import QtWidgets
from configuration.Appconfig import Appconfig

logger = logging.getLogger(__name__)


def _block_to_array(rows: List[str], usecols: Tuple[int, ...],
                    is_ac: bool) -> np.ndarray:
    """Convert a group's raw data-row strings to a 2-D float64 array.

    `rows` are verbatim file lines (each still ending in '\\n') that start
    with a digit.  `usecols` selects the x column and the wanted node
    columns (real parts only, for AC).  Returns shape (n_rows, len(usecols)).

    Fast path: one np.loadtxt over the joined block.  The trailing tab on
    every ngspice row produces an extra empty field that `usecols` simply
    never selects, so it needs no special handling.

    Defensive path: if a row is malformed (too few fields), loadtxt raises;
    we then drop the ragged rows — mirroring the original parser, which
    skipped any row shorter than the expected width — and retry.  Clean
    files (the overwhelming common case) never hit this branch.
    """
    if not rows:
        return np.empty((0, len(usecols)), dtype=np.float64)

    text = "".join(rows)
    if is_ac:
        # Drop the real-part trailing comma so every field is a bare float.
        text = text.replace(",", "")
    try:
        return np.loadtxt(io.StringIO(text), delimiter="\t",
                          usecols=usecols, ndmin=2, comments=None)
    except Exception:
        max_field = usecols[-1]  # usecols is ascending
        good = [ln for ln in rows if ln.count("\t") >= max_field]
        if not good:
            return np.empty((0, len(usecols)), dtype=np.float64)
        text = "".join(good)
        if is_ac:
            text = text.replace(",", "")
        return np.loadtxt(io.StringIO(text), delimiter="\t",
                          usecols=usecols, ndmin=2, comments=None)


class DataExtraction:
    """Extracts simulation data from NGSpice output files."""

    AC_ANALYSIS = 0
    TRANSIENT_ANALYSIS = 1
    DC_ANALYSIS = 2

    def __init__(self) -> None:
        self.obj_appconfig = Appconfig()
        self.x: np.ndarray = np.array([], dtype=np.float64)
        self.y: List[np.ndarray] = []
        self.NBList: List[str] = []
        self.NBIList: List[str] = []
        self.volts_length: int = 0
        self.data: List[str] = []       # kept for backward compat
        self.analysisType: int = self.TRANSIENT_ANALYSIS
        self.dec: int = 0

    def _parse_plot_file(
        self, filepath: str, is_ac: bool = False
    ) -> Tuple[np.ndarray, str, List[str], List[np.ndarray]]:
        """
        Parse one ngspice plot file (vectorized).

        Returns (x_array, x_name, names, arrays) where names and arrays are
        parallel lists — one entry per output column in file order.

        Duplicate column names (ngspice truncates long node names so two
        distinct nodes can share the same string) are preserved as separate
        entries; each gets its own data array keyed by position, not by name.

        is_ac=True: each node occupies 2 tab columns ("real,  imag"); only
        the real part is kept (comma stripped), imaginary discarded.

        Pass 1 (this method): a cheap per-line scan classifies lines and
        buckets the raw data-row strings into column groups, exactly like the
        original state machine — but it never parses a number here:
        - starts with digit      -> data row (appended verbatim to current group)
        - stripped starts with * -> new column group incoming
        - stripped starts with - -> separator, skip
        - stripped starts 'Index'-> column header (new group or page-break)
        - everything else        -> analysis-type banner, skip

        Pass 2 (_block_to_array): each group's rows are bulk-parsed with one
        numpy reader.  The x axis is taken from the first group only (all
        groups share the same time/frequency axis, as ngspice emits them).
        """
        cols_per_node = 2 if is_ac else 1
        x_name = 'time'
        all_names: List[str] = []          # output channel names (duplicates kept)
        groups: List[dict] = []            # each: {'indices': [...], 'rows': [str]}

        # Indices into all_names for the columns of the current group.
        current: Optional[dict] = None
        new_group_incoming: bool = True
        collecting_x: bool = True          # True only for the first group

        def _open_group(col_names: List[str]) -> dict:
            indices: List[int] = []
            for nm in col_names:
                all_names.append(nm)
                indices.append(len(all_names) - 1)
            g = {'indices': indices, 'rows': [], 'collect_x': collecting_x}
            groups.append(g)
            return g

        try:
            with open(filepath, 'r') as f:
                for line in f:
                    if line and line[0].isdigit():
                        if current is not None:
                            current['rows'].append(line)
                        continue

                    stripped = line.strip()
                    if not stripped:
                        continue

                    first = stripped[0]
                    if first == '*':
                        new_group_incoming = True
                        if current is not None:
                            collecting_x = False
                        continue

                    if first == '-':
                        continue

                    if stripped.startswith('Index'):
                        parts = stripped.split()
                        col_names = parts[2:]
                        if new_group_incoming:
                            x_name = parts[1]
                            current = _open_group(col_names)
                            new_group_incoming = False
                        elif (current is not None
                              and col_names != [all_names[i]
                                                for i in current['indices']]):
                            # New column group without a * marker (newer ngspice
                            # format). Distinct column names signal a new signal
                            # group, not a page-break. Time axis is shared ->
                            # stop collecting x.
                            collecting_x = False
                            current = _open_group(col_names)
                        # else: page-break — same group, same columns, reuse it
                        continue

        except OSError as e:
            logger.error(f"Cannot open {filepath}: {e}")
            raise

        n_channels = len(all_names)
        arrays: List[Optional[np.ndarray]] = [None] * n_channels
        x_arr = np.array([], dtype=np.float64)

        for g in groups:
            indices = g['indices']
            n_nodes = len(indices)
            if n_nodes == 0:
                continue
            if not g['rows']:
                for ch_idx in indices:
                    arrays[ch_idx] = np.array([], dtype=np.float64)
                continue

            if is_ac:
                node_cols = tuple(range(2, 2 + 2 * n_nodes, 2))   # reals only
            else:
                node_cols = tuple(range(2, 2 + n_nodes))
            usecols = (1,) + node_cols

            block = _block_to_array(g['rows'], usecols, is_ac)
            # block columns: [x, node0, node1, ...]
            if g['collect_x'] and x_arr.size == 0 and block.shape[0] > 0:
                x_arr = np.ascontiguousarray(block[:, 0], dtype=np.float64)
            for k, ch_idx in enumerate(indices):
                arrays[ch_idx] = np.ascontiguousarray(
                    block[:, 1 + k], dtype=np.float64)

        out_arrays = [a if a is not None else np.array([], dtype=np.float64)
                      for a in arrays]

        logger.debug(
            f"Parsed {filepath}: {len(x_arr)} x-pts, "
            f"{len(out_arrays)} channels, x_name='{x_name}'"
        )
        return x_arr, x_name, all_names, out_arrays

    def _detect_analysis_type(self, file_path: str) -> Tuple[int, int]:
        """
        Read the 'analysis' file and return (analysis_type, dec_flag).

        dec_flag=1 means AC analysis uses decade (log) frequency sweep.
        """
        analysis_file = os.path.join(file_path, "analysis")
        with open(analysis_file, 'r') as f:
            content = f.read().strip()

        tokens = content.split()
        dec = 0

        if not tokens:
            logger.warning("analysis file is empty, defaulting to Transient")
            return self.TRANSIENT_ANALYSIS, 0

        first = tokens[0].lower()

        if first.endswith('.ac'):
            if 'dec' in tokens:
                dec = 1
            return self.AC_ANALYSIS, dec

        if '.tran' in tokens:
            return self.TRANSIENT_ANALYSIS, dec

        return self.DC_ANALYSIS, dec

    def openFile(self, file_path: str) -> List[int]:
        """
        Open and process both simulation data files.

        Returns:
            [analysis_type, dec_flag]
            where analysis_type is AC_ANALYSIS=0, TRANSIENT_ANALYSIS=1, DC_ANALYSIS=2
            and dec_flag=1 for log-scale AC sweep, 0 otherwise.
        """
        try:
            v_path = os.path.join(file_path, "plot_data_v.txt")
            i_path = os.path.join(file_path, "plot_data_i.txt")

            analysis_type, dec = self._detect_analysis_type(file_path)
            self.analysisType = analysis_type
            self.dec = dec
            is_ac = (analysis_type == self.AC_ANALYSIS)

            x_arr, x_name, v_names, v_arrays = self._parse_plot_file(v_path, is_ac=is_ac)

            i_names: List[str] = []
            i_arrays: List[np.ndarray] = []
            try:
                _, _, i_names, i_arrays = self._parse_plot_file(i_path, is_ac=is_ac)
            except OSError:
                logger.warning(f"Current file not found or unreadable: {i_path}")
            except Exception as e:
                logger.warning(f"Could not parse current file: {e}")

            self.x = x_arr
            self.volts_length = len(v_names)
            self.NBIList = i_names
            self.NBList = v_names + i_names
            self.y = v_arrays + i_arrays

            # self.data kept as non-empty so numVals() won't crash on old
            # callers that still reach for data[0] - we give it one dummy row
            # with the right column count so numVals()[0] is correct.
            dummy_cols = '\t'.join(['0.0'] * len(self.NBList))
            self.data = [dummy_cols]

            _analysis_name = {
                self.AC_ANALYSIS: 'AC',
                self.TRANSIENT_ANALYSIS: 'Tran',
                self.DC_ANALYSIS: 'DC',
            }.get(analysis_type, '?')
            logger.info(
                f"openFile done | analysis={_analysis_name} "
                f"| {len(v_names)} V-nodes, {len(i_names)} I-branches "
                f"| {len(x_arr)} data points"
            )
            logger.info(f"NBList: {self.NBList}")

            return [analysis_type, dec]

        except Exception as e:
            logger.error(f"openFile failed: {e}", exc_info=True)
            self.obj_appconfig.print_error(f'DataExtraction error: {e}')
            try:
                msg = QtWidgets.QErrorMessage()
                msg.setModal(True)
                msg.setWindowTitle("Error Message")
                msg.showMessage(f'Unable to open plot data files:\n{e}')
                msg.exec()
            except Exception:
                pass
            return [self.TRANSIENT_ANALYSIS, 0]

    def computeAxes(self) -> None:
        """
        No-op: x and y are already numpy arrays populated by openFile().
        Kept for backward compatibility with plot_window.py call sequence.
        """
        pass

    def numVals(self) -> List[int]:
        """
        Return [total_node_count, voltage_node_count].

        plot_window.py only uses index [1] (volts_length).
        """
        return [len(self.y), self.volts_length]
