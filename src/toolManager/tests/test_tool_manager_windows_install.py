"""Unit tests for the ngspice and KiCad install logic in tool_manager_windows.py.

Chocolatey and the KiCad cleanup are always mocked, so these tests run on any
OS without Chocolatey, admin rights or EDA tools. Most tests also replace the
installed-tool lookups to drive the install flow; the "already installed"
decisions are tested at the end against the REAL find_ngspice_safe() and
find_kicad_fixed(), with only Chocolatey's output, the registry and the file
system faked. The module is imported with a non-Windows platform so it does
not re-wrap sys.stdout (which it does on real Windows).
"""
import subprocess
import sys
import types

import pytest


@pytest.fixture
def tmw(fresh_import, monkeypatch):
    mod = fresh_import("tool_manager_windows", "linux")
    monkeypatch.setattr(mod.time, "sleep", lambda s: None)
    return mod


class FakeChoco:
    """Records every command the installer would run."""

    def __init__(self, mod, monkeypatch, rc=0, available=True):
        self.rc = rc
        self.commands = []
        monkeypatch.setattr(mod, "find_chocolatey",
                            lambda v=None: ("choco", "2.2.2") if available else (None, None))
        monkeypatch.setattr(mod, "run_cmd_stream", self._stream)
        monkeypatch.setattr(mod, "run_cmd_safe", self._safe)

    def _stream(self, cmd, timeout=900, **kw):
        self.commands.append(list(cmd))
        return self.rc, "" if self.rc == 0 else "Chocolatey installed 0/1 packages"

    def _safe(self, cmd, timeout=30, **kw):
        self.commands.append(list(cmd))
        return None

    def ran(self, word):
        """Commands whose choco sub-command is *word* (install/upgrade/uninstall)."""
        return [c for c in self.commands if len(c) > 1 and c[1] == word]


def last_status(out):
    return [l for l in out.splitlines() if l.count("|") == 2][-1]


def version_arg(cmd):
    return cmd[cmd.index("--version") + 1]


# --------------------------------------------------------------------------- #
#  _version_satisfies
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("installed,target,expected", [
    ("42", "42", True),
    ("42.1", "42", True),
    ("9.0.7", "9", True),
    ("9.x", "9", True),
    ("41", "42", False),
    ("4", "42", False),
    ("42", "4", False),        # "42" must not satisfy version "4"
    ("unknown", "42", False),
    (None, "42", False),
    ("unknown", "latest", True),
])
def test_version_satisfies(tmw, installed, target, expected):
    assert tmw._version_satisfies(installed, target) is expected


