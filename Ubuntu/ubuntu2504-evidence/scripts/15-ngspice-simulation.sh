#!/bin/bash
# Run a real ngspice simulation through an eSim example project, exactly the
# way eSim drives it: the .cir netlist eSim generates, executed by ngspice.
set -uo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get install -y -qq ngspice >/dev/null 2>&1
echo "=== ngspice: $(ngspice --version 2>&1 | head -1)"

EX=/mnt/e/fossee/Evidence_Ubuntu2504/esim-pkg/eSim-2.5/Examples/Astable555
OUT=/mnt/e/fossee/Evidence_Ubuntu2504/screenshots
cd "$EX" || exit 1

echo
echo "=== eSim example: Astable555 (the shipped .cir netlist)"
echo "--- first 20 lines of Astable555.cir:"
head -20 Astable555.cir

echo
echo "=== running the simulation with ngspice"
ngspice -b Astable555.cir 2>&1 | tail -30
echo "sim-exit=$?"
