"""Unit tests for src/toolManager/platform_utils.py.

platform_utils decides everything at import time from ``sys.platform``, so each
test loads a FRESH copy of the module with ``sys.platform`` faked. That makes
the suite independent of the host OS: it behaves the same on a Windows dev box
and on Linux CI. External commands (``shutil.which``) and platform info
(``platform.release`` / ``freedesktop_os_release``) are mocked, so no real
package manager or tool is ever executed or installed.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

_MODULE_PATH = Path(__file__).resolve().parents[1] / "platform_utils.py"

_CREATE_NO_WINDOW = 0x08000000


class _FakeStartupInfo:
    """Stand-in for subprocess.STARTUPINFO (only exists on Windows)."""

    def __init__(self):
        self.dwFlags = 0
        self.wShowWindow = None


@pytest.fixture
def load(monkeypatch):
    """Return load(platform_string) -> a fresh platform_utils module as it
    would import on that platform."""

    def _load(plat):
        monkeypatch.setattr(sys, "platform", plat)
        if plat == "win32":
            # These attributes are Windows-only; provide them (raising=False)
            # so the win32 branch of subprocess_flags() can run anywhere.
            monkeypatch.setattr(subprocess, "STARTUPINFO", _FakeStartupInfo,
                                raising=False)
            monkeypatch.setattr(subprocess, "STARTF_USESHOWWINDOW", 1,
                                raising=False)
            monkeypatch.setattr(subprocess, "SW_HIDE", 0, raising=False)
            monkeypatch.setattr(subprocess, "CREATE_NO_WINDOW",
                                _CREATE_NO_WINDOW, raising=False)
        spec = importlib.util.spec_from_file_location(
            "platform_utils_under_test", _MODULE_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    return _load


def _fake_which(available):
    """shutil.which replacement that 'finds' only the named commands."""
    names = set(available)
    return lambda cmd, *a, **kw: ("/fake/bin/" + cmd) if cmd in names else None


# --------------------------------------------------------------------------- #
#  OS flags / get_os_id
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("plat,expected,flags", [
    ("win32", "win32", (True, False, False)),
    ("linux", "linux", (False, True, False)),
    ("darwin", "darwin", (False, False, True)),
    ("freebsd14", "unknown", (False, False, False)),
])
def test_get_os_id_and_flags(load, plat, expected, flags):
    pu = load(plat)
    assert pu.get_os_id() == expected
    assert (pu.IS_WINDOWS, pu.IS_LINUX, pu.IS_MAC) == flags


# --------------------------------------------------------------------------- #
#  detect_package_manager
# --------------------------------------------------------------------------- #
class TestDetectPackageManager:
    def test_windows_returns_none_even_if_linux_tools_on_path(
            self, load, monkeypatch):
        pu = load("win32")
        monkeypatch.setattr(pu.shutil, "which",
                            _fake_which({"apt-get", "brew", "choco"}))
        assert pu.detect_package_manager() is None

    def test_linux_apt(self, load, monkeypatch):
        pu = load("linux")
        monkeypatch.setattr(pu.shutil, "which", _fake_which({"apt-get"}))
        assert pu.detect_package_manager() == "apt"

    def test_linux_dnf(self, load, monkeypatch):
        pu = load("linux")
        monkeypatch.setattr(pu.shutil, "which", _fake_which({"dnf"}))
        assert pu.detect_package_manager() == "dnf"

    def test_linux_priority_apt_before_dnf(self, load, monkeypatch):
        pu = load("linux")
        monkeypatch.setattr(pu.shutil, "which",
                            _fake_which({"dnf", "apt-get"}))
        assert pu.detect_package_manager() == "apt"

    def test_linux_no_supported_manager(self, load, monkeypatch):
        pu = load("linux")
        monkeypatch.setattr(pu.shutil, "which", _fake_which(set()))
        assert pu.detect_package_manager() is None

    def test_macos_brew(self, load, monkeypatch):
        pu = load("darwin")
        monkeypatch.setattr(pu.shutil, "which", _fake_which({"brew"}))
        assert pu.detect_package_manager() == "brew"

    def test_macos_brew_preferred_over_port(self, load, monkeypatch):
        pu = load("darwin")
        monkeypatch.setattr(pu.shutil, "which", _fake_which({"port", "brew"}))
        assert pu.detect_package_manager() == "brew"

    def test_macos_linux_tools_are_ignored(self, load, monkeypatch):
        pu = load("darwin")
        monkeypatch.setattr(pu.shutil, "which", _fake_which({"apt-get"}))
        assert pu.detect_package_manager() is None


# --------------------------------------------------------------------------- #
#  distro_label
# --------------------------------------------------------------------------- #
class TestDistroLabel:
    def test_windows(self, load, monkeypatch):
        pu = load("win32")
        monkeypatch.setattr(pu.platform, "release", lambda: "11")
        assert pu.distro_label() == "Windows 11"

    def test_linux_from_freedesktop_os_release(self, load, monkeypatch):
        pu = load("linux")
        monkeypatch.setattr(
            pu.platform, "freedesktop_os_release",
            lambda: {"NAME": "Ubuntu", "VERSION_ID": "24.04"},
            raising=False)
        assert pu.distro_label() == "Ubuntu 24.04"

    def test_linux_rolling_release_has_no_version(self, load, monkeypatch):
        pu = load("linux")
        monkeypatch.setattr(pu.platform, "freedesktop_os_release",
                            lambda: {"NAME": "Arch Linux"}, raising=False)
        assert pu.distro_label() == "Arch Linux"

    def test_linux_os_release_unreadable_falls_back(self, load, monkeypatch):
        pu = load("linux")

        def boom():
            raise OSError("no /etc/os-release")

        monkeypatch.setattr(pu.platform, "freedesktop_os_release", boom,
                            raising=False)
        assert pu.distro_label() == "Linux"


# --------------------------------------------------------------------------- #
#  subprocess_flags
# --------------------------------------------------------------------------- #
class TestSubprocessFlags:
    def test_windows_hides_console(self, load):
        pu = load("win32")
        flags = pu.subprocess_flags()
        assert flags["creationflags"] == _CREATE_NO_WINDOW
        si = flags["startupinfo"]
        assert si.dwFlags & subprocess.STARTF_USESHOWWINDOW
        assert si.wShowWindow == subprocess.SW_HIDE

    @pytest.mark.parametrize("plat", ["linux", "darwin"])
    def test_non_windows_is_empty(self, load, plat):
        assert load(plat).subprocess_flags() == {}


# --------------------------------------------------------------------------- #
#  Regression tests: verify the get_mysys2_path / __all__ fixes
# --------------------------------------------------------------------------- #
class TestRegressions:
    def test_all_lists_only_names_that_exist(self, load):
        """``__all__`` once listed get_mysys32_path while the function is
        get_mysys2_path, so ``from platform_utils import *`` raised
        AttributeError. Every name in ``__all__`` must now exist."""
        pu = load("linux")
        missing = [n for n in pu.__all__ if not hasattr(pu, n)]
        assert missing == []

    def test_get_mysys2_path_raises_on_non_windows(self, load):
        """The function once did ``return RuntimeError(...)`` instead of
        raising, so callers' ``except RuntimeError`` never fired and they
        received an exception object as the path. It must now raise."""
        pu = load("linux")
        with pytest.raises(RuntimeError):
            pu.get_mysys2_path()

    def test_get_mysys2_path_default_on_windows(self, load, monkeypatch):
        pu = load("win32")
        monkeypatch.delenv("MSYS2_PATH", raising=False)
        assert str(pu.get_mysys2_path()) == r"C:\msys64"

    def test_get_mysys2_path_env_override_on_windows(self, load, monkeypatch):
        pu = load("win32")
        monkeypatch.setenv("MSYS2_PATH", r"D:\tools\msys2")
        assert str(pu.get_mysys2_path()) == r"D:\tools\msys2"
