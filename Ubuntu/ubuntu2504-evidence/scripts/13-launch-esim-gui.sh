#!/bin/bash
# Launch eSim 2.5 GUI detached (survives the calling shell) and screenshot it.
set -uo pipefail
PKG=/mnt/e/fossee/Evidence_Ubuntu2504/esim-pkg/eSim-2.5
V=/root/esim-env
OUT=/mnt/e/fossee/Evidence_Ubuntu2504/screenshots
mkdir -p "$OUT"

export HOME=/root
export DISPLAY=:0
export XDG_RUNTIME_DIR=/tmp/runtime-root
mkdir -p "$XDG_RUNTIME_DIR"; chmod 700 "$XDG_RUNTIME_DIR"
export QT_QPA_PLATFORM=xcb

cd "$PKG/src/frontEnd" || exit 1

pkill -f "Application.py" 2>/dev/null
sleep 1

echo "=== launching eSim 2.5 detached"
setsid nohup "$V/bin/python" Application.py >/tmp/esim-gui.log 2>&1 < /dev/null &
disown
sleep 15

if pgrep -f "Application.py" >/dev/null; then
    echo "=== process alive"
    echo "=== eSim window:"
    xdotool search --name "^eSim$" 2>/dev/null | while read -r w; do
        echo "  window $w: $(xdotool getwindowname "$w") $(xdotool getwindowgeometry "$w" | tr '\n' ' ')"
    done
    echo
    echo "=== capturing full screen"
    xwd -root -silent | convert xwd:- "$OUT/esim-main-window.png"
    ls -la "$OUT/esim-main-window.png"
    echo
    echo "=== capturing just the eSim window"
    WID=$(xdotool search --name "^eSim$" 2>/dev/null | head -1)
    if [ -n "$WID" ]; then
        xdotool windowactivate "$WID" 2>/dev/null
        xdotool windowsize "$WID" 1280 800 2>/dev/null
        sleep 1
        xwd -id "$WID" -silent 2>/dev/null | convert xwd:- "$OUT/esim-app-window.png" \
            && ls -la "$OUT/esim-app-window.png"
    fi
else
    echo "=== process died. log tail:"
    tail -40 /tmp/esim-gui.log
fi
