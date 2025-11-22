#!/bin/bash

nghdl="nghdl-simulator"
ghdl="ghdl-4.1.0"
verilator="verilator-4.210"
config_dir="$HOME/.nghdl"
config_file="config.ini"
src_dir=`pwd`

error_exit() {
    echo -e "\n\nError! Kindly resolve above error(s) and try again."
    echo -e "Aborting Installation...\n"
    exit 1
}

###############################################
# LLVM FIX FOR UBUNTU 25.04
###############################################
installLLVM() {

    ubuntu_ver=$(lsb_release -rs)

    echo "Installing LLVM for GHDL..."

    if dpkg --compare-versions "$ubuntu_ver" ge "25.04"; then
        echo "Ubuntu 25.04 detected — Installing LLVM 15 + clang++-15"

        sudo apt install -y llvm-15 llvm-15-dev clang-15 clang-format-15 clang-tidy-15 clang-tools-15 zlib1g-dev

        sudo ln -sf /usr/bin/llvm-config-15 /usr/bin/llvm-config
        sudo ln -sf /usr/bin/clang++-15 /usr/bin/clang++
        sudo ln -sf /usr/bin/clang-15 /usr/bin/clang

    else
        echo "Using system LLVM..."
        sudo apt install -y llvm llvm-dev clang zlib1g-dev
    fi
}

###############################################
# INSTALL DEPENDENCIES
###############################################
installDependency() {

    echo "Installing Make, GNAT..."
    sudo apt install -y make gnat

    installLLVM

    echo "Installing graphics dependencies..."
    sudo apt install -y libxaw7 libxaw7-dev

    echo "Installing Verilator deps..."
    sudo apt install -y autoconf g++ flex bison
}

###############################################
# INSTALL GHDL (LLVM backend)
###############################################
installGHDL() {

    echo "Installing $ghdl..."

    tar xvf $ghdl.tar.gz
    cd $ghdl/

    chmod +x configure
    ./configure --with-llvm-config=/usr/bin/llvm-config

    make -j$(nproc)
    sudo make install

    cd ../
    echo "GHDL installed successfully."
}

###############################################
# INSTALL VERILATOR
###############################################
installVerilator() {

    echo "Installing $verilator..."

    tar -xvf $verilator.tar.xz
    cd $verilator

    chmod +x configure
    ./configure
    make -j$(nproc)
    sudo make install

    cd ../
    echo "Verilator installed successfully."
}

###############################################
# INSTALL NGHDL (Ngspice Digital)
###############################################
installNGHDL() {

    echo "Installing NGHDL..."

    cd $src_dir
    tar -xJf $nghdl-source.tar.xz -C $HOME
    mv $HOME/$nghdl-source $HOME/$nghdl

    cd $HOME/$nghdl

    mkdir -p install_dir release
    cd release

    chmod +x ../configure
    ../configure --enable-xspice --disable-debug \
        --prefix=$HOME/$nghdl/install_dir/ \
        --exec-prefix=$HOME/$nghdl/install_dir/

    make -j$(nproc)
    make install

    sudo chmod 755 $HOME/$nghdl/install_dir/bin/ngspice
    sudo rm -f /usr/bin/ngspice
    sudo ln -sf $HOME/$nghdl/install_dir/bin/ngspice /usr/bin/ngspice

    echo "NGHDL installed successfully."
}

###############################################
# CREATE CONFIG
###############################################
createConfigFile() {

    mkdir -p $config_dir
    rm -f $config_dir/$config_file

    echo "[NGHDL]" >> $config_dir/$config_file
    echo "NGHDL_HOME = $HOME/$nghdl" >> $config_dir/$config_file
    echo "DIGITAL_MODEL = %(NGHDL_HOME)s/src/xspice/icm" >> $config_dir/$config_file
    echo "RELEASE = %(NGHDL_HOME)s/release" >> $config_dir/$config_file
    echo "[SRC]" >> $config_dir/$config_file
    echo "SRC_HOME = $src_dir" >> $config_dir/$config_file
    echo "LICENSE = %(SRC_HOME)s/LICENSE" >> $config_dir/$config_file
}

###############################################
# CREATE SOFTLINK
###############################################
createSoftLink() {

    sudo chmod 755 $src_dir/src/ngspice_ghdl.py
    sudo ln -sf $src_dir/src/ngspice_ghdl.py /usr/local/bin/nghdl

    echo "Softlink for NGHDL created."
}

###############################################
# MAIN EXECUTION
###############################################
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 --install"
    exit 1
fi

option=$1

if [[ "$option" == "--install" ]]; then

    set -e
    set -E
    trap error_exit ERR

    installDependency
    installGHDL
    installVerilator
    installNGHDL
    createConfigFile
    createSoftLink

    echo "---------- NGHDL Installed Successfully ----------"

else
    echo "Invalid option."
    exit 1
fi

