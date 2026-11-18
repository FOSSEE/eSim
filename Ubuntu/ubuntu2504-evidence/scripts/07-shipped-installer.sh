#!/bin/bash
# Run the ACTUAL shipped eSim 2.5 installer, unmodified, on Ubuntu 25.04.
# This is step 2 of the task: "Download and try installing eSim-2.5 on Ubuntu
# 25.04 machine". Nothing here is mocked.
set -uo pipefail
PKG=/mnt/e/fossee/Evidence_Ubuntu2504/esim-pkg/eSim-2.5
cd "$PKG" || exit 1

echo "=================================================================="
echo " SHIPPED eSim 2.5 installer, unmodified, on Ubuntu $(. /etc/os-release; echo $VERSION_ID)"
echo " package: $PKG"
echo " VERSION file: $(cat VERSION 2>/dev/null)"
echo "=================================================================="
echo
echo "=== the dispatcher as shipped:"
echo "  case \$VERSION_ID in 22.04|23.04|24.04 ... *) Unsupported ... exit 1"
echo
echo "=== running: ./install-eSim.sh --install  (with 'n' to the proxy prompt)"
echo "------------------------------------------------------------------"
printf 'n\n' | timeout 600 bash ./install-eSim.sh --install 2>&1
rc=$?
echo "------------------------------------------------------------------"
echo "installer-exit=$rc"
echo
echo "=== CONCLUSION: on a stock Ubuntu 25.04 machine the shipped"
echo "    installer refuses to run at all. There is no 25.04 script in the"
echo "    package - it only knows 22.04, 23.04 and 24.04."
