#!/usr/bin/env python3
import argparse, sys
from pathlib import Path
_local = str(Path(__file__).resolve().parent)
if _local not in sys.path: sys.path.insert(0, _local)
from backends.linux import LinuxBackend
from backends.tools import run

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=["check", "install", "update", "uninstall"])
    parser.add_argument("tool")
    parser.add_argument("version")
    args = parser.parse_args()
    run(args.tool, args.cmd, args.version, LinuxBackend(), upgrade=(args.cmd == "update"))

if __name__ == "__main__":
    main()
