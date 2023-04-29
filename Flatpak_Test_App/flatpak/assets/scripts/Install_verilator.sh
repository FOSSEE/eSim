#!/bin/bash

# Install dependencies
sudo apt-get update
sudo apt-get install git make autoconf g++ flex bison -y

# Clone Verilator repository
git clone http://git.veripool.org/git/verilator

# Switch to version 4.106
cd verilator
git checkout v4.106

# Build Verilator
autoconf
./configure
make
sudo make install