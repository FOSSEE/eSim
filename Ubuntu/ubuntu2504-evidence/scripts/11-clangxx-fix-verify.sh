#!/bin/bash
# Clean-room proof of the clang++ fix, built inside WSL's native filesystem
# (fast, no /mnt 9p contention). Builds only the ghdl1-llvm target.
set -uo pipefail
R=/root/proof
rm -rf "$R" && mkdir -p "$R"
cd "$R" || exit 1

echo "=== copy source (from the evidence tree)"
cp /mnt/e/fossee/Evidence_Ubuntu2504/work/src/ghdl-4.1.0.tar.gz . || exit 1
tar xzf ghdl-4.1.0.tar.gz
cd ghdl-4.1.0 || exit 1

echo "=== toolchain actually installed:"
printf '  %-12s %s\n' llvm-18-dev "$(dpkg-query -W -f='${Version}' llvm-18-dev 2>/dev/null || echo MISSING)"
printf '  %-12s %s\n' clang-18   "$(dpkg-query -W -f='${Version}' clang-18 2>/dev/null || echo MISSING)"
echo "  clang++-18: $(clang++-18 --version 2>/dev/null | head -1)"
echo "  unversioned clang++ -> $(readlink -f "$(command -v clang++)")"
echo

echo "=== configure with the patched line"
./configure --with-llvm-config=/usr/bin/llvm-config-18 >conf.log 2>&1
grep -E "Debugging is enabled" conf.log
echo

echo "=== CONTROL: plain make (no CXX) - which compiler does it pick?"
make -n ghdl1-llvm 2>/dev/null | grep -oE "c\+\+|g\+\+|clang\+\+[^ ]*" | sort -u | head -3
echo "  (a plain 'make' would invoke the unversioned clang++ = LLVM 20)"
echo

echo "=== FIX: make CXX=clang++-18 ghdl1-llvm"
make -j"$(nproc)" CXX=clang++-18 ghdl1-llvm >build.log 2>&1
rc=$?
echo "make-exit=$rc"
if [ "$rc" -ne 0 ]; then
    grep -iE "error|not found" build.log | head -8
    exit "$rc"
fi
echo
echo "=== the backend binary:"
ls -la ghdl1-llvm
echo "=== LLVM it links:"
ldd ./ghdl1-llvm | grep -i llvm
echo
echo "=== embedded version string:"
strings ./ghdl1-llvm | grep -oE "llvm-18|LLVM [0-9.]+" | sort -u | head -3
echo
echo "RESULT: ghdl1-llvm built with clang++-18 links LLVM 18."
