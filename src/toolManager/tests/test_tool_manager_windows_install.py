"""Unit tests for the install logic in tool_manager_windows.py.

Chocolatey, downloads, installers and the KiCad cleanup are always mocked, so
these tests run on any OS without Chocolatey, admin rights or EDA tools. The
first tests replace the installed-tool lookups to drive the install flow; the
later ones (LookupHost) run the REAL find_ngspice_safe(), find_kicad_fixed()
and find_llvm_fixed() with only Chocolatey, the registry and the file system
faked. The module is imported with a non-Windows platform so it does not
re-wrap sys.stdout (which it does on real Windows).
"""
import subprocess
import sys
import types
import zipfile

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
        """find_ngspice_safe returns each state in turn (last one repeats)."""
        states = list(states)

        def fake_find(version=None):
            return states.pop(0) if len(states) > 1 else states[0]

        monkeypatch.setattr(tmw, "find_ngspice_safe", fake_find)

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
#  Detection, using the REAL lookup functions
# --------------------------------------------------------------------------- #
CHOCO = r"C:\ProgramData\chocolatey\bin\choco.exe"


class _FakeRegKey:
    def __init__(self, entry=None):
        self.entry = entry

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class LookupHost:
    """A fake Windows machine for the real lookup functions.

    Only the outside world is faked: what is on PATH, Chocolatey (its version,
    its locally installed packages and the online feed), the default install
    folders (redirected into tmp_path) and the Uninstall registry key.
    find_ngspice_safe(), find_kicad_fixed() and find_llvm_fixed() run
    unchanged. Package installs are recorded, never executed; ``on_install``
    can simulate what an install leaves behind.
    """

    def __init__(self, tmw, monkeypatch, tmp_path):
        self.tmp = tmp_path
        self.choco_version = "2.2.2"   # None: Chocolatey is not installed
        self.local = {}                # packages Chocolatey installed here
        self.feed = {}                 # what the online feed offers
        self.list_rc = 0
        self.list_commands = []
        self.registry = []             # Uninstall entries (dicts)
        self.installs = []
        self.cleanups = []
        self.on_install = None         # callable(cmd) run for each install
        self.clang_version = {}        # clang.exe path -> "--version" output

        self.ngspice_exe = tmp_path / "ngspice" / "bin" / "ngspice.exe"
        self.clang_exe = tmp_path / "LLVM" / "bin" / "clang.exe"
        monkeypatch.setattr(tmw, "WIN_NGSPICE_PATHS", [str(self.ngspice_exe)])
        monkeypatch.setattr(tmw, "WIN_KICAD_PATHS", [
            (str(self.kicad_exe(v)), v) for v in ("9", "8", "7", "6")])
        monkeypatch.setattr(tmw, "WIN_LLVM_PATHS", [str(self.clang_exe)])
        monkeypatch.setattr(tmw, "which", self._which)
        monkeypatch.setattr(tmw, "run_cmd_safe", self._run_cmd_safe)
        monkeypatch.setattr(tmw, "run_cmd_stream", self._run_cmd_stream)
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
        if name in ("choco", "choco.exe") and self.choco_version is not None:
            return CHOCO
        return None                    # no ngspice / kicad / clang on PATH

    def _run_cmd_safe(self, cmd, timeout=30, **kw):
        if cmd[:2] == [CHOCO, "--version"]:
            return subprocess.CompletedProcess(cmd, 0, self.choco_version + "\n", "")
        if cmd[:2] == [CHOCO, "list"]:
            self.list_commands.append(list(cmd))
            return self._choco_list(cmd)
        if cmd[1:] == ["--version"] and cmd[0] in self.clang_version:
            return subprocess.CompletedProcess(cmd, 0, self.clang_version[cmd[0]], "")
        return None

    def _choco_list(self, cmd):
        """Chocolatey 2.x lists local packages; 1.x lists the online feed
        unless --local-only is given (and has no --local-only in 2.x)."""
        v2 = int(self.choco_version.split(".")[0]) >= 2
        if v2 and "--local-only" in cmd:
            return subprocess.CompletedProcess(cmd, 1, "", "Unknown option --local-only")
        source = self.local if (v2 or "--local-only" in cmd) else self.feed
        name = cmd[cmd.index("--exact") + 1]
        lines = [f"{name}|{source[name]}"] if name in source else []
        if "--limit-output" not in cmd:
            lines = [f"Chocolatey v{self.choco_version}"] + \
                    [l.replace("|", " ") for l in lines] + ["0 packages found."]
        return subprocess.CompletedProcess(cmd, self.list_rc, "\n".join(lines) + "\n", "")

    def _run_cmd_stream(self, cmd, timeout=900, **kw):
        self.installs.append(list(cmd))
        if self.on_install:
            self.on_install(cmd)
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


