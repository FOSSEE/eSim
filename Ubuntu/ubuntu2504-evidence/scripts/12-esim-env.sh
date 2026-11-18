#!/bin/bash
# Build the eSim 2.5 Python environment exactly as the fixed installer does.
set -uo pipefail
PKG=/mnt/e/fossee/Evidence_Ubuntu2504/esim-pkg/eSim-2.5
V=/root/esim-env

rm -rf "$V"
python3 -m venv "$V" || exit 1
"$V/bin/pip" install -q --upgrade pip 2>&1 | tail -2

echo "=== installing the patched installer's Python set"
"$V/bin/pip" install -q \
    watchdog \
    "git+https://github.com/hdl/pyhdlparser.git@e1153ace8ca1e25f9fb53350c41058ef8eb8dacf" \
    makerchip-app sandpiper-saas matplotlib PyQt5 2>&1 | tail -6
echo "pip-exit=$?"

echo
echo "=== verify the imports eSim's Application.py needs"
"$V/bin/python" - <<'PY'
import PyQt5, matplotlib, watchdog
import hdlparse.verilog_parser as v
v.VerilogExtractor()
from PyQt5 import QtWidgets, QtCore, QtGui
print("PyQt5 + QtWidgets + matplotlib + hdlparse: OK")
print("pyhdlparser hdlparse version:", __import__("importlib.metadata", fromlist=["version"]).version("hdlparse"))
PY
