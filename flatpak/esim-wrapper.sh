#!/bin/bash
# eSim Flatpak wrapper - sets up environment and launches the application
# Supports all Linux distributions (Fedora, Ubuntu, openSUSE, Arch, etc.)

export ESIM_HOME="/app/share/esim"

# eSim uses ~/.esim for config (see configuration/Appconfig.py)
CONFIG_DIR="$HOME/.esim"
CONFIG_FILE="config.ini"

mkdir -p "$CONFIG_DIR"

if [ ! -f "$CONFIG_DIR/$CONFIG_FILE" ]; then
    cat > "$CONFIG_DIR/$CONFIG_FILE" << EOF
[eSim]
eSim_HOME = $ESIM_HOME
LICENSE = %(eSim_HOME)s/LICENSE
KicadLib = %(eSim_HOME)s/library/kicadLibrary.tar.xz
IMAGES = %(eSim_HOME)s/images
VERSION = %(eSim_HOME)s/VERSION
MODELICA_MAP_JSON = %(eSim_HOME)s/library/ngspicetoModelica/Mapping.json
EOF
fi

# Create workspace file for first run (eSim expects workspace.txt in .esim)
WORKSPACE_FILE="$CONFIG_DIR/workspace.txt"
if [ ! -f "$WORKSPACE_FILE" ]; then
    mkdir -p "$HOME/eSim-Workspace"
    echo "0 $HOME/eSim-Workspace" > "$WORKSPACE_FILE"
fi

# Run eSim from the correct directory (init_path expects ../../ from frontEnd)
cd "$ESIM_HOME/src/frontEnd"
exec python3 Application.py "$@"
