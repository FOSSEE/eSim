"""Unit tests for src/toolManager/tool_manager_linux.py.

Package-manager detection, elevation (pkexec/sudo) and the "is it installed?"
lookup are all mocked: tests record the command that WOULD run instead of
running it, so they need no root, no package manager and no EDA tools, and
behave the same on Windows and on Linux CI.
"""
import contextlib
import subprocess
import sys
import types

import pytest


@pytest.fixture
def tml(fresh_import, monkeypatch):
    monkeypatch.delenv("WSL_DISTRO_NAME", raising=False)
    mod = fresh_import("tool_manager_linux", "linux")
    monkeypatch.setattr(mod, "_IS_WSL", False)
    return mod


class FakeSystem:
    """Stands in for the package manager, elevation and installed-tool lookup."""

    def __init__(self, mod, monkeypatch, pm="apt", rc=0, fake_lock=True):
        self.pm = pm
        self.rc = rc                  # exit code of the elevated command
        self.installed = {}           # tool -> location
        self.commands = []            # every elevated command, in order
        self.streamed = []            # every non-elevated command (_stream)
        self.events = []              # "run" and lock events, in order

        monkeypatch.setattr(mod, "detect_package_manager", lambda: self.pm)
        monkeypatch.setattr(mod, "_run_elevated", self._run_elevated)
        monkeypatch.setattr(mod, "_stream", self._stream)
        monkeypatch.setattr(mod, "_find_installed", self.installed.get)
        if fake_lock:
            monkeypatch.setattr(mod, "_apt_lock", self._apt_lock)

    def _run_elevated(self, args):
        self.commands.append(list(args))
        self.events.append("run")
        return self.rc

    def _stream(self, args):
        self.streamed.append(list(args))
        return self.rc

    @contextlib.contextmanager
    def _apt_lock(self, pm="apt"):
        yield


def status_lines(out):
    """The machine-readable state|tool|detail lines the GUI parses."""
    return [l for l in out.splitlines() if l.count("|") == 2]


# --------------------------------------------------------------------------- #
#  Package selection and command construction
# --------------------------------------------------------------------------- #
# Expected commands are written out by hand (not read from PACKAGE_MAP /
# INSTALL_CMD), so a wrong package name or flag in the module is caught.
INSTALL_CASES = [
    ("apt", "kicad", ["apt-get", "install", "-y", "kicad", "kicad-footprints",
                      "kicad-libraries", "kicad-symbols", "kicad-templates"]),
    ("apt", "llvm", ["apt-get", "install", "-y", "clang", "llvm"]),
    ("dnf", "llvm", ["dnf", "install", "-y", "clang", "llvm-devel"]),
    ("yum", "ngspice", ["yum", "install", "-y", "ngspice"]),
    ("pacman", "kicad", ["pacman", "-S", "--noconfirm", "kicad",
                         "kicad-library", "kicad-library-3d"]),
    ("zypper", "verilator", ["zypper", "install", "--non-interactive",
                             "verilator"]),
]

UNINSTALL_CASES = [
    ("apt", "kicad", ["apt-get", "remove", "-y", "--autoremove", "kicad",
                      "kicad-footprints", "kicad-libraries", "kicad-symbols",
                      "kicad-templates"]),
    ("dnf", "llvm", ["dnf", "remove", "-y", "clang", "llvm-devel"]),
    ("yum", "kicad", ["yum", "remove", "-y", "kicad"]),
    ("pacman", "ghdl", ["pacman", "-Rs", "--noconfirm", "ghdl"]),
    ("zypper", "ngspice", ["zypper", "remove", "--non-interactive",
                           "--clean-deps", "ngspice"]),
]

PM_BINARY = {"apt": "apt-get", "dnf": "dnf", "yum": "yum",
             "pacman": "pacman", "zypper": "zypper"}