class TestChocoInstalledVersion:
    def test_v2_lists_local_packages_without_local_only(self, tmw, host):
        host.local["ngspice"] = "42"
        assert tmw._choco_installed_version("ngspice") == "42"
        assert host.list_commands == [[CHOCO, "list", "--exact", "ngspice",
                                       "--limit-output"]]

    def test_v1_uses_local_only_and_ignores_the_feed(self, tmw, host):
        host.choco_version = "1.4.0"
        host.local["ngspice"] = "41"
        host.feed["ngspice"] = "44.2"
        assert tmw._choco_installed_version("ngspice") == "41"
        assert host.list_commands == [[CHOCO, "list", "--local-only", "--exact",
                                       "ngspice", "--limit-output"]]

    def test_v1_feed_only_is_not_installed(self, tmw, host):
        host.choco_version = "1.4.0"
        host.feed["ngspice"] = "44.2"
        assert tmw._choco_installed_version("ngspice") is None

    @pytest.mark.parametrize("choco_version", [None, "unknown", ""])
    def test_no_or_unparseable_chocolatey_gives_no_version(self, tmw, host,
                                                           choco_version):
        host.choco_version = choco_version
        host.local["ngspice"] = "42"
        assert tmw._choco_installed_version("ngspice") is None
        assert host.list_commands == []

    def test_failed_query_gives_no_version(self, tmw, host):
        host.local["ngspice"] = "42"
        host.list_rc = 1
        assert tmw._choco_installed_version("ngspice") is None

    def test_other_package_names_are_ignored(self, tmw, host):
        host.local["ngspice-dev"] = "1.0"
        assert tmw._choco_installed_version("ngspice") is None


class TestNgspiceDetection:
    @pytest.mark.parametrize("target", ["latest", "44"])
    def test_v1_feed_listing_without_executable_installs(self, tmw, host,
                                                         target):
        """Regression (independent review): on Chocolatey 1.x "choco list"
        shows the online feed, and find_ngspice_safe() used to report
        ngspice 44.2 although nothing was installed, so the install was
        skipped."""
        host.choco_version = "1.4.0"
        host.feed["ngspice"] = "44.2"
        assert tmw.find_ngspice_safe(None) == (None, None)

        tmw.install_ngspice(target)

        assert len(host.installs) == 1
        assert host.installs[0][:3] == ["choco", "install", "ngspice"]

    def test_v1_reports_the_local_version_not_the_feed(self, tmw, host):
        host.choco_version = "1.4.0"
        host.create(host.ngspice_exe)
        host.local["ngspice"] = "41"
        host.feed["ngspice"] = "44.2"
        assert tmw.find_ngspice_safe(None) == (str(host.ngspice_exe), "41")
        tmw.install_ngspice("44.2")
        assert [version_arg(c) for c in host.installs] == ["44.2"]

    def test_registered_package_without_executable_installs(self, tmw, host):
        host.local["ngspice"] = "42"
        assert tmw.find_ngspice_safe(None) == (None, None)
        tmw.install_ngspice("42")
        assert len(host.installs) == 1

    def test_installed_executable_with_matching_version_is_skipped(
            self, tmw, host, capsys):
        host.create(host.ngspice_exe)
        host.local["ngspice"] = "42"
        tmw.install_ngspice("42")
        assert host.installs == []
        assert last_status(capsys.readouterr().out) == "installed|42|42"

    def test_installed_executable_with_other_version_installs(self, tmw, host):
        host.create(host.ngspice_exe)
        host.local["ngspice"] = "41"
        tmw.install_ngspice("42")
        assert [version_arg(c) for c in host.installs] == ["42"]

    def test_executable_with_unknown_version(self, tmw, host):
        """Installed outside Chocolatey: the version is "unknown", which is
        good enough for "latest" but never for a specific version."""
        host.create(host.ngspice_exe)
        assert tmw.find_ngspice_safe(None) == (str(host.ngspice_exe), "unknown")
        tmw.install_ngspice("latest")
        assert host.installs == []
        tmw.install_ngspice("42")
        assert [version_arg(c) for c in host.installs] == ["42"]

    def test_nothing_installed_installs(self, tmw, host):
        tmw.install_ngspice("latest")
        assert host.installs == [["choco", "install", "ngspice", "-y", "--no-progress"]]


