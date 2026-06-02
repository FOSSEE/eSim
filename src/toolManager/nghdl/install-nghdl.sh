#!/bin/bash 
#==========================================================
#          FILE: install-nghdl.sh
# 
#         USAGE: ./install-nghdl.sh --install
#                 			OR
#                ./install-nghdl.sh --uninstall
# 
#   DESCRIPTION: Installation script for Ngspice, GHDL 
#                and Verilator simulators (NGHDL)
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, Rahul Paknikar, Sumanto Kar
#  ORGANIZATION: eSim, FOSSEE group at IIT Bombay
#       CREATED: Tuesday 02 December 2014 17:01
#      REVISION: Tuesday 02 February 2022 01:35
#==========================================================

nghdl="nghdl-simulator"
ghdl="ghdl-4.0.0"
verilator="verilator-4.210"
llvm_version="14"
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
    sudo apt install -y make
    
    echo "Installing GNAT..........................................."
    sudo apt install -y gnat

	echo "Installing LLVM-${llvm_version}........................................"
    sudo apt install -y llvm-${llvm_version} llvm-${llvm_version}-dev

    echo "Installing Clang.........................................."
    sudo apt install -y clang

    echo "Installing Zlib1g-dev....................................."
    sudo apt install -y zlib1g-dev
  
    # Specific dependency for canberra-gtk modules
    echo "Installing Gtk Canberra modules..........................."
    sudo apt install -y libcanberra-gtk-module libcanberra-gtk3-module

    # Specific dependency for nvidia graphic cards
    echo "Installing graphics dependency for Ngspice source build"
    echo "Installing libxaw7........................................"
    sudo apt install -y libxaw7

    echo "Installing libxaw7-dev...................................."
    sudo apt install -y libxaw7-dev


    echo "Installing dependencies for $verilator...................."
    if [[ -n "$(which apt 2> /dev/null)" ]]
    then
    # Ubuntu
        sudo apt install -y make autoconf g++ flex bison
    else [[ -n "$(which yum 2> /dev/null)" ]]
    # Ubuntu
        sudo yum install make autoconf flex bison which -y
        sudo yum groupinstall 'Development Tools'  -y
    fi

    echo "D1. installDependency Function"
}


function installGHDL
{   

    echo "Installing $ghdl LLVM................................."
    tar -xzf $ghdl.tar.gz
    echo "$ghdl successfully extracted"
    echo "Changing directory to $ghdl installation"
    cd $ghdl/
    echo "Configuring $ghdl build as per requirements"
    chmod +x configure
    # Other configure flags can be found at - https://github.com/ghdl/ghdl/blob/master/configure
    ./configure --with-llvm-config=/usr/bin/llvm-config-${llvm_version}
    echo "Building the install file for $ghdl LLVM"
    make
    sudo make install

    # set +e 		# Temporary disable exit on error
    # trap "" ERR # Do not trap on error of any command
    
    # echo "Removing unused part of $ghdl LLVM"
    # sudo rm -rf ../$ghdl
    
    # set -e 		# Re-enable exit on error
    # trap error_exit ERR

    echo "GHDL installed successfully"
    cd ../

    echo "D2. installGHDL Function"
    
}


function installVerilator
{   
    
    echo "Installing $verilator......................."
    tar -xJf $verilator.tar.xz
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
    #sudo rm -v -r'!("config.status"|"configure.ac"|"Makefile.in"|"verilator.1"|"configure"|"Makefile"|"src"|"verilator.pc")'

    echo "Verilator installed successfully"
    cd ../

    echo "D3. installVerilator Function"
}