SUPPORTED = [(pm, tool) for pm in ("apt", "dnf", "pacman", "zypper")
             for tool in ("kicad", "ngspice", "ghdl", "verilator", "llvm")]


@pytest.mark.parametrize("pm,tool,expected", INSTALL_CASES)
def test_install_command(tml, monkeypatch, capsys, pm, tool, expected):
    fs = FakeSystem(tml, monkeypatch, pm=pm)
    fs.installed[tool] = f"/usr/bin/{tool}"

    assert tml.install_tool(tool, "latest") == tml.EXIT_OK
    assert fs.commands == [expected]
    assert status_lines(capsys.readouterr().out) == [
        f"installed|{tool}|/usr/bin/{tool}"]


@pytest.mark.parametrize("pm,tool,expected", UNINSTALL_CASES)
def test_uninstall_command(tml, monkeypatch, capsys, pm, tool, expected):
    fs = FakeSystem(tml, monkeypatch, pm=pm)   # tool absent after removal

    assert tml.uninstall_tool(tool, "none") == tml.EXIT_OK
    assert fs.commands == [expected]
    assert status_lines(capsys.readouterr().out) == [f"not_installed|{tool}|none"]


@pytest.mark.parametrize("pm,tool", SUPPORTED)
def test_every_supported_tool_installs_and_uninstalls(tml, monkeypatch, pm, tool):
    """Breadth check: each tool these managers support runs exactly one
    command with that manager and reports success."""
    fs = FakeSystem(tml, monkeypatch, pm=pm)
    fs.installed[tool] = f"/usr/bin/{tool}"
    assert tml.install_tool(tool, "latest") == tml.EXIT_OK
    fs.installed.clear()
    assert tml.uninstall_tool(tool, "none") == tml.EXIT_OK
    assert [c[0] for c in fs.commands] == [PM_BINARY[pm]] * 2


def test_package_map_and_commands_cover_the_same_managers(tml):
    assert set(tml.PACKAGE_MAP) == set(tml.INSTALL_CMD) == set(tml.UNINSTALL_CMD)


def test_update_uses_the_install_command(tml, monkeypatch):
    fs = FakeSystem(tml, monkeypatch, pm="dnf")
    fs.installed["ngspice"] = "/usr/bin/ngspice"
    assert tml.install_tool("ngspice", "latest", upgrade=True) == tml.EXIT_OK
    assert fs.commands == [["dnf", "install", "-y", "ngspice"]]


class TestCommandsRunInsideAptLock:
    """Uses the REAL _apt_lock with a fake fcntl, and checks the package
    command runs after the lock is taken and before it is released."""

    @pytest.fixture
    def fs(self, tml, monkeypatch, tmp_path):
        fs = FakeSystem(tml, monkeypatch, fake_lock=False)
        fake_fcntl = types.SimpleNamespace(
            LOCK_EX="lock", LOCK_UN="unlock",
            flock=lambda f, op: fs.events.append(op))
        monkeypatch.setitem(sys.modules, "fcntl", fake_fcntl)
        monkeypatch.setattr(tml, "_APT_LOCK_FILE", str(tmp_path / "apt.lock"))
        return fs

    def test_apt_install(self, tml, fs):
        fs.installed["ghdl"] = "/usr/bin/ghdl"
        tml.install_tool("ghdl", "latest")
        assert fs.events == ["lock", "run", "unlock"]

    def test_apt_uninstall(self, tml, fs):
        tml.uninstall_tool("ghdl", "none")
        assert fs.events == ["lock", "run", "unlock"]

    def test_lock_released_when_command_fails(self, tml, fs):
        fs.rc = 100
        tml.install_tool("ghdl", "latest")
        assert fs.events == ["lock", "run", "unlock"]

    @pytest.mark.parametrize("pm", ["dnf", "pacman", "zypper", "yum"])
    def test_other_managers_are_not_locked(self, tml, fs, pm):
        fs.pm = pm
        fs.installed["ngspice"] = "/usr/bin/ngspice"
        tml.install_tool("ngspice", "latest")
        assert fs.events == ["run"]


