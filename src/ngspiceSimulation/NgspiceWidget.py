import os
import shlex
import logging
from typing import List, Optional
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from configuration.Appconfig import Appconfig
from frontEnd import TerminalUi
from configparser import ConfigParser

logger = logging.getLogger(__name__)


class NgspiceWidget(QtWidgets.QWidget):
    """Runs an NGSpice simulation and displays output in a terminal widget."""

    ERROR_FAILED_TO_START = 0
    ERROR_CRASHED = 1
    ERROR_TIMED_OUT = 2

    SUCCESS_FORMAT = ('<span style="color:#00ff00; font-size:26px;">'
                     '{}'
                     '</span>')
    FAILURE_FORMAT = ('<span style="color:#ff3333; font-size:26px;">'
                     '{}'
                     '</span>')

    def __init__(self, netlist: str, sim_end_signal: pyqtSignal, plotFlag: Optional[bool] = None) -> None:
        super().__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                          QtWidgets.QSizePolicy.Policy.Expanding)
        self.setMinimumSize(300, 200)

        self.obj_appconfig = Appconfig()
        self.project_dir = self.obj_appconfig.current_project["ProjectName"]
        self.netlist_path = netlist
        self.sim_end_signal = sim_end_signal
        self.plotFlag = plotFlag
        self.command = netlist
        logger.info(f"Value of plotFlag: {self.plotFlag}")

        self.ngspice_args = self._prepare_ngspice_arguments(netlist)
        logger.info(f"NGSpice arguments: {self.ngspice_args}")

        self.process = QtCore.QProcess(self)
        self.terminal_ui = TerminalUi.TerminalUi(self.process, self.ngspice_args)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.terminal_ui)

        self._configure_process()
        self._start_process()

        if self._is_linux():
            self._start_gaw_process(netlist)

    def _prepare_ngspice_arguments(self, netlist: str) -> List[str]:
        raw_file = netlist.replace(".cir.out", ".raw")
        return ['-b', '-r', raw_file, netlist]

    def _configure_process(self) -> None:
        self.process.setWorkingDirectory(self.project_dir)
        self.process.setProcessChannelMode(QtCore.QProcess.ProcessChannelMode.SeparateChannels)
        self.process.readyReadStandardOutput.connect(self._handle_stdout)
        self.process.readyReadStandardError.connect(self._handle_stderr)
        self.process.finished.connect(
            lambda exit_code, exit_status: self.finish_simulation(
                exit_code, exit_status, self.sim_end_signal, False
            )
        )
        self.process.errorOccurred.connect(
            lambda: self.finish_simulation(None, None, self.sim_end_signal, True)
        )

    def _register_process(self, process: QtCore.QProcess) -> None:
        self.obj_appconfig.process_obj.append(process)
        current_project_name = self.obj_appconfig.current_project['ProjectName']
        if current_project_name in self.obj_appconfig.proc_dict:
            self.obj_appconfig.proc_dict[current_project_name].append(process.processId())

    def _start_process(self) -> None:
        self.process.start('ngspice', self.ngspice_args)
        logger.debug(f"Process dictionary: {self.obj_appconfig.proc_dict}")
        self._register_process(self.process)

    def _is_linux(self) -> bool:
        return os.name != "nt"

    def _start_gaw_process(self, netlist: str) -> None:
        try:
            self.gaw_process = QtCore.QProcess(self)
            raw_file = netlist.replace(".cir.out", ".raw")
            self.gaw_command = f"gaw {shlex.quote(raw_file)}"
            self.gaw_process.start('sh', ['-c', self.gaw_command])
            logger.info(f"Started GAW with command: {self.gaw_command}")
        except Exception as e:
            logger.error(f"Failed to start GAW process: {e}")

    @pyqtSlot()
    def _handle_stdout(self) -> None:
        try:
            data = self.process.readAllStandardOutput().data()
            if data:
                self.terminal_ui.simulationConsole.insertPlainText(
                    data.decode('utf-8', errors='replace')
                )
        except Exception as e:
            logger.error(f"Error reading stdout: {e}")

    @pyqtSlot()
    def _handle_stderr(self) -> None:
        """Read stderr, filter batch-mode noise, display the rest."""
        try:
            data = self.process.readAllStandardError().data()
            if not data:
                return
            text = data.decode('utf-8', errors='replace')
            filtered = '\n'.join(
                line for line in text.split('\n')
                if 'PrinterOnly' not in line and 'viewport for graphics' not in line
            )
            if filtered.strip():
                self.terminal_ui.simulationConsole.insertPlainText(filtered)
        except Exception as e:
            logger.error(f"Error reading stderr: {e}")

    def finish_simulation(self, exit_code: Optional[int],
                         exit_status: Optional[QtCore.QProcess.ExitStatus],
                         sim_end_signal: pyqtSignal,
                         has_error_occurred: bool) -> None:
        # Skip finished signal if cancellation triggered both finished and error signals
        if not has_error_occurred and self.terminal_ui.simulationCancelled:
            return

        # Resolve exit code and status before any UI work so finally block has them
        if exit_code is None:
            exit_code = self.process.exitCode()
        error_type = self.process.error()
        if error_type in (QtCore.QProcess.ProcessError.FailedToStart,
                          QtCore.QProcess.ProcessError.Crashed,
                          QtCore.QProcess.ProcessError.Timedout):
            exit_status = QtCore.QProcess.ExitStatus.CrashExit
        elif exit_status is None:
            exit_status = self.process.exitStatus()

        try:
            self._update_ui_after_simulation()

            if self.terminal_ui.simulationCancelled:
                self._show_cancellation_message()
            elif self._is_simulation_successful(exit_status, exit_code, error_type):
                self._show_success_message()

                # On redo-simulation, TerminalUi sets "redoPlotFlag" on the process
                # to pass the user's plot choice back here
                redo_flag = self.process.property("redoPlotFlag")
                if redo_flag is not None:
                    self.plotFlag = redo_flag

                if self.plotFlag:
                    self.open_ngspice_plots()
            else:
                self._show_failure_message(error_type)

            self._scroll_terminal_to_bottom()
        except Exception as e:
            logger.error(f"finish_simulation UI error: {e}", exc_info=True)
        finally:
            # Emit completion signal — must always run so plot window can open
            sim_end_signal.emit(exit_status, exit_code)

    def open_ngspice_plots(self) -> None:
        logger.info("Opening NGSpice native plots")

        if os.name == 'nt':
            try:
                parser_nghdl = ConfigParser()
                config_path = os.path.join('library', 'config', '.nghdl', 'config.ini')
                parser_nghdl.read(config_path)
                msys_home = parser_nghdl.get('COMPILER', 'MSYS_HOME')
                mintty_exe = os.path.join(msys_home, 'usr', 'bin', 'mintty.exe')

                self.mintty_process = QtCore.QProcess(self)
                self.mintty_process.setWorkingDirectory(self.project_dir)
                # Pass program + args directly — Qt handles quoting internally
                self.mintty_process.start(mintty_exe, ['ngspice', '-p', self.command])
                logger.info(f"Started mintty: {mintty_exe} ngspice -p {self.command}")

            except Exception as e:
                logger.error(f"Failed to start Windows NGSpice plots: {e}")

        else:  # Linux/Unix
            try:
                raw_file = self.command.replace('.cir.out', '.raw')
                # Quote all paths so spaces in project names don't break the shell command
                xterm_command = (
                    f"cd {shlex.quote(self.project_dir)} && "
                    f"ngspice -r {shlex.quote(raw_file)} {shlex.quote(self.command)}"
                )
                self.xterm_process = QtCore.QProcess(self)
                self.xterm_process.start('xterm', ['-hold', '-e', 'sh', '-c', xterm_command])

                self._register_process(self.xterm_process)

                if hasattr(self, 'gaw_process') and hasattr(self, 'gaw_command'):
                    self.gaw_process.start('sh', ['-c', self.gaw_command])
                    logger.info(f"Restarted GAW: {self.gaw_command}")

                logger.info(f"Started xterm: {xterm_command}")

            except Exception as e:
                logger.error(f"Failed to start Linux NGSpice plots: {e}")

    def _update_ui_after_simulation(self) -> None:
        self.terminal_ui.progressBar.setMaximum(100)
        self.terminal_ui.progressBar.setProperty("value", 100)
        self.terminal_ui.cancelSimulationButton.setEnabled(False)
        self.terminal_ui.redoSimulationButton.setEnabled(True)

    def _is_simulation_successful(self, exit_status: QtCore.QProcess.ExitStatus,
                                exit_code: int,
                                error_type: QtCore.QProcess.ProcessError) -> bool:
        return (exit_status == QtCore.QProcess.ExitStatus.NormalExit and
                exit_code == 0)

    def _show_cancellation_message(self) -> None:
        message_dialog = QtWidgets.QMessageBox()
        message_dialog.setModal(True)
        message_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        message_dialog.setWindowTitle("Warning Message")
        message_dialog.setText("Simulation was cancelled.")
        message_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        message_dialog.exec()

    def _show_success_message(self) -> None:
        success_message = self.SUCCESS_FORMAT.format("Simulation Completed Successfully!")
        self.terminal_ui.simulationConsole.append(success_message)

    def _show_failure_message(self, error_type: QtCore.QProcess.ProcessError) -> None:
        failure_message = self.FAILURE_FORMAT.format("Simulation Failed!")
        self.terminal_ui.simulationConsole.append(failure_message)

        error_message = self._get_error_message(error_type)
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.setModal(True)
        error_dialog.setWindowTitle("Error Message")
        error_dialog.showMessage(error_message)
        error_dialog.exec()

    def _get_error_message(self, error_type: QtCore.QProcess.ProcessError) -> str:
        error_messages = {
            QtCore.QProcess.ProcessError.FailedToStart: (
                'Simulation failed to start. '
                'Ensure that eSim is installed correctly.'
            ),
            QtCore.QProcess.ProcessError.Crashed: (
                'Simulation crashed. Try again later.'
            ),
            QtCore.QProcess.ProcessError.Timedout: (
                'Simulation has timed out. Try to reduce the '
                'simulation time or the simulation step interval.'
            )
        }
        
        return error_messages.get(
            error_type, 
            'Simulation could not complete. Try again later.'
        )

    def _scroll_terminal_to_bottom(self) -> None:
        scrollbar = self.terminal_ui.simulationConsole.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(800, 600)
