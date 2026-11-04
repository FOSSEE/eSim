"""Unit tests for the ngspice and KiCad install logic in tool_manager_windows.py.

Chocolatey, the installed-tool lookups and the KiCad cleanup are mocked, so
these tests run on any OS without Chocolatey, admin rights or EDA tools. The
module is imported with a non-Windows platform so it does not re-wrap
sys.stdout (which it does on real Windows).
"""
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

    def test_already_installed_version_is_not_reinstalled(self, tmw, monkeypatch,
                                                          capsys):
        choco = FakeChoco(tmw, monkeypatch)
        self._installed(tmw, monkeypatch, ("C:/ngspice.exe", "42"))
        tmw.install_ngspice("42")
        assert choco.commands == []
        assert last_status(capsys.readouterr().out) == "installed|42|42"

    def test_latest_already_installed_is_not_reinstalled(self, tmw, monkeypatch):
        choco = FakeChoco(tmw, monkeypatch)
        self._installed(tmw, monkeypatch, ("C:/ngspice.exe", "unknown"))
        tmw.install_ngspice("latest")
        assert choco.commands == []

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

    @pytest.mark.parametrize("current,target", [("9.0.7", "9"), ("9.x", "9"),
                                                ("8.0.9", "latest")])
    def test_already_installed_is_not_removed(self, tmw, monkeypatch, capsys,
                                              cleanups, current, target):
        """Regression: installing the version already present ran
        cleanup_kicad() (uninstall + delete folders) and reinstalled."""
        choco = FakeChoco(tmw, monkeypatch)
        self._installed(tmw, monkeypatch, ("C:/KiCad/bin/kicad.exe", current))
        tmw.install_kicad(target)
        assert cleanups == []
        assert choco.commands == []
        assert last_status(capsys.readouterr().out) == f"installed|{current}|{target}"

    def test_kicad6_already_installed_skips_direct_download(self, tmw,
                                                            monkeypatch, cleanups):
        FakeChoco(tmw, monkeypatch)
        self._installed(tmw, monkeypatch, ("C:/KiCad/bin/kicad.exe", "6.0.11"))
        monkeypatch.setattr(tmw, "install_kicad_direct", pytest.fail)
        tmw.install_kicad("6")
        assert cleanups == []

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