# --------------------------------------------------------------------------- #
#  install_ngspice
# --------------------------------------------------------------------------- #
class TestInstallNgspice:
    def _installed(self, tmw, monkeypatch, *states):
        """find_ngspice_safe returns each state in turn (last one repeats);
        the executable from the first state is what is on disk beforehand."""
        states = list(states)
        exe_before = states[0][0]

        def fake_find(version=None):
            return states.pop(0) if len(states) > 1 else states[0]

        monkeypatch.setattr(tmw, "find_ngspice_safe", fake_find)
        monkeypatch.setattr(tmw, "_find_ngspice_exe", lambda: exe_before)

    def test_fresh_install_succeeds(self, tmw, monkeypatch, capsys):
        choco = FakeChoco(tmw, monkeypatch)
        self._installed(tmw, monkeypatch, (None, None), ("C:/ngspice.exe", "42"))
        tmw.install_ngspice("42")
        assert choco.ran("install") == [[
            "choco", "install", "ngspice", "--version", "42", "-y",
            "--no-progress", "--allow-downgrade", "--force"]]
        assert last_status(capsys.readouterr().out) == "installed|42|42"

    def test_never_uninstalls_before_installing(self, tmw, monkeypatch):
        """Regression: install_ngspice used to run 'choco uninstall ngspice'
        first, so a failed install left the user with no ngspice at all."""
        choco = FakeChoco(tmw, monkeypatch, rc=1)
        self._installed(tmw, monkeypatch, ("C:/ngspice.exe", "41"))
        tmw.install_ngspice("42")
        assert choco.ran("uninstall") == []
        assert len(choco.ran("install")) == 1

    def test_failed_install_reports_failure(self, tmw, monkeypatch, capsys):
        FakeChoco(tmw, monkeypatch, rc=1)
        self._installed(tmw, monkeypatch, ("C:/ngspice.exe", "41"))
        tmw.install_ngspice("42")
        state, detail, target = last_status(capsys.readouterr().out).split("|")
        assert (state, target) == ("install_failed", "42")
        assert detail                      # carries a hint from choco's output

    def test_unknown_installed_version_still_installs_requested(self, tmw,
                                                                monkeypatch):
        choco = FakeChoco(tmw, monkeypatch)
        self._installed(tmw, monkeypatch, ("C:/ngspice.exe", "unknown"))
        tmw.install_ngspice("40")
        assert [version_arg(c) for c in choco.ran("install")] == ["40"]

    def test_switching_version_installs_over_existing(self, tmw, monkeypatch,
                                                      capsys):
        choco = FakeChoco(tmw, monkeypatch)
        self._installed(tmw, monkeypatch, ("C:/ngspice.exe", "42"),
                        ("C:/ngspice.exe", "38"))
        tmw.install_ngspice("38")
        assert choco.ran("uninstall") == []
        cmd = choco.ran("install")[0]
        assert version_arg(cmd) == "38" and "--allow-downgrade" in cmd
        assert last_status(capsys.readouterr().out) == "installed|38|38"

    def test_update_to_latest_uses_choco_upgrade(self, tmw, monkeypatch):
        choco = FakeChoco(tmw, monkeypatch)
        self._installed(tmw, monkeypatch, ("C:/ngspice.exe", "41"))
        tmw.install_ngspice("latest", upgrade=True)
        assert choco.ran("uninstall") == []
        assert choco.ran("upgrade") == [
            ["choco", "upgrade", "ngspice", "-y", "--no-progress"]]

    def test_update_reinstalls_even_when_version_matches(self, tmw, monkeypatch):
        choco = FakeChoco(tmw, monkeypatch)
        self._installed(tmw, monkeypatch, ("C:/ngspice.exe", "42"))
        tmw.install_ngspice("42", upgrade=True)
        assert len(choco.ran("install")) == 1

    def test_installed_but_not_found_afterwards(self, tmw, monkeypatch, capsys):
        FakeChoco(tmw, monkeypatch)
        self._installed(tmw, monkeypatch, (None, None))
        tmw.install_ngspice("42")
        assert last_status(capsys.readouterr().out) == "install_failed|not_found|42"

    def test_chocolatey_missing(self, tmw, monkeypatch, capsys):
        choco = FakeChoco(tmw, monkeypatch, available=False)
        self._installed(tmw, monkeypatch, (None, None))
        tmw.install_ngspice("42")
        assert choco.commands == []
        assert last_status(capsys.readouterr().out) == "install_failed|choco_missing|42"


# --------------------------------------------------------------------------- #
#  install_kicad: cleanup_kicad() removes KiCad, so it must not run needlessly
# --------------------------------------------------------------------------- #
class TestInstallKicad:
    @pytest.fixture
    def cleanups(self, tmw, monkeypatch):
        calls = []
        monkeypatch.setattr(tmw, "cleanup_kicad", lambda: calls.append(True))
        return calls

    def _installed(self, tmw, monkeypatch, *states):
        states = list(states)

        def fake_find(version=None):
            return states.pop(0) if len(states) > 1 else states[0]

        monkeypatch.setattr(tmw, "find_kicad_fixed", fake_find)

    def test_different_version_still_installs(self, tmw, monkeypatch, capsys,
                                              cleanups):
        """Switching major version keeps the existing cleanup + install flow."""
        choco = FakeChoco(tmw, monkeypatch)
        self._installed(tmw, monkeypatch, ("C:/KiCad/bin/kicad.exe", "8.0.9"),
                        ("C:/KiCad/bin/kicad.exe", "9.0.7"))
        tmw.install_kicad("9")
        assert cleanups == [True]
        assert choco.ran("install")[0][:5] == ["choco", "install", "kicad",
                                               "--version", "9.0.7"]
        assert last_status(capsys.readouterr().out) == "installed|9.0.7|9"

    def test_update_still_runs_full_install(self, tmw, monkeypatch, cleanups):
        choco = FakeChoco(tmw, monkeypatch)
        self._installed(tmw, monkeypatch, ("C:/KiCad/bin/kicad.exe", "9.0.7"))
        tmw.install_kicad("latest", upgrade=True)
        assert cleanups == [True]
        assert len(choco.ran("install")) == 1

    def test_not_installed_installs(self, tmw, monkeypatch, cleanups):
        choco = FakeChoco(tmw, monkeypatch)
        self._installed(tmw, monkeypatch, (None, None),
                        ("C:/KiCad/bin/kicad.exe", "9.0.7"))
        tmw.install_kicad("latest")
        assert len(choco.ran("install")) == 1

    def test_chocolatey_missing(self, tmw, monkeypatch, capsys, cleanups):
        FakeChoco(tmw, monkeypatch, available=False)
        self._installed(tmw, monkeypatch, (None, None))
        tmw.install_kicad("9")
        assert cleanups == []
        assert last_status(capsys.readouterr().out) == "install_failed|choco_missing|9"


