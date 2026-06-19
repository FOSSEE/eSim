"""backends/linux/search.py — Linux executable discovery.

Finds installed tool binaries by checking PATH, standard system
directories, and common Linux installation prefixes (/usr/local,
/opt, snap, flatpak, ~/.local).

Each `find_*` function returns ``(path, version)`` and takes injected
callbacks (``which``, ``run_cmd``) so tests can provide mocks.
"""

import shutil
from pathlib import Path
from typing import Callable, Optional


# Standard directories to scan beyond PATH
_STANDARD_PREFIXES: list[Path] = [
    Path("/usr/local/bin"),
    Path("/usr/local/sbin"),
    Path("/opt"),
    Path.home() / ".local" / "bin",
]

_SNAP_BIN = Path("/snap/bin")
_FLATPAK_BIN = Path("/var/lib/flatpak/exports/bin")


def find_tool(
    tool_id: str,
    version: Optional[str],
    run_cmd: Callable,
    which_fn: Optional[Callable] = None,
    extra_prefixes: Optional[list[Path]] = None,
) -> tuple[Optional[str], Optional[str]]:
    """Locate *tool_id* on the system and return ``(exe_path, installed_version)``.

    Steps:
    1. ``shutil.which(tool_id)`` — PATH search
    2. Scan *extra_prefixes* ∪ *STANDARD_PREFIXES* ∪ snap/flatpak
    3. Run ``--version`` on the first candidate found.

    Returns ``(None, None)`` if the tool is not found.
    """
    if which_fn is None:
        which_fn = shutil.which

    # 1. PATH
    exe = which_fn(tool_id)
    if exe:
        ver = _get_version(exe, run_cmd)
        return exe, ver

    # 2. Extra prefixes (tool-specific)
    if extra_prefixes:
        for prefix in extra_prefixes:
            candidate = _find_in_prefix(tool_id, prefix, which_fn)
            if candidate:
                ver = _get_version(candidate, run_cmd)
                return candidate, ver

    # 3. Standard prefixes
    for prefix in _STANDARD_PREFIXES:
        candidate = _find_in_prefix(tool_id, prefix, which_fn)
        if candidate:
            ver = _get_version(candidate, run_cmd)
            return candidate, ver

    # 4. Snap
    snap_exe = _SNAP_BIN / tool_id
    if snap_exe.exists() and os.access(str(snap_exe), os.X_OK):
        ver = _get_version(str(snap_exe), run_cmd)
        return str(snap_exe), ver

    # 5. Flatpak
    flatpak_exe = _FLATPAK_BIN / tool_id
    if flatpak_exe.exists() and os.access(str(flatpak_exe), os.X_OK):
        ver = _get_version(str(flatpak_exe), run_cmd)
        return str(flatpak_exe), ver

    return None, None


def find_kicad(
    version: Optional[str],
    run_cmd: Callable,
    which_fn: Optional[Callable] = None,
) -> tuple[Optional[str], Optional[str]]:
    """Locate KiCad on Linux."""
    return find_tool("kicad", version, run_cmd, which_fn,
                     extra_prefixes=[Path("/usr/local/kicad")])


def find_ngspice(
    version: Optional[str],
    run_cmd: Callable,
    which_fn: Optional[Callable] = None,
) -> tuple[Optional[str], Optional[str]]:
    """Locate Ngspice on Linux."""
    return find_tool("ngspice", version, run_cmd, which_fn,
                     extra_prefixes=[Path("/usr/local/ngspice")])


def find_ghdl(
    version: Optional[str],
    run_cmd: Callable,
    which_fn: Optional[Callable] = None,
) -> tuple[Optional[str], Optional[str]]:
    """Locate GHDL on Linux."""
    return find_tool("ghdl", version, run_cmd, which_fn,
                     extra_prefixes=[Path("/usr/local/ghdl")])


def find_verilator(
    version: Optional[str],
    run_cmd: Callable,
    which_fn: Optional[Callable] = None,
) -> tuple[Optional[str], Optional[str]]:
    """Locate Verilator on Linux."""
    return find_tool("verilator", version, run_cmd, which_fn,
                     extra_prefixes=[Path("/usr/local/verilator")])


def find_llvm(
    version: Optional[str],
    run_cmd: Callable,
    which_fn: Optional[Callable] = None,
) -> tuple[Optional[str], Optional[str]]:
    """Locate LLVM/Clang on Linux."""
    # Try clang first (most common), then llvm-config
    result = find_tool("clang", version, run_cmd, which_fn,
                       extra_prefixes=[Path("/usr/local/llvm")])
    if result[0]:
        return result
    return find_tool("llvm-config", version, run_cmd, which_fn)


# ── Internal helpers ────────────────────────────────────────────────────

def _find_in_prefix(
    exe_name: str,
    prefix: Path,
    which_fn: Callable,
) -> Optional[str]:
    """Search for *exe_name* under *prefix* (recursive up to 2 levels)."""
    if not prefix.exists():
        return None

    # Direct match
    candidate = prefix / exe_name
    if candidate.exists() and os.access(str(candidate), os.X_OK):
        return str(candidate)

    # bin/ subdir
    candidate = prefix / "bin" / exe_name
    if candidate.exists() and os.access(str(candidate), os.X_OK):
        return str(candidate)

    # sbin/ subdir
    candidate = prefix / "sbin" / exe_name
    if candidate.exists() and os.access(str(candidate), os.X_OK):
        return str(candidate)

    return None


def _get_version(exe_path: str, run_cmd: Callable) -> Optional[str]:
    """Extract version by running ``<exe> --version``."""
    result = run_cmd([exe_path, "--version"], timeout=10)
    if result is None or result.returncode != 0:
        return None
    line = (result.stdout or "").split("\n")[0].strip()
    if not line:
        return None
    # Take the last whitespace-separated token
    parts = line.split()
    return parts[-1] if parts else None


import os  # noqa: E402 (used by _find_in_prefix and find_tool)
