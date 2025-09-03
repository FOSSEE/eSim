#!/usr/bin/env bash
set -euo pipefail
python3 -m etm doctor
python3 -m etm install ngspice kicad ghdl verilator
python3 -m etm configure
