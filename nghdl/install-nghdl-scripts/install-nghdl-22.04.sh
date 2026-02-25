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
#        AUTHOR: Fahim Khan, Rahul Paknikar, Sumanto Kar,
#                Shiva Krishna Sangati, Jayanth Tatineni, Anshul Verma
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
    sudo apt install -y make
    
    echo "Installing GNAT..........................................."
    sudo apt install -y gnat
    
    # It will remove older versions of llvm if any 
    echo "Removing older LLVM........................................"
    sudo apt remove -y llvm llvm-dev

    echo "Installing LLVM........................................"
    sudo apt install -y llvm llvm-dev

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
    # Other configure flags can be found at - https://github.com/ghdl/ghdl/blob/master/configure
    ./configure --with-llvm-config=/usr/bin/llvm-config
    echo "Building the install file for $ghdl LLVM"
    make -j$(nproc)
    sudo make install

    # set +e 		# Temporary disable exit on error
    # trap "" ERR # Do not trap on error of any command
    
    # echo "Removing unused part of $ghdl LLVM"
    # sudo rm -rf ../$ghdl
    
    # set -e 		# Re-enable exit on error
    # trap error_exit ERR

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
    #sudo rm -v -r'!("config.status"|"configure.ac"|"Makefile.in"|"verilator.1"|"configure"|"Makefile"|"src"|"verilator.pc")'

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
            
    # Adding patch to Ngspice base code
    # cp $src_dir/src/outitf.c $HOME/$nghdl/src/frontend

    make -j$(nproc)
    make install

    # Make it executable
    sudo chmod 755 $HOME/$nghdl/install_dir/bin/ngspice
    
    set +e 		# Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command

    echo "Removing previously installed Ngspice (if any)"    
    sudo apt-get purge -y ngspice

    echo "NGHDL installed sucessfully"
    echo "Adding softlink for the installed Ngspice"

    # Add symlink to the path
    sudo rm /usr/bin/ngspice

    set -e 		# Re-enable exit on error
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
#       Script start from here                                     #
#####################################################################

### Checking if file is passsed as argument to script

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
    
    #Calling functions
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
    # sudo rm -rf /usr/local/bin/ghdl /usr/local/bin/ghdl1-llvm /usr/local/lib/ghdl /usr/local/lib/libghdlvpi.so /usr/local/include/vpi_user.h

    echo "Removing Verilator................."
    cd $verilator/
    sudo make uninstall
    cd ../
    sudo rm -rf $verilator/

    echo "Removing libxaw7-dev..............."
    sudo apt purge -y libxaw7-dev
    echo "Removing LLVM......................"
    sudo apt-get purge -y llvm-${llvm_version} llvm-${llvm_version}-dev
    echo "Removing GNAT......................"
    sudo apt purge -y gnat
else 
    echo "Please select the proper operation."
    echo "--install"
    echo "--uninstall"
fi
