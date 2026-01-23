#!/bin/bash

VERSION_ID=$(grep "^VERSION_ID" /etc/os-release | cut -d '"' -f 2)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/install-nghdl-scripts"

echo "Detected Ubuntu: $VERSION_ID"

case "$VERSION_ID" in
    "22.04")
        SCRIPT="$SCRIPT_DIR/install-nghdl-22.04.sh"
        ;;
    "23.04")
        SCRIPT="$SCRIPT_DIR/install-nghdl-23.04.sh"
        ;;
    "24.04"|"25.04")
        SCRIPT="$SCRIPT_DIR/install-nghdl-24.04.sh"
        ;;
    *)
        echo "Unsupported Ubuntu version: $VERSION_ID"
        exit 1
        ;;
esac

chmod +x "$SCRIPT"
bash "$SCRIPT" "$1"