class TestNgspiceInstallResult:
    def _installs(self, host, version, create_exe=True):
        def on_install(cmd):
            host.local["ngspice"] = version
            if create_exe:
                host.create(host.ngspice_exe)
        host.on_install = on_install

    def test_success_reports_the_installed_version(self, tmw, host, capsys):
        self._installs(host, "42")
        tmw.install_ngspice("42")
        assert last_status(capsys.readouterr().out) == "installed|42|42"

    def test_command_succeeded_but_no_executable_is_a_failure(self, tmw, host,
                                                              capsys):
        """Regression: on Chocolatey 1.x the feed listing alone used to make
        a failed install look successful."""
        host.choco_version = "1.4.0"
        host.feed["ngspice"] = "44.2"
        tmw.install_ngspice("latest")
        assert last_status(capsys.readouterr().out) == "install_failed|not_found|latest"

    def test_different_version_after_install_is_a_failure(self, tmw, host,
                                                          capsys):
        host.create(host.ngspice_exe)
        host.local["ngspice"] = "41"
        tmw.install_ngspice("42")              # command "succeeds", 41 stays
        assert last_status(capsys.readouterr().out) == "install_failed|version_41|42"

    def test_unknown_version_after_install_is_not_invented(self, tmw, host,
                                                           capsys):
        host.on_install = lambda cmd: host.create(host.ngspice_exe)
        tmw.install_ngspice("42")              # not recorded by Chocolatey
        assert last_status(capsys.readouterr().out) == "installed|unknown|42"


class TestKicadDetection:
    def stale_entry(self, host, version="8.0.9"):
        return {"DisplayName": f"KiCad {version}", "DisplayVersion": version,
                "InstallLocation": str(host.tmp / "Program Files" / "KiCad" / "removed")}

    @pytest.mark.parametrize("target", ["latest", "8"])
    def test_stale_registry_entry_does_not_block_install(self, tmw, host, target):
        """Regression (independent review): an Uninstall registry entry whose
        folder was deleted made find_kicad_fixed() return that folder, and the
        install was skipped as "already installed"."""
        host.registry.append(self.stale_entry(host))
        assert tmw.find_kicad_fixed(None) == (None, None)

        tmw.install_kicad(target)

        assert host.cleanups == [True]
        assert host.installs and host.installs[0][:3] == ["choco", "install", "kicad"]

    def test_stale_registry_entry_is_not_reported_as_success(self, tmw, host,
                                                             capsys):
        """After a "successful" choco run that left no kicad.exe, the stale
        entry used to be accepted as proof of installation."""
        host.registry.append(self.stale_entry(host))
        tmw.install_kicad("latest")
        assert last_status(capsys.readouterr().out).startswith("install_failed|")

    def test_install_that_creates_kicad_succeeds(self, tmw, host, capsys):
        host.on_install = lambda cmd: host.create(host.kicad_exe("9"))
        tmw.install_kicad("latest")
        assert last_status(capsys.readouterr().out) == "installed|9.x|latest"

    def test_stale_entry_does_not_hide_a_real_install(self, tmw, host):
        location = host.tmp / "Apps" / "KiCad"
        host.create(location / "bin" / "kicad.exe")
        host.registry += [self.stale_entry(host, "7.0.11"),
                          {"DisplayName": "KiCad 8.0.9", "DisplayVersion": "8.0.9",
                           "InstallLocation": str(location)}]
        assert tmw.find_kicad_fixed(None) == (str(location / "bin" / "kicad.exe"), "8.0.9")

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

    def test_uninstall_with_only_a_stale_entry_left_succeeds(self, tmw, host,
                                                             capsys):
        """The stale entry made uninstall_kicad() report still_found."""
        host.registry.append(self.stale_entry(host))
        tmw.uninstall_kicad()
        assert last_status(capsys.readouterr().out) == "not_installed|none|none"


