#!/bin/bash
#=============================================================================
#          FILE: install-eSim.sh
# 
#         USAGE: ./install-eSim.sh --install 
#                            OR
#                ./install-eSim.sh --uninstall
#                
#   DESCRIPTION: Installation script for eSim EDA Suite
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#       AUTHORS: Fahim Khan, Rahul Paknikar, Saurabh Bansode,
#                Sumanto Kar, Partha Singha Roy, Jayanth Tatineni,
#                Anshul Verma, Shiva Krishna Sangati, Harsha Narayana P
#  ORGANIZATION: eSim Team, FOSSEE, IIT Bombay
#       CREATED: Wednesday 15 July 2015 15:26
#      REVISION: Sunday 15 November 2026 12:15
#=============================================================================

# Function to detect Ubuntu version and full version string
get_ubuntu_version() {
    # Check whether OS information available
    if [[ ! -r /etc/os-release ]]; then
        echo "/etc/os-release not readable"
        exit 1
    fi

    source /etc/os-release

    # Verify Linux distribution
    if [[ "$ID" != "ubuntu" ]]; then
        echo "Installer supports Ubuntu only."
        exit 1
    fi

    FULL_VERSION=$(lsb_release -d | grep -oP '\d+\.\d+(?:\.\d+)?')
    echo "Detected Ubuntu Version: $FULL_VERSION"
}

# Function to choose and run the appropriate script
run_version_script() {
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/install-eSim-scripts"
    
    # Decide script based on full version
    case "$VERSION_ID" in
        "22.04")
            if [[ "$FULL_VERSION" == "22.04.4" ]]; then
                SCRIPT="$SCRIPT_DIR/install-eSim-22.04.sh"
            else
                SCRIPT="$SCRIPT_DIR/install-eSim-23.04.sh"
            fi
            ;;
        "23.04")
            SCRIPT="$SCRIPT_DIR/install-eSim-23.04.sh"
            ;;
        "24.04")
            SCRIPT="$SCRIPT_DIR/install-eSim-24.04.sh"
            ;;
        "25.04")
            SCRIPT="$SCRIPT_DIR/install-eSim-25.04.sh"
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
        echo "Installation Script not found: $SCRIPT"
        exit 1
    fi
}


# --- Main Execution Starts Here ---

####################################################################
#                   MAIN START FROM HERE                           #
####################################################################

# Checking if file is passed as argument to script
if [[ "$#" -ne 1 ]]; then
    echo "Usage: $0 --install | --uninstall"
    exit 1
fi

ARGUMENT="$1"
if [[ "$ARGUMENT" != "--install" && "$ARGUMENT" != "--uninstall" ]]; then
    echo "Invalid argument: $ARGUMENT"
    echo "Usage: $0 --install | --uninstall"
    exit 1
fi

get_ubuntu_version
run_version_script
