"""
NGSpice Widget Module

This module provides the NgspiceWidget class for running NGSpice simulations
within a PyQt5 application interface.
"""

import os
import sys #added by THSS
import logging
from typing import List, Optional
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from configuration.Appconfig import Appconfig
from frontEnd import TerminalUi
from configparser import ConfigParser

# Set up logging
logger = logging.getLogger(__name__)

def get_bundle_bin(name: str) -> str:
    """
    Resolve path to a binary, whether running from source or inside .app bundle.
    
    Inside .app:  Contents/MacOS/eSim  → sys.executable
                  Contents/Resources/bin/ngspice  → what we want
    From source:  falls back to /usr/local/bin/
    """
    if getattr(sys, 'frozen', False):
        # Running inside PyInstaller .app bundle
        # sys.executable = .../eSim.app/Contents/MacOS/eSim
        contents_dir = os.path.dirname(os.path.dirname(sys.executable))
        return os.path.join(contents_dir, 'Resources', 'bin', name)
    else:
        # Running from source — use system install
        return os.path.join('/usr/local/bin', name)
    
def get_bundle_share(relative_path: str) -> str:
    """
    Resolve path to shared data (e.g. ngspice/scripts), 
    whether bundled or from source.
    
    relative_path: e.g. 'ngspice/scripts'
    """
    if getattr(sys, 'frozen', False):
        contents_dir = os.path.dirname(os.path.dirname(sys.executable))
        return os.path.join(contents_dir, 'Resources', 'share', relative_path)
    else:
        return os.path.join('/usr/local/share', relative_path)

