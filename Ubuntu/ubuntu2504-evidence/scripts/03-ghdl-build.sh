#!/bin/bash
# N2/N3: build GHDL 4.1.0 against LLVM 18 and confirm the binary links LLVM 18.
#
# Additional finding (not in the original report): GHDL's LLVM backend needs a
# C++ compiler. install-nghdl.sh installs clang-${llvm_version} (clang-18) but
# never clang++-18, and even when clang++ is present the unversioned
# /usr/bin/clang++ belongs to the system default LLVM 20. The build must be
# told CXX=clang++-18 explicitly, exactly as it is told
# --with-llvm-config=/usr/bin/llvm-config-18.
set -uo pipefail
W=/mnt/e/fossee/Evidence_Ubuntu2504/work
cd "$W/src/ghdl-4.1.0" || exit 1

echo "=== C++ compilers present:"
for c in clang++ clang++-18 clang++-20; do
    if command -v "$c" >/dev/null 2>&1; then
        printf '  %-12s -> %s\n' "$c" "$(readlink -f "$(command -v "$c")")"
    fi
done
echo
echo "=== rebuilding with CXX=clang++-18 (the versioned C++ compiler)"
start=$(date +%s)
make -j"$(nproc)" CXX=clang++-18 2>&1 | tail -30
rc=${PIPESTATUS[0]}
end=$(date +%s)
echo "make-exit=$rc  elapsed=$((end-start))s"
if [ "$rc" -ne 0 ]; then
    echo "BUILD FAILED"
    exit "$rc"
fi

echo
echo "=== built binary:"
ls -la bin/ghdl 2>&1
echo
echo "=== version reported by the freshly built compiler:"
./bin/ghdl --version 2>&1 | head -6
echo
echo "=== LLVM linkage of the built binary:"
ldd ./bin/ghdl 2>/dev/null | grep -i llvm || echo "  (ghdl1-llvm is the backend; checking it too)"
ls -la bin/ghdl1-llvm 2>/dev/null && ldd bin/ghdl1-llvm 2>/dev/null | grep -i llvm
