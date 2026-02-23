#!/bin/bash
# Launcher script for testapp, ensuring proper Python and Qt environment
export PYTHONPATH=$HOME/eSim/src:$SNAP/usr/lib/python3/dist-packages:$SNAP/lib/python3.10/site-packages:$PYTHONPATH
export QT_LOGGING_RULES="qt5.*=false"  # Suppress Qt debug output (optional, remove for debugging)
# Force Qt to use non-native dialogs
# export QT_QPA_PLATFORMTHEME: ""  # Disable platform theme integration
# export QT_FILE_DIALOG_NON_NATIVE: "1"  # Force non-native dialogs
# export QT_QPA_MENUBAR_NO_NATIVE: "1"  # Disable native menu bar
# export QT_SYSTEM_TRAY_DISABLED: "1"  # Disable system tray integration
$SNAP/usr/bin/setup-esim.sh
cd $SNAP/eSim/src/frontEnd
# Run the Python application
exec python3 ./Application.py "$@"
