"""Unit tests for src/toolManager/utils.py and for importing the Windows
backend on other platforms.

utils.py is imported by tool_manager_windows.py; both used to call
get_mysys2_path() unguarded at import time. Off Windows that printed an
"[ERROR]" line (which the GUI treats as a failed operation) and left
MSYS2_PATH undefined, so the MSYS2 helpers raised NameError.
"""
import subprocess
import sys

import pytest


@pytest.fixture
def utils_linux(fresh_import):
    return fresh_import("utils", "linux")


# --------------------------------------------------------------------------- #
#  Import safety (regressions)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("module", ["utils", "tool_manager_windows"])
@pytest.mark.parametrize("plat", ["linux", "darwin"])
def test_import_off_windows_is_silent(fresh_import, capsys, module, plat):
    mod = fresh_import(module, plat)
    out = capsys.readouterr()
    assert out.out == "" and out.err == ""
    assert mod.MSYS2_PATH is None


def test_msys2_helpers_return_none_off_windows(utils_linux):
    assert utils_linux.get_msys2_bash() is None
    assert utils_linux.get_msys2_mingw_bin() is None


def test_windows_backend_dispatch_table_loads_off_windows(fresh_import):
    tmw = fresh_import("tool_manager_windows", "linux")
    assert set(tmw.TOOLS) >= {"kicad", "ngspice", "llvm", "ghdl", "verilator",
                              "esim", "chocolatey"}


# --------------------------------------------------------------------------- #
#  MSYS2 helpers on Windows (preserved behaviour)
# --------------------------------------------------------------------------- #
class TestMsys2OnWindows:
    @pytest.fixture
    def utils_win(self, fresh_import, monkeypatch, tmp_path):
        monkeypatch.setenv("MSYS2_PATH", str(tmp_path))
        return fresh_import("utils", "win32")

    def test_msys2_path_comes_from_platform_utils(self, utils_win, tmp_path):
        assert str(utils_win.MSYS2_PATH) == str(tmp_path)

    def test_bash_found(self, utils_win, tmp_path):
        bash = tmp_path / "usr" / "bin" / "bash.exe"
        bash.parent.mkdir(parents=True)
        bash.write_text("")
        assert utils_win.get_msys2_bash() == bash

    def test_bash_missing(self, utils_win):
        assert utils_win.get_msys2_bash() is None

    def test_mingw64_preferred_over_ucrt64(self, utils_win, tmp_path):
        for sub in ("ucrt64", "mingw64"):
            (tmp_path / sub / "bin").mkdir(parents=True)
        assert utils_win.get_msys2_mingw_bin() == tmp_path / "mingw64" / "bin"

    def test_falls_back_to_ucrt64(self, utils_win, tmp_path):
        (tmp_path / "ucrt64" / "bin").mkdir(parents=True)
        assert utils_win.get_msys2_mingw_bin() == tmp_path / "ucrt64" / "bin"

    def test_no_mingw_dir(self, utils_win):
        assert utils_win.get_msys2_mingw_bin() is None


# --------------------------------------------------------------------------- #
#  Command helpers and status output
# --------------------------------------------------------------------------- #
def test_print_status_strips_newlines(utils_linux, capsys):
    utils_linux.print_status("installed", "42\r\n", "latest")
    assert capsys.readouterr().out == "installed|42|latest\n"


def test_print_status_keeps_falsy_installed(utils_linux, capsys):
    utils_linux.print_status("not_installed", None, "latest")
    assert capsys.readouterr().out == "not_installed|None|latest\n"


def test_run_cmd_safe_returns_result(utils_linux, monkeypatch):
    seen = {}

    def fake_run(cmd, **kw):
        seen.update(kw)
        return subprocess.CompletedProcess(cmd, 0, stdout="ok", stderr="")

    monkeypatch.setattr(utils_linux.subprocess, "run", fake_run)
    result = utils_linux.run_cmd_safe(["tool", "--version"], timeout=5)
    assert result.stdout == "ok"
    assert seen["timeout"] == 5 and seen["shell"] is False


@pytest.mark.parametrize("exc", [FileNotFoundError("tool"),
                                 subprocess.TimeoutExpired("tool", 5)])
def test_run_cmd_safe_returns_none_on_error(utils_linux, monkeypatch, exc):
    def fake_run(cmd, **kw):
        raise exc

    monkeypatch.setattr(utils_linux.subprocess, "run", fake_run)
    assert utils_linux.run_cmd_safe(["tool"]) is None


def test_run_cmd_stream_streams_and_collects_output(utils_linux, capsys):
    rc, out = utils_linux.run_cmd_stream(
        [sys.executable, "-c", "print('one'); print(); print('two')"],
        timeout=60)
    assert rc == 0
    assert out == "one\ntwo"
    assert capsys.readouterr().out.splitlines() == ["one", "two"]


def test_run_cmd_stream_missing_command(utils_linux):
    rc, out = utils_linux.run_cmd_stream(["definitely-not-a-real-command-xyz"])
    assert rc == -1 and out


def test_run_cmd_stream_closes_its_output_pipe(utils_linux, monkeypatch):
    """Regression: the pipe was left open, which surfaced as a
    ResourceWarning (and a failure under -W error) when it was collected."""
    procs = []
    real_popen = subprocess.Popen

    def recording_popen(*args, **kwargs):
        procs.append(real_popen(*args, **kwargs))
        return procs[-1]

    monkeypatch.setattr(utils_linux.subprocess, "Popen", recording_popen)
    utils_linux.run_cmd_stream([sys.executable, "-c", "print('x')"], timeout=60)
    assert procs[0].stdout.closed
