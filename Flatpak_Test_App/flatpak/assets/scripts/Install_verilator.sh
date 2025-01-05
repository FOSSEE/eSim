#!/bin/bash

## Clone Verilator repository

echo '# Please wait... cloning https://github.com/verilator/verilator'
git clone http://git.veripool.org/git/verilator
echo '# repo cloned...'
echo "===============================================\n"

echo '# changing dir to verilator/'
cd ./verilator

echo '# current working directory is: ' 
pwd
echo "===============================================\n"

# Switch to version 4.106
git checkout v4.106

# Build Verilator
autoconf

echo '# please wait... This may take some time'
echo "===============================================\n"
./configure --prefix=/usr --libdir=/usr/lib64

echo '# current working directory is (supposed to be verilator): ' 
pwd
echo "==========================="
echo "Please enter root password:"
flatpak-spawn --host sudo -S make


echo 'Installing make...'
echo "==========================="
echo "Please enter root password:"
flatpak-spawn --host sudo -S make install

flatpak-spawn --host verilator --version

echo "===============================================\n"
echo "Cleaning up..."

flatpak-spawn --host rm -rf ./verilator