function installNGHDL
{
    echo "Installing NGHDL..."
    
    # Extracting NGHDL
    cd $src_dir
    tar -xJf $nghdl-source.tar.xz -C $HOME
    mv $HOME/$nghdl-source $HOME/$nghdl

    echo "NGHDL extracted successfully to $HOME"
    cd $HOME/$nghdl
    mkdir -p install_dir
    mkdir -p release
    cd release
    chmod +x ../configure

    # Configure Ngspice-only build in Analog Mode
    if [ "$install_mode" == "--analog" ]; then
        echo "Configuring Ngspice for Analog Mode..."
        ../configure --enable-xspice --disable-debug --prefix=$HOME/$nghdl/install_dir/
    else
        echo "Configuring full NGHDL (Ngspice + GHDL + Verilator)..."
        ../configure --enable-xspice --disable-debug --prefix=$HOME/$nghdl/install_dir/
    fi

    make -j$(nproc)
    make install

    sudo chmod 755 $HOME/$nghdl/install_dir/bin/ngspice

    set +e 		# Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command

    echo "Removing previously installed Ngspice (if any)"    
    sudo apt-get purge -y ngspice

    echo "Adding softlink for the installed Ngspice..."
    sudo rm /usr/bin/ngspice
    sudo ln -sf $HOME/$nghdl/install_dir/bin/ngspice /usr/bin/ngspice
    echo "Added softlink for Ngspice....."

    echo "A1. installNGHDL Function"
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

    echo "A2. createConfigFile Function"

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

    echo "A3. createSoftLink"

}


#####################################################################
#       Script start from here                                     #
#####################################################################

### Checking if file is passsed as argument to script

if [ "$#" -ge 1 ]; then
    option=$1
    install_mode=${2:-"--all"}
else
    echo "USAGE:"
    echo "./install-nghdl.sh --install --analog"
    echo "./install-nghdl.sh --install --digital"
    echo "./install-nghdl.sh --uninstall --digital"
    echo "./install-nghdl.sh --uninstall"
    exit 1
fi

## Checking flags

if [ "$option" == "--install" ]; then
    set -e
    set -E
    trap error_exit ERR

    if [ "$install_mode" == "--analog" ]; then
        echo "Installing only Ngspice for Analog Mode..."
        installNGHDL  # Only installs Ngspice
        createConfigFile
        createSoftLink

    elif [ "$install_mode" == "--digital" ]; then
        echo "Installing full NGHDL (GHDL + Verilator + Ngspice)..."
        installDependency
        installGHDL
        installVerilator
        installNGHDL
        createConfigFile
        createSoftLink

    else
        echo "Invalid mode. Use --analog or --digital."
        exit 1
    fi

    echo "Installation complete!"


elif [ $option == "--uninstall" ];then
    if [ "$install_mode" == "--digital" ]; then
        echo "Uninstalling only digital components..."
        
        # Get LLVM version number (extract major version)
        llvm_full_version=$(dpkg -l | grep -oP 'llvm-\K[0-9]+' | head -n 1)
        
        if [ -z "$llvm_full_version" ]; then
            echo "Could not determine LLVM version, using default version 9."
            llvm_full_version=9
        fi
        
        echo "Detected LLVM version: $llvm_full_version"
        
        echo "D1. Removing GHDL..."
        cd $ghdl/
        sudo make uninstall
        cd ../
        sudo rm -rf $ghdl/
        
        echo "D2. Removing Verilator..."
        cd $verilator/
        sudo make uninstall
        cd ../
        sudo rm -rf $verilator/
        
        echo "D3. Removing libxaw7-dev..."
        sudo apt purge -y libxaw7-dev
        
        echo "D4. Removing LLVM..."
        sudo apt-get purge -y llvm-$llvm_full_version llvm-${llvm_full_version}-dev
        
        echo "D5. Removing GNAT..."
        sudo apt purge -y gnat
    else
        echo "Uninstalling all components..."
        sudo rm -rf $HOME/$nghdl $HOME/.nghdl /usr/share/kicad/library/eSim_Nghdl.lib /usr/local/bin/nghdl /usr/bin/ngspice

        echo "Removing GHDL..."
        cd $ghdl/
        sudo make uninstall
        cd ../
        sudo rm -rf $ghdl/
        
        echo "Removing Verilator..."
        cd $verilator/
        sudo make uninstall
        cd ../
        sudo rm -rf $verilator/
        
        echo "Removing libxaw7-dev..."
        sudo apt purge -y libxaw7-dev
        
        echo "Removing LLVM..."
        sudo apt-get purge -y llvm-${llvm_version} llvm-${llvm_version}-dev
        
        echo "Removing GNAT..."
        sudo apt purge -y gnat
    fi
else 
    echo "Please select the proper operation."
    echo "--install"
    echo "--uninstall"
fi
