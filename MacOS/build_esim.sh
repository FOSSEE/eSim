#!/bin/bash

root_dir=$(pwd)

function installDependency {

    set +e          # Temporary disable exit on error
    trap "" ERR     # Do not trap on error of any command

    set -e          # Re-enable exit on error
    trap error_exit ERR
   
    echo "Creating virtual environment to isolate packages "
    python3 -m venv esim-env
    
    echo "Starting the virtual env..................."
    source esim-env/bin/activate

    echo "Upgrading Pip.............................."
    pip install --upgrade pip

    echo "Installing Required Dependencies..........."
    pip install PyQt5
    pip install numpy
    pip install matplotlib
    pip install scipy
    pip install watchdog
    pip install psutil
    pip install pyinstaller
    pip install makerchip-app
    pip install sandpiper-saas
    pip install setuptools
    pip install xterm
    pip install --upgrade https://github.com/hdl/pyhdlparser/tarball/master #python3 compatible hdlparse fork

    pip install pyinstaller #for app bundling
}

function buildNgspice {
    
}

function unzipFiles {
    echo "Unzipping nghdl folder..........................."
    unzip -o nghdl.zip -d nghdl

    echo "Unzipping esim symbols folder..........................."
    tar -xzf library/kicadLibrary.tar.xz -C library/
}

unzipFiles
installDependency