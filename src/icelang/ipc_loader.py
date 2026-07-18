"""
ICELang IPC Loader
==================
Connects to KiCad 9's IPC API server and loads a compiled .kicad_sch
into the active schematic editor.

KiCad 9 on Debian/Ubuntu ships with the internal scripting console
disabled. Instead it exposes an IPC API server (eeschema listens on
127.0.0.1:4243 by default). This script bridges ICELang's compiler
output to that API.

Usage:
    # Step 1: Open KiCad and enable the API server
    # Preferences -> Preferences -> Scripting -> Enable IPC API server

    # Step 2: Compile your circuit
    python3 main.py test_circuits/rc_filter.ilang output/

    # Step 3: Load it into KiCad
    python3 ipc_loader.py output/rc_filter.kicad_sch

    # Or do both in one command
    python3 ipc_loader.py --compile test_circuits/rc_filter.ilang output/
"""

import sys
import os
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path.home()))

IPC_HOST = "127.0.0.1"
IPC_PORT = 4243


def _check_server():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((IPC_HOST, IPC_PORT))
        s.close()
        return True
    except (ConnectionRefusedError, OSError):
        return False


def load_schematic(kicad_sch: str):
    kicad_sch = Path(kicad_sch).resolve()

    if not kicad_sch.exists():
        print(f"Error: {kicad_sch} does not exist")
        sys.exit(1)

    if not _check_server():
        print(
            "KiCad IPC server not reachable on 127.0.0.1:4243.\n"
            "Enable it: KiCad -> Preferences -> Preferences -> "
            "Scripting -> Enable IPC API server\n"
            "Then restart KiCad and try again."
        )
        sys.exit(1)

   
    # kipy 0.7.1. Auto-load is skipped; the schematic is on disk and
    print(f"\nSchematic ready. Open in KiCad:")
    print(f"  File -> Open -> {kicad_sch}\n")
    # Auto-load via kipy or raw IPC not available on this KiCad build.
    


def _raw_open(path: str):
    """
    Fallback: send a raw open command over the IPC socket.
    KiCad 9 IPC protocol is JSON-RPC over TCP.
    """
    import socket
    import json

    payload = json.dumps({
        "jsonrpc": "2.0",
        "method":  "openFile",
        "params":  {"path": path},
        "id":      1
    }) + "\n"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((IPC_HOST, IPC_PORT))
        s.sendall(payload.encode())
        response = s.recv(4096).decode()
        s.close()
        result = json.loads(response)
        if "error" in result:
            print(f"KiCad IPC error: {result['error']}")
        else:
            print(f"Loaded into KiCad: {path}")
    except Exception as e:
        print(
            f"Raw IPC also failed: {e}\n"
            "Open the file manually in KiCad: File -> Open -> "
            f"{path}"
        )


def compile_and_load(ilang_path: str, output_dir: str):
    from icelang_plugin.runner import run, RunnerError
    os.environ.setdefault("ICELANG_ROOT", str(ROOT))
    print(f"Compiling {Path(ilang_path).name} ...")
    try:
        result = run(ilang_path, output_dir)
        print(f"Compiled: {result['kicad_sch']}")
        if result.get("spice_cir"):
            print(f"SPICE:    {result['spice_cir']}")
        load_schematic(result["kicad_sch"])
    except RunnerError as e:
        print(f"Compiler error: {e}")
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(
        description="ICELang IPC Loader — compile .ilang and load into KiCad 9"
    )
    ap.add_argument(
        "--compile", "-c",
        action="store_true",
        help="Compile a .ilang file before loading"
    )
    ap.add_argument(
        "input",
        help=".ilang source file (with --compile) or .kicad_sch file"
    )
    ap.add_argument(
        "output_dir",
        nargs="?",
        default="output",
        help="Output directory when using --compile (default: output/)"
    )
    args = ap.parse_args()

    if args.compile:
        compile_and_load(args.input, args.output_dir)
    else:
        load_schematic(args.input)


if __name__ == "__main__":
    main()
