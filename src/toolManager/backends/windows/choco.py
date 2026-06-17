"""
Windows Chocolatey package manager helpers.

Low-level wrappers around choco.exe for install, uninstall, and query.
"""
from typing import Optional


def choco_install(package: str, version: str,
                  run_cmd) -> bool:
    """Install *package* at *version* via Chocolatey.

    *run_cmd* is a callable (typically Backend.run_cmd).
    Returns True on success.
    """
    if not version or version == "latest":
        cmd = ["choco", "install", package, "-y"]
    else:
        cmd = ["choco", "install", package, "--version", version, "-y"]

    result = run_cmd(cmd, timeout=300)
    return result is not None and result.returncode == 0


def choco_uninstall(package: str, version: str,
                    run_cmd) -> bool:
    """Uninstall *package* via Chocolatey."""
    cmd = ["choco", "uninstall", package, "-y"]
    result = run_cmd(cmd, timeout=120)
    return result is not None and result.returncode == 0


def choco_list(package: str, run_cmd) -> Optional[str]:
    """Query Chocolatey for the installed version of *package*.

    Returns the version string or None if not installed.
    """
    import re

    for cmd in [
        ["choco", "list", "--exact", package],
        ["choco", "list", "--local-only", "--exact", package],
    ]:
        result = run_cmd(cmd, timeout=15)
        if result and result.returncode == 0:
            for line in result.stdout.splitlines():
                m = re.match(rf"{re.escape(package)}\s+(\S+)", line,
                             re.IGNORECASE)
                if m:
                    return m.group(1)
    return None
