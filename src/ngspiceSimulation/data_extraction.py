# ngspiceSimulation/data_extraction.py
"""
Data extraction module for NGSpice simulation results.

Parses plot_data_v.txt and plot_data_i.txt produced by ngspice.

Transient / DC format:
  * /path/to/circuit.cir          <- marks start of each column group
  Transient Analysis  date        <- analysis type line
  ----...                         <- separator
  Index   time   node1   node2    <- header (parts[1]=x-axis, parts[2:]=node names)
  ----...
  0\tt0\tv1\tv2\t                 <- data rows (tab-separated, trailing \t)
  ...
  54\tt54\tv1\tv2\t
                                  <- blank line
  Index   time   node1   node2    <- page-break header (every ~55 rows, same group)
  ----...
  55\tt55\tv1\tv2\t
  ...
  * /path/to/circuit.cir          <- new column group (circuit with many nodes)
  Transient Analysis  date
  Index   time   node3   node4
  0\tt0\tv3\tv4\t                 <- same time axis, new node values

AC format (differs from Transient/DC):
  Each node value is split into TWO tab columns per row:
    real_part,\timaginary_part
  The real_part has a trailing comma (ngspice artifact).
  Example: 0\t1.0e+03\t9.96e+00,\t-4.50e+00\t
  Only the real part is stored; the imaginary part is discarded,
  matching the original implementation behaviour.
"""

import os
import logging
import numpy as np
from typing import List, Tuple, Optional
from PyQt6 import QtWidgets
from configuration.Appconfig import Appconfig

logger = logging.getLogger(__name__)


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

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _parse_plot_file(
        self, filepath: str, is_ac: bool = False
    ) -> Tuple[np.ndarray, str, List[str], List[np.ndarray]]:
        """
        Parse one ngspice plot file.

        Returns (x_array, x_name, names, arrays) where names and arrays are
        parallel lists — one entry per output column in file order.

        Duplicate column names (ngspice truncates long node names so two
        distinct nodes can share the same string) are preserved as separate
        entries; each gets its own data list keyed by position, not by name.

        is_ac=True: each node occupies 2 tab columns ("real,  imag"); only
        the real part is kept (comma stripped), imaginary discarded.

        Line dispatch:
        - starts with digit      -> data row (fast path)
        - stripped starts with * -> new column group incoming
        - stripped starts with - -> separator, skip
        - stripped starts 'Index'-> column header (new group or page-break)
        - everything else        -> analysis-type banner, skip
        """
        x_list: List[float] = []
        all_names: List[str] = []           # output channel names (duplicates kept)
        all_data: List[List[float]] = []    # parallel data lists, one per channel

        x_name: str = 'time'
        # Indices into all_data for the columns of the current group.
        # On a page-break (same group, same header) we reuse the same indices.
        current_indices: Optional[List[int]] = None
        new_group_incoming: bool = False
        collecting_x: bool = True
        cols_per_node: int = 2 if is_ac else 1

        try:
            with open(filepath, 'r') as f:
                for line in f:
                    # ---- Fast path: data rows always start with a digit ----
                    if line and line[0].isdigit():
                        if current_indices is None:
                            continue
                        parts = line.split('\t')
                        if len(parts) < 2 + cols_per_node * len(current_indices):
                            continue
                        try:
                            x_val = float(parts[1])
                            if collecting_x:
                                x_list.append(x_val)
                            for i, idx in enumerate(current_indices):
                                if is_ac:
                                    raw = parts[2 + 2 * i].rstrip(',')
                                else:
                                    raw = parts[2 + i]
                                all_data[idx].append(float(raw))
                        except (ValueError, IndexError):
                            continue
                        continue

                    # ---- Non-data lines ----
                    stripped = line.strip()
                    if not stripped:
                        continue

                    if stripped[0] == '*':
                        new_group_incoming = True
                        if current_indices is not None:
                            collecting_x = False
                        continue

                    if stripped[0] == '-':
                        continue

                    if stripped.startswith('Index'):
                        parts = stripped.split()
                        if new_group_incoming:
                            x_name = parts[1]
                            col_names = parts[2:]
                            current_indices = []
                            for name in col_names:
                                all_names.append(name)
                                all_data.append([])
                                current_indices.append(len(all_data) - 1)
                            new_group_incoming = False
                        # else: page-break — same group, same columns, same indices
                        continue

        except OSError as e:
            logger.error(f"Cannot open {filepath}: {e}")
            raise

        x_arr = np.array(x_list, dtype=np.float64)
        arrays = [np.array(d, dtype=np.float64) for d in all_data]

        logger.debug(
            f"Parsed {filepath}: {len(x_arr)} x-pts, "
            f"{len(arrays)} channels, x_name='{x_name}'"
        )
        return x_arr, x_name, all_names, arrays

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

    # ------------------------------------------------------------------
    # Public interface (matches what plot_window.py expects)
    # ------------------------------------------------------------------

    def openFile(self, file_path: str) -> List[int]:
        """
        Open and process both simulation data files.

        Returns:
            [analysis_type, dec_flag]
            where analysis_type is AC_ANALYSIS=0, TRANSIENT_ANALYSIS=1, DC_ANALYSIS=2
            and dec_flag=1 for log-scale AC sweep, 0 otherwise.

        Populates:
            self.x          - 1-D numpy array of x-axis values (time/freq/sweep)
            self.y          - list of 1-D numpy arrays, one per node/branch
            self.NBList     - list of all node+branch names (voltage first, then current)
            self.NBIList    - list of current branch names only
            self.volts_length - number of voltage nodes
        """
        try:
            v_path = os.path.join(file_path, "plot_data_v.txt")
            i_path = os.path.join(file_path, "plot_data_i.txt")

            # ---- Detect analysis type ----
            analysis_type, dec = self._detect_analysis_type(file_path)
            self.analysisType = analysis_type
            self.dec = dec
            is_ac = (analysis_type == self.AC_ANALYSIS)

            # ---- Parse voltage file ----
            x_arr, x_name, v_names, v_arrays = self._parse_plot_file(v_path, is_ac=is_ac)

            # ---- Parse current file (graceful if missing or empty) ----
            i_names: List[str] = []
            i_arrays: List[np.ndarray] = []
            try:
                _, _, i_names, i_arrays = self._parse_plot_file(i_path, is_ac=is_ac)
            except OSError:
                logger.warning(f"Current file not found or unreadable: {i_path}")
            except Exception as e:
                logger.warning(f"Could not parse current file: {e}")

            # ---- Populate public attributes ----
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
        # plot_window.py calls: openFile() -> computeAxes() -> numVals()
        # In the old implementation computeAxes() built self.x and self.y
        # from self.data. Now openFile() does it all directly.
        pass

    def numVals(self) -> List[int]:
        """
        Return [total_node_count, voltage_node_count].

        plot_window.py only uses index [1] (volts_length).
        """
        return [len(self.y), self.volts_length]
