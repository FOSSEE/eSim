#!/bin/bash 
#==========================================================
#          FILE: install-nghdl-arch.sh
# 
#         USAGE: ./install-nghdl.sh --install
#                 		OR
#                ./install-nghdl.sh --uninstall
# 
#   DESCRIPTION: Installation script for Ngspice, GHDL 
#                and Verilator simulators (NGHDL) - Arch Linux
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, Rahul Paknikar, Sumanto Kar,
#                Harsha Narayana P, Jayanth Tatineni, Anshul Verma
#  ORGANIZATION: eSim, FOSSEE group at IIT Bombay
#       CREATED: Tuesday 02 December 2014 17:01
#      REVISION: Monday 23 June 2025 15:20
#==========================================================

nghdl="nghdl-simulator"
ghdl="ghdl-4.1.0"
verilator="verilator-4.210"
config_dir="$HOME/.nghdl"
config_file="config.ini"
src_dir=`pwd`

# Will be used to take backup of any file
sysdate="$(date)"
timestamp=`echo $sysdate|awk '{print $3"_"$2"_"$6"_"$4 }'`


# All functions goes here

error_exit() {
    echo -e "\n\nError! Kindly resolve above error(s) and try again."
    echo -e "\nAborting Installation...\n"
}


function installDependency
{
    echo "Installing dependencies for $ghdl LLVM................"

    echo "Installing Make..........................................."
    sudo pacman -S --noconfirm --needed make

    echo "Installing GNAT..........................................."
    # On Arch, GNAT is bundled with gcc-ada
    sudo pacman -S --noconfirm --needed gcc-ada

    # GHDL 4.1.0 supports LLVM up to 18.1 only.
    # Arch's rolling llvm is too new (19+), so we install llvm18 from AUR.
    echo "Installing LLVM 18 (AUR - required by GHDL 4.1.0)....."
    $AUR_HELPER -S --noconfirm --needed llvm18 llvm18-libs

    echo "Installing Clang.........................................."
    sudo pacman -S --noconfirm --needed clang

    echo "Installing zlib (zlib1g-dev equivalent)..................."
    sudo pacman -S --noconfirm --needed zlib

    # libcanberra for GTK modules
    echo "Installing libcanberra (GTK modules)....................."
    sudo pacman -S --noconfirm --needed libcanberra

    # Xaw / libxaw (nvidia / ngspice graphics dependency)
    echo "Installing libxaw (Ngspice graphics dependency)........."
    sudo pacman -S --noconfirm --needed libxaw

    echo "Installing dependencies for $verilator..................."
    sudo pacman -S --noconfirm --needed autoconf flex bison base-devel
}


function installGHDL
{   
    echo "Installing $ghdl LLVM................................."
    tar xvf $ghdl.tar.gz
    echo "$ghdl successfully extracted"
    echo "Changing directory to $ghdl installation"
    cd $ghdl/
    echo "Configuring $ghdl build as per requirements"
    chmod +x configure
    # GHDL 4.1.0 supports LLVM up to 18.1. On Arch we install llvm18 from AUR
    # which provides llvm-config-18 at /usr/lib/llvm18/bin/llvm-config.
    ./configure --with-llvm-config=/usr/lib/llvm18/bin/llvm-config
    echo "Building the install file for $ghdl LLVM"
    make -j$(nproc)
    sudo make install

    echo "GHDL installed successfully"
    cd ../
}


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
    make -j$(nproc)
    sudo make install
    echo "Removing the unessential verilator files........"
    rm -r docs
    rm -r examples
    rm -r include
    rm -r test_regress
    rm -r bin
    ls -1 | grep -E -v 'config.status|configure.ac|Makefile.in|verilator.1|configure|Makefile|src|verilator.pc' | xargs rm -f

    echo "Verilator installed successfully"
    cd ../
}


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
    ../configure --enable-xspice --disable-debug  --prefix=$HOME/$nghdl/install_dir/ --exec-prefix=$HOME/$nghdl/install_dir/

    make -j$(nproc)
    make install

    # Make it executable
    sudo chmod 755 $HOME/$nghdl/install_dir/bin/ngspice

    set +e      # Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command

    echo "Removing previously installed Ngspice (if any)"
    # On Arch, ngspice is a pacman package — use pacman to remove it cleanly
    sudo pacman -Rns --noconfirm ngspice 2>/dev/null || true

    echo "NGHDL installed sucessfully"
    echo "Adding softlink for the installed Ngspice"

    # Add symlink to the path
    sudo rm -f /usr/bin/ngspice

    set -e      # Re-enable exit on error
    trap error_exit ERR

    sudo ln -sf $HOME/$nghdl/install_dir/bin/ngspice /usr/bin/ngspice
    echo "Added softlink for Ngspice....."
}


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


#####################################################################
#       Script start from here                                      #
#####################################################################

### Checking if file is passed as argument to script

if [ "$#" -eq 1 ];then
    option=$1
else
    echo "USAGE : "
    echo "./install-nghdl.sh --install"
    exit 1;
fi

## Checking flags
if [ $option == "--install" ];then

    set -e  # Set exit option immediately on error
    set -E  # inherit ERR trap by shell functions

    # Trap on function error_exit before exiting on error
    trap error_exit ERR

    # Calling functions
    installDependency
    if [ $? -ne 0 ];then
        echo -e "\n\n\nERROR: Unable to install required packages. Please check your internet connection.\n\n"
        exit 0
    fi

    installGHDL
    installVerilator
    installNGHDL
    createConfigFile
    createSoftLink

elif [ $option == "--uninstall" ];then
    sudo rm -rf $HOME/$nghdl $HOME/.nghdl /usr/share/kicad/library/eSim_Nghdl.lib /usr/local/bin/nghdl /usr/bin/ngspice

    echo "Removing GHDL......................"
    cd $ghdl/
    sudo make uninstall
    cd ../
    sudo rm -rf $ghdl/

    echo "Removing Verilator................."
    cd $verilator/
    sudo make uninstall
    cd ../
    sudo rm -rf $verilator/

    echo "Removing libxaw....................."
    sudo pacman -Rns --noconfirm libxaw
    echo "Removing LLVM 18........................"
    sudo pacman -Rns --noconfirm llvm18 llvm18-libs
    echo "Removing GNAT / gcc-ada............."
    sudo pacman -Rns --noconfirm gcc-ada
else 
    echo "Please select the proper operation."
    echo "--install"
    echo "--uninstall"
fi