# --------------------------------------------------------------------------- #
#  install: never report success when nothing was installed (regressions)
# --------------------------------------------------------------------------- #
class TestInstallReportsHonestly:
    def test_no_package_manager_is_unsupported(self, tml, monkeypatch, capsys):
        fs = FakeSystem(tml, monkeypatch, pm=None)
        assert tml.install_tool("kicad", "latest") == tml.EXIT_UNSUPPORTED
        assert fs.commands == []
        assert "not_supported|kicad|none" in status_lines(capsys.readouterr().out)

    def test_detected_but_unmapped_manager_is_unsupported(self, tml,
                                                          monkeypatch, capsys):
        """platform_utils can detect 'apk' but there is no package map for it.
        This used to print not_supported and still exit 0 (= success)."""
        fs = FakeSystem(tml, monkeypatch, pm="apk")
        assert tml.install_tool("kicad", "latest") == tml.EXIT_UNSUPPORTED
        assert fs.commands == []
        assert status_lines(capsys.readouterr().out) == ["not_supported|kicad|apk"]

    @pytest.mark.parametrize("tool", ["ghdl", "verilator"])
    def test_empty_package_mapping_is_unsupported(self, tml, monkeypatch,
                                                  capsys, tool):
        """yum has no ghdl/verilator packages; this used to exit 0 after an
        [INFO] line, so the GUI said 'installed successfully'."""
        fs = FakeSystem(tml, monkeypatch, pm="yum")
        assert tml.install_tool(tool, "latest") == tml.EXIT_UNSUPPORTED
        assert fs.commands == []
        assert status_lines(capsys.readouterr().out) == [f"not_supported|{tool}|yum"]

    def test_unknown_tool_is_unsupported(self, tml, monkeypatch, capsys):
        fs = FakeSystem(tml, monkeypatch, pm="apt")
        assert tml.install_tool("nosuchtool", "latest") == tml.EXIT_UNSUPPORTED
        assert fs.commands == []
        assert status_lines(capsys.readouterr().out) == [
            "not_supported|nosuchtool|apt"]

    @pytest.mark.parametrize("pm", ["dnf", "pacman", "zypper", "yum"])
    def test_esim_on_non_apt_distro_is_unsupported(self, tml, monkeypatch,
                                                   capsys, pm):
        """eSim only installs via the apt script. Other distros used to get
        exit 0 and a link, which the GUI showed as a successful install."""
        fs = FakeSystem(tml, monkeypatch, pm=pm)
        assert tml.install_tool("esim", "2.4") == tml.EXIT_UNSUPPORTED
        assert fs.commands == [] and fs.streamed == []
        out = capsys.readouterr().out
        assert status_lines(out) == [f"not_supported|esim|{pm}"]
        assert "esim.fossee.in" in out

    def test_failed_package_command_is_a_failure(self, tml, monkeypatch, capsys):
        fs = FakeSystem(tml, monkeypatch, pm="apt", rc=100)
        fs.installed["kicad"] = "/usr/bin/kicad"   # e.g. an older copy
        assert tml.install_tool("kicad", "latest") == tml.EXIT_FAILED
        assert status_lines(capsys.readouterr().out) == ["install_failed|kicad|exit_100"]

    def test_command_succeeded_but_tool_missing_is_a_failure(self, tml,
                                                             monkeypatch, capsys):
        """Used to print install_failed but still return the package
        manager's exit code 0."""
        FakeSystem(tml, monkeypatch, pm="apt", rc=0)
        assert tml.install_tool("verilator", "latest") == tml.EXIT_FAILED
        assert status_lines(capsys.readouterr().out) == [
            "install_failed|verilator|not_found"]

    def test_failure_exit_code_never_collides_with_unsupported(self, tml,
                                                               monkeypatch):
        FakeSystem(tml, monkeypatch, pm="apt", rc=tml.EXIT_UNSUPPORTED)
        assert tml.install_tool("kicad", "latest") == tml.EXIT_FAILED


