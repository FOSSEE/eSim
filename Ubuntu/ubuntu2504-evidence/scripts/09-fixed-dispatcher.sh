#!/bin/bash
# Prove the FIXED dispatcher selects the 25.04 script on Ubuntu 25.04.
# We run the real dispatcher; the 25.04 child script is stubbed so the run
# stops after routing and we can see exactly what was chosen.
set -uo pipefail
SRC=/mnt/e/fossee/Evidence_Ubuntu2504/esim-pkg/eSim-2.5
FIX=/mnt/e/fossee/Task4_Install_Fix/fixed-files
W=/mnt/e/fossee/Evidence_Ubuntu2504/work/fixed-pkg

echo "=================================================================="
echo " FIXED dispatcher on Ubuntu $(. /etc/os-release; echo $VERSION_ID)"
echo "=================================================================="

echo
echo "############ ORIGINAL (shipped) dispatcher, same machine ############"
rm -rf /tmp/orig && mkdir -p /tmp/orig
cp -a "$SRC/install-eSim.sh" "$SRC/install-eSim-scripts" /tmp/orig/
cd /tmp/orig || exit 1
printf 'n\n' | timeout 120 bash ./install-eSim.sh --install 2>&1 | sed 's/^/  /'
echo "  original-exit=${PIPESTATUS[1]}"

echo
echo "############ FIXED dispatcher, same machine ############"
rm -rf "$W" && mkdir -p "$W"
cp -a "$SRC/install-eSim.sh" "$SRC/install-eSim-scripts" /tmp/orig/../orig/ >/dev/null 2>&1 || true
cp -a /tmp/orig/install-eSim-scripts "$W"/ 2>/dev/null || cp -a "$SRC/install-eSim-scripts" "$W"/
cp -a "$FIX/install-eSim.sh" "$W/install-eSim.sh"
# Replace the 25.04 child with a recorder so the dispatcher's choice is visible.
cat > "$W/install-eSim-scripts/install-eSim-25.04.sh" <<'RECORDER'
#!/bin/bash
echo "  >>> ROUTED to install-eSim-25.04.sh, argument=$1"
echo "  >>> version gate passed - the installation would proceed here"
RECORDER
cd "$W" || exit 1
printf 'n\n' | timeout 120 bash ./install-eSim.sh --install 2>&1 | sed 's/^/  /'
echo "  fixed-exit=${PIPESTATUS[1]}"
