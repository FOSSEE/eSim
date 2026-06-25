#!/usr/bin/env python3
"""
CLI adapter — delegates to backends/windows.py + backends/tools/.

Subprocess protocol (unchanged):
    python tool_manager_windows.py check kicad latest
    python tool_manager_windows.py install ngspice 42
    python tool_manager_windows.py update llvm 19
    python tool_manager_windows.py uninstall ghdl none

Stdout output is in pipe-delimited format consumed by UI worker threads.
"""

import argparse
import os
import sys
from pathlib import Path

_local_path = str(Path(__file__).resolve().parent)
if _local_path not in sys.path:
    sys.path.insert(0, _local_path)

from backends.windows import WindowsBackend
from backends.tools import run

# ── Keep the original argparse help text for backward compat ─────────

EPILOG = """
IMPROVED VERSION - Better Version Support and Updates:

Available tools and versions:
  chocolatey: latest
  kicad: 6, 7, 8, 9, latest (Note: KiCad 6 may use direct download if Chocolatey fails)
  ngspice: 35, 36, 37, 38, 39, 40, 41, 42, latest
  llvm: 13, 14, 15, 16, 17, 18, 19, latest
  python-pyqt5: 5.15.9, 5.15.10, 6.5.0, 6.6.0, latest
  ghdl: 4.0.0, 5.1.1, latest
  verilator: latest (via MSYS2)

Examples:
  # Check current installation
  python tool_manager_windows.py check kicad none

  # Install specific version
  python tool_manager_windows.py install ngspice 38
  python tool_manager_windows.py install llvm 17
  python tool_manager_windows.py install kicad 6

  # Update to specific version (from any version)
  python tool_manager_windows.py update ngspice 40
  python tool_manager_windows.py update llvm 19
  python tool_manager_windows.py update kicad 7

  # Update to latest
  python tool_manager_windows.py update kicad latest

Note: If KiCad 6 installation via Chocolatey fails, the script will automatically
      attempt a direct download from KiCad's official releases.
"""


def main():
    parser = argparse.ArgumentParser(
        description="COMPLETE Tool Manager - All Tools in One",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EPILOG,
    )

    parser.add_argument("cmd",
                        choices=["check", "install", "update", "uninstall"])
    parser.add_argument("tool")
    parser.add_argument("version")

    args = parser.parse_args()

    backend = WindowsBackend()
    run(args.tool, args.cmd, args.version, backend,
        upgrade=(args.cmd == "update"))


if __name__ == "__main__":
    main()
