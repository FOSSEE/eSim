import os
import re
import shlex
import shutil
import codecs
import logging
from typing import List, Optional
from PyQt6 import QtWidgets, QtCore
from configuration import Dialogs
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from configuration.Appconfig import Appconfig
from frontEnd import TerminalUi
from maker import CosimConfig
from maker.CosimLogger import CosimLog

logger = logging.getLogger(__name__)


def _make_abandon_reporter(state, sim_end_signal, process, obj_appconfig):
    """Build the slot that reports a run the widget can no longer report itself.

    The Simulation dock can be torn down while ngspice is still running -- one
    click on the tab's X. Qt then destroys the widget and its child QProcess
    without ever delivering ``finished``, so nothing emits the completion
    signal and Simulate / Convert / Close Project / Workspace stay greyed out
    until the app is restarted, which reads as a frozen eSim.

    The returned slot is wired to ``destroyed``. It closes over plain Python
    objects *only* -- never the widget: by the time ``destroyed`` fires the C++
    side is already gone, and any Qt call on it would raise RuntimeError from
    inside a destructor.
    """
    def abandon(*_args):
        if state['finished']:
            return
        state['finished'] = True
        # Prune the shared registries by identity: list.remove() compares with
        # ==, which reaches into the deleted C++ object.
        proj = obj_appconfig.current_project.get('ProjectName')
        registries = [obj_appconfig.process_obj]
        handles = obj_appconfig.proc_dict.get(proj) if proj else None
        if handles is not None:
            registries.append(handles)
        for registry in registries:
            for index, handle in enumerate(registry):
                if handle is process:
                    del registry[index]
                    break
        try:
            sim_end_signal.emit(QtCore.QProcess.ExitStatus.CrashExit, -1)
        except RuntimeError:
            pass
    return abandon


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
        self.raw_file = self._raw_path(netlist)
        logger.info(f"Value of plotFlag: {self.plotFlag}")

        # Incremental UTF-8 decoders so a multibyte character split across two
        # readyRead chunks is reassembled instead of being mangled by a
        # per-chunk decode.
        self._stdout_decoder = codecs.getincrementaldecoder('utf-8')('replace')
        self._stderr_decoder = codecs.getincrementaldecoder('utf-8')('replace')
        self._main_pid: Optional[int] = None

        # Coalesce console writes. A chatty run fires readyRead in rapid bursts;
        # one insertPlainText per burst thrashes the widget and stalls the UI.
        # Buffer decoded text and flush it once per 50 ms tick instead.
        self._console_buffer: List[str] = []
        self._console_flush_timer = QtCore.QTimer(self)
        self._console_flush_timer.setSingleShot(True)
        self._console_flush_timer.setInterval(50)
        self._console_flush_timer.timeout.connect(self._flush_console)

        # Read before _prepare_ngspice_arguments: it decides whether '-r' is
        # passed, and a d_cosim netlist must not get it.
        self.uses_dcosim = self._netlist_uses_dcosim(netlist)

        self.ngspice_args = self._prepare_ngspice_arguments(netlist)
        logger.info(f"NGSpice arguments: {self.ngspice_args}")

        # Use eSim's ngspice (the nghdl-simulator build that carries d_cosim +
        # ivlng) for ALL simulations; resolved without hardcoded paths.
        self.ngspice_bin = CosimConfig.ngspice_binary()

        self.process = QtCore.QProcess(self)
        # Redo restarts ngspice from inside TerminalUi, bypassing
        # _start_process, so a model rebuilt between the two runs would go
        # unnoticed there. Hand it the same re-staging step as a callback.
        self.terminal_ui = TerminalUi.TerminalUi(
            self.process, self.ngspice_args, self.ngspice_bin,
            pre_start=self._restage_on_redo if self.uses_dcosim else None)

        # One-shot completion bookkeeping, shared with the abandon reporter so
        # a run is reported exactly once no matter which path ends it: a clean
        # exit, a crash that fires BOTH finished and errorOccurred, or the dock
        # being destroyed mid-run. Reset per run in _on_process_started, since
        # redo-simulation reuses this same widget and QProcess.
        self._run_state = {'finished': False}
        self._abandon_run = _make_abandon_reporter(
            self._run_state, sim_end_signal, self.process, self.obj_appconfig)
        self.destroyed.connect(self._abandon_run)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.terminal_ui)

        self._configure_process()

        # Feedback before the process exists: on a cold boot the very first
        # ngspice launch can take seconds (the OS scans the exe, its DLL
        # closure and every spinit codemodel on first load), during which the
        # console would otherwise sit empty and look hung.
        self.terminal_ui.simulationConsole.insertPlainText(
            "[eSim] Starting ngspice ...\n[eSim] "
            + self.ngspice_bin + " " + " ".join(self.ngspice_args) + "\n")

        # Paint first, spawn second: process.start() runs CreateProcess on the
        # GUI thread, so a cold ngspice.exe blocks it before this widget has
        # ever painted -- the user saw an empty white Simulation page. One
        # deferred event-loop turn lets the dock render the banner + busy bar
        # before any stall can happen.
        QtCore.QTimer.singleShot(0, self._start_process)

    @staticmethod
    def _raw_path(netlist: str) -> str:
        """Derive the rawfile path from the netlist path without clobbering it.

        eSim netlists are '<name>.cir.out' and the rawfile is '<name>.raw'. A
        bare str.replace('.cir.out', '.raw') is a no-op when the suffix is
        absent, which would make the rawfile path equal the netlist path and
        let ngspice overwrite the netlist via '-r'. Strip the known suffix when
        present, otherwise swap the final extension.
        """
        if netlist.endswith(".cir.out"):
            return netlist[:-len(".cir.out")] + ".raw"
        return os.path.splitext(netlist)[0] + ".raw"

    def _prepare_ngspice_arguments(self, netlist: str) -> List[str]:
        """ngspice argv for this netlist.

        '-r' is omitted for a d_cosim run. Its analysis card lives inside
        .control (the Icarus engine is one-shot and must run exactly once), so
        ngspice's own '-r' pass finds nothing left in the deck to run and
        writes only an empty rawfile header -- while holding the filename open,
        which stops the netlist's own 'write <project>.raw' from producing the
        real thing. Dropping '-r' lets that write land, so a co-simulation
        leaves the same rawfile behind as every other backend.
        """
        if self.uses_dcosim:
            return ['-b', netlist]
        return ['-b', '-r', self.raw_file, netlist]

    def _configure_process(self) -> None:
        self.process.setWorkingDirectory(self.project_dir)
        self.process.setProcessChannelMode(QtCore.QProcess.ProcessChannelMode.SeparateChannels)
        self.process.started.connect(self._on_process_started)
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
        """Register the running simulation in the shared registries.

        Idempotent at both call sites on purpose. Windows delivers ``started``
        synchronously from inside QProcess.start() (CreateProcess succeeds
        before start() returns) while Linux queues it, so _on_process_started
        and _start_process register in the opposite order on the two platforms.
        Without the membership checks, Windows appended the same handle twice
        and the single unregister in finish_simulation removed one -- leaking a
        dead QProcess into process_obj and proc_dict on *every* simulation.
        Do not "fix" that by reordering the calls: only idempotence is
        ordering-proof.
        """
        if process not in self.obj_appconfig.process_obj:
            self.obj_appconfig.process_obj.append(process)
        current_project_name = self.obj_appconfig.current_project['ProjectName']
        handles = self.obj_appconfig.proc_dict.get(current_project_name)
        if handles is not None and process not in handles:
            # Store the QProcess handle (not its pid): Close Project terminates
            # through the handle, never a bare recycled pid.
            handles.append(process)

    def _unregister_process(self) -> None:
        """Drop the finished main-simulation process from the shared registries.

        Without this, every simulation leaves its QProcess in
        ``process_obj`` and its PID in ``proc_dict`` forever, so a long eSim
        session accumulates dead references. Only the main ngspice process is
        pruned here; the xterm/gaw helpers manage their own lifetimes.
        """
        try:
            if self.process in self.obj_appconfig.process_obj:
                self.obj_appconfig.process_obj.remove(self.process)
        except (ValueError, AttributeError):
            pass
        proj = self.obj_appconfig.current_project.get('ProjectName')
        handles = self.obj_appconfig.proc_dict.get(proj) if proj else None
        if handles is not None:
            try:
                handles.remove(self.process)
            except ValueError:
                pass

    @pyqtSlot()
    def _on_process_started(self) -> None:
        """Reset per-run decoder state at the start of every run, including redo.

        Redo reuses the same QProcess (via TerminalUi.redoSimulation), so the
        previous run's decoder state must be reset here. A redo also runs after
        the first run deregistered the process, so re-register it for cleanup.
        """
        self._stdout_decoder.reset()
        self._stderr_decoder.reset()
        self._main_pid = self.process.processId()
        self._queue_console(
            "[eSim] ngspice running (PID %s)\n" % self._main_pid)
        # A redo starts a fresh run on a widget whose previous run already
        # reported: re-arm the one-shot so this one can report too.
        self._run_state['finished'] = False
        self._register_process(self.process)
        self._clear_error_log()

    def _error_log_path(self) -> str:
        return os.path.join(self.project_dir, "ngspice_error.log")

    def _write_error_log(self) -> None:
        """Keep a failed run's ngspice output for the AI assistant to explain.

        The console also carries eSim's own "[eSim] ..." status lines (the
        command line, the PID); they are not ngspice output and only distract
        the model from the error, so they are left out.
        """
        console = self.terminal_ui.simulationConsole.toPlainText()
        output = "".join(line for line in console.splitlines(keepends=True)
                         if not line.startswith("[eSim]"))
        try:
            with open(self._error_log_path(), "w", encoding="utf-8") as log:
                log.write(output)
        except OSError as e:
            logger.error(f"Could not write ngspice error log: {e}")

    def _clear_error_log(self) -> None:
        """Drop the previous failure's log so it is never mistaken for this run's."""
        try:
            os.remove(self._error_log_path())
        except FileNotFoundError:
            pass
        except OSError as e:
            logger.error(f"Could not remove old ngspice error log: {e}")

    def _start_process(self) -> None:
        # NGHDL ghdl models spawn mintty/bash from inside ngspice on Windows.
        self._add_msys_paths()
        if self.uses_dcosim:
            if not CosimConfig.has_dcosim():
                from maker import ToolchainCheck
                Dialogs.warning(
                    self, "d_cosim unavailable",
                    ToolchainCheck.failure_message(ToolchainCheck.DCOSIM) or
                    CosimConfig.missing_reason() or
                    "This ngspice build cannot run d_cosim co-simulation.")
            # ngspice's ivlng adapter dlopens libvvp at runtime, so the iverilog
            # lib dir must be on the dynamic-loader search path.
            self._add_iverilog_libpath()
            # Tell both audiences this is a co-sim run and which libvvp ngspice
            # will dlopen -- ivlng load failures otherwise look like generic
            # ngspice noise. GUI sim console is plain-text, so banner it there;
            # full detail goes to the terminal + ~/.esim/dcosim.log.
            clog = CosimLog()
            clog.phase("d_cosim co-simulation run")
            clog.info("ngspice: " + str(self.ngspice_bin))
            clog.info("ivlng libvvp dir: " +
                      (CosimConfig.iverilog_libdir() or "<none>"))
            restaged = self._restage_dcosim_vvps(
                self.netlist_path, self.project_dir, clog)
            self.terminal_ui.simulationConsole.insertPlainText(
                "\n[eSim] d_cosim co-simulation: loading Verilog model(s) "
                "via ngspice ivlng/libvvp ...\n")
            if restaged:
                self.terminal_ui.simulationConsole.insertPlainText(
                    "[eSim] refreshed rebuilt model(s): "
                    + ", ".join(restaged) + "\n")
        logger.info(f"Launching ngspice -> {self.ngspice_bin}")
        self.process.start(self.ngspice_bin, self.ngspice_args)
        logger.debug(f"Process dictionary: {self.obj_appconfig.proc_dict}")
        self._register_process(self.process)
        # Capture the PID now (valid while running); processId() returns 0 once
        # the process has finished, so _unregister_process needs the cached value.
        self._main_pid = self.process.processId()

    def _add_iverilog_libpath(self) -> None:
        """Prepend the iverilog lib dir (libvvp) to the dynamic-loader search
        path so ngspice's ivlng adapter can load it. Cross-platform: PATH on
        Windows, LD_LIBRARY_PATH elsewhere.

        On Windows the codemodel dir (lib\\ngspice) is prepended too: it holds
        ivlng.dll itself, which d_cosim's cosim_dlopen resolves via a plain
        LoadLibrary("ivlng") (PATH search) before falling back to its
        compile-time NGSPICELIBDIR -- a build-machine path that does not exist
        on user installs. The launcher already puts it on PATH; this keeps
        d_cosim working even when eSim is started some other way."""
        dirs = []
        if os.name == 'nt':
            cmdir = CosimConfig.ngspice_codemodel_dir()
            if cmdir:
                dirs.append(cmdir)
        lib = CosimConfig.iverilog_libdir()
        if lib:
            dirs.append(lib)
        if not dirs:
            return
        var = CosimConfig.loader_path_var()
        # Extend any environment already set on the process (_add_msys_paths
        # may have run first) instead of resetting to the system one.
        env = self.process.processEnvironment()
        if env.isEmpty():
            env = QtCore.QProcessEnvironment.systemEnvironment()
        existing = env.value(var, "")
        prefix = os.pathsep.join(dirs)
        env.insert(var, prefix + (os.pathsep + existing if existing else ""))
        self.process.setProcessEnvironment(env)

    def _add_msys_paths(self) -> None:
        """Windows only: put the bundled MSYS2 dirs on ngspice's PATH.

        NGHDL's generated ghdl code models launch their per-instance VHDL
        testbench server with ``system("start mintty.exe ... bash.exe ...")``
        from INSIDE ngspice, so mintty/bash must be resolvable from the
        ngspice process environment (mingw64/bin additionally covers the
        ghdl/gcc the server scripts call). No-op when MSYS2 is not installed
        or on POSIX."""
        if os.name != 'nt':
            return
        msys_home = CosimConfig.nghdl_cfg('COMPILER', 'MSYS_HOME')
        if not msys_home or not os.path.isdir(msys_home):
            return
        extra = os.pathsep.join([
            os.path.join(msys_home, 'usr', 'bin'),
            os.path.join(msys_home, 'mingw64', 'bin'),
        ])
        env = self.process.processEnvironment()
        if env.isEmpty():
            env = QtCore.QProcessEnvironment.systemEnvironment()
        existing = env.value('PATH', "")
        env.insert('PATH', extra + (os.pathsep + existing if existing else ""))
        self.process.setProcessEnvironment(env)

    @staticmethod
    def _netlist_uses_dcosim(netlist: str) -> bool:
        """True if the netlist instantiates a d_cosim code-model block."""
        try:
            with open(netlist, "r") as handle:
                return "d_cosim" in handle.read().lower()
        except OSError:
            return False

    # '.model u5 d_cosim simulation="ivlng" sim_args=["adder"]' -> 'adder'.
    # lib_args (also a quoted vector on the same line) must not match.
    _SIM_ARGS_RE = re.compile(r'\bsim_args\s*=\s*\[\s*"([^"]+)"')

    @staticmethod
    def _dcosim_model_names(netlist: str) -> List[str]:
        """Verilog model names the netlist's d_cosim blocks load, in file
        order, de-duplicated (one model may back several instances)."""
        try:
            with open(netlist, "r", errors="replace") as handle:
                text = handle.read()
        except OSError:
            return []
        names: List[str] = []
        for match in NgspiceWidget._SIM_ARGS_RE.finditer(text):
            name = match.group(1)
            if name not in names:
                names.append(name)
        return names

    def _restage_on_redo(self) -> None:
        """TerminalUi's redo hook: same re-staging as a fresh run, announced
        on the console the redo just cleared."""
        refreshed = self._restage_dcosim_vvps(
            self.netlist_path, self.project_dir, CosimLog())
        if refreshed:
            self.terminal_ui.simulationConsole.insertPlainText(
                "[eSim] refreshed rebuilt model(s): "
                + ", ".join(refreshed) + "\n")

    @staticmethod
    def _restage_dcosim_vvps(netlist: str, project_dir: str,
                             log=None) -> List[str]:
        """Refresh the staged vvp of every d_cosim model that was rebuilt
        since the netlist was converted. Returns the names refreshed.

        ivlng loads sim_args relative to ngspice's working directory, so
        ``Convert._cosim_model_line`` copies each compiled vvp next to the
        netlist -- but only at *conversion* time. Convert once, spot a logic
        bug, rebuild the model in the NgVeri tab, hit Simulate again, and the
        stale copy runs: the user's fix silently "does nothing". Compare
        mtimes against the canonical build output (the same
        ``CosimConfig.cosim_vvp_path`` both the builder and the netlister
        use) and re-copy what is older, at every simulation start.

        ``project_dir`` -- not the netlist's dirname -- is what ngspice runs
        in (``_configure_process`` sets it as the working directory), so it
        is the directory ivlng will resolve the model name from.

        Staging only: a model that was never built, or whose build output is
        gone, is left to the existing error path in the netlister and to
        ngspice itself. copy2 preserves the source mtime, so a refreshed
        model compares equal on the next run and is not copied again.
        """
        refreshed: List[str] = []
        for name in NgspiceWidget._dcosim_model_names(netlist):
            src = CosimConfig.cosim_vvp_path(name)
            if not src or not os.path.isfile(src):
                continue
            dst = os.path.join(project_dir, name)
            if os.path.isdir(dst):
                # copy2 would happily write INSIDE it (<dst>/<name>), leaving
                # ivlng to load a directory. Report instead.
                if log is not None:
                    log.error('d_cosim: cannot stage the vvp for "%s": %s is '
                              'a directory' % (name, dst))
                continue
            try:
                staged = os.path.isfile(dst)
                if staged and os.path.getmtime(dst) >= os.path.getmtime(src):
                    continue
                shutil.copy2(src, dst)
            except OSError as error:
                if log is not None:
                    log.error('d_cosim: could not refresh the staged vvp for '
                              '"%s": %s' % (name, str(error)))
                continue
            refreshed.append(name)
            if log is not None:
                log.info('d_cosim: %s vvp for "%s" -> %s'
                         % ("restaged newer" if staged else "staged missing",
                            name, dst))
        return refreshed

    def _is_linux(self) -> bool:
        return os.name != "nt"

    # Terminal emulators that can host the interactive ngspice plot session,
    # in preference order. Each entry is (binary, args-before-the-command);
    # the shell command string is appended to that list. xterm keeps its
    # window open with -hold; gnome-terminal separates its own args with --.
    _TERMINALS = (
        ('xterm', ['-hold', '-e', 'sh', '-c']),
        ('x-terminal-emulator', ['-e', 'sh', '-c']),
        ('gnome-terminal', ['--', 'sh', '-c']),
        ('konsole', ['-e', 'sh', '-c']),
    )

    @classmethod
    def _resolve_terminal(cls):
        """Return (path, args-template) for the first installed terminal, else
        None. Modern Ubuntu/GNOME ships no xterm, so falling back keeps the
        interactive plot feature working instead of silently doing nothing."""
        for binary, template in cls._TERMINALS:
            path = shutil.which(binary)
            if path:
                return path, template
        return None

    def _start_gaw_process(self) -> None:
        """Launch the GTK analog wave viewer on the rawfile.

        Only called after the batch run has finished and actually written the
        rawfile — starting it in __init__ (as before) opened gaw on a file that
        ngspice had not produced yet, flashing an empty viewer on every run.

        gaw is a bonus viewer: if it isn't installed, log and skip silently (no
        dialog — the xterm ngspice plot is the primary path).
        """
        if not shutil.which('gaw'):
            logger.info("gaw not installed; skipping analog wave viewer.")
            return
        try:
            self.gaw_process = QtCore.QProcess(self)
            self.gaw_command = f"gaw {shlex.quote(self.raw_file)}"
            self.gaw_process.errorOccurred.connect(
                lambda err: logger.error(f"gaw process error: {err}"))
            self.gaw_process.start('sh', ['-c', self.gaw_command])
            logger.info(f"Started GAW with command: {self.gaw_command}")
        except Exception as e:
            logger.error(f"Failed to start GAW process: {e}")

    def _queue_console(self, text: str) -> None:
        """Buffer console text; a 50 ms single-shot timer flushes it in one
        insert. Coalesces the readyRead bursts of a chatty simulation."""
        self._console_buffer.append(text)
        if not self._console_flush_timer.isActive():
            self._console_flush_timer.start()

    def _flush_console(self) -> None:
        """Write buffered text in one insert. Auto-scroll only when the user is
        already at the bottom, so scrolling back through the log isn't yanked."""
        if not self._console_buffer:
            return
        text = ''.join(self._console_buffer)
        self._console_buffer.clear()
        console = self.terminal_ui.simulationConsole
        scrollbar = console.verticalScrollBar()
        at_bottom = scrollbar.value() >= scrollbar.maximum() - 4
        console.insertPlainText(text)
        if at_bottom:
            scrollbar.setValue(scrollbar.maximum())

    @pyqtSlot()
    def _handle_stdout(self) -> None:
        try:
            data = self.process.readAllStandardOutput().data()
            if data:
                text = self._stdout_decoder.decode(data)
                if text:
                    self._queue_console(text)
        except Exception as e:
            logger.error(f"Error reading stdout: {e}")

    @pyqtSlot()
    def _handle_stderr(self) -> None:
        """Read stderr, filter batch-mode noise, display the rest."""
        try:
            data = self.process.readAllStandardError().data()
            if not data:
                return
            text = self._stderr_decoder.decode(data)
            if not text:
                return
            filtered = '\n'.join(
                line for line in text.split('\n')
                if 'PrinterOnly' not in line and 'viewport for graphics' not in line
            )
            if filtered.strip():
                self._queue_console(filtered)
        except Exception as e:
            logger.error(f"Error reading stderr: {e}")

    def finish_simulation(self, exit_code: Optional[int],
                         exit_status: Optional[QtCore.QProcess.ExitStatus],
                         sim_end_signal: pyqtSignal,
                         has_error_occurred: bool) -> None:
        # Skip finished signal if cancellation triggered both finished and error signals
        if not has_error_occurred and self.terminal_ui.simulationCancelled:
            return

        # A hard ngspice crash fires BOTH errorOccurred(Crashed) and
        # finished(...), so this method is entered twice for one run: two
        # stacked failure dialogs, a double _unregister_process, and
        # sim_end_signal (hence plotSimulationData) emitted twice. One-shot it.
        # The abandon reporter shares this same flag, so a mid-run dock close
        # followed by a late finished() cannot double-report either.
        if self._run_state['finished']:
            return
        self._run_state['finished'] = True

        # Drop both process signals now that this run is finalized, so the twin
        # signal a crash emits (errorOccurred + finished, in either order)
        # cannot re-enter this method at all. The early-return above already
        # makes re-entry harmless; this also keeps it from happening.
        for signal in (self.process.finished, self.process.errorOccurred):
            try:
                signal.disconnect()
            except (TypeError, RuntimeError):
                pass

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
            # Drain any buffered console output before the verdict banner so
            # "Simulation Completed/Failed" lands after the last ngspice line.
            self._flush_console()
            self._update_ui_after_simulation()

            if self.uses_dcosim:
                # Record the co-sim verdict where developers can grep it.
                dlog = CosimLog()
                if self._is_simulation_successful(
                        exit_status, exit_code, error_type):
                    dlog.ok("d_cosim run finished OK (ngspice rc=%s)."
                            % str(exit_code))
                else:
                    dlog.error("d_cosim run FAILED (ngspice rc=%s)."
                               % str(exit_code))
                    dlog.fix("Check the ngspice console above. If it mentions "
                             "ivlng/libvvp, the model failed to load -- rebuild "
                             "it in the NgVeri tab and confirm libvvp is found.")

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
                self._write_error_log()
                self._show_failure_message(error_type)

            self._scroll_terminal_to_bottom()
        except Exception as e:
            logger.error(f"finish_simulation UI error: {e}", exc_info=True)
        finally:
            # Drop the finished process from the shared registries so they don't
            # accumulate dead references across a long session.
            self._unregister_process()
            # Emit completion signal — must always run so plot window can open
            sim_end_signal.emit(exit_status, exit_code)

    def open_ngspice_plots(self) -> None:
        logger.info("Opening NGSpice native plots")

        if os.name == 'nt':
            try:
                # self.ngspice_bin is a console build with no graphics device,
                # so its `plot` only ever answers "Can't open viewport for
                # graphics". Plots need the wingui twin shipped beside it, which
                # owns its console window -- no mintty, so this works on Compact
                # installs that carry no MSYS2 too.
                gui_bin = CosimConfig.ngspice_gui_binary()
                if not gui_bin:
                    Dialogs.warning(
                        self, "Interactive plots unavailable",
                        "The graphics-capable ngspice (ngspice_gui.exe) was not "
                        "found next to:\n" + self.ngspice_bin + "\n\n"
                        "eSim's simulation ngspice is a console build and cannot "
                        "draw plot windows. Reinstall eSim to get it.\n\n"
                        "Your waveforms are already available in eSim's own "
                        "plotting window.")
                    logger.warning("ngspice_gui.exe not found; skipping nt plots.")
                    return

                self.plot_process = QtCore.QProcess(self)
                self.plot_process.setWorkingDirectory(self.project_dir)
                self.plot_process.errorOccurred.connect(
                    lambda err: logger.error(f"ngspice_gui plot error: {err}"))
                env = QtCore.QProcessEnvironment.systemEnvironment()
                # d_cosim re-runs need ivlng.dll (codemodel dir) and libvvp
                # on the loader path (PATH on nt), exactly like the batch run.
                if self.uses_dcosim:
                    for extra in (CosimConfig.iverilog_libdir(),
                                  CosimConfig.ngspice_codemodel_dir()):
                        if extra:
                            env.insert('PATH', extra + os.pathsep +
                                       env.value('PATH', ''))
                # mintty/bash for any NGHDL testbench relaunched by the model.
                msys_home = CosimConfig.nghdl_cfg('COMPILER', 'MSYS_HOME')
                if msys_home and os.path.isdir(msys_home):
                    env.insert('PATH', os.path.join(msys_home, 'usr', 'bin') +
                               os.pathsep + env.value('PATH', ''))
                self.plot_process.setProcessEnvironment(env)
                # The netlist's own .control block re-runs the analysis and
                # replays its `plot` lines, so no -r/-p is needed: hand over the
                # netlist and let the window sit at the ngspice prompt.
                self.plot_process.start(gui_bin, [self.command])
                self._register_process(self.plot_process)
                logger.info(f"Started ngspice_gui: {gui_bin} {self.command}")

            except Exception as e:
                logger.error(f"Failed to start Windows NGSpice plots: {e}")

        else:  # Linux/Unix
            try:
                # Re-run the netlist in an interactive ngspice so the user gets
                # a plot prompt with the vectors loaded. NOTE: passing the
                # rawfile as a positional arg does NOT work -- ngspice parses it
                # as a netlist and aborts ("UTF-8 syntax error ... fatal error").
                # Loading a raw needs the interactive `load` command, which the
                # batch '-r' output path doesn't give us, so we re-source the
                # netlist (wasteful but correct).
                # d_cosim runs need libvvp on the loader path for ngspice's
                # ivlng adapter; prepend it for this xterm only.
                ld_prefix = ""
                if self.uses_dcosim:
                    iv_lib = CosimConfig.iverilog_libdir()
                    if iv_lib:
                        var = CosimConfig.loader_path_var()
                        ld_prefix = (f"{var}={shlex.quote(iv_lib)}:"
                                     f"${{{var}}} ")
                # Quote all paths so spaces in project names don't break the shell command
                xterm_command = (
                    f"cd {shlex.quote(self.project_dir)} && "
                    f"{ld_prefix}{shlex.quote(self.ngspice_bin)} "
                    f"-r {shlex.quote(self.raw_file)} {shlex.quote(self.command)}"
                )
                terminal = self._resolve_terminal()
                if terminal is None:
                    Dialogs.warning(
                        self, "Terminal emulator not found",
                        "Interactive ngspice plots need a terminal emulator "
                        "(e.g. xterm). None was found on this system.\n\n"
                        "Install one — for example: sudo apt install xterm")
                    logger.warning(
                        "No terminal emulator found; skipping ngspice plots.")
                    return
                terminal_bin, template = terminal
                self.xterm_process = QtCore.QProcess(self)
                self.xterm_process.errorOccurred.connect(
                    lambda err: logger.error(f"Plot terminal error: {err}"))
                self.xterm_process.start(terminal_bin, template + [xterm_command])
                self._register_process(self.xterm_process)
                logger.info(f"Started {terminal_bin}: {xterm_command}")

                # Launch the GTK analog wave viewer now that the rawfile exists.
                self._start_gaw_process()

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
        return (exit_status == QtCore.QProcess.ExitStatus.NormalExit
                and exit_code == 0)

    def _show_cancellation_message(self) -> None:
        message_dialog = Dialogs.make_message_box(self)
        message_dialog.setModal(True)
        message_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        message_dialog.setWindowTitle("Warning Message")
        message_dialog.setText("Simulation was cancelled.")
        message_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        message_dialog.exec()

    def _show_success_message(self) -> None:
        success_message = self.SUCCESS_FORMAT.format("Simulation Completed Successfully!")
        self.terminal_ui.simulationConsole.appendHtml(success_message)

    def _show_failure_message(self, error_type: QtCore.QProcess.ProcessError) -> None:
        failure_message = self.FAILURE_FORMAT.format("Simulation Failed!")
        self.terminal_ui.simulationConsole.appendHtml(failure_message)

        error_message = self._get_error_message(error_type)
        error_dialog = Dialogs.make_error_message(self)
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