# --------------------------------------------------------------------------- #
#  LLVM: same uninstall-first and invented-version problems as ngspice
# --------------------------------------------------------------------------- #
class TestInstallLlvm:
    def _clang(self, host, version_output="clang version 17.0.6\nTarget: x86_64"):
        host.create(host.clang_exe)
        host.clang_version[str(host.clang_exe)] = version_output

    def test_already_installed_version_is_skipped(self, tmw, host, capsys):
        self._clang(host)
        tmw.install_llvm("17")
        assert host.installs == []
        assert last_status(capsys.readouterr().out) == "installed|17|17"

    def test_switching_version_never_uninstalls_first(self, tmw, host):
        """Regression: install_llvm() ran "choco uninstall llvm" first."""
        self._clang(host)
        tmw.install_llvm("18")
        assert [c for c in host.installs if c[1] == "uninstall"] == []
        assert [version_arg(c) for c in host.installs] == ["18.1.8"]

    def test_update_to_latest_uses_choco_upgrade(self, tmw, host):
        self._clang(host)
        tmw.install_llvm("latest", upgrade=True)
        assert host.installs == [["choco", "upgrade", "llvm", "-y", "--no-progress"]]

    def test_success_reports_the_version_clang_reports(self, tmw, host, capsys):
        host.on_install = lambda cmd: self._clang(host, "clang version 18.1.8\n")
        tmw.install_llvm("18")
        assert last_status(capsys.readouterr().out) == "installed|18|18"

    def test_unreadable_version_is_not_invented(self, tmw, host, capsys):
        """Regression: when clang --version could not be read, the requested
        version was reported as installed."""
        host.on_install = lambda cmd: self._clang(host, "garbage\n")
        tmw.install_llvm("18")
        assert last_status(capsys.readouterr().out) == "install_failed|verification_failed|18"

    def test_wrong_version_after_install_is_a_failure(self, tmw, host, capsys):
        self._clang(host)                      # 17 stays after the "install"
        tmw.install_llvm("18")
        assert last_status(capsys.readouterr().out) == "install_failed|version_17|18"


# --------------------------------------------------------------------------- #
#  GHDL, Verilator, eSim and MSYS2 helpers
# --------------------------------------------------------------------------- #
class TestInstallGhdl:
    @pytest.fixture
    def ghdl(self, tmw, monkeypatch, tmp_path):
        """A downloadable zip containing ghdl.exe; BASE_DIR moved to tmp."""
        monkeypatch.setattr(tmw, "BASE_DIR", tmp_path / "toolManager")

        def fake_download(url, dest, hook=None):
            with zipfile.ZipFile(dest, "w") as zf:
                zf.writestr("GHDL/bin/ghdl.exe", "")

        monkeypatch.setattr(tmw.urllib.request, "urlretrieve", fake_download)
        version = {}

        def fake_run(cmd, timeout=30, env=None, **kw):
            return subprocess.CompletedProcess(cmd, version["rc"], version["out"], "")

        monkeypatch.setattr(tmw, "run_cmd_safe", fake_run)
        return version

    def test_working_exe_reports_its_version(self, tmw, ghdl, capsys):
        ghdl.update(rc=0, out="GHDL 5.1.1 (tarball) [Dunoon edition]\n")
        tmw.install_ghdl("latest")
        assert last_status(capsys.readouterr().out) == "installed|5.1.1|latest"

    def test_exe_that_does_not_run_is_a_failure(self, tmw, ghdl, capsys):
        """Regression: a ghdl.exe failing --version was reported as
        installed with the requested version."""
        ghdl.update(rc=1, out="")
        tmw.install_ghdl("5.1.1")
        assert last_status(capsys.readouterr().out) == "install_failed|version_check_failed|5.1.1"