class TestEsimOnApt:
    @pytest.fixture
    def script(self, tml, monkeypatch, tmp_path):
        path = tmp_path / "install-eSim.sh"
        path.write_text("#!/bin/bash\n")
        monkeypatch.setattr(tml, "INSTALL_SH", path)
        return path

    @pytest.mark.parametrize("upgrade,flag", [(False, "--install"),
                                              (True, "--upgrade")])
    def test_install_runs_the_script(self, tml, monkeypatch, script,
                                     upgrade, flag):
        fs = FakeSystem(tml, monkeypatch, pm="apt")
        assert tml.install_tool("esim", "2.4", upgrade=upgrade) == tml.EXIT_OK
        assert fs.streamed == [["bash", str(script), flag]]
        assert fs.commands == []

    def test_script_failure_is_reported(self, tml, monkeypatch, capsys, script):
        FakeSystem(tml, monkeypatch, pm="apt", rc=2)
        assert tml.install_tool("esim", "2.4") == tml.EXIT_FAILED
        assert status_lines(capsys.readouterr().out) == ["install_failed|esim|exit_2"]

    def test_missing_script_is_a_failure(self, tml, monkeypatch, capsys, tmp_path):
        monkeypatch.setattr(tml, "INSTALL_SH", tmp_path / "missing.sh")
        fs = FakeSystem(tml, monkeypatch, pm="apt")
        assert tml.install_tool("esim", "2.4") == tml.EXIT_FAILED
        assert fs.streamed == []
        assert "install_failed|esim|script_missing" in capsys.readouterr().out

    def test_uninstall_runs_the_script(self, tml, monkeypatch, script):
        fs = FakeSystem(tml, monkeypatch, pm="apt")
        assert tml.uninstall_tool("esim", "none") == tml.EXIT_OK
        assert fs.streamed == [["bash", str(script), "--uninstall"]]

    def test_uninstall_script_failure_is_reported(self, tml, monkeypatch,
                                                  capsys, script):
        FakeSystem(tml, monkeypatch, pm="apt", rc=1)
        assert tml.uninstall_tool("esim", "none") == tml.EXIT_FAILED
        assert "uninstall_failed|esim|exit_1" in capsys.readouterr().out

    def test_uninstall_with_missing_script_is_a_failure(self, tml, monkeypatch,
                                                        capsys, tmp_path):
        """Used to fall through to 'Nothing to uninstall' and exit 0."""
        monkeypatch.setattr(tml, "INSTALL_SH", tmp_path / "missing.sh")
        FakeSystem(tml, monkeypatch, pm="apt")
        assert tml.uninstall_tool("esim", "none") == tml.EXIT_FAILED
        assert "uninstall_failed|esim|script_missing" in capsys.readouterr().out