# --------------------------------------------------------------------------- #
#  "Already installed?" decisions, using the REAL lookup functions
# --------------------------------------------------------------------------- #
CHOCO_V1_FEED = ("Chocolatey v1.4.0\n"
                 "ngspice 44.2 [Approved] Downloads cached for licensed users\n"
                 "1 packages found.\n")


def choco_v2_local(version):
    return f"Chocolatey v2.2.2\nngspice {version}\n1 packages installed.\n"


class _FakeRegKey:
    def __init__(self, entry=None):
        self.entry = entry

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class LookupHost:
    """A fake Windows machine for find_ngspice_safe() / find_kicad_fixed().

    Only the outside world is faked: what is on PATH, the output of
    "choco list", the default install folders (redirected into tmp_path) and
    the Uninstall registry key. The lookup functions themselves run unchanged.
    Installs are recorded, never executed.
    """

    def __init__(self, tmw, monkeypatch, tmp_path):
        self.tmp = tmp_path
        self.choco_list = None       # None: choco is not on PATH
        self.registry = []           # Uninstall entries (dicts)
        self.installs = []
        self.cleanups = []

        self.ngspice_exe = tmp_path / "ngspice" / "bin" / "ngspice.exe"
        monkeypatch.setattr(tmw, "WIN_NGSPICE_PATHS", [str(self.ngspice_exe)])
        monkeypatch.setattr(tmw, "WIN_KICAD_PATHS", [
            (str(self.kicad_exe(v)), v) for v in ("9", "8", "7", "6")])
        monkeypatch.setattr(tmw, "which", self._which)
        monkeypatch.setattr(tmw, "run_cmd_safe", self._run_cmd_safe)
        monkeypatch.setattr(tmw, "run_cmd_stream", self._run_cmd_stream)
        monkeypatch.setattr(tmw, "find_chocolatey", lambda v=None: ("choco", "2.2.2"))
        monkeypatch.setattr(tmw, "cleanup_kicad", lambda: self.cleanups.append(True))
        monkeypatch.setattr(tmw, "install_kicad_direct", pytest.fail)
        monkeypatch.setitem(sys.modules, "winreg", self._winreg())

    # -- what exists on the fake machine --------------------------------
    def kicad_exe(self, major):
        return self.tmp / "Program Files" / "KiCad" / f"{major}.0" / "bin" / "kicad.exe"

    @staticmethod
    def create(path, text=""):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    # -- faked externals ------------------------------------------------
    def _which(self, name):
        if name in ("choco", "choco.exe") and self.choco_list is not None:
            return r"C:\ProgramData\chocolatey\bin\choco.exe"
        return None                  # no ngspice / kicad on PATH

    def _run_cmd_safe(self, cmd, timeout=30, **kw):
        if cmd[1:2] == ["list"]:
            return subprocess.CompletedProcess(cmd, 0, self.choco_list or "", "")
        return None

    def _run_cmd_stream(self, cmd, timeout=900, **kw):
        self.installs.append(list(cmd))
        return 0, ""

    def _winreg(self):
        host = self

        def open_key(parent, sub=None, *args):
            if isinstance(parent, _FakeRegKey):          # an Uninstall subkey
                return _FakeRegKey(host.registry[int(sub)])
            return _FakeRegKey()                          # the Uninstall key

        def query_value(key, name):
            if name not in key.entry:
                raise FileNotFoundError(name)
            return key.entry[name], 1

        return types.SimpleNamespace(
            HKEY_LOCAL_MACHINE=1, HKEY_CURRENT_USER=2,
            KEY_READ=0, KEY_WOW64_64KEY=0, KEY_WOW64_32KEY=0,
            OpenKey=open_key,
            QueryInfoKey=lambda key: (len(host.registry), 0, 0),
            EnumKey=lambda key, i: str(i),
            QueryValueEx=query_value)


@pytest.fixture
def host(tmw, monkeypatch, tmp_path):
    return LookupHost(tmw, monkeypatch, tmp_path)


