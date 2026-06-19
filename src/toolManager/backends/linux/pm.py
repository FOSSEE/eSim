"""backends/linux/pm.py — Package manager abstraction for Linux.

Thin wrappers over system package managers (apt, dnf, pacman, zypper,
pkg, xbps).  Each function takes a `run_cmd` callback so callers can
inject their own subprocess wrapper (e.g. Backend.run_cmd).

Usage:
    from .pm import pm_install, pm_uninstall, pm_list_installed

    ok = pm_install("apt", "kicad", backend.run_cmd)
    ver = pm_list_installed("apt", "kicad", backend.run_cmd)
"""

from typing import Callable, Optional


# ── Command tables ──────────────────────────────────────────────────────
# Each entry: (check_cmd_fmt,    install_cmd,    uninstall_cmd,
#              search_cmd_fmt,   update_cmd)

_PM_COMMANDS: dict[str, dict] = {
    "apt": {
        "check":   "dpkg -s {pkg}",
        "install": ["apt", "install", "-y"],
        "uninstall": ["apt", "remove", "-y"],
        "search":  "apt-cache show {pkg}",
        "update":  ["apt", "update"],
        "version_parse": "dpkg-query -W -f='${{Version}}' {pkg}",
    },
    "dnf": {
        "check":   "rpm -q {pkg}",
        "install": ["dnf", "install", "-y"],
        "uninstall": ["dnf", "remove", "-y"],
        "search":  "dnf info {pkg}",
        "update":  ["dnf", "check-update"],
        "version_parse": "rpm -q --queryformat '%{{VERSION}}' {pkg}",
    },
    "pacman": {
        "check":   "pacman -Q {pkg}",
        "install": ["pacman", "-S", "--noconfirm"],
        "uninstall": ["pacman", "-R", "--noconfirm"],
        "search":  "pacman -Si {pkg}",
        "update":  ["pacman", "-Sy"],
        "version_parse": "pacman -Q {pkg}",
    },
    "zypper": {
        "check":   "rpm -q {pkg}",
        "install": ["zypper", "install", "-y"],
        "uninstall": ["zypper", "remove", "-y"],
        "search":  "zypper info {pkg}",
        "update":  ["zypper", "refresh"],
        "version_parse": "rpm -q --queryformat '%{{VERSION}}' {pkg}",
    },
    "pkg": {
        "check":   "pkg info {pkg}",
        "install": ["pkg", "install", "-y"],
        "uninstall": ["pkg", "delete", "-y"],
        "search":  "pkg search {pkg}",
        "update":  ["pkg", "update"],
        "version_parse": "pkg info {pkg}",
    },
    "xbps": {
        "check":   "xbps-query {pkg}",
        "install": ["xbps-install", "-y"],
        "uninstall": ["xbps-remove", "-y"],
        "search":  "xbps-query -Rs {pkg}",
        "update":  ["xbps-install", "-Su"],
        "version_parse": "xbps-query -p pkgver {pkg}",
    },
}

_SUPPORTED_PMS = frozenset(_PM_COMMANDS.keys())


def _sudo_prefix(cmd: list[str]) -> list[str]:
    """Prepend `sudo` if the command isn't already running as root."""
    import os
    if os.geteuid() == 0:
        return cmd
    return ["sudo"] + cmd


def _cmd_str_to_list(cmd_str: str, pkg: str) -> list[str]:
    """Convert a format-string command like 'dpkg -s {pkg}' to a list."""
    return cmd_str.format(pkg=pkg).split()


# ── Public API ──────────────────────────────────────────────────────────

def pm_install(
    pm_name: str,
    package: str,
    run_cmd: Callable,
    use_sudo: bool = True,
    timeout: int = 300,
) -> bool:
    """Install *package* using *pm_name* package manager.

    Returns True on success.
    """
    if pm_name not in _PM_COMMANDS:
        return False
    cmd = _PM_COMMANDS[pm_name]["install"] + [package]
    if use_sudo:
        cmd = _sudo_prefix(cmd)
    result = run_cmd(cmd, timeout=timeout)
    return result is not None and result.returncode == 0


def pm_uninstall(
    pm_name: str,
    package: str,
    run_cmd: Callable,
    use_sudo: bool = True,
    timeout: int = 120,
) -> bool:
    """Uninstall *package* using *pm_name* package manager.

    Returns True on success.
    """
    if pm_name not in _PM_COMMANDS:
        return False
    cmd = _PM_COMMANDS[pm_name]["uninstall"] + [package]
    if use_sudo:
        cmd = _sudo_prefix(cmd)
    result = run_cmd(cmd, timeout=timeout)
    return result is not None and result.returncode == 0


def pm_list_installed(
    pm_name: str,
    package: str,
    run_cmd: Callable,
    timeout: int = 30,
) -> Optional[str]:
    """Check if *package* is installed and return its version string.

    Returns the installed version, or None if not installed.
    """
    if pm_name not in _PM_COMMANDS:
        return None

    cfg = _PM_COMMANDS[pm_name]
    version_parse_cmd = cfg.get("version_parse", cfg["check"])
    cmd = version_parse_cmd.format(pkg=package).split()
    result = run_cmd(cmd, timeout=timeout)
    if result is None or result.returncode != 0:
        return None

    # Parse version from output
    output = (result.stdout or "").strip()
    if not output:
        return None

    # apt: 'Version: 8.0.9-0kicad1~22.04' or 'dpkg-query: ... 8.0.9'
    if pm_name == "apt":
        for line in output.splitlines():
            if line.startswith("Version:"):
                return line.split(":", 1)[-1].strip()
        # dpkg-query -W format
        return output.strip("'")

    # pacman: 'kicad 8.0.9-1' → second field
    if pm_name == "pacman":
        parts = output.split()
        return parts[-1] if len(parts) >= 2 else output

    # dnf/zypper (rpm -q): just the version
    # pkg info: 'Version  : 8.0'
    # xbps: 'kicad-8.0.9_1'
    return output


def pm_search(
    pm_name: str,
    package: str,
    run_cmd: Callable,
    timeout: int = 30,
) -> bool:
    """Check if *package* is available in *pm_name*'s repositories."""
    if pm_name not in _PM_COMMANDS:
        return False
    cmd = _PM_COMMANDS[pm_name]["search"].format(pkg=package).split()
    result = run_cmd(cmd, timeout=timeout)
    return result is not None and result.returncode == 0


def pm_update_index(
    pm_name: str,
    run_cmd: Callable,
    use_sudo: bool = True,
    timeout: int = 120,
) -> bool:
    """Update the package manager's index (apt update, etc.)."""
    if pm_name not in _PM_COMMANDS:
        return False
    cmd = list(_PM_COMMANDS[pm_name]["update"])
    if use_sudo:
        cmd = _sudo_prefix(cmd)
    result = run_cmd(cmd, timeout=timeout)
    return result is not None and result.returncode == 0
