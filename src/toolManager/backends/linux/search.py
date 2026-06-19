import os, shutil
from pathlib import Path
from typing import Callable, Optional

_STANDARD_PREFIXES = [Path("/usr/local/bin"), Path("/usr/local/sbin"),
    Path("/opt"), Path.home() / ".local" / "bin"]
_SNAP_BIN = Path("/snap/bin")
_FLATPAK_BIN = Path("/var/lib/flatpak/exports/bin")

def find_tool(name, version, run_cmd, which_fn, extra_prefixes=None):
    which_fn = which_fn or shutil.which
    exe = which_fn(name)
    if exe: return exe, _get_version(exe, run_cmd)
    for pfx in (extra_prefixes or []):
        r = _find_in_prefix(name, pfx, which_fn)
        if r: return r, _get_version(r, run_cmd)
    for pfx in _STANDARD_PREFIXES:
        r = _find_in_prefix(name, pfx, which_fn)
        if r: return r, _get_version(r, run_cmd)
    for p in [_SNAP_BIN / name, _FLATPAK_BIN / name]:
        if p.exists() and os.access(str(p), os.X_OK):
            return str(p), _get_version(str(p), run_cmd)
    return (None, None)

def find_kicad(version, run_cmd, which_fn):
    return find_tool("kicad", version, run_cmd, which_fn,
        extra_prefixes=[Path("/usr/local/kicad"), Path("/opt/kicad"), Path("/usr/share/kicad")])

def find_ngspice(version, run_cmd, which_fn):
    return find_tool("ngspice", version, run_cmd, which_fn,
        extra_prefixes=[Path("/usr/local/ngspice"), Path("/opt/ngspice")])

def find_ghdl(version, run_cmd, which_fn):
    return find_tool("ghdl", version, run_cmd, which_fn,
        extra_prefixes=[Path("/usr/local/ghdl")])

def find_verilator(version, run_cmd, which_fn):
    return find_tool("verilator", version, run_cmd, which_fn,
        extra_prefixes=[Path("/usr/local/verilator")])

def find_llvm(version, run_cmd, which_fn):
    result = find_tool("clang", version, run_cmd, which_fn,
        extra_prefixes=[Path("/usr/local/llvm")])
    if result[0]: return result
    return find_tool("llvm-config", version, run_cmd, which_fn)

def _find_in_prefix(exe_name, prefix, which_fn):
    if not prefix.exists(): return None
    for sub in ("", "bin", "sbin"):
        c = prefix / sub / exe_name if sub else prefix / exe_name
        if c.exists() and os.access(str(c), os.X_OK): return str(c)
    return None

def _get_version(exe_path, run_cmd):
    if not run_cmd: return None
    result = run_cmd([exe_path, "--version"], timeout=10)
    if result and result.returncode == 0:
        parts = (result.stdout or "").split("\n")[0].strip().split()
        return parts[-1] if parts else None
    return None