class TestNgspiceDetection:
    @pytest.mark.parametrize("target", ["latest", "44"])
    def test_feed_listing_without_executable_still_installs(self, tmw, host,
                                                            target):
        """Regression (independent review): on Chocolatey 1.x "choco list"
        shows the online feed, so find_ngspice_safe() reports ngspice 44.2
        although nothing is installed. The install used to be skipped."""
        host.choco_list = CHOCO_V1_FEED
        assert tmw.find_ngspice_safe(None) == ("ngspice", "44.2")  # the trigger

        tmw.install_ngspice(target)

        assert len(host.installs) == 1
        assert host.installs[0][:3] == ["choco", "install", "ngspice"]

    def test_local_listing_without_executable_still_installs(self, tmw, host):
        """Package registered with Chocolatey but its files are gone."""
        host.choco_list = choco_v2_local("42")
        tmw.install_ngspice("42")
        assert len(host.installs) == 1

    def test_installed_executable_with_matching_version_is_skipped(
            self, tmw, host, capsys):
        host.create(host.ngspice_exe)
        host.choco_list = choco_v2_local("42")
        tmw.install_ngspice("42")
        assert host.installs == []
        assert last_status(capsys.readouterr().out) == "installed|42|42"

    def test_installed_executable_with_other_version_installs(self, tmw, host):
        host.create(host.ngspice_exe)
        host.choco_list = choco_v2_local("41")
        tmw.install_ngspice("42")
        assert [version_arg(c) for c in host.installs] == ["42"]

    def test_executable_with_unknown_version(self, tmw, host):
        """Without Chocolatey the version is "unknown": good enough for
        "latest", never for a specific version."""
        host.create(host.ngspice_exe)
        tmw.install_ngspice("latest")
        assert host.installs == []
        tmw.install_ngspice("42")
        assert [version_arg(c) for c in host.installs] == ["42"]

    def test_nothing_installed_installs(self, tmw, host):
        tmw.install_ngspice("latest")
        assert host.installs == [["choco", "install", "ngspice", "-y", "--no-progress"]]


class TestKicadDetection:
    def stale_entry(self, host, version="8.0.9"):
        return {"DisplayName": f"KiCad {version}", "DisplayVersion": version,
                "InstallLocation": str(host.tmp / "Program Files" / "KiCad" / "removed")}

    @pytest.mark.parametrize("target", ["latest", "8"])
    def test_stale_registry_entry_still_installs(self, tmw, host, target):
        """Regression (independent review): an Uninstall registry entry whose
        folder was deleted made find_kicad_fixed() return that folder, and the
        install was skipped as "already installed"."""
        host.registry.append(self.stale_entry(host))
        assert tmw.find_kicad_fixed(None) == (
            host.registry[0]["InstallLocation"], "8.0.9")         # the trigger

        tmw.install_kicad(target)

        assert host.cleanups == [True]
        assert host.installs and host.installs[0][:3] == ["choco", "install", "kicad"]

    def test_registry_entry_with_executable_is_skipped(self, tmw, host, capsys):
        location = host.tmp / "Apps" / "KiCad"
        host.create(location / "bin" / "kicad.exe")
        host.registry.append({"DisplayName": "KiCad 8.0.9", "DisplayVersion": "8.0.9",
                              "InstallLocation": str(location)})
        tmw.install_kicad("8")
        assert host.cleanups == [] and host.installs == []
        assert last_status(capsys.readouterr().out) == "installed|8.0.9|8"

    def test_default_install_with_version_file_is_skipped(self, tmw, host, capsys):
        exe = host.create(host.kicad_exe("9"))
        host.create(exe.parent.parent / "version.txt", "KiCad 9.0.7\n")
        tmw.install_kicad("9")
        assert host.cleanups == [] and host.installs == []
        assert last_status(capsys.readouterr().out) == "installed|9.0.7|9"

    def test_default_install_without_version_file_is_skipped(self, tmw, host,
                                                             capsys):
        host.create(host.kicad_exe("9"))
        tmw.install_kicad("latest")
        assert host.cleanups == [] and host.installs == []
        assert last_status(capsys.readouterr().out) == "installed|9.x|latest"

    def test_kicad6_installed_skips_cleanup_and_direct_download(self, tmw, host):
        host.create(host.kicad_exe("6"))
        tmw.install_kicad("6")             # install_kicad_direct would fail the test
        assert host.cleanups == []

    def test_other_version_installed_keeps_version_switch(self, tmw, host):
        """Switching versions keeps the existing cleanup + install flow."""
        host.create(host.kicad_exe("9"))
        tmw.install_kicad("8")
        assert host.cleanups == [True]
        assert version_arg(host.installs[0]) == "8.0.9"

    def test_nothing_installed_installs(self, tmw, host):
        assert tmw.find_kicad_fixed(None) == (None, None)
        tmw.install_kicad("latest")
        assert host.cleanups == [True]
        assert host.installs[0][:3] == ["choco", "install", "kicad"]