class TestInstallVerilator:
    @pytest.fixture
    def archive(self, tmw, monkeypatch, tmp_path):
        """A local Verilator archive with a fake py7zr and MSYS2 in tmp."""
        monkeypatch.setattr(tmw, "DOWNLOAD_DIR", tmp_path / "Download")
        monkeypatch.setattr(tmw, "MSYS2_PATH", tmp_path / "msys64")
        archive = tmp_path / "Download" / "verilator-5.032.7z"
        archive.parent.mkdir(parents=True)
        archive.write_text("")

        class SevenZipFile:
            def __init__(self, path, mode="r"):
                pass

            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

            def extractall(self, dest):
                (dest / "verilator" / "bin").mkdir(parents=True)

        monkeypatch.setitem(sys.modules, "py7zr",
                            types.SimpleNamespace(SevenZipFile=SevenZipFile))
        return archive

    def test_copied_but_not_found_is_a_failure(self, tmw, archive, monkeypatch,
                                               capsys):
        """Regression: files copied but no executable found was reported as
        installed with the requested version."""
        monkeypatch.setattr(tmw, "find_verilator", lambda v=None: (None, None))
        tmw.install_verilator("5.032")
        out = capsys.readouterr().out
        assert last_status(out) == "install_failed|not_found_after_install|5.032"
        assert "installed|" not in out.replace("install_failed|", "")

    def test_found_with_unknown_version_is_not_invented(self, tmw, archive,
                                                        monkeypatch, capsys):
        monkeypatch.setattr(tmw, "find_verilator",
                            lambda v=None: ("C:/msys64/mingw64/bin/verilator.exe", None))
        tmw.install_verilator("5.032")
        assert last_status(capsys.readouterr().out) == "installed|unknown|5.032"

    def test_msys2_update_does_not_remove_verilator_first(self, tmw, monkeypatch,
                                                          capsys):
        """Regression: an update ran "pacman -R" before installing again."""
        commands = []
        monkeypatch.setattr(tmw, "get_msys2_bash", lambda: "C:/msys64/usr/bin/bash.exe")
        monkeypatch.setattr(tmw, "run_msys2_command",
                            lambda cmd, timeout=300: commands.append(cmd)
                            or types.SimpleNamespace(returncode=1, stdout="", stderr=""))
        tmw.install_verilator("latest", upgrade=True)
        assert not [c for c in commands if "pacman -R" in c]
        assert any("pacman -S --noconfirm mingw-w64-x86_64-verilator" in c for c in commands)
        assert last_status(capsys.readouterr().out).startswith("install_failed|")


class TestInstallEsim:
    @pytest.fixture
    def esim(self, tmw, monkeypatch, tmp_path):
        monkeypatch.setattr(tmw, "BASE_DIR", tmp_path / "toolManager")
        monkeypatch.setattr(tmw, "ESIM_DIR", tmp_path / "FOSSEE" / "eSim")
        monkeypatch.setattr(tmw, "STATE_FILE", tmp_path / "information.json")
        installer = tmp_path / "eSim-2.4_installer.exe"
        installer.write_text("")
        monkeypatch.setattr(tmw, "_get_package", lambda *a, **kw: installer)
        result = {}
        monkeypatch.setattr(tmw.subprocess, "run",
                            lambda cmd, timeout=None: subprocess.CompletedProcess(
                                cmd, result["rc"]))
        return result

    def test_failed_installer_over_old_install_is_a_failure(self, tmw, esim,
                                                            capsys):
        """Regression: the installer's exit code was ignored, so an older
        eSim still on disk made a failed install look successful."""
        LookupHost.create(tmw.ESIM_DIR / "eSim.bat")
        esim["rc"] = 2
        tmw.install_esim("2.4")
        assert last_status(capsys.readouterr().out) == "install_failed|installer_exit_2|2.4"
        assert not tmw.STATE_FILE.exists()

    def test_successful_installer_is_verified(self, tmw, esim, capsys):
        LookupHost.create(tmw.ESIM_DIR / "eSim.bat")
        esim["rc"] = 0
        tmw.install_esim("2.4")
        assert last_status(capsys.readouterr().out) == "installed|2.4|2.4"


def test_msys2_env_adds_msys2_usr_bin(tmw, monkeypatch, tmp_path):
    """Regression: get_msys2_env() added <MSYS2>/../usr/bin (C:\\usr\\bin)
    instead of <MSYS2>/usr/bin to PATH."""
    usr_bin = tmp_path / "msys64" / "usr" / "bin"
    usr_bin.mkdir(parents=True)
    monkeypatch.setattr(tmw, "MSYS2_PATH", tmp_path / "msys64")
    monkeypatch.setattr(tmw, "get_msys2_mingw_bin", lambda: None)
    path = tmw.get_msys2_env()["PATH"].split(tmw.os.pathsep)
    assert path[0] == str(usr_bin)