class NgspiceWidget(QtWidgets.QWidget):
    """
    Widget for running NGSpice simulations with terminal interface.
    
    This class creates a widget that runs NGSpice processes and displays
    their output in a terminal interface. It handles simulation execution,
    logging, and provides status feedback through signals.
    """
    
    # Process error types
    ERROR_FAILED_TO_START = 0
    ERROR_CRASHED = 1
    ERROR_TIMED_OUT = 2
    
    # Message formatting templates
    SUCCESS_FORMAT = ('<span style="color:#00ff00; font-size:26px;">'
                     '{}'
                     '</span>')
    FAILURE_FORMAT = ('<span style="color:#ff3333; font-size:26px;">'
                     '{}'
                     '</span>')

    def __init__(self, netlist: str, sim_end_signal: pyqtSignal, plotFlag: Optional[bool] = None) -> None:
        """
        Initialize the NgspiceWidget.
        
        Creates NGSpice simulation window and runs the simulation process.
        Handles logging of the NGSpice process, returns simulation status,
        and calls the plotter. Also checks if running on Linux and starts GAW.
        
        Args:
            netlist: Path to the .cir.out file containing simulation instructions
            sim_end_signal: Signal emitted to Application class for enabling
                          simulation interaction and plotting data if successful
            plotFlag: Whether to show NGSpice plots (True/False)
        """
        super().__init__()

        # **CRITICAL FIX**: Set expanding size policy
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                          QtWidgets.QSizePolicy.Expanding)

        # Set minimum size
        self.setMinimumSize(300, 200)
        
        self.obj_appconfig = Appconfig()

        # added block by THSS to set DISPLAY variable on macOS for NGSpice plotting
        if sys.platform == 'darwin':
            if 'DISPLAY' not in os.environ:
                # Try to get DISPLAY from launchctl (XQuartz socket)
                import subprocess
                try:
                    result = subprocess.run(
                        ['launchctl', 'getenv', 'DISPLAY'],
                        capture_output=True, text=True
                    )
                    if result.stdout.strip():
                        os.environ['DISPLAY'] = result.stdout.strip()
                    else:
                        os.environ['DISPLAY'] = ':0'
                except Exception:
                    os.environ['DISPLAY'] = ':0'
        # end of added block by THSS

        self.project_dir = self.obj_appconfig.current_project["ProjectName"]
        self.netlist_path = netlist
        self.sim_end_signal = sim_end_signal
        
        # **IMPORTANT**: Store plotFlag and command for dual plot functionality
        self.plotFlag = plotFlag
        self.command = netlist
        logger.info(f"Value of plotFlag: {self.plotFlag}")
        
        # Prepare NGSpice arguments
        self.ngspice_args = self._prepare_ngspice_arguments(netlist)
        logger.info(f"NGSpice arguments: {self.ngspice_args}")

        # Set up the main process
        self.process = QtCore.QProcess(self)
        self.terminal_ui = TerminalUi.TerminalUi(self.process, self.ngspice_args)
        
        # Set up layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.terminal_ui)

        # Configure and start the NGSpice process
        self._configure_process()
        self._start_process()
        
        # Start GAW on Linux systems (first instance)
        if self._is_linux():
            self._start_gaw_process(netlist)

    def _prepare_ngspice_arguments(self, netlist: str) -> List[str]:
        """
        Prepare command line arguments for NGSpice.
        
        Args:
            netlist: Path to the netlist file
            
        Returns:
            List of command line arguments for NGSpice
        """
        raw_file = netlist.replace(".cir.out", ".raw")
        return ['-b', '-r', raw_file, netlist]

    def _configure_process(self) -> None:
        """Configure the NGSpice process with working directory and signals."""
        self.process.setWorkingDirectory(self.project_dir)
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        
        # Connect process signals
        self.process.readyRead.connect(self.ready_read_all)
        self.process.finished.connect(
            lambda exit_code, exit_status: self.finish_simulation(
                exit_code, exit_status, self.sim_end_signal, False
            )
        )
        self.process.errorOccurred.connect(
            lambda: self.finish_simulation(None, None, self.sim_end_signal, True)
        )

    def _ensure_display(self) -> str:
        """
        Resolve DISPLAY for XQuartz on macOS.
        Tries multiple sources in order of reliability.
        Returns the DISPLAY string.
        """
        import subprocess
        import glob

        # 1. Already set correctly
        current = os.environ.get('DISPLAY', '')
        if current:
            logger.info(f"DISPLAY already set: {current}")
            return current

        # 2. Try launchctl (works if XQuartz was launched before .app)
        try:
            r = subprocess.run(
                ['launchctl', 'getenv', 'DISPLAY'],
                capture_output=True, text=True, timeout=2
            )
            val = r.stdout.strip()
            if val:
                logger.info(f"DISPLAY from launchctl: {val}")
                os.environ['DISPLAY'] = val
                return val
        except Exception as e:
            logger.warning(f"launchctl getenv DISPLAY failed: {e}")

        # 3. Find XQuartz socket file directly
        patterns = [
            '/private/tmp/com.apple.launchd.*/org.xquartz:0',
            '/tmp/com.apple.launchd.*/org.xquartz:0',
        ]
        for pattern in patterns:
            matches = glob.glob(pattern)
            if matches:
                # Socket found — XQuartz is running, use :0
                logger.info(f"Found XQuartz socket: {matches[0]}, using DISPLAY=:0")
                os.environ['DISPLAY'] = ':0'
                return ':0'

        # 4. Try to start XQuartz and wait for it
        logger.warning("XQuartz not running — attempting to start it")
        try:
            subprocess.Popen(
                ['open', '-a', 'XQuartz'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # Poll for socket to appear (up to 8 seconds)
            import time
            for _ in range(16):
                time.sleep(0.5)
                for pattern in patterns:
                    matches = glob.glob(pattern)
                    if matches:
                        logger.info(f"XQuartz started, socket={matches[0]}")
                        os.environ['DISPLAY'] = ':0'
                        return ':0'
        except Exception as e:
            logger.error(f"Failed to start XQuartz: {e}")

        # 5. Hardcoded fallback — what worked for you manually
        logger.warning("All DISPLAY detection failed — falling back to :0")
        os.environ['DISPLAY'] = ':0'
        return ':0'

    def _start_process(self) -> None:
        ngspice_bin = self._get_ngspice_binary()

        from PyQt5.QtCore import QProcessEnvironment
        env = QProcessEnvironment.systemEnvironment()

        if sys.platform == 'darwin':
            # ── Resolve DISPLAY before anything else ──────────────────
            display = self._ensure_display()

            spice_scripts = self._get_spice_scripts(ngspice_bin)
            spinit_path   = self._generate_spinit()
            scripts_dir   = os.path.dirname(spinit_path)
            os.rename(spinit_path, os.path.join(scripts_dir, 'spinit'))

            env.insert('DISPLAY',       display)
            env.insert('SPICE_SCRIPTS', scripts_dir)
            logger.info(f"Starting ngspice with DISPLAY={display}, "
                        f"SPICE_SCRIPTS={scripts_dir}")

        self.process.setProcessEnvironment(env)
        self.process.start(ngspice_bin, self.ngspice_args)

        self.obj_appconfig.process_obj.append(self.process)
        current_project_name = self.obj_appconfig.current_project['ProjectName']
        if current_project_name in self.obj_appconfig.proc_dict:
            self.obj_appconfig.proc_dict[current_project_name].append(
                self.process.pid()
            )

    def _get_ngspice_binary(self) -> str:
        """
        Get ngspice binary path — works both from source and inside .app bundle.
        """
        if sys.platform == 'darwin':
            path = get_bundle_bin('ngspice')
            if os.path.exists(path):
                logger.info(f"Using ngspice binary at: {path}")
                return path
            else:
                logger.warning(
                    f"ngspice not found at bundled path: {path}, "
                    f"falling back to /usr/local/bin/ngspice"
                )
                return '/usr/local/bin/ngspice'
        return 'ngspice'  # Linux: rely on PATH

    def _get_spice_scripts(self, ngspice_bin: str) -> str:
        """
        Get SPICE_SCRIPTS path — works both from source and inside .app bundle.
        """
        if sys.platform == 'darwin':
            path = get_bundle_share('ngspice/scripts')
            if os.path.exists(path):
                logger.info(f"Using SPICE_SCRIPTS at: {path}")
                return path
            else:
                logger.warning(
                    f"SPICE_SCRIPTS not found at bundled path: {path}, "
                    f"falling back to /usr/local/share/ngspice/scripts"
                )
                return '/usr/local/share/ngspice/scripts'
        return os.environ.get('SPICE_SCRIPTS', '')

    def _is_linux(self) -> bool:
        """Check if the current operating system is Linux."""
        # return os.name != "nt" # Original code, modified by THSS to also exclude macOS
        return os.name != "nt" and sys.platform != "darwin" #modified by THSS

    def _start_gaw_process(self, netlist: str) -> None:
        """
        Start GAW (GTK Analog Waveform viewer) process on Linux.
        
        Args:
            netlist: Path to the netlist file
        """
        try:
            self.gaw_process = QtCore.QProcess(self)
            raw_file = netlist.replace(".cir.out", ".raw")
            self.gaw_command = f"gaw {raw_file}"
            self.gaw_process.start('sh', ['-c', self.gaw_command])
            logger.info(f"Started GAW with command: {self.gaw_command}")
        except Exception as e:
            logger.error(f"Failed to start GAW process: {e}")

    @pyqtSlot()
    def ready_read_all(self) -> None:
        try:
            std_output = self.process.readAllStandardOutput().data()
            if std_output:
                output_text = str(std_output, encoding='utf-8')
                self.terminal_ui.simulationConsole.insertPlainText(output_text)

            std_error = self.process.readAllStandardError().data()
            if std_error:
                error_text = str(std_error, encoding='utf-8')
                filtered_lines = []
                for line in error_text.split('\n'):
                    # Filter noise from batch-mode display attempts
                    if ('PrinterOnly' not in line and
                        'viewport for graphics' not in line and
                        'no DC value' not in line):        # ← also suppress this warning
                        filtered_lines.append(line)

                filtered_error = '\n'.join(filtered_lines)
                if filtered_error.strip():
                    self.terminal_ui.simulationConsole.insertPlainText(filtered_error)

        except Exception as e:
            logger.error(f"Error reading process output: {e}")

    def finish_simulation(self, exit_code: Optional[int], 
                         exit_status: Optional[QtCore.QProcess.ExitStatus],
                         sim_end_signal: pyqtSignal, 
                         has_error_occurred: bool) -> None:
        """
        Handle simulation completion and update UI accordingly.
        
        This method is called when the NGSpice simulation finishes. It updates
        the UI state, displays appropriate status messages, and emits signals
        for plot generation if the simulation was successful.
        
        Args:
            exit_code: Process exit code
            exit_status: Process exit status
            sim_end_signal: Signal to emit when simulation ends
            has_error_occurred: Whether an error occurred during simulation
        """
        # Skip finished signal if cancellation triggered both finished and error signals
        if not has_error_occurred and self.terminal_ui.simulationCancelled:
            return

        # Update UI state after simulation completion
        self._update_ui_after_simulation()

        # Get actual exit code and status if not provided
        if exit_code is None:
            exit_code = self.process.exitCode()

        error_type = self.process.error()
        if error_type <= self.ERROR_TIMED_OUT:  # FailedToStart, Crashed, TimedOut
            exit_status = QtCore.QProcess.CrashExit
        elif exit_status is None:
            exit_status = self.process.exitStatus()

        # Handle different simulation outcomes
        if self.terminal_ui.simulationCancelled:
            self._show_cancellation_message()
        elif self._is_simulation_successful(exit_status, exit_code, error_type):
            self._show_success_message()
            
            # **CRITICAL ADDITION**: Check and update plotFlag from process properties
            # This handles the re-simulation case from TerminalUi
            new_plot_flag = self.process.property("plotFlag")
            if new_plot_flag is not None:
                self.plotFlag = new_plot_flag
            
            new_plot_flag2 = self.process.property("plotFlag2")
            if new_plot_flag2 is not None:
                self.plotFlag = new_plot_flag2
            
            # **CRITICAL ADDITION**: Open NGSpice plot windows if requested
            if self.plotFlag:
                self.open_ngspice_plots()
        else:
            self._show_failure_message(error_type)

        # Scroll terminal to bottom
        self._scroll_terminal_to_bottom()

        # Emit completion signal
        sim_end_signal.emit(exit_status, exit_code)

    def open_ngspice_plots(self) -> None:
        """
        Open NGSpice plotting windows (native NGSpice plots).
        This function handles both Windows and Linux platforms.
        """
        logger.info("Opening NGSpice native plots")
        
        if os.name == 'nt':  # Windows
            try:
                parser_nghdl = ConfigParser()
                config_path = os.path.join('library', 'config', '.nghdl', 'config.ini')
                parser_nghdl.read(config_path)
                msys_home = parser_nghdl.get('COMPILER', 'MSYS_HOME')
                
                temp_dir = os.getcwd()
                os.chdir(self.project_dir)
                
                # Create command for Windows using mintty
                mintty_command = (
                    f'cmd /c "start /min {msys_home}/usr/bin/mintty.exe '
                    f'ngspice -p {self.command}"'
                )
                
                # Create a new QProcess for mintty
                self.mintty_process = QtCore.QProcess(self)
                self.mintty_process.start(mintty_command)
                
                os.chdir(temp_dir)
                logger.info(f"Started mintty with command: {mintty_command}")
                
            except Exception as e:
                logger.error(f"Failed to start Windows NGSpice plots: {e}")

        # Added block by THSS to handle macOS using AppleScript to open Terminal and run NGSpice
        elif sys.platform == 'darwin':
            xterm_path = '/opt/X11/bin/xterm'
            if not os.path.exists(xterm_path):
                self.msg = QtWidgets.QErrorMessage()
                self.msg.setModal(True)
                self.msg.setWindowTitle("XQuartz Required")
                self.msg.showMessage(
                    'NGSpice plots require XQuartz.\n'
                    'Please install XQuartz from https://www.xquartz.org\n'
                    'then log out and log back in.'
                )
                self.msg.exec_()
                return

            try:
                # ── Single source of truth for DISPLAY ────────────────────
                display       = self._ensure_display()
                ngspice_bin   = get_bundle_bin('ngspice')
                spice_scripts = get_bundle_share('ngspice/scripts')
                raw_file      = self.command.replace('.cir.out', '.raw')

                logger.info(f"open_ngspice_plots: DISPLAY={display}, "
                            f"ngspice={ngspice_bin}")

                xterm_command = (
                    f'export DISPLAY="{display}"; '
                    f'export SPICE_SCRIPTS="{spice_scripts}"; '
                    f'cd "{self.project_dir}"; '
                    f'"{ngspice_bin}" -r "{raw_file}" "{self.command}"; '
                    f'echo "--- ngspice exited $? — press Enter to close ---"; '
                    f'read _'
                )

                from PyQt5.QtCore import QProcessEnvironment
                xterm_env = QProcessEnvironment.systemEnvironment()
                xterm_env.insert('DISPLAY', display)

                self.xterm_process = QtCore.QProcess(self)
                self.xterm_process.setProcessEnvironment(xterm_env)
                self.xterm_process.errorOccurred.connect(
                    lambda err: logger.error(f"xterm error: {err} — "
                                            f"{self.xterm_process.errorString()}")
                )
                self.xterm_process.start(
                    xterm_path,
                    ['-title', 'NGSpice Plot', '-hold',
                    '-e', 'bash', '-c', xterm_command]
                )

                if not self.xterm_process.waitForStarted(5000):
                    logger.error(f"xterm failed: {self.xterm_process.errorString()}")
                    QtWidgets.QMessageBox.critical(
                        None, "Plot Error",
                        f"Could not open NGSpice plot window.\n\n"
                        f"DISPLAY={display}\n"
                        f"Error: {self.xterm_process.errorString()}\n\n"
                        f"Try running: open -a XQuartz\n"
                        f"then restart eSim."
                    )
                    return

                self.obj_appconfig.process_obj.append(self.xterm_process)
                current_project = self.obj_appconfig.current_project['ProjectName']
                if current_project in self.obj_appconfig.proc_dict:
                    self.obj_appconfig.proc_dict[current_project].append(
                        self.xterm_process.pid()
                    )

            except Exception as e:
                logger.error(f"macOS ngspice plots failed: {e}", exc_info=True)
        # End of added macOS block by THSS, rest of the code remains unchanged for Linux
                
        else:  # Linux/Unix
            try:
                # Create xterm command for interactive NGSpice
                xterm_command = (
                    f"cd {self.project_dir}; "
                    f"ngspice -r {self.command.replace('.cir.out', '.raw')} "
                    f"{self.command}"
                )
                xterm_args = ['-hold', '-e', xterm_command]
                
                # Create new QProcess for xterm
                self.xterm_process = QtCore.QProcess(self)
                self.xterm_process.start('xterm', xterm_args)
                
                # Register the process
                self.obj_appconfig.process_obj.append(self.xterm_process)
                current_project = self.obj_appconfig.current_project['ProjectName']
                if current_project in self.obj_appconfig.proc_dict:
                    self.obj_appconfig.proc_dict[current_project].append(
                        self.xterm_process.pid()
                    )
                
                # Also restart GAW for the new plot window
                if hasattr(self, 'gaw_process') and hasattr(self, 'gaw_command'):
                    self.gaw_process.start('sh', ['-c', self.gaw_command])
                    logger.info(f"Restarted GAW: {self.gaw_command}")
                
                logger.info(f"Started xterm with args: {xterm_args}")
                
            except Exception as e:
                logger.error(f"Failed to start Linux NGSpice plots: {e}")

    def _update_ui_after_simulation(self) -> None:
        """Update UI elements after simulation completion."""
        self.terminal_ui.progressBar.setMaximum(100)
        self.terminal_ui.progressBar.setProperty("value", 100)
        self.terminal_ui.cancelSimulationButton.setEnabled(False)
        self.terminal_ui.redoSimulationButton.setEnabled(True)

    def _is_simulation_successful(self, exit_status: QtCore.QProcess.ExitStatus,
                                exit_code: int, 
                                error_type: QtCore.QProcess.ProcessError) -> bool:
        """
        Determine if the simulation completed successfully.
        
        Args:
            exit_status: Process exit status
            exit_code: Process exit code
            error_type: Process error type
            
        Returns:
            True if simulation was successful, False otherwise
        """
        return (exit_status == QtCore.QProcess.NormalExit and 
                exit_code == 0 and 
                error_type == QtCore.QProcess.UnknownError)

    def _show_cancellation_message(self) -> None:
        """Display simulation cancellation message."""
        message_dialog = QtWidgets.QMessageBox()
        message_dialog.setModal(True)
        message_dialog.setIcon(QtWidgets.QMessageBox.Warning)
        message_dialog.setWindowTitle("Warning Message")
        message_dialog.setText("Simulation was cancelled.")
        message_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
        message_dialog.exec()

    def _show_success_message(self) -> None:
        """Display simulation success message in the terminal."""
        success_message = self.SUCCESS_FORMAT.format("Simulation Completed Successfully!")
        self.terminal_ui.simulationConsole.append(success_message)

    def _show_failure_message(self, error_type: QtCore.QProcess.ProcessError) -> None:
        """
        Display simulation failure message.
        
        Args:
            error_type: Type of process error that occurred
        """
        # Display failure message in terminal
        failure_message = self.FAILURE_FORMAT.format("Simulation Failed!")
        self.terminal_ui.simulationConsole.append(failure_message)

        # Determine specific error message
        error_message = self._get_error_message(error_type)
        
        # Show error dialog
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.setModal(True)
        error_dialog.setWindowTitle("Error Message")
        error_dialog.showMessage(error_message)
        error_dialog.exec()

    def _get_error_message(self, error_type: QtCore.QProcess.ProcessError) -> str:
        """
        Get appropriate error message based on error type.
        
        Args:
            error_type: Type of process error
            
        Returns:
            Human-readable error message
        """
        error_messages = {
            QtCore.QProcess.FailedToStart: (
                'Simulation failed to start. '
                'Ensure that eSim is installed correctly.'
            ),
            QtCore.QProcess.Crashed: (
                'Simulation crashed. Try again later.'
            ),
            QtCore.QProcess.Timedout: (
                'Simulation has timed out. Try to reduce the '
                'simulation time or the simulation step interval.'
            )
        }
        
        return error_messages.get(
            error_type, 
            'Simulation could not complete. Try again later.'
        )

    def _scroll_terminal_to_bottom(self) -> None:
        """Scroll the terminal console to the bottom."""
        scrollbar = self.terminal_ui.simulationConsole.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def sizeHint(self) -> QtCore.QSize:
        """Provide proper size hint."""
        return QtCore.QSize(800, 600)
    
    def _generate_spinit(self) -> str:
        """
        Generate a spinit file with correct absolute paths for the bundled
        .cm code models. Returns path to the generated spinit file.
        """
        import tempfile

        if getattr(sys, 'frozen', False):
            contents_dir = os.path.dirname(os.path.dirname(sys.executable))
            cm_dir  = os.path.join(contents_dir, 'Resources', 'lib', 'ngspice')
            src_spinit = os.path.join(contents_dir, 'Resources', 'share',
                                    'ngspice', 'scripts', 'spinit')
        else:
            cm_dir  = '/usr/local/lib/ngspice'
            src_spinit = '/usr/local/share/ngspice/scripts/spinit'

        # Read template spinit
        try:
            with open(src_spinit, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            logger.error(f"spinit not found at {src_spinit}")
            return src_spinit  # fall back to original path

        # Replace placeholder (bundled) or hardcoded path (dev)
        content = content.replace('__ESIM_LIB__', cm_dir)
        content = content.replace('/usr/local/lib/ngspice', cm_dir)

        # Write resolved spinit to a temp file
        tmp = tempfile.NamedTemporaryFile(
            mode='w', suffix='_spinit', delete=False, prefix='esim_'
        )
        tmp.write(content)
        tmp.flush()
        tmp.close()

        logger.info(f"Generated spinit at {tmp.name} with cm_dir={cm_dir}")
        return tmp.name
