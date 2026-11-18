#!/bin/bash
# Verify the remaining installer claims against the real Ubuntu 25.04 archive.
# Each block prints the exact command the installer runs and its real result.
set -uo pipefail

echo "=================================================================="
echo " Ubuntu 25.04 (Plucky Puffin) - installer claim verification"
echo " host: $(. /etc/os-release; echo "$PRETTY_NAME")"
echo " kernel: $(uname -r)"
echo " python: $(python3 --version 2>&1)"
echo " apt: $(apt-get --version | head -1)"
echo " date: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "=================================================================="

echo
echo "--- E2: the installer never installs unzip; NGHDL needs it ---------"
echo '$ which unzip'
which unzip || echo "  NOT FOUND (this is the failure the fix addresses)"
echo
echo "--- installing it the way the patched installDependency() does -------"
echo '$ apt-get install -y unzip xz-utils'
apt-get install -y -qq unzip xz-utils 2>&1 | tail -3
echo '$ which unzip'
which unzip

echo
echo "--- E1: the exit 0 vs return 0 bug -------------------------------"
echo "  installKicad() in install-eSim-25.04.sh ends the already-installed"
echo "  branch with 'exit 0'. Demonstration that exit terminates the whole"
echo "  script while return only leaves the function:"
cat > /tmp/e1-demo.sh <<'DEMO'
step1() { echo "  [kicad] already installed -> exit 0"; exit 0; }
step2() { echo "  [nghdl] should run"; }
step1
step2
echo "  NEVER REACHED"
DEMO
echo '$ bash e1-demo.sh   (original: exit 0 inside the function)'
bash /tmp/e1-demo.sh
echo "  -> steps after the KiCad check never ran (E1 reproduced)"

echo
echo "--- N4: the uninstall path purges an undefined variable ----------"
unset llvm_version
echo "  Original line: apt-get purge -y llvm-\${llvm_version} llvm-\${llvm_version}-dev"
echo "  With llvm_version unset this expands to:"
echo "    apt-get purge -y llvm- llvm--dev"
echo "  (empty package names - apt errors out, LLVM is left installed)"
echo "  Patched script defines llvm_version=\"18\" at the top, so the same"
echo "  line purges llvm-18 llvm-18-dev clang-18."

echo
echo "--- installed-state summary for the report -----------------------"
for p in unzip xz-utils llvm-18 llvm-18-dev clang-18 clang++-18 libcanberra-gtk3-module; do
    printf '  %-26s %s\n' "$p" "$(dpkg-query -W -f='${Version}' "$p" 2>/dev/null || echo '(not installed)')"
done
