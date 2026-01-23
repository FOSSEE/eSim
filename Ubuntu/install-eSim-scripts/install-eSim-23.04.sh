#!/bin/bash 
#=============================================================================
#          FILE: install-eSim.sh
# 
#         USAGE: ./install-eSim.sh --install 
#                            OR
#                ./install-eSim.sh --uninstall
#                
#   DESCRIPTION: Installation script for eSim EDA Suite
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#       AUTHORS: Fahim Khan, Rahul Paknikar, Saurabh Bansode,
#                Sumanto Kar, Partha Singha Roy, Jayanth Tatineni,
#                Anshul Verma
#  ORGANIZATION: eSim Team, FOSSEE, IIT Bombay
#       CREATED: Wednesday 15 July 2015 15:26
#      REVISION: Sunday 25 May 2025 17:40
#=============================================================================
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
KICAD_CONFIG="/home/vishal/.config/kicad/6.0"


sudo apt install -y libxcb-xinerama0 libxcb1 libx11-xcb1 libxcb-glx0 libxcb-util1 libxrender1 libxi6 libxrandr2 libqt5gui5 libqt5core5a libqt5widgets5

# Creating the Virtual Environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    
    # Try to find a usable Python 3 version
    PYTHON_BIN=$(which python3.11 || which python3.10 || which python3)

    if [ -z "$PYTHON_BIN" ]; then
        echo "No suitable Python 3.x found. Please install Python 3.10 or 3.11."
        exit 1
    fi

    PYTHON_VERSION=$($PYTHON_BIN -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    VENV_PACKAGE="python${PYTHON_VERSION}-venv"
    
    # Check if the venv module is available
    if ! $PYTHON_BIN -m venv --help > /dev/null 2>&1; then
        echo "! venv not found for Python $PYTHON_VERSION. Attempting to install $VENV_PACKAGE..."
        sudo apt update
        sudo apt install -y "$VENV_PACKAGE"
    fi
    
    # Try to fix ensurepip-related issues
    
    if ! $PYTHON_BIN -c "import ensurepip" &>/dev/null; then
        echo "! ensurepip is missing. Installing full Python package for $PYTHON_VERSION..."
        sudo apt install -y "python${PYTHON_VERSION}-full"
    fi

    $PYTHON_BIN -m venv venv
    # python3.11 -m venv venv      
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source ./venv/bin/activate

# Ensure virtual environment is deactivated when script exits
trap 'if [[ -d "venv" ]]; then deactivate; fi' EXIT

# Update Sources list if necessary
# Get Ubuntu version
UBUNTU_VERSION=$(lsb_release -rs)
UBUNTU_CODENAME=$(lsb_release -cs)

echo "Detected Ubuntu version: $UBUNTU_VERSION ($UBUNTU_CODENAME)"

# Check if running Ubuntu 23.04 (Lunar)
if [[ "$UBUNTU_CODENAME" == "lunar" ]]; then
    echo "Ubuntu 23.04 detected. Checking sources list..."

    # Check if the old-releases mirror is already set
    if grep -q "old-releases.ubuntu.com" /etc/apt/sources.list; then
        echo "Old-releases mirror is already in use. No changes needed."
    else
        echo "Switching to old-releases mirror..."
        
        # Backup existing sources.list (only if not backed up before)
        if [ ! -f /etc/apt/sources.list.bak ]; then
            sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
        fi

        # Replace standard mirrors with old-releases
        sudo sed -i 's|http://\(.*\).ubuntu.com/ubuntu|http://old-releases.ubuntu.com/ubuntu|g' /etc/apt/sources.list

        echo "Updated sources.list to use old-releases. Running apt update..."
        
        # Update package lists
        sudo apt update -y && sudo apt upgrade -y
    fi
else
    echo "Not running Ubuntu 23.04, no changes needed."
fi

# All variables goes here
config_dir="$HOME/.esim"
config_file="config.ini"
eSim_Home=`pwd`
ngspiceFlag=0

## All Functions goes here

error_exit()
{

    echo -e "\n\nError! Kindly resolve above error(s) and try again."
    echo -e "\nAborting Installation...\n"

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
    
    echo "[eSim]" >> $config_dir/$config_file
    echo "eSim_HOME = $eSim_Home" >> $config_dir/$config_file
    echo "LICENSE = %(eSim_HOME)s/LICENSE" >> $config_dir/$config_file
    echo "KicadLib = %(eSim_HOME)s/library/kicadLibrary.tar.xz" >> $config_dir/$config_file
    echo "IMAGES = %(eSim_HOME)s/images" >> $config_dir/$config_file
    echo "VERSION = %(eSim_HOME)s/VERSION" >> $config_dir/$config_file
    echo "MODELICA_MAP_JSON = %(eSim_HOME)s/library/ngspicetoModelica/Mapping.json" >> $config_dir/$config_file
    
}


function installNghdl
{

    echo "Installing NGHDL..........................."

cd "$BASE_DIR"
unzip -o nghdl.zip
cd nghdl

chmod +x install-nghdl.sh


    # Do not trap on error of any command. Let NGHDL script handle its own errors.
    trap "" ERR

    ./install-nghdl.sh --install       # Install NGHDL
        
    # Set trap again to error_exit function to exit on errors
    trap error_exit ERR

    ngspiceFlag=1
    cd ../

}


function installSky130Pdk
{

    echo "Installing SKY130 PDK......................"
    
    # Extract SKY130 PDK
    tar -xJf library/sky130_fd_pr.tar.xz

    # Remove any previous sky130-fd-pdr instance, if any
    sudo rm -rf /usr/share/local/sky130_fd_pr

    # Copy SKY130 library
    echo "Copying SKY130 PDK........................."

    sudo mkdir -p /usr/share/local/
    sudo mv sky130_fd_pr /usr/share/local/

    # Change ownership from root to the user
    sudo chown -R $USER:$USER /usr/share/local/sky130_fd_pr/

}


function installKicad
{
    echo "Installing KiCad..........................."
      sudo rm -f /etc/apt/sources.list.d/kicad*
    sudo add-apt-repository --remove ppa:kicad/kicad-6.0-releases -y 2>/dev/null
    sudo add-apt-repository --remove ppa:kicad/kicad-8.0-releases -y 2>/dev/null
    sudo apt-get update

    ubuntu_version=$(lsb_release -rs)

    if [[ "$ubuntu_version" == "25.04" ]]; then
        echo "Ubuntu 25.04 detected — using official Ubuntu repository"
        sudo apt update
        sudo apt install -y kicad
        return
    fi

    if [[ "$ubuntu_version" == "24.04" ]]; then
        echo "Ubuntu 24.04 detected — using KiCad 8 PPA"
        sudo add-apt-repository -y ppa:kicad/kicad-8.0-releases
        sudo apt update
        sudo apt install -y kicad
        return
    fi

    echo "Unsupported Ubuntu version for KiCad"
    exit 1
}



function installDependency
{

    set +e      # Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command

    # Update apt repository
    echo "Updating apt index files..................."
    sudo apt-get update
    
    set -e      # Re-enable exit on error
    trap error_exit ERR
    
    echo "Installing Xterm..........................."
    sudo apt-get install -y xterm
    
    echo "Installing Psutil.........................."
    sudo apt-get install -y python3-psutil
    
    echo "Installing PyQt5..........................."
    #sudo apt-get install -y python3-pyqt5
    pip install PyQt5

    echo "Installing Matplotlib......................"
    #sudo apt-get install -y python3-matplotlib
    pip install matplotlib

    echo "Installing Distutils......................."


    # Install NgVeri Depedencies
    echo "Installing Pip3............................"
    sudo apt install -y python3-pip

    echo "Installing Watchdog........................"
    #sudo apt install watchdog
    pip install watchdog

    echo "Installing Hdlparse........................"
    pip3 install --upgrade https://github.com/hdl/pyhdlparser/tarball/master
    pip3 install hdlparse

    echo "Installing Makerchip......................."
    pip3 install makerchip-app

    echo "Installing SandPiper Saas.................."
    pip3 install sandpiper-saas

}


function copyKicadLibrary
{

    #Extract custom KiCad Library
tar xf "$BASE_DIR/library/kicadLibrary.tar.xz" -C /usr/share/kicad


    if [ -d ~/.config/kicad/6.0 ];then
        echo "kicad config folder already exists"
    else 
        echo ".config/kicad/6.0 does not exist"
        mkdir -p ~/.config/kicad/6.0
    fi

    # Copy symbol table for eSim custom symbols 

cp "$BASE_DIR/library/kicadLibrary/template/sym-lib-table" "$KICAD_CONFIG/sym-lib-table"


    echo "symbol table copied in the directory"

    # Copy KiCad symbols made for eSim
    mkdir -p "$KICAD_CONFIG/symbols"
cp "$BASE_DIR/library/kicadLibrary/eSim-symbols/"* "$KICAD_CONFIG/symbols/"


    set +e      # Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command
    
    # Remove extracted KiCad Library - not needed anymore
    rm -rf kicadLibrary

    set -e      # Re-enable exit on error
    trap error_exit ERR

    #Change ownership from Root to the User
    sudo chown -R $USER:$USER /usr/share/kicad/symbols/

}


function createDesktopStartScript
{    

    # Generating new esim-start.sh
    echo '#!/bin/bash' > esim-start.sh
    echo "cd $eSim_Home/src/frontEnd || exit" >> esim-start.sh
    echo "$eSim_Home/venv/bin/python Application.py" >> esim-start.sh

    # Make it executable
    sudo chmod 755 esim-start.sh
    # Copy esim start script
    sudo cp -vp esim-start.sh /usr/bin/esim
    # Remove local copy of esim start script
    rm esim-start.sh

    # Generating esim.desktop file
    echo "[Desktop Entry]" > esim.desktop
    echo "Version=1.0" >> esim.desktop
    echo "Name=eSim" >> esim.desktop
    echo "Comment=EDA Tool" >> esim.desktop
    echo "GenericName=eSim" >> esim.desktop
    echo "Keywords=eda-tools" >> esim.desktop
    echo "Exec=esim %u" >> esim.desktop
    echo "Terminal=true" >> esim.desktop
    echo "X-MultipleArgs=false" >> esim.desktop
    echo "Type=Application" >> esim.desktop
    getIcon="$config_dir/logo.png"
    echo "Icon=$getIcon" >> esim.desktop
    echo "Categories=Development;" >> esim.desktop
    echo "MimeType=text/html;text/xml;application/xhtml+xml;application/xml;application/rss+xml;application/rdf+xml;image/gif;image/jpeg;image/png;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;x-scheme-handler/chrome;video/webm;application/x-xpinstall;" >> esim.desktop
    echo "StartupNotify=true" >> esim.desktop

    # Make esim.desktop file executable
    sudo chmod 755 esim.desktop
    # Copy desktop icon file to share applications
    sudo cp -vp esim.desktop /usr/share/applications/
    # Copy desktop icon file to Desktop
    cp -vp esim.desktop $HOME/Desktop/

    set +e      # Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command

    # Make esim.desktop file as trusted application
    gio set $HOME/Desktop/esim.desktop "metadata::trusted" true
    # Set Permission and Execution bit
    chmod a+x $HOME/Desktop/esim.desktop

    # Remove local copy of esim.desktop file
    rm esim.desktop

    set -e      # Re-enable exit on error
    trap error_exit ERR

    # Copying logo.png to .esim directory to access as icon
    cp -vp images/logo.png $config_dir

}


####################################################################
#                   MAIN START FROM HERE                           #
####################################################################

### Checking if file is passsed as argument to script

if [ "$#" -eq 1 ];then
    option=$1
else
    echo "USAGE : "
    echo "./install-eSim.sh --install"
    echo "./install-eSim.sh --uninstall"
    exit 1;
fi

## Checking flags

if [ $option == "--install" ];then

    set -e  # Set exit option immediately on error
    set -E  # inherit ERR trap by shell functions

    # Trap on function error_exit before exiting on error
    trap error_exit ERR


    echo "Enter proxy details if you are connected to internet thorugh proxy"
    
    echo -n "Is your internet connection behind proxy? (y/n): "
    read getProxy
    if [ $getProxy == "y" -o $getProxy == "Y" ];then
        echo -n 'Proxy Hostname :'
        read proxyHostname

        echo -n 'Proxy Port :'
        read proxyPort

        echo -n username@$proxyHostname:$proxyPort :
        read username

        echo -n 'Password :'
        read -s passwd

        unset http_proxy
        unset https_proxy
        unset HTTP_PROXY
        unset HTTPS_PROXY
        unset ftp_proxy
        unset FTP_PROXY

        export http_proxy=http://$username:$passwd@$proxyHostname:$proxyPort
        export https_proxy=http://$username:$passwd@$proxyHostname:$proxyPort
        export https_proxy=http://$username:$passwd@$proxyHostname:$proxyPort
        export HTTP_PROXY=http://$username:$passwd@$proxyHostname:$proxyPort
        export HTTPS_PROXY=http://$username:$passwd@$proxyHostname:$proxyPort
        export ftp_proxy=http://$username:$passwd@$proxyHostname:$proxyPort
        export FTP_PROXY=http://$username:$passwd@$proxyHostname:$proxyPort

        echo "Install with proxy"

    elif [ $getProxy == "n" -o $getProxy == "N" ];then
        echo "Install without proxy"
    
    else
        echo "Please select the right option"
        exit 0    
    fi

    # Calling functions
    createConfigFile
    installDependency
    installKicad
    copyKicadLibrary
    installNghdl
    installSky130Pdk
    createDesktopStartScript

    if [ $? -ne 0 ];then
        echo -e "\n\n\nERROR: Unable to install required packages. Please check your internet connection.\n\n"
        exit 0
    fi

    echo "-----------------eSim Installed Successfully-----------------"
    echo "Type \"esim\" in Terminal to launch it"
    echo "or double click on \"eSim\" icon placed on Desktop"


elif [ $option == "--uninstall" ];then
    echo -n "Are you sure? It will remove eSim completely including KiCad, Makerchip, NGHDL and SKY130 PDK along with their models and libraries (y/n):"
    read getConfirmation
    if [ $getConfirmation == "y" -o $getConfirmation == "Y" ];then
        echo "Removing eSim............................"
        sudo rm -rf $HOME/.esim $HOME/Desktop/esim.desktop /usr/bin/esim /usr/share/applications/esim.desktop
        echo "Removing KiCad..........................."
        sudo apt purge -y kicad kicad-footprints kicad-libraries kicad-symbols kicad-templates
        sudo rm -rf /usr/share/kicad
        rm -rf $HOME/.config/kicad/6.0

        echo "Removing Makerchip......................."
        pip3 uninstall -y hdlparse makerchip-app sandpiper-saas

        echo "Removing SKY130 PDK......................"
        sudo rm -rf /usr/share/local/sky130_fd_pr

        echo "Removing NGHDL..........................."
        rm -rf library/modelParamXML/Nghdl/*
        rm -rf library/modelParamXML/Ngveri/*
        cd nghdl/
        if [ $? -eq 0 ];then
        	chmod +x install-nghdl.sh
    	    ./install-nghdl.sh --uninstall
    	    cd ../
    	    rm -rf nghdl
            if [ $? -eq 0 ];then
                echo -e "----------------eSim Uninstalled Successfully----------------"
            else
                echo -e "\nError while removing some files/directories in \"nghdl\". Please remove it manually"
            fi
        else
            echo -e "\nCannot find \"nghdl\" directory. Please remove it manually"
        fi

        deactivate
        
        rm -rf venv

    elif [ $getConfirmation == "n" -o $getConfirmation == "N" ];then
        exit 0
    else 
        echo "Please select the right option."
        exit 0
    fi
    
else 
    echo "Please select the proper operation."
    echo "--install"
    echo "--uninstall"
fi
