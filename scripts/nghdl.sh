#!/bin/sh

# Set PYTHONPATH so relative imports in ngspice_ghdl.py work
export PYTHONPATH=$SNAP/nghdl/src:$PYTHONPATH

# Execute the main script with Python
exec python3 $SNAP/nghdl/src/ngspice_ghdl.py "$@"