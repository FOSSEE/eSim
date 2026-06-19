#!/usr/bin/env python3
"""
CLI adapter — delegates to backends/linux + backends/tools/.

Subprocess protocol (unchanged):
    python tool_manager_linux.py check kicad latest
    python tool_manager_linux.py install ngspice 42
    python tool_manager_linux.py update llvm 19
    python tool_manager_linux.py uninstall ghdl none
"""

import argparse
import sys
from pathlib import Path

_local_path = str(Path(__file__).resolve().parent)
if _local_path not in sys.path:
    sys.path.insert(0, _local_path)

from backends.linux import LinuxBackend
from backends.tools import run


def main():
    parser = argparse.ArgumentParser(
        description="eSim Tool Manager — Linux Backend",
    )
    parser.add_argument("cmd", choices=["check", "install", "update", "uninstall"])
    parser.add_argument("tool")
    parser.add_argument("version")

    args = parser.parse_args()

    backend = LinuxBackend()
    run(args.tool, args.cmd, args.version, backend,
        upgrade=(args.cmd == "update"))


if __name__ == "__main__":
    main()
