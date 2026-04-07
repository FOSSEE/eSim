#!/bin/bash 
#==========================================================
#          FILE: install-nghdl.sh
# 
#         USAGE: ./install-nghdl.sh --install
#                 			OR
#                ./install-nghdl.sh --uninstall
# 
#   DESCRIPTION: Installation script for Ngspice, GHDL 
#                and Verilator simulators (NGHDL)
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, Rahul Paknikar, Sumanto Kar, Jayanth Tatineni,
#                Anshul Verma, Shiva Krishna Sangati, Harsha Narayana P
#  ORGANIZATION: eSim, FOSSEE group at IIT Bombay
#       CREATED: Monday 23 June 2025 15:20
#      REVISION: ---
#==========================================================


# Function to detect Ubuntu version and full version string
get_ubuntu_version() {
    VERSION_ID=$(grep "^VERSION_ID" /etc/os-release | cut -d '"' -f 2)
    FULL_VERSION=$(lsb_release -d | grep -oP '\d+\.\d+\.\d+')
    echo "Detected Ubuntu Version: $FULL_VERSION"
}

# Function to choose and run the appropriate script
run_version_script() {
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/install-nghdl-scripts"
    
    # Decide script based on full version
    case $VERSION_ID in
        "22.04")
            if [[ "$FULL_VERSION" == "22.04.4" ]]; then
                SCRIPT="$SCRIPT_DIR/install-nghdl-22.04.sh"
            else
                SCRIPT="$SCRIPT_DIR/install-nghdl-23.04.sh"
            fi
            ;;
        "23.04")
            SCRIPT="$SCRIPT_DIR/install-nghdl-23.04.sh"
            ;;
        "24.04")
            SCRIPT="$SCRIPT_DIR/install-nghdl-24.04.sh"
            ;;
        *)
            echo "Unsupported Ubuntu version: $VERSION_ID ($FULL_VERSION)"
            exit 1
            ;;
    esac

    # Run the script if found
    if [[ -f "$SCRIPT" ]]; then
        echo "Running script: $SCRIPT $ARGUMENT"
        bash "$SCRIPT" "$ARGUMENT"
    else
        echo "Installation script not found: $SCRIPT"
        exit 1
    fi
}

# --- Main Execution Starts Here ---

# Validate argument
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
