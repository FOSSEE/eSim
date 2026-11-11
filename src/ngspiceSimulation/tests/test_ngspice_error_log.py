"""A failed run's console is kept as <project>/ngspice_error.log.

The AI assistant reads that file to explain the failure. Each run removes
the previous log when it starts, so a later cancelled or abandoned run can
never be explained with a stale one. Like test_ngspice_widget, these avoid
constructing the widget, which would launch ngspice.
"""
from unittest.mock import MagicMock

import pytest
from PyQt6 import QtCore

from ngspiceSimulation.NgspiceWidget import NgspiceWidget


def _widget(tmp_path, console="", cancelled=False, succeeded=False):
    widget = MagicMock()
    widget.project_dir = str(tmp_path)
    widget.terminal_ui.simulationConsole.toPlainText.return_value = console
    widget.terminal_ui.simulationCancelled = cancelled
    widget._run_state = {'finished': False}
    widget.uses_dcosim = False
    widget.process.error.return_value = \
        QtCore.QProcess.ProcessError.UnknownError
    widget._is_simulation_successful.return_value = succeeded
    widget._error_log_path.side_effect = \
        lambda: NgspiceWidget._error_log_path(widget)
    return widget


def test_error_log_lives_in_the_project_directory(tmp_path):
    widget = _widget(tmp_path)

    assert NgspiceWidget._error_log_path(widget) == \
        str(tmp_path / "ngspice_error.log")


def test_failed_run_console_is_saved(tmp_path):
    console = "Error: unknown subckt: x1\nSimulation interrupted due to error!\n"
    widget = _widget(tmp_path, console=console)

    NgspiceWidget._write_error_log(widget)

    assert (tmp_path / "ngspice_error.log").read_text() == console


def test_unwritable_project_does_not_break_the_run(tmp_path):
    widget = _widget(tmp_path / "missing-dir", console="Error")

    NgspiceWidget._write_error_log(widget)  # must not raise


def test_run_start_removes_the_previous_log(tmp_path):
    log = tmp_path / "ngspice_error.log"
    log.write_text("old failure")
    widget = _widget(tmp_path)

    NgspiceWidget._clear_error_log(widget)
    NgspiceWidget._clear_error_log(widget)  # already gone: still fine

    assert not log.exists()


def test_every_run_start_clears_the_log(tmp_path):
    widget = _widget(tmp_path)

    NgspiceWidget._on_process_started(widget)

    widget._clear_error_log.assert_called_once()


@pytest.mark.parametrize("succeeded, cancelled, saved", [
    (False, False, True),    # ngspice failed
    (True, False, False),    # clean run
    (False, True, False),    # user cancelled
])
def test_log_is_saved_only_for_real_failures(tmp_path, succeeded, cancelled, saved):
    widget = _widget(tmp_path, succeeded=succeeded, cancelled=cancelled)

    NgspiceWidget.finish_simulation(
        widget, 1, QtCore.QProcess.ExitStatus.NormalExit, MagicMock(), False)

    assert widget._write_error_log.called is saved


def test_saved_log_is_ngspice_output_without_esim_console_lines(tmp_path):
    console = ("[eSim] Starting ngspice ...\n"
               "[eSim] /usr/bin/ngspice -b -r rc.raw rc.cir.out\n"
               "[eSim] ngspice running (PID 42)\n"
               "Error: unknown subckt: x1\n")
    widget = _widget(tmp_path, console=console)

    NgspiceWidget._write_error_log(widget)

    assert (tmp_path / "ngspice_error.log").read_text() == "Error: unknown subckt: x1\n"