# --------------------------------------------------------------------------- #
#  uninstall
# --------------------------------------------------------------------------- #
class TestUninstall:
    def test_failed_package_command_is_a_failure(self, tml, monkeypatch, capsys):
        fs = FakeSystem(tml, monkeypatch, pm="dnf", rc=1)
        fs.installed["ngspice"] = "/usr/bin/ngspice"
        assert tml.uninstall_tool("ngspice", "none") == tml.EXIT_FAILED
        assert status_lines(capsys.readouterr().out) == [
            "uninstall_failed|ngspice|exit_1"]

    def test_tool_still_present_is_a_failure(self, tml, monkeypatch, capsys):
        fs = FakeSystem(tml, monkeypatch, pm="apt", rc=0)
        fs.installed["kicad"] = "/usr/local/bin/kicad"
        assert tml.uninstall_tool("kicad", "none") == tml.EXIT_FAILED
        assert status_lines(capsys.readouterr().out) == [
            "uninstall_failed|kicad|still_found"]

    def test_no_package_manager_is_unsupported(self, tml, monkeypatch):
        FakeSystem(tml, monkeypatch, pm=None)
        assert tml.uninstall_tool("kicad", "none") == tml.EXIT_UNSUPPORTED

    @pytest.mark.parametrize("pm,tool", [("apk", "kicad"), ("yum", "ghdl"),
                                         ("dnf", "esim")])
    def test_nothing_to_remove_when_absent_is_success(self, tml, monkeypatch,
                                                      capsys, pm, tool):
        fs = FakeSystem(tml, monkeypatch, pm=pm)
        assert tml.uninstall_tool(tool, "none") == tml.EXIT_OK
        assert fs.commands == []
        assert status_lines(capsys.readouterr().out) == [f"not_installed|{tool}|none"]

    @pytest.mark.parametrize("pm,tool", [("apk", "kicad"), ("yum", "ghdl"),
                                         ("dnf", "esim")])
    def test_present_but_unmanaged_is_unsupported(self, tml, monkeypatch,
                                                  capsys, pm, tool):
        """Used to claim not_installed (exit 0) even though the tool was
        still on the system."""
        fs = FakeSystem(tml, monkeypatch, pm=pm)
        fs.installed[tool] = f"/opt/{tool}/bin/{tool}"
        assert tml.uninstall_tool(tool, "none") == tml.EXIT_UNSUPPORTED
        assert fs.commands == []
        assert status_lines(capsys.readouterr().out) == [f"not_supported|{tool}|{pm}"]


# --------------------------------------------------------------------------- #
#  check / _find_installed
# --------------------------------------------------------------------------- #
class TestCheck:
    def test_binary_on_path(self, tml, monkeypatch, capsys):
        monkeypatch.setattr(tml, "_which_native",
                            lambda b: "/usr/bin/ngspice" if b == "ngspice" else None)
        assert tml.check_tool("ngspice", "none") == 0
        assert capsys.readouterr().out.strip() == "installed|ngspice|/usr/bin/ngspice"

    def test_any_listed_binary_counts(self, tml, monkeypatch):
        monkeypatch.setattr(tml, "_which_native",
                            lambda b: "/usr/bin/llvm-config" if b == "llvm-config" else None)
        assert tml._find_installed("llvm") == "/usr/bin/llvm-config"

    def test_not_installed_on_non_apt(self, tml, monkeypatch, capsys):
        monkeypatch.setattr(tml, "_which_native", lambda b: None)
        monkeypatch.setattr(tml, "detect_package_manager", lambda: "dnf")
        monkeypatch.setattr(tml.subprocess, "run", pytest.fail)  # no dpkg here
        assert tml.check_tool("ghdl", "none") == 1
        assert capsys.readouterr().out.strip() == "not_installed|ghdl|none"

    @pytest.mark.parametrize("stdout,rc,expected", [
        ("Status: install ok installed\n", 0, "dpkg"),
        ("Status: deinstall ok config-files\n", 0, None),
        ("", 1, None),
    ])
    def test_dpkg_fallback_on_apt(self, tml, monkeypatch, stdout, rc, expected):
        monkeypatch.setattr(tml, "_which_native", lambda b: None)
        monkeypatch.setattr(tml, "detect_package_manager", lambda: "apt")
        calls = []

        def fake_run(cmd, **kw):
            calls.append(cmd)
            return subprocess.CompletedProcess(cmd, rc, stdout=stdout, stderr="")

        monkeypatch.setattr(tml.subprocess, "run", fake_run)
        assert tml._find_installed("kicad") == expected
        assert calls == [["dpkg", "-s", "kicad"]]

    def test_missing_dpkg_does_not_crash(self, tml, monkeypatch):
        monkeypatch.setattr(tml, "_which_native", lambda b: None)
        monkeypatch.setattr(tml, "detect_package_manager", lambda: "apt")

        def no_dpkg(cmd, **kw):
            raise FileNotFoundError(cmd[0])

        monkeypatch.setattr(tml.subprocess, "run", no_dpkg)
        assert tml._find_installed("kicad") is None


