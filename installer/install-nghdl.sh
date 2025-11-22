#!/bin/bash

# ============================================================
# Detect Ubuntu version (fixed for 25.04)
# ============================================================
get_ubuntu_version() {
    VERSION_ID=$(grep "^VERSION_ID" /etc/os-release | cut -d '"' -f 2)
    FULL_VERSION=$(lsb_release -rs)      # Reliable on all Ubuntu versions

    echo "Detected Ubuntu Version: $FULL_VERSION"
}

# ============================================================
# Select correct NGHDL installer script
# ============================================================
run_version_script() {
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/install-nghdl-scripts"

    case "$VERSION_ID" in
        "22.04")
            SCRIPT="$SCRIPT_DIR/install-nghdl-23.04.sh"
            ;;
        "23.04")
            SCRIPT="$SCRIPT_DIR/install-nghdl-23.04.sh"
            ;;
        "24.04")
            SCRIPT="$SCRIPT_DIR/install-nghdl-24.04.sh"
            ;;
        "25.04")
            echo "Ubuntu 25.04 detected — using 24.04 NGHDL installer (compatible)."
            SCRIPT="$SCRIPT_DIR/install-nghdl-24.04.sh"
            ;;
        *)
            echo "Unsupported Ubuntu version: $VERSION_ID ($FULL_VERSION)"
            exit 1
            ;;
    esac

    if [[ -f "$SCRIPT" ]]; then
        echo "Running NGHDL script: $SCRIPT $ARGUMENT"
        bash "$SCRIPT" "$ARGUMENT"
    else
        echo "ERROR: Installer script not found: $SCRIPT"
        exit 1
    fi
}

# ============================================================
# MAIN EXECUTION
# ============================================================

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 --install | --uninstall"
    exit 1
fi

ARGUMENT=$1

if [[ "$ARGUMENT" != "--install" && "$ARGUMENT" != "--uninstall" ]]; then
    echo "Invalid argument: $ARGUMENT"
    echo "Usage: $0 --install | --uninstall"
    exit 1
fi

get_ubuntu_version
run_version_script

