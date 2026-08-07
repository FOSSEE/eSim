#!/bin/bash
#=====================================================================
#           FILE: install-ngspice-latest.sh
#
#        USAGE:  ./install-ngspice-latest.sh
#
#   DESCRIPTION: Installation script for ngspice latest version
#       OPTIONS: 
#  REQUIREMENTS: eSim/NGHDL must be installed first (for ngspice with OSDI)
#          BUGS: ---
#         NOTES: ---
#       Contributors: Sumanto Kar
#  ORGANIZATION: eSim Team, FOSSEE, IIT Bombay
#       CREATED: 2026-06-28
#=====================================================================

### CONFIG ###

sudo apt install build-essential git autoconf libtool automake libxaw7-dev libreadline-dev clang llvm lld cargo

git clone git://git.code.sf.net/p/ngspice/ngspice
cd ngspice

sudo mv /usr/bin/ngspice /usr/bin/ngspice35

./autogen.sh
mkdir release && cd release
../configure --with-x --enable-predictor --enable-osdi
make -j4
sudo make install
