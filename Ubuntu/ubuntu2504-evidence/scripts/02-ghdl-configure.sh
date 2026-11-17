#!/bin/bash
# N3: configure GHDL 4.1.0 against LLVM 18, the way the patched installer does.
set -uo pipefail
W=/mnt/e/fossee/Evidence_Ubuntu2504/work
cd "$W/src/ghdl-4.1.0" || exit 1

echo "=== unversioned llvm-config on this system:"
if [ -e /usr/bin/llvm-config ]; then
    /usr/bin/llvm-config --version
else
    echo "  ABSENT - the unversioned 'llvm' package was never installed"
    echo "  (on Ubuntu 25.04 apt would supply llvm 20.0, which GHDL 4.1.0 cannot use)"
fi
echo
echo "=== configure with the patched line: --with-llvm-config=/usr/bin/llvm-config-18"
chmod +x configure
./configure --with-llvm-config=/usr/bin/llvm-config-18
echo "configure-exit=$?"
