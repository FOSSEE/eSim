#!/bin/sh

echo "Installing ngspice..."
echo "==========================="

# write a script to install ngspice on any platform

# Download ngspice source code from GitHub
git clone https://github.com/ngspice/ngspice.git

# Change directory to ngspice folder
cd ngspice

# Install prerequisites

# Configure and build ngspice
echo '# please wait... This may take some time'
echo "===============================================\n"
./autogen.sh
./configure
make
sudo make install

# Add ngspice executable to PATH environment variable
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
source ~/.bashrc

# Test ngspice installation
ngspice --version