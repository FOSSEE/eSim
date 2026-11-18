#!/bin/bash
# Fetch and unpack the GHDL 4.1.0 source tree used by the NGHDL installer.
set -euo pipefail
W=/mnt/e/fossee/Evidence_Ubuntu2504/work
mkdir -p "$W/src"
cd "$W/src"
if [ ! -d ghdl-4.1.0 ]; then
    echo "=== fetching GHDL 4.1.0 source"
    curl -sL --max-time 900 -o ghdl-4.1.0.tar.gz \
        "https://github.com/ghdl/ghdl/archive/refs/tags/v4.1.0.tar.gz"
    ls -la ghdl-4.1.0.tar.gz
    tar xzf ghdl-4.1.0.tar.gz
fi
echo "=== source tree:"
ls -d "$W"/src/ghdl-*/
