#!/bin/bash
# NGHDL: run the shipped nghdl.zip dispatcher on real Ubuntu 25.04, then show
# the same 24.04 dependency step's bugs executed directly (since the dispatcher
# refuses 25.04 before any bug can fire).
set -uo pipefail
N=/mnt/e/fossee/Evidence_Ubuntu2504/work/nghdl-pkg/nghdl
cd "$N" || exit 1

echo "=================================================================="
echo " SHIPPED nghdl.zip (from eSim 2.5) on Ubuntu $(. /etc/os-release; echo $VERSION_ID)"
echo "=================================================================="
echo
echo "=== 1) the dispatcher as shipped, on 25.04:"
printf '' | timeout 60 bash ./install-nghdl.sh --install 2>&1 | sed 's/^/  /'
echo "  dispatcher-exit=${PIPESTATUS[0]}"
echo
echo "  -> same wall as eSim itself: the NGHDL package only ships 22.04/23.04/24.04."
echo
echo "=== 2) the bugs the 24.04 script WOULD hit, executed on 25.04 directly ==="
echo
echo "--- N1: libcanberra-gtk-module (line 68 of install-nghdl-24.04.sh):"
echo '$ apt-get install -y libcanberra-gtk-module libcanberra-gtk3-module'
apt-get install -y libcanberra-gtk-module libcanberra-gtk3-module 2>&1 | tail -4 | sed 's/^/  /'
echo
echo "--- N2: unversioned llvm (line 55/58) resolves to LLVM 20 on 25.04:"
echo '$ apt-cache policy llvm | grep Candidate'
apt-cache policy llvm 2>&1 | grep Candidate | sed 's/^/  /'
echo "  (GHDL 4.1.0 cannot use LLVM >= 19 - ghdl/ghdl#2711)"
echo
echo "--- N3: configure line (105) points at the system default llvm-config:"
echo '  ./configure --with-llvm-config=/usr/bin/llvm-config'
if [ -e /usr/bin/llvm-config ]; then
    echo "  /usr/bin/llvm-config -> LLVM $(/usr/bin/llvm-config --version)"
else
    echo "  /usr/bin/llvm-config absent (would be created by the unversioned llvm install, at LLVM 20)"
fi
echo
echo "--- N4: uninstall purge line (305) with llvm_version undefined:"
# The real script does not use set -u, so unset variables silently expand to "".
echo '  apt-get purge -y llvm-${llvm_version} llvm-${llvm_version}-dev'
unset llvm_version
set +u
echo "  expands to: apt-get purge -y llvm-${llvm_version} llvm-${llvm_version}-dev   (empty package names)"
set -u
echo
echo "=== 3) the FIXED script's dependency set, installed for real above:"
for p in llvm-18 llvm-18-dev clang-18 libcanberra-gtk3-module; do
    printf '  %-26s %s\n' "$p" "$(dpkg-query -W -f='${Version}' "$p" 2>/dev/null || echo '(not installed)')"
done
