#!/bin/bash
#==================================================
#          FILE: install-nghdl.sh
#         USAGE: ./install-nghdl.sh
#   DESCRIPTION: Script to install nghdl
#==================================================

# ==========
# Variables
# ==========

nghdl="nghdl-simulator"
#ghdl="ghdl-4.1.0"
verilator="verilator-4.210"
config_dir="$HOME/.nghdl"
config_file="config.ini"
src_dir="$(pwd)"

# Will be used to take backup of any file
# sysdate="$(date)"
# timestamp=`echo $sysdate|awk '{print $3"_"$2"_"$6"_"$4 }'`

# ===============
# Error function
# ===============

error_exit()
{
    echo -e "\n\nError! Kindly resolve above error(s) and try again."
    echo -e "\nAborting Installation...\n"
}

# =================================
# Function to install Dependencies
# =================================

# =========================
# Function to install GHDL
# =========================



# ==============================
# Function to install Verilator
# ==============================

function installVerilator
{
    echo "Installing $verilator......................."
    tar -xvf $verilator.tar.xz
    echo "$verilator successfully extracted"
    echo "Changing directory to $verilator installation"
    cd $verilator
    echo "Configuring $verilator build as per requirements"
    chmod +x configure
    ./configure
    make -j$(sysctl -n hw.ncpu) # macOS cpu cores
    sudo make install
    echo "Removing the unessential verilator files........"
    rm -r docs
    rm -r examples
    rm -r include
    rm -r test_regress
    rm -r bin
    ls -1 | grep -E -v 'config.status|configure.ac|Makefile.in|verilator.1|configure|Makefile|src|verilator.pc' | xargs rm -f
    #sudo rm -v -r'!("config.status"|"configure.ac"|"Makefile.in"|"verilator.1"|"configure"|"Makefile"|"src"|"verilator.pc")'

    echo "Verilator installed successfully"
    cd ../
}

# ==============================
# Function to install Ngspice
# ==============================

function installNGHDL
{
    echo "Installing NGHDL........................................"

    # Extracting NGHDL to Home Directory
    cd $src_dir
    tar -xJf $nghdl-source.tar.xz -C $HOME
    mv $HOME/$nghdl-source $HOME/$nghdl

    echo "NGHDL extracted sucessfully to $HOME"
    # Change to nghdl directory
    cd $HOME/$nghdl
    # Make local install directory
    mkdir -p install_dir
    # Make release directory for build
    mkdir -p release
    # Change to release directory
    cd release
    echo "Configuring NGHDL..........."
    sleep 2
    
    chmod +x ../configure
    ../confi.gure --enable-xspice --disable-debug  --prefix=$HOME/$nghdl/install_dir/ --exec-prefix=$HOME/$nghdl/install_dir/
            
    # Adding patch to Ngspice base code
    # cp $src_dir/src/outitf.c $HOME/$nghdl/src/frontend

    make -j$(sysctl -n hw.ncpu) # macOS cpu cores
    make install

    # Make it executable
    sudo chmod 755 $HOME/$nghdl/install_dir/bin/ngspice
    
    set +e 		# Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command

    echo "NGHDL installed sucessfully"
    echo "Adding softlink for the installed Ngspice"

    # Add symlink to the path
    sudo rm /usr/local/bin/ngspice

    set -e 		# Re-enable exit on error
    trap error_exit ERR

    sudo ln -sf $HOME/$nghdl/install_dir/bin/ngspice /usr/local/bin/ngspice
    echo "Added softlink for Ngspice....."
}

# =======================================================
# Function to create softlink (ngspice_ghdl.py --> nghdl)
# =======================================================

function createSoftLink
{
    # Make it executable
    sudo chmod 755 $src_dir/src/ngspice_ghdl.py

    # Creating softlink
    cd /usr/local/bin
    if [[ -L nghdl ]];then
        echo "Symlink was already present"
        sudo unlink nghdl
    fi
    
    sudo ln -sf $src_dir/src/ngspice_ghdl.py nghdl
    echo "Added softlink for NGHDL....."

    cd $pwd
}

# =======================================
# Function to create NGHDL configurations
# =======================================

function createConfigFile
{
    # Creating config.ini file and adding configuration information
    # Check if config file is present
    if [ -d $config_dir ];then
        rm $config_dir/$config_file && touch $config_dir/$config_file
    else
        mkdir $config_dir && touch $config_dir/$config_file
    fi

    echo "[NGHDL]" >> $config_dir/$config_file
    echo "NGHDL_HOME = $HOME/$nghdl" >> $config_dir/$config_file
    echo "DIGITAL_MODEL = %(NGHDL_HOME)s/src/xspice/icm" >> $config_dir/$config_file
    echo "RELEASE = %(NGHDL_HOME)s/release" >> $config_dir/$config_file
    echo "[SRC]" >> $config_dir/$config_file
    echo "SRC_HOME = $src_dir" >> $config_dir/$config_file
    echo "LICENSE = %(SRC_HOME)s/LICENSE" >> $config_dir/$config_file
}

# ===========================
# Interactive Menu
# ===========================

function show_menu {
    echo "Select the step you want to run:"
    echo "1) Install Verilator"
    echo "2) Install NGHDL"
    echo "3) Create NGHDL Softlink"
    echo "4) Create NGHDL Config File"
    echo "5) Exit"
    read -p "Enter choice [1-5]: " choice
    case $choice in
        1) installVerilator ;;
        2) installNGHDL ;;
        3) createSoftLink ;;
        4) createConfigFile ;;
        5) echo "Exiting..."; exit 0 ;;
        *) echo "Invalid choice"; show_menu ;;
    esac
}

# ===========================
# Main Logic
# ===========================

if [ $# -eq 0 ]; then
    show_menu
else
    case $1 in
        verilator) installVerilator ;;
        nghdl) installNGHDL ;;
        softlink) createSoftLink ;;
        config) createConfigFile ;;
        *) echo "Unknown argument. Use one of: verilator, nghdl, softlink, config" ;;
    esac
fi