# --------------------------------------------------------------------------- #
#  Elevation, WSL handling and the apt lock
# --------------------------------------------------------------------------- #
class TestElevation:
    @pytest.fixture
    def streamed(self, tml, monkeypatch):
        calls = []
        monkeypatch.setattr(tml, "_stream", lambda args: calls.append(args) or 0)
        return calls

    def _which(self, available):
        return lambda name: f"/usr/bin/{name}" if name in available else None

    def test_prefers_pkexec_when_usable(self, tml, monkeypatch, streamed):
        monkeypatch.setattr(tml.shutil, "which", self._which({"pkexec", "sudo"}))
        monkeypatch.setattr(tml, "_pkexec_usable", lambda: True)
        tml._run_elevated(["apt-get", "install", "-y", "x"])
        assert streamed == [["/usr/bin/pkexec", "apt-get", "install", "-y", "x"]]

    def test_falls_back_to_sudo(self, tml, monkeypatch, streamed):
        monkeypatch.setattr(tml.shutil, "which", self._which({"pkexec", "sudo"}))
        monkeypatch.setattr(tml, "_pkexec_usable", lambda: False)
        tml._run_elevated(["dnf", "install", "-y", "x"])
        assert streamed == [["/usr/bin/sudo", "-S", "dnf", "install", "-y", "x"]]

    def test_runs_unelevated_when_nothing_available(self, tml, monkeypatch,
                                                    streamed):
        monkeypatch.setattr(tml.shutil, "which", self._which(set()))
        tml._run_elevated(["pacman", "-S", "x"])
        assert streamed == [["pacman", "-S", "x"]]

    def test_pkexec_not_usable_on_wsl(self, tml, monkeypatch):
        monkeypatch.setattr(tml, "_IS_WSL", True)
        monkeypatch.setenv("DISPLAY", ":0")
        assert tml._pkexec_usable() is False

    def test_pkexec_needs_a_display(self, tml, monkeypatch):
        monkeypatch.delenv("DISPLAY", raising=False)
        monkeypatch.delenv("WAYLAND_DISPLAY", raising=False)
        assert tml._pkexec_usable() is False
        monkeypatch.setenv("WAYLAND_DISPLAY", "wayland-0")
        assert tml._pkexec_usable() is True

    def test_wsl_detected_from_environment(self, tml, monkeypatch):
        monkeypatch.setenv("WSL_DISTRO_NAME", "Ubuntu")
        assert tml._detect_wsl() is True

    def test_which_native_off_wsl_uses_shutil_which(self, tml, monkeypatch):
        monkeypatch.setattr(tml.shutil, "which", lambda b: "/usr/bin/" + b)
        assert tml._which_native("ghdl") == "/usr/bin/ghdl"


class TestAptLock:
    def test_non_apt_managers_do_not_lock(self, tml, monkeypatch):
        # Would fail if it tried to import fcntl or open the lock file.
        monkeypatch.setattr(tml, "_APT_LOCK_FILE", "/nonexistent/dir/lock")
        with tml._apt_lock("dnf"):
            pass

    def test_apt_takes_and_releases_an_exclusive_lock(self, tml, monkeypatch,
                                                      tmp_path):
        # A fake fcntl keeps this test runnable on Windows too.
        calls = []
        fake_fcntl = types.SimpleNamespace(
            LOCK_EX="EX", LOCK_UN="UN",
            flock=lambda f, op: calls.append(op))
        monkeypatch.setitem(sys.modules, "fcntl", fake_fcntl)
        monkeypatch.setattr(tml, "_APT_LOCK_FILE", str(tmp_path / "apt.lock"))

        with tml._apt_lock("apt"):
            assert calls == ["EX"]
        assert calls == ["EX", "UN"]
