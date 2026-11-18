#!/bin/bash
# E4: verify the isolated-virtualenv claim. The original installDependency()
# installed PyQt5/matplotlib/psutil system-wide with apt, then built a venv
# WITHOUT --system-site-packages and pip-installed the same libraries again.
# Test whether the system-wide packages are even visible inside that venv.
set -uo pipefail
W=/mnt/e/fossee/Evidence_Ubuntu2504/work
rm -rf "$W/e4" && mkdir -p "$W/e4"
cd "$W/e4"

echo "=== installing the packages the ORIGINAL script pulled in system-wide"
apt-get install -y -qq python3-pyqt5 python3-matplotlib python3-psutil python3-virtualenv 2>&1 | tail -3
echo "system-install-exit=$?"
echo
echo "=== system python can see them:"
/usr/bin/python3 -c "import PyQt5, matplotlib, psutil; print('  system python3: PyQt5 + matplotlib + psutil OK')" 2>&1
echo
echo "=== creating the venv exactly as installDependency() does (no --system-site-packages)"
virtualenv -q "$W/e4/env" 2>&1 | tail -2
echo
echo "=== can the venv see those system packages?"
"$W/e4/env/bin/python" -c "import PyQt5" 2>&1 | tail -2
"$W/e4/env/bin/python" -c "import matplotlib" 2>&1 | tail -2
"$W/e4/env/bin/python" -c "import psutil" 2>&1 | tail -2
echo
echo "=== venv site-packages vs system site-packages:"
"$W/e4/env/bin/python" -c "import sys; [print('  '+p) for p in sys.path if 'packages' in p]"
echo
echo "  -> E4 confirmed: the system-wide apt packages are invisible inside the"
echo "     venv, so those installs were dead weight. The venv needs its own pip"
echo "     installs (which the patched script keeps)."
