#!/bin/bash

# ============================================================
#   Function to detect Ubuntu version
# ============================================================
get_ubuntu_version() {
    VERSION_ID=$(grep "^VERSION_ID" /etc/os-release | cut -d '"' -f 2)
    FULL_VERSION=$(lsb_release -rs)
    echo "Detected Ubuntu Version: $FULL_VERSION"
}

# ============================================================
#   KiCad fix for Ubuntu 25.04
# ============================================================
install_kicad_for_25() {
    echo ""
    echo "==============================================="
    echo "  Ubuntu 25.04 detected — KiCad PPA NOT SUPPORTED"
    echo "  Installing KiCad from Ubuntu repository..."
    echo "==============================================="
    echo ""

    sudo apt update
    sudo apt install -y kicad kicad-footprints kicad-libraries \
         kicad-symbols kicad-templates

    echo "KiCad installation complete."
}

# ============================================================
#   Function to run proper installer
# ============================================================
run_version_script() {
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/install-eSim-scripts"

    case $VERSION_ID in
        "22.04") SCRIPT="$SCRIPT_DIR/install-eSim-23.04.sh" ;;
        "23.04") SCRIPT="$SCRIPT_DIR/install-eSim-23.04.sh" ;;
        "24.04") SCRIPT="$SCRIPT_DIR/install-eSim-24.04.sh" ;;
        "25.04")
            echo "Ubuntu 25.04 detected — enabling compatibility mode."
            SCRIPT="$SCRIPT_DIR/install-eSim-24.04.sh"
            ;;
        *)
            echo "Unsupported Ubuntu version: $VERSION_ID ($FULL_VERSION)"
            exit 1
            ;;
    esac

    # Special Fix for KiCad
    if [[ "$VERSION_ID" == "25.04" ]]; then
        install_kicad_for_25
        export ESIM_SKIP_KICAD=1
    else
        export ESIM_SKIP_KICAD=0
    fi

    # Execute final script
    echo "Running: $SCRIPT $ARGUMENT"
    bash "$SCRIPT" "$ARGUMENT"
}

# ============================================================
# MAIN LOGIC
# ============================================================

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 --install | --uninstall"
    exit 1
fi

ARGUMENT=$1
if [[ "$ARGUMENT" != "--install" && "$ARGUMENT" != "--uninstall" ]]; then
    echo "Usage: $0 --install | --uninstall"
    exit 1
fi

get_ubuntu_version
run_version_script

