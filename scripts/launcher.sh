#!/bin/sh

# Versions 7.90.x and later seems to not work correctly under Wayland.
# That's why we force X11 backend with this script.
# GDK_BACKEND=x11 $1
# Setup KiCad 6.0 eSim libraries — only once per user
TARGET="$HOME/.local/kicad/6.0"
FLAG="$TARGET/.esim_kicad_setup_done"

if [ ! -f "$FLAG" ]; then
    echo "Setting up eSim libraries for the first time..."

#    install -d "$TARGET/symbols"
    install -d "$TARGET/template"

#    cp -r "$SNAP/3rdparty/symbols/." "$TARGET/symbols/"
    cp "$SNAP/3rdparty/template/sym-lib-table" "$TARGET/template/"

    touch "$FLAG"
    echo "eSim libraries setup completed."
else
    echo "eSim libraries already set up."
fi
# we are using version 6
exec "$1" "$2"
