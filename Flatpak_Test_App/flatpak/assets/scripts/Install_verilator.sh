#!/bin/bash

# Clone Verilator repository
echo '# Please wait... cloning https://github.com/verilator/verilator'
git clone http://git.veripool.org/git/verilator
echo '# repo cloned...'

cd verilator
echo '# changing dir to verilator/'

# Switch to version 4.106
git checkout v4.106

# Build Verilator
autoconf
./configure
echo '# please wait... This may take some time'

cd ./verilator/

make
echo 'installing make...'

make install

echo '# verilator installed...'
verilator --version